#!/usr/bin/env python
"""Comment Response Bot
By Todd Roberts
"""

import threading

import redball
from redball import logger

# Import bot-specific modules
import os
import praw
import sqlite3
import time

__version__ = "1.0.0"

tl = threading.local()


def run(bot, settings):
    # Start logging
    tl.log = logger.init_logger(
        logger_name="redball.bots." + threading.current_thread().name,
        log_to_console=settings.get("Logging", {}).get("LOG_TO_CONSOLE", True),
        log_to_file=settings.get("Logging", {}).get("LOG_TO_FILE", True),
        log_path=redball.LOG_PATH,
        log_file="{}.log".format(threading.current_thread().name),
        file_log_level=settings.get("Logging", {}).get("FILE_LOG_LEVEL"),
        log_retention=settings.get("Logging", {}).get("LOG_RETENTION", 7),
        console_log_level=settings.get("Logging", {}).get("CONSOLE_LOG_LEVEL"),
        clear_first=True,
        propagate=settings.get("Logging", {}).get("PROPAGATE", False),
    )
    tl.log.debug("Bot received settings: {}".format(settings))

    # Initialize vars and do one-time setup steps
    dbTable = settings.get("Database").get("dbTablePrefix", "") + "comments"
    keyResp = settings.get("Keyword Response", {})
    reqName = str(settings.get("Bot", {}).get("REQ_NAME", "True")).lower() == "true"
    sub = settings.get("Bot", {}).get("SUBREDDIT")
    delThreshold = int(settings.get("Bot", {}).get("DEL_THRESHOLD", -2))
    historicalDays = int(settings.get("Bot", {}).get("HISTORICAL_DAYS", 1))
    pauseAfter = int(settings.get("Bot", {}).get("PAUSE_AFTER", 5))
    replyFooter = settings.get("Bot", {}).get(
        "REPLY_FOOTER",
        "^^I ^^am ^^a ^^bot. ^^Downvoted ^^replies ^^will ^^be ^^deleted. ^^[[source/doc](https://github.com/toddrob99/redball/wiki/Comment-Response-Bot)] ^^[[feedback](https://reddit.com/r/redball/)]",
    )
    comments = {}

    tl.log.info("Initializing Reddit API...")
    try:
        r = praw.Reddit(
            client_id=settings["Reddit Auth"]["reddit_clientId"],
            client_secret=settings["Reddit Auth"]["reddit_clientSecret"],
            refresh_token=settings["Reddit Auth"]["reddit_refreshToken"],
            user_agent="redball Comment Response Bot - https://github.com/toddrob99/redball/ v{}".format(
                __version__
            ),
        )
    except Exception as e:
        tl.log.error(
            "Error authenticating with Reddit. Ensure the bot has a valid Reddit Auth selected (with Refresh Token) and try again. Error message: {}".format(
                e
            )
        )
        raise

    try:
        if "identity" in r.auth.scopes():
            tl.log.info("Authorized Reddit user: {}".format(r.user.me()))
        elif str(reqName).lower() == "true":
            tl.log.error(
                "Reddit auth does not have `identity` scope authorized; cannot identify bot name in comments as required."
            )
            raise Exception(
                "Reddit auth does not have `identity` scope authorized; cannot identify bot name in comments as required."
            )
    except Exception as e:
        tl.log.error(
            "Reddit authentication failure. Ensure the bot has a valid Reddit Auth selected (with Refresh Token and relevant scopes selected) and try again. Error message: {}".format(
                e
            )
        )
        raise

    try:
        db = sqlite3.connect(
            os.path.join(
                settings["Database"]["dbPath"], settings["Database"]["dbFile"]
            ),
            timeout=30,
        )
        """Local sqlite database to store info about processed comments"""
        db.execute("PRAGMA journal_mode = off;")
        # db.set_trace_callback(print)
    except sqlite3.Error as e:
        tl.log.error("Error connecting to database: {}".format(e))
        raise

    dbc = db.cursor()
    dbc.execute(
        """CREATE TABLE IF NOT EXISTS {} (
                        comment_id text PRIMARY KEY,
                        sub text NOT NULL,
                        author text NOT NULL,
                        post text NOT NULL,
                        date text NOT NULL,
                        kw text,
                        errors text,
                        reply text,
                        removed integer
                    );""".format(
            dbTable
        )
    )

    dbc.execute(
        "SELECT comment_id, date, reply, errors, removed FROM {} ORDER BY date DESC LIMIT 500;".format(
            dbTable
        )
    )
    cids = dbc.fetchall()
    for cid in cids:
        comments.update(
            {
                cid[0]: {
                    "date": cid[1],
                    "reply": r.comment(cid[2]) if cid[2] else None,
                    "errors": cid[3],
                    "removed": cid[4],
                    "historical": True,
                }
            }
        )

    tl.log.debug("Loaded {} comments from db.".format(len(comments)))

    tl.log.info("Monitoring comments in the following subreddit(s): {}...".format(sub))
    while True:  # This loop keeps the bot running
        if (
            redball.SIGNAL is None and not bot.STOP
        ):  # Make sure the main thread hasn't sent a stop command
            for comment in r.subreddit(sub).stream.comments(pause_after=pauseAfter):
                if bot and bot.STOP:
                    tl.log.info("Received stop signal! Closing DB connection...")
                    # Close DB connection before exiting
                    try:
                        db.close()
                    except sqlite3.Error as e:
                        tl.log.error("Error closing database connection: {}".format(e))
                    return

                if not comment:
                    break  # take a break to delete downvoted replies

                replyText = ""
                if (
                    any(k for k in keyResp if k.lower() in comment.body.lower())
                    and (
                        (reqName and str(r.user.me()).lower() in comment.body.lower())
                        or not reqName
                    )
                    and comment.author != r.user.me()
                ):
                    if comment.id in comments.keys():
                        tl.log.debug("Already processed comment {}".format(comment.id))
                        continue
                    elif (
                        comment.created_utc
                        <= time.time() - 60 * 60 * 24 * historicalDays - 3600
                    ):  # Add 1 hour buffer to ensure recent comments are processed
                        tl.log.debug(
                            "Stream returned comment {} which is older than the HISTORICAL_DAYS setting ({}), ignoring...".format(
                                comment.id, historicalDays
                            )
                        )
                        comments.update(
                            {
                                comment.id: {
                                    "sub": comment.subreddit,
                                    "author": comment.author,
                                    "post": comment.submission,
                                    "date": time.time(),
                                    "kw": [],
                                    "errors": [],
                                }
                            }
                        )
                        continue

                    comments.update(
                        {
                            comment.id: {
                                "sub": comment.subreddit,
                                "author": comment.author,
                                "post": comment.submission,
                                "date": time.time(),
                                "kw": [],
                                "errors": [],
                            }
                        }
                    )
                    dbc.execute(
                        "insert or ignore into {} (comment_id, sub, author, post, date) values (?, ?, ?, ?, ?);".format(
                            dbTable
                        ),
                        (
                            str(comment.id),
                            str(comment.subreddit),
                            str(comment.author),
                            str(comment.submission),
                            str(comment.created_utc),
                        ),
                    )
                    tl.log.debug(
                        "({}) {} - {}: {}".format(
                            comment.subreddit, comment.id, comment.author, comment.body
                        )
                    )

                    for k in (
                        k for k in keyResp.keys() if k.lower() in comment.body.lower()
                    ):
                        comments[comment.id]["kw"].append(k)
                        if replyText != "":
                            replyText += "\n\n"

                        replyText += keyResp[k]

                    if replyText != "":
                        try:
                            latest_reply = comment.reply(
                                replyText + "\n\n" + replyFooter
                            )
                            comments[comment.id].update({"reply": latest_reply})
                            latest_reply.disable_inbox_replies()
                            tl.log.info(
                                "Replied with comment id {} and disabled inbox replies.".format(
                                    latest_reply
                                )
                            )
                            dbc.execute(
                                "update {} set kw=?,reply=? where comment_id=?;".format(
                                    dbTable
                                ),
                                (
                                    str(comments[comment.id]["kw"]),
                                    str(latest_reply),
                                    str(comment.id),
                                ),
                            )
                        except Exception as e:
                            tl.log.error(
                                "Error replying to comment or disabling inbox replies: {}".format(
                                    e
                                )
                            )
                            comments[comment.id]["errors"].append(
                                "Error submitting comment or disabling inbox replies: {}".format(
                                    e
                                )
                            )

                    if len(comments[comment.id].get("errors")):
                        dbc.execute(
                            "update {} set errors=? where comment_id=?;".format(
                                dbTable
                            ),
                            (str(comments[comment.id].get("errors")), str(comment.id)),
                        )

                    db.commit()

            tl.log.debug(
                "Checking for downvotes on {} replies...".format(
                    sum(
                        1
                        for x in comments
                        if comments[x].get("reply")
                        and not comments[x].get("removed")
                        and float(comments[x].get("date"))
                        >= time.time() - 60 * 60 * 24 * historicalDays - 3600
                    )
                )
            )
            for x in (
                x
                for x in comments
                if comments[x].get("reply")
                and not comments[x].get("removed")
                and float(comments[x].get("date"))
                >= time.time() - 60 * 60 * 24 * historicalDays - 3600
            ):
                # print('Submission: {}, reply: {}'.format(r.comment(x).submission, comments[x]['reply']))
                try:
                    comments[x]["reply"].refresh()
                except praw.exceptions.ClientException as e:
                    print(
                        "Error refreshing attributes for comment reply {}: {}".format(
                            comments[x]["reply"], e
                        )
                    )
                    if "comment does not appear to be in the comment tree" in str(e):
                        comments[x].update({"removed": time.time()})
                        dbc.execute(
                            "update {} set removed=? where comment_id=?;".format(
                                dbTable
                            ),
                            (str(comments[x].get("removed")), str(x)),
                        )

                if not comments[x].get("removed"):
                    if comments[x]["reply"].score <= delThreshold:
                        tl.log.info(
                            "Deleting comment {} with score ({}) at or below threshold ({})...".format(
                                comments[x]["reply"],
                                comments[x]["reply"].score,
                                delThreshold,
                            )
                        )
                        try:
                            comments[x]["reply"].delete()
                            comments[x].update({"removed": time.time()})
                            dbc.execute(
                                "update {} set removed=? where comment_id=?;".format(
                                    dbTable
                                ),
                                (str(comments[x].get("removed")), str(x)),
                            )
                            db.commit()
                        except Exception as e:
                            tl.log.error(
                                "Error deleting downvoted comment: {}".format(e)
                            )
                            comments[x]["errors"].append(
                                "Error deleting downvoted comment: {}".format(e)
                            )

            limits = r.auth.limits
            if limits.get("remaining") < 60:
                tl.log.warning(
                    "Approaching Reddit API rate limit, sleeping for a minute... {}".format(
                        limits
                    )
                )
                time.sleep(60)
            else:
                tl.log.debug("Reddit API limits: {}".format(limits))
        else:  # If main thread has said to stop, we stop!
            tl.log.info("Bot {} (id={}) exiting...".format(bot.name, bot.id))
            break  # Exit the infinite loop to stop the bot

    # Close DB connection before exiting
    try:
        tl.log.info("Closing DB connection.")
        db.close()
    except sqlite3.Error as e:
        tl.log.error("Error closing database connection: {}".format(e))
