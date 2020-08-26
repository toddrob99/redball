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

__version__ = "1.0.2-alpha"


def run(bot, settings):
    global log  # Make logger available to the whole module
    # Start logging
    log = logger.init_logger(
        logger_name="redball.bots." + threading.current_thread().name,
        log_to_console=str(
            settings.get("Logging", {}).get("LOG_TO_CONSOLE", True)
        ).lower()
        == "true",
        log_to_file=str(settings.get("Logging", {}).get("LOG_TO_FILE", True)).lower()
        == "true",
        log_path=redball.LOG_PATH,
        log_file=f"{threading.current_thread().name}.log",
        file_log_level=settings.get("Logging", {}).get("FILE_LOG_LEVEL"),
        log_retention=settings.get("Logging", {}).get("LOG_RETENTION", 7),
        console_log_level=settings.get("Logging", {}).get("CONSOLE_LOG_LEVEL"),
        clear_first=True,
        propagate=False,
    )
    log.debug(f"Bot received settings: {settings}")
    # Initialize vars and do one-time setup steps
    dbTable = settings.get("Database").get("dbTablePrefix", "") + "posts"
    sub = settings.get("Bot", {}).get("SUBREDDIT")
    audit = settings.get("Bot", {}).get("REPORT_ONLY", False)
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

    log.info("Initializing Reddit API...")
    try:
        r = praw.Reddit(
            client_id=settings["Reddit Auth"]["reddit_clientId"],
            client_secret=settings["Reddit Auth"]["reddit_clientSecret"],
            refresh_token=settings["Reddit Auth"]["reddit_refreshToken"],
            user_agent=f"redball Duplicate Link Removal Bot - https://github.com/toddrob99/redball/ v{__version__}",
        )
    except Exception as e:
        log.error(
            f"Error authenticating with Reddit. Ensure the bot has a valid Reddit Auth selected (with Refresh Token) and try again. Error message: {e}"
        )
        raise

    try:
        if "identity" in r.auth.scopes():
            log.info(f"Authorized Reddit user: {r.user.me()}")
    except Exception as e:
        log.error(
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
        log.error(f"Error connecting to database: {e}")
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

    log.debug(f"Loaded {len(postCache)} post(s) from db.")

    log.info(f"Monitoring posts in the following subreddit(s): {sub}...")
    while True:  # This loop keeps the bot running
        if (
            redball.SIGNAL is None and not bot.STOP
        ):  # Make sure the main thread hasn't sent a stop command
            try:
                log.debug("Checking for new posts...")
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

                    if newPost.is_self:
                        log.debug(f"Post [{newPost.id}] is a self post--skipping.")
                        ignoredPostIdCache.append(newPost.id)
                        continue
                    elif next((True for y in ignoreDomains if y in newPost.url), False):
                        log.debug(
                            f"Post [{newPost.id}] has an ignored domain [{newPost.url}]--skipping."
                        )
                        ignoredPostIdCache.append(newPost.id)
                        q = None
                    else:
                        log.debug(
                            f"Post [{newPost.id}] has a non-ignored domain link [{newPost.url}]..."
                        )
                        this = getUrls(newPost)
                        if matchingSubmissionId := next(
                            (
                                k
                                for k, v in postCache.items()
                                if k != newPost.id
                                and (
                                    next(
                                        (True for i in this["urls"] if i in v["urls"]),
                                        False,
                                    )
                                    or this["contentHash"] == v["contentHash"]
                                )
                            ),
                            None,
                        ):
                            matchingSubmission = r.submission(matchingSubmissionId)
                            if newPost.id != matchingSubmissionId:
                                log.info(
                                    f"Duplicate link for submission {newPost.id} found in submission {matchingSubmission.id}"
                                )
                                if audit:
                                    # Report the post
                                    try:
                                        parsedReportText = reportText.replace(
                                            "(title)", matchingSubmission.title
                                        ).replace(
                                            "(link)", matchingSubmission.shortlink
                                        )
                                        newPost.report(parsedReportText)
                                    except Exception as e:
                                        log.error(
                                            f"Error reporting submission [{newPost.id}]: {e}"
                                        )
                                else:
                                    # Remove the post
                                    try:
                                        newPost.mod.remove(
                                            mod_note=f"Removed as duplicate of [{matchingSubmission.id}]"
                                        )
                                    except Exception as e:
                                        log.error(
                                            f"Error removing submission [{newPost.id}]: {e}"
                                        )

                                    # Reply to the post
                                    try:
                                        parsedReplyText = removalCommentText.replace(
                                            "(title)", matchingSubmission.title
                                        ).replace(
                                            "(link)", matchingSubmission.shortlink
                                        )
                                        removalReply = newPost.reply(parsedReplyText)
                                        removalReply.mod.distinguish(sticky=True)
                                    except Exception as e:
                                        log.error(
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
                                log.debug("Inserted record to db.")
                            except Exception as e:
                                log.error(f"Error inserting into database: {e}")

                        postCache.update({newPost.id: this})
            except Exception as e:
                log.error(
                    f"Sleeping for 10 seconds and then continuing after exception: {e}"
                )
                time.sleep(10)
        else:  # If main thread has said to stop, we stop!
            log.info(f"Bot {bot.name} (id={bot.id}) exiting...")
            break  # Exit the infinite loop to stop the bot


def serialize(theObject):
    return json.dumps(theObject)


def deserialize(theString):
    return json.loads(theString)


def getUrls(submission):
    log.debug(
        f"Getting URLs for submission id [{submission.id}] with URL [{submission.url}]..."
    )
    req = requests.get(submission.url)
    if req.status_code != 200:
        log.error(
            f"Request for {submission.url} returned status code {req.status_code}"
        )
        return {
            "submissionId": submission.id,
            "url": submission.url,
            "canonical": None,
            "redir": None,
            "contentHash": None,
            "urls": [submission.url],
            "dateCreated": submission.created_utc,
            "dateRemoved": None,
        }

    log.debug(f"Request redirect history: {[h.url for h in req.history]}")

    src = req.text
    soup = BeautifulSoup(src, features="html.parser")

    canonical = soup.find("link", {"rel": "canonical"})
    log.debug(
        f"Canonical URL: {canonical['href']}"
        if canonical
        else "No canonical link found."
    )

    redir = soup.find("meta", {"http-equiv": "refresh"})
    if redir:
        redirContentParts = redir["content"].split(";")
        redirUrl = next(
            (x.split("=")[1] for x in redirContentParts if "url=" in x.lower()), None
        )
        log.debug(
            f"Meta redirect URL detected: {redirUrl}"
            if redirUrl
            else "Unable to extract redirect URL from meta refresh tag."
        )
    else:
        redirUrl = None
        log.debug("No meta redirect found.")

    contentHash = hashlib.md5(src.encode("utf-8")).hexdigest()
    log.debug(f"Content hash: {contentHash}")

    urls = [submission.url]
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

    log.debug(f"Urls: {urls}")

    urlInfo = {
        "submissionId": submission.id,
        "url": submission.url,
        "canonical": canonical["href"] if canonical else None,
        "redir": redirUrl,
        "contentHash": contentHash,
        "urls": list(set(urls)),
        "dateCreated": submission.created_utc,
        "dateRemoved": None,
    }

    log.debug(f"Resulting URL info: {urlInfo}")

    return urlInfo
