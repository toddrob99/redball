#!/usr/bin/env python

import time
import threading

import redball
from redball import logger

from bs4 import BeautifulSoup
import hashlib
import json
import os
import praw
import requests
import sqlite3

__version__ = "1.0.8"

tl = threading.local()


def run(bot, settings):
    # Start logging
    tl.log = logger.init_logger(
        logger_name=f"redball.bots.{threading.current_thread().name}",
        log_to_console=settings.get("Logging", {}).get("LOG_TO_CONSOLE", True),
        log_to_file=settings.get("Logging", {}).get("LOG_TO_FILE", True),
        log_path=redball.LOG_PATH,
        log_file=f"{threading.current_thread().name}.log",
        file_log_level=settings.get("Logging", {}).get("FILE_LOG_LEVEL"),
        log_retention=settings.get("Logging", {}).get("LOG_RETENTION", 7),
        console_log_level=settings.get("Logging", {}).get("CONSOLE_LOG_LEVEL"),
        clear_first=True,
        propagate=False,
    )
    tl.log.debug(f"Bot received settings: {settings}")
    # Initialize vars and do one-time setup steps
    dbTable = settings.get("Database").get("dbTablePrefix", "") + "posts"
    sub = settings.get("Bot", {}).get("SUBREDDIT")
    audit = settings.get("Bot", {}).get("REPORT_ONLY", False)
    useContentHash = settings.get("Bot", {}).get("USE_CONTENT_HASH", False)
    historicalPosts = int(settings.get("Bot", {}).get("HISTORICAL_POSTS", 100))
    pauseAfter = int(settings.get("Bot", {}).get("PAUSE_AFTER", 5))
    ignoreDomains = [
        x.strip()
        for x in settings.get("Bot", {})
        .get("IGNORE_DOMAINS", "i.redd.it,v.redd.it")
        .split(",")
    ]
    removalCommentText = settings.get("Bot", {}).get(
        "REMOVAL_COMMENT_TEXT",
        "This post has been automatically removed as a duplicate of [[(title)]((link))]. If you believe this is a mistake, please send a message to the subreddit moderators.",
    )
    reportText = settings.get("Bot", {}).get("REPORT_TEXT", "Duplicate: (link)")

    postCache = {}
    ignoredPostIdCache = []

    tl.log.info("Initializing Reddit API...")
    try:
        r = praw.Reddit(
            client_id=settings["Reddit Auth"]["reddit_clientId"],
            client_secret=settings["Reddit Auth"]["reddit_clientSecret"],
            refresh_token=settings["Reddit Auth"]["reddit_refreshToken"],
            user_agent=f"redball Duplicate Link Removal Bot - https://github.com/toddrob99/redball/ v{__version__}",
        )
    except Exception as e:
        tl.log.error(
            f"Error authenticating with Reddit. Ensure the bot has a valid Reddit Auth selected (with Refresh Token) and try again. Error message: {e}"
        )
        raise

    try:
        if "identity" in r.auth.scopes():
            tl.log.info(f"Authorized Reddit user: {r.user.me()}")
    except Exception as e:
        tl.log.error(
            f"Reddit authentication failure. Ensure the bot has a valid Reddit Auth selected (with Refresh Token and relevant scopes selected) and try again. Error message: {e}"
        )
        raise

    try:
        db = sqlite3.connect(
            os.path.join(
                settings["Database"]["dbPath"], settings["Database"]["dbFile"]
            ),
            timeout=30,
        )
        """Local sqlite database to store info about processed posts"""
        db.execute("PRAGMA journal_mode = off;")
    except sqlite3.Error as e:
        tl.log.error(f"Error connecting to database: {e}")
        raise

    dbc = db.cursor()
    dbc.execute(
        f"""CREATE TABLE IF NOT EXISTS {dbTable} (
            submissionId text PRIMARY KEY,
            url text,
            canonical text,
            contentHash text,
            urls text,
            dateCreated text,
            dateRemoved text
        );"""
    )

    dbc.execute(
        f"SELECT submissionId, url, canonical, contentHash, urls, dateCreated, dateRemoved FROM {dbTable} ORDER BY dateCreated ASC LIMIT {historicalPosts};"
    )
    pids = dbc.fetchall()
    for pid in pids:
        post = {
            "submissionId": pid[0],
            "url": pid[1],
            "canonical": pid[2],
            "contentHash": pid[3],
            "urls": deserialize(pid[4]),
            "dateCreated": pid[5],
            "dateRemoved": pid[6],
        }
        postCache.update({post["submissionId"]: post})

    tl.log.debug(f"Loaded {len(postCache)} post(s) from db.")

    tl.log.info(f"Monitoring posts in the following subreddit(s): {sub}...")
    while True:  # This loop keeps the bot running
        if (
            redball.SIGNAL is None and not bot.STOP
        ):  # Make sure the main thread hasn't sent a stop command
            try:
                tl.log.debug("Checking for new posts...")
                for newPost in r.subreddit(sub).stream.submissions(
                    pause_after=pauseAfter
                ):
                    if newPost is None:
                        break

                    if (
                        newPost.id in postCache.keys()
                        or newPost.id in ignoredPostIdCache
                    ):
                        continue

                    if not newPost.is_self and (newPost.url.startswith("/")):
                        checkUrl = f"https://reddit.com{newPost.url}"
                        tl.log.debug(
                            f"Detected relative URL, checking URL for ignored domains with https://reddit.com prepended: [{checkUrl}]"
                        )
                    else:
                        checkUrl = None

                    if newPost.is_self:
                        tl.log.debug(f"Post [{newPost.id}] is a self post--skipping.")
                        ignoredPostIdCache.append(newPost.id)
                        continue
                    elif newPost.is_reddit_media_domain:
                        tl.log.debug(
                            f"Post [{newPost.id}] is a reddit media domain--skipping."
                        )
                        ignoredPostIdCache.append(newPost.id)
                        continue
                    elif next(
                        (
                            True
                            for y in ignoreDomains
                            if y in (checkUrl if checkUrl else newPost.url)
                        ),
                        False,
                    ):
                        tl.log.debug(
                            f"Post [{newPost.id}] has an ignored domain [{newPost.url}]--skipping."
                        )
                        ignoredPostIdCache.append(newPost.id)
                        q = None
                    else:
                        try:
                            if newPost.is_gallery:
                                tl.log.debug(
                                    f"Post [{newPost.id}] is a gallery--skipping."
                                )
                                ignoredPostIdCache.append(newPost.id)
                                continue
                        except AttributeError:
                            pass

                        tl.log.debug(
                            f"Post [{newPost.id}] has a non-ignored domain link [{newPost.url}]..."
                        )
                        this = getUrls(newPost)
                        foundActiveDupeSubmissionId = None
                        foundRemovedDupeSubmissionId = None
                        matchingSubmissionGenerator = (
                            k
                            for k, v in postCache.items()
                            if k != newPost.id
                            and (
                                next(
                                    (True for i in this["urls"] if i in v["urls"]),
                                    False,
                                )
                                or (
                                    useContentHash
                                    and (
                                        this["contentHash"] == v["contentHash"]
                                        and v["contentHash"]
                                        is not None  # url GET likely failed if None
                                    )
                                )
                            )
                        )
                        while matchingSubmissionId := next(
                            matchingSubmissionGenerator, None
                        ):
                            matchingSubmission = r.submission(matchingSubmissionId)
                            if not matchingSubmission.author:
                                # Matching submission is deleted!
                                tl.log.info(
                                    f"Matching prior submission [{matchingSubmission.id}] is deleted, ignoring."
                                )
                                continue

                            if not matchingSubmission.is_robot_indexable:
                                # Matching submission is removed (not deleted since the last condition was not met)
                                tl.log.info(
                                    f"Matching prior submission [{matchingSubmission.id}] is removed, ignoring unless no other dupes are found."
                                )
                                foundRemovedDupeSubmissionId = matchingSubmissionId
                                continue

                            if newPost.id != matchingSubmissionId:
                                # Matching submission found, not deleted or removed
                                tl.log.info(
                                    f"New submission [{newPost.id}] identified as duplicate of submission [{matchingSubmission.id}]"
                                )
                                foundActiveDupeSubmissionId = matchingSubmissionId
                                break

                        if foundActiveDupeSubmissionId or foundRemovedDupeSubmissionId:
                            # Duplicate identified
                            dupePost = r.submission(
                                foundActiveDupeSubmissionId
                                if foundActiveDupeSubmissionId
                                else foundRemovedDupeSubmissionId
                            )
                            if audit or not foundActiveDupeSubmissionId:
                                # Report the post
                                if audit and not foundActiveDupeSubmissionId:
                                    tl.log.info(
                                        f"Reporting new submission [{newPost.id}] due to audit mode (and prior post [{dupePost.id}] is removed)..."
                                    )
                                elif audit:
                                    tl.log.info(
                                        f"Reporting new submission [{newPost.id}] due to audit mode..."
                                    )
                                elif foundRemovedDupeSubmissionId:
                                    tl.log.info(
                                        f"Reporting new submission [{newPost.id}] since prior post [{dupePost.id}] is removed..."
                                    )

                                try:
                                    parsedReportText = reportText.replace(
                                        "(title)", dupePost.title
                                    ).replace("(link)", dupePost.shortlink)
                                    if not foundActiveDupeSubmissionId:
                                        parsedReportText += " (prior post is removed)"

                                    newPost.report(parsedReportText)
                                except Exception as e:
                                    tl.log.error(
                                        f"Error reporting submission [{newPost.id}]: {e}"
                                    )
                            else:
                                # Remove the post
                                tl.log.info(
                                    f"Removing new post [{newPost.id}] as a duplicate of [{dupePost.id}]..."
                                )
                                try:
                                    newPost.mod.remove(
                                        mod_note=f"Removed as duplicate of [{dupePost.id}]"
                                    )
                                except Exception as e:
                                    tl.log.error(
                                        f"Error removing submission [{newPost.id}]: {e}"
                                    )

                                # Reply to the post
                                try:
                                    parsedReplyText = removalCommentText.replace(
                                        "(title)", dupePost.title
                                    ).replace("(link)", dupePost.shortlink)
                                    removalReply = newPost.reply(parsedReplyText)
                                    removalReply.mod.distinguish(sticky=True)
                                except Exception as e:
                                    tl.log.error(
                                        f"Error submitting reply to submission [{newPost.id}]: {e}"
                                    )

                            q = f"INSERT OR IGNORE INTO {dbTable} (submissionId, url, canonical, contentHash, urls, dateCreated, dateRemoved) VALUES (?, ?, ?, ?, ?, ?, ?);"
                            qa = (
                                newPost.id,
                                newPost.url,
                                this["canonical"],
                                this["contentHash"],
                                serialize(this["urls"]),
                                newPost.created_utc,
                                time.time(),
                            )
                        else:
                            # No duplicate found
                            tl.log.debug(
                                f"No duplicates found for submission [{newPost.id}]"
                            )
                            q = f"INSERT OR IGNORE INTO {dbTable} (submissionId, url, canonical, contentHash, urls, dateCreated) VALUES (?, ?, ?, ?, ?, ?);"
                            qa = (
                                newPost.id,
                                newPost.url,
                                this["canonical"],
                                this["contentHash"],
                                serialize(this["urls"]),
                                newPost.created_utc,
                            )

                        if q:
                            try:
                                dbc.execute(q, qa)
                                db.commit()
                                tl.log.debug("Inserted record to db.")
                            except Exception as e:
                                tl.log.error(f"Error inserting into database: {e}")

                        postCache.update({newPost.id: this})
            except Exception as e:
                tl.log.error(
                    f"Sleeping for 10 seconds and then continuing after exception: {e}"
                )
                time.sleep(10)
        else:  # If main thread has said to stop, we stop!
            tl.log.info(f"Bot {bot.name} (id={bot.id}) exiting...")
            break  # Exit the infinite loop to stop the bot


def serialize(theObject):
    return json.dumps(theObject)


def deserialize(theString):
    return json.loads(theString)


def getUrls(submission):
    if submission.url.startswith("/"):
        checkUrl = f"https://reddit.com{submission.url}"
        tl.log.debug(f"Prepended https://reddit.com to relative url: [{checkUrl}]")
    else:
        checkUrl = submission.url

    tl.log.debug(
        f"Getting URLs for submission id [{submission.id}] with URL [{checkUrl}]..."
    )
    req = requests.get(checkUrl)
    if req.status_code != 200:
        tl.log.error(f"Request for {checkUrl} returned status code {req.status_code}")
        return {
            "submissionId": submission.id,
            "url": checkUrl,
            "canonical": None,
            "redir": None,
            "contentHash": None,
            "urls": [checkUrl],
            "dateCreated": submission.created_utc,
            "dateRemoved": None,
        }

    tl.log.debug(f"Request redirect history: {[h.url for h in req.history]}")

    if (
        not req.headers.get("content-type")
        or "text/html" not in req.headers["content-type"]
    ):
        # Target is not an html page, might be a video or image
        tl.log.debug(
            "Target is not an html page, so not parsing canonical link, looking for meta redirect, or calculating content hash."
        )
        canonical = None
        redirUrl = None
        contentHash = None
    else:
        src = req.text
        soup = BeautifulSoup(src, features="html.parser")

        canonical = soup.find("link", {"rel": "canonical"})
        tl.log.debug(
            f"Canonical URL: {canonical['href']}"
            if canonical
            else "No canonical link found."
        )

        redir = soup.find("meta", {"http-equiv": "refresh"})
        if redir:
            redirContentParts = redir["content"].split(";")
            redirUrl = next(
                (x.split("=")[1] for x in redirContentParts if "url=" in x.lower()),
                None,
            )
            tl.log.debug(
                f"Meta redirect URL detected: {redirUrl}"
                if redirUrl
                else "Unable to extract redirect URL from meta refresh tag."
            )
        else:
            redirUrl = None
            tl.log.debug("No meta redirect found.")

        contentHash = hashlib.md5(src.encode("utf-8")).hexdigest()
        tl.log.debug(f"Content hash: {contentHash}")

    urls = [checkUrl]
    if checkUrl != submission.url:
        urls.append(submission.url)
    if canonical:
        urls.append(canonical["href"])
    urls.extend([x.url for x in req.history])
    if redirUrl:
        urls.append(redirUrl)

    for x in urls:
        alt = (
            x.replace("https://", "http://")
            if "https://" in x
            else x.replace("http://", "https://")
        )
        if alt not in urls:
            urls.append(alt)

    tl.log.debug(f"Urls: {urls}")

    urlInfo = {
        "submissionId": submission.id,
        "url": checkUrl,
        "canonical": canonical["href"] if canonical else None,
        "redir": redirUrl,
        "contentHash": contentHash,
        "urls": list(set(urls)),
        "dateCreated": submission.created_utc,
        "dateRemoved": None,
    }

    tl.log.debug(f"Resulting URL info: {urlInfo}")

    return urlInfo
