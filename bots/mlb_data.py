#!/usr/bin/env python
# encoding=utf-8
"""MLB Data Bot
By Todd Roberts
"""

from datetime import datetime
import os
import praw
import requests
import sqlite3
import statsapi
import threading
import time

import redball
from redball import logger

__version__ = "1.1"

tl = threading.local()


class StatBot:
    def __init__(self, settings, bot):
        self.bot = bot
        self.log = tl.log
        self.log.info("StatBot starting up...")

        self.sub = settings.get("Reddit", {}).get("SUBREDDIT")
        self.replyFooter = settings.get("Bot", {}).get(
            "REPLY_FOOTER",
            "\n\n^^I ^^am ^^a ^^bot. ^^Not ^^affiliated ^^with ^^MLB. ^^Downvoted ^^replies ^^will ^^be ^^deleted. ^^[[source/doc](https://github.com/toddrob99/MLB-StatBot)] ^^[[feedback](https://reddit.com/r/redball/)]",
        )
        self.delThreshold = settings.get("Bot", {}).get("DEL_THRESHOLD", -2)
        self.historicalDays = int(settings.get("Bot", {}).get("HISTORICAL_DAYS", 1))
        self.pauseAfter = int(settings.get("Bot", {}).get("PAUSE_AFTER", 5))
        self.dbPath = settings.get("Database", {}).get(
            "dbPath", os.path.dirname(os.path.realpath(__file__))
        )
        self.dbFile = settings.get("Database", {}).get("dbFile", "statbot.db")
        self.dbTable = (
            settings.get("Database", {}).get("dbTablePrefix", "") + "comments"
        )
        reddit_clientId = settings.get("Reddit Auth", {}).get("reddit_clientId")
        reddit_clientSecret = settings.get("Reddit Auth", {}).get("reddit_clientSecret")
        self.comments = {}

        self.log.info("Initializing Reddit API...")
        with redball.REDDIT_AUTH_LOCKS[self.bot.redditAuth]:
            try:
                self.r = praw.Reddit(
                    client_id=reddit_clientId,
                    client_secret=reddit_clientSecret,
                    token_manager=self.bot.reddit_auth_token_manager,
                    user_agent="redball Baseball Stat Bot - https://github.com/toddrob99/redball/ v{}".format(
                        __version__
                    ),
                )
            except Exception as e:
                self.log.error(
                    "Error authenticating with Reddit. Error message: {}".format(e)
                )

            try:
                if "identity" in self.r.auth.scopes():
                    self.log.info("Authorized Reddit user: {}".format(self.r.user.me()))
            except Exception as e:
                self.log.error(
                    "Reddit authentication failure. Error message: {}".format(e)
                )
                raise

        try:
            self.db = sqlite3.connect(os.path.join(self.dbPath, self.dbFile))
            """Local sqlite database to store info about processed comments"""
        except sqlite3.Error as e:
            self.log.error("Error connecting to database: {}".format(e))
            raise

        self.dbc = self.db.cursor()
        self.dbc.execute(
            """CREATE TABLE IF NOT EXISTS {} (
                            comment_id text PRIMARY KEY,
                            sub text NOT NULL,
                            author text NOT NULL,
                            post text NOT NULL,
                            date text NOT NULL,
                            cmd text,
                            errors text,
                            reply text,
                            removed integer
                        );""".format(
                self.dbTable
            )
        )
        self.db.commit()

    def __del__(self):
        try:
            self.log.info("Closing DB connection.")
            self.db.close()
        except sqlite3.Error as e:
            self.log.error("Error closing database connection: {}".format(e))

    def run(self):
        if not self.sub:
            self.log.error("No subreddit specified!")
            self.bot.STOP = True
            return

        self.dbc.execute(
            "SELECT comment_id, date, reply, errors, removed FROM {} ORDER BY date DESC LIMIT 500;".format(
                self.dbTable
            )
        )
        comment_ids = self.dbc.fetchall()
        for cid in comment_ids:
            self.comments.update(
                {
                    cid[0]: {
                        "date": cid[1],
                        "reply": self.r.comment(cid[2]) if cid[2] else None,
                        "errors": cid[3],
                        "removed": cid[4],
                        "historical": True,
                    }
                }
            )

        self.log.debug("Loaded {} comments from db.".format(len(self.comments)))
        self.log.info(
            "Monitoring comments in the following subreddit(s): {}...".format(self.sub)
        )
        while True:
            if self.bot and self.bot.STOP:
                self.log.info("Received stop signal...")
                return

            try:
                for comment in self.r.subreddit(self.sub).stream.comments(
                    pause_after=self.pauseAfter
                ):
                    if self.bot and self.bot.STOP:
                        self.log.info("Received stop signal...")
                        return

                    if not comment:
                        break  # Take a break to delete downvoted replies

                    replyText = ""
                    if (
                        str(self.r.user.me()).lower() in comment.body.lower()
                        and comment.author != self.r.user.me()
                    ):
                        if comment.id in self.comments.keys():
                            self.log.debug(
                                "Already processed comment {}".format(comment.id)
                            )
                            continue
                        elif (
                            comment.created_utc
                            <= time.time() - 60 * 60 * 24 * self.historicalDays - 3600
                        ):  # Add 1 hour buffer to ensure recent comments are processed
                            self.log.debug(
                                "Stream returned comment {} which is older than the HISTORICAL_DAYS setting ({}), ignoring...".format(
                                    comment.id, self.historicalDays
                                )
                            )
                            self.comments.update(
                                {
                                    comment.id: {
                                        "sub": comment.subreddit,
                                        "author": comment.author,
                                        "post": comment.submission,
                                        "date": time.time(),
                                        "cmd": [],
                                        "errors": [],
                                    }
                                }
                            )
                            continue

                        self.comments.update(
                            {
                                comment.id: {
                                    "sub": comment.subreddit,
                                    "author": comment.author,
                                    "post": comment.submission,
                                    "date": time.time(),
                                    "cmd": [],
                                    "errors": [],
                                }
                            }
                        )
                        self.dbc.execute(
                            "insert or ignore into {} (comment_id, sub, author, post, date) values (?, ?, ?, ?, ?);".format(
                                self.dbTable
                            ),
                            (
                                str(comment.id),
                                str(comment.subreddit),
                                str(comment.author),
                                str(comment.submission),
                                str(comment.created_utc),
                            ),
                        )
                        self.log.debug(
                            "({}) {} - {}: {}".format(
                                comment.subreddit,
                                comment.id,
                                comment.author,
                                comment.body,
                            )
                        )
                        if "help" in comment.body.lower():
                            self.comments[comment.id]["cmd"].append("help")
                            replyText += "I am a bot that can provide MLB data, but I am not affiliated with MLB or any team.\n\n"
                            replyText += "Invoke me by including my name anywhere in your comment.\n\n"
                            replyText += "Include an available command in your comment: [help, score, careerstats, lastgame, nextgame, seasonstats, standings, winprob, rundiff], "
                            replyText += "along with the subject in curly brackets.\n\n"
                            replyText += "For stats commands, you can also include the type: [hitting, pitching, fielding].\n\n"
                            replyText += "For example, `careerstats {hamels} pitching` or `score {phillies}` or `standings {nle}` "
                            replyText += "(try including the word wildcard when asking for standings).\n\n"
                            replyText += (
                                "I am currently monitoring the following subreddit(s): "
                                + self.sub.replace("+", ", ")
                                + "."
                            )

                        if "seasonstats" in comment.body.lower():
                            self.comments[comment.id]["cmd"].append("seasonstats")
                            if replyText != "":
                                replyText += "\n\n*****\n\n"

                            try:
                                who = statsapi.lookup_player(
                                    comment.body[
                                        comment.body.find("{")
                                        + 1 : comment.body.find("}")
                                    ]
                                )[0]["id"]
                                what = []
                                if (
                                    "hitting" in comment.body.lower()
                                    or "batting" in comment.body.lower()
                                ):
                                    what.append("hitting")

                                if "pitching" in comment.body.lower():
                                    what.append("pitching")

                                if "fielding" in comment.body.lower():
                                    what.append("fielding")

                                if len(what):
                                    stats = statsapi.player_stats(
                                        who,
                                        str(what).replace("'", "").replace(" ", ""),
                                        "season",
                                    )
                                else:
                                    stats = statsapi.player_stats(who, type="season")

                                replyText += "\n    " + stats.replace("\n", "\n    ")
                            except Exception as e:
                                self.log.error(
                                    "Error generating response for seasonstats: {}".format(
                                        e
                                    )
                                )
                                self.comments[comment.id]["errors"].append(
                                    "Error generating response for seasonstats: {}".format(
                                        e
                                    )
                                )

                        if "careerstats" in comment.body.lower():
                            self.comments[comment.id]["cmd"].append("careerstats")
                            if replyText != "":
                                replyText += "\n\n*****\n\n"

                            try:
                                who = self.lookup_player(
                                    comment.body[
                                        comment.body.find("{")
                                        + 1 : comment.body.find("}")
                                    ]
                                )
                                what = []
                                if (
                                    "hitting" in comment.body.lower()
                                    or "batting" in comment.body.lower()
                                ):
                                    what.append("hitting")

                                if "pitching" in comment.body.lower():
                                    what.append("pitching")

                                if "fielding" in comment.body.lower():
                                    what.append("fielding")

                                if len(what):
                                    stats = statsapi.player_stats(
                                        who,
                                        str(what).replace("'", "").replace(" ", ""),
                                        "career",
                                    )
                                else:
                                    stats = statsapi.player_stats(who, type="career")

                                replyText += "\n    " + stats.replace("\n", "\n    ")
                            except Exception as e:
                                self.log.error(
                                    "Error generating response for careerstats: {}".format(
                                        e
                                    )
                                )
                                self.comments[comment.id]["errors"].append(
                                    "Error generating response for careerstats: {}".format(
                                        e
                                    )
                                )

                        if "nextgame" in comment.body.lower():
                            self.comments[comment.id]["cmd"].append("nextgame")
                            if replyText != "":
                                replyText += "\n\n*****\n\n"

                            try:
                                who = statsapi.lookup_team(
                                    comment.body[
                                        comment.body.find("{")
                                        + 1 : comment.body.find("}")
                                    ]
                                )[0]["id"]
                                next = statsapi.next_game(who)
                                game = statsapi.schedule(game_id=next)
                                replyText += game[0]["summary"]
                            except Exception as e:
                                self.log.error(
                                    "Error generating response for nextgame: {}".format(
                                        e
                                    )
                                )
                                self.comments[comment.id]["errors"].append(
                                    "Error generating response for nextgame: {}".format(
                                        e
                                    )
                                )

                        if "lastgame" in comment.body.lower():
                            self.comments[comment.id]["cmd"].append("lastgame")
                            if replyText != "":
                                replyText += "\n\n*****\n\n"

                            try:
                                who = statsapi.lookup_team(
                                    comment.body[
                                        comment.body.find("{")
                                        + 1 : comment.body.find("}")
                                    ]
                                )[0]["id"]
                                last = statsapi.last_game(who)
                                game = statsapi.schedule(game_id=last)
                                replyText += game[0]["summary"]
                            except Exception as e:
                                self.log.error(
                                    "Error generating response for lastgame: {}".format(
                                        e
                                    )
                                )
                                self.comments[comment.id]["errors"].append(
                                    "Error generating response for lastgame: {}".format(
                                        e
                                    )
                                )

                        if "winprob" in comment.body.lower():
                            self.comments[comment.id]["cmd"].append("winprob")
                            if replyText != "":
                                replyText += "\n\n*****\n\n"

                            try:
                                who = statsapi.lookup_team(
                                    comment.body[
                                        comment.body.find("{")
                                        + 1 : comment.body.find("}")
                                    ]
                                )[0]["id"]
                                game = statsapi.schedule(team=who)[0]
                                contextMetrics = statsapi.get(
                                    "game_contextMetrics", {"gamePk": game["game_id"]}
                                )
                                away_win_prob = contextMetrics.get(
                                    "awayWinProbability", "-"
                                )
                                home_win_prob = contextMetrics.get(
                                    "homeWinProbability", "-"
                                )
                                replyText += "\n    " + game["summary"] + "\n"
                                replyText += (
                                    "    Current win probabilities: "
                                    + game["away_name"]
                                    + " "
                                    + str(away_win_prob)
                                    + "%, "
                                    + game["home_name"]
                                    + " "
                                    + str(home_win_prob)
                                    + "%"
                                )
                            except Exception as e:
                                self.log.error(
                                    "Error generating response for winprob: {}".format(
                                        e
                                    )
                                )
                                self.comments[comment.id]["errors"].append(
                                    "Error generating response for winprob: {}".format(
                                        e
                                    )
                                )

                        if (
                            "score" in comment.body.lower()
                            and "Current win probabilities" not in replyText
                        ):
                            self.comments[comment.id]["cmd"].append("score")
                            if replyText != "":
                                replyText += "\n\n*****\n\n"

                            try:
                                who = comment.body[
                                    comment.body.find("{") + 1 : comment.body.find("}")
                                ].lower()
                                if who in [
                                    "nle",
                                    "nlw",
                                    "nlc",
                                    "ale",
                                    "alw",
                                    "alc",
                                    "all",
                                ]:
                                    todaysGames = statsapi.get(
                                        "schedule",
                                        {
                                            "fields": "dates,date,games,gamePk,teams,away,team,division,abbreviation",
                                            "sportId": 1,
                                            "hydrate": "team(division)",
                                        },
                                    )
                                    gamePks = ""
                                    for i in (
                                        x["gamePk"]
                                        for x in todaysGames["dates"][0]["games"]
                                        if who == "all"
                                        or x["teams"]["away"]["team"]["division"][
                                            "abbreviation"
                                        ].lower()
                                        == who
                                        or x["teams"]["home"]["team"]["division"][
                                            "abbreviation"
                                        ].lower()
                                        == who
                                    ):
                                        gamePks += "{},".format(i)

                                    if len(gamePks):
                                        if gamePks[-1] == ",":
                                            gamePks = gamePks[:-1]

                                    games = statsapi.schedule(game_id=gamePks)
                                    for game in games:
                                        replyText += "\n    " + game["summary"]
                                else:
                                    who = statsapi.lookup_team(
                                        comment.body[
                                            comment.body.find("{")
                                            + 1 : comment.body.find("}")
                                        ]
                                    )[0]["id"]
                                    game = statsapi.schedule(team=who)
                                    replyText += game[0]["summary"]
                            except Exception as e:
                                self.log.error(
                                    "Error generating response for score: {}".format(e)
                                )
                                self.comments[comment.id]["errors"].append(
                                    "Error generating response for score: {}".format(e)
                                )

                        if "standings" in comment.body.lower():
                            self.comments[comment.id]["cmd"].append("standings")
                            if replyText != "":
                                replyText += "\n\n*****\n\n"

                            try:
                                if comment.body.find("{") != -1:
                                    who = comment.body[
                                        comment.body.find("{")
                                        + 1 : comment.body.find("}")
                                    ].lower()
                                else:
                                    who = "all"

                                wc = (
                                    True
                                    if any(
                                        True
                                        for x in ["wc", "wildcard", "wild card"]
                                        if x in comment.body
                                    )
                                    else False
                                )
                                if who == "all":
                                    standings = statsapi.standings(
                                        date=datetime.today().strftime("%m/%d/%Y"),
                                        include_wildcard=wc,
                                    )
                                elif who in ["nle", "nlw", "nlc", "ale", "alw", "alc"]:
                                    standings = statsapi.standings(
                                        date=datetime.today().strftime("%m/%d/%Y"),
                                        division=who,
                                        include_wildcard=wc,
                                    )
                                elif who in ["nl", "al"]:
                                    leagueId = 103 if who == "al" else 104
                                    standings = statsapi.standings(
                                        leagueId=leagueId,
                                        date=datetime.today().strftime("%m/%d/%Y"),
                                        include_wildcard=wc,
                                    )

                                replyText += "\n    {}".format(
                                    standings.replace("\n", "\n    ")
                                )
                            except Exception as e:
                                self.log.error(
                                    "Error generating response for standings: {}".format(
                                        e
                                    )
                                )
                                self.comments[comment.id]["errors"].append(
                                    "Error generating response for standings: {}".format(
                                        e
                                    )
                                )

                        if "rundiff" in comment.body.lower():
                            self.comments[comment.id]["cmd"].append("rundiff")
                            if replyText != "":
                                replyText += "\n\n*****\n\n"

                            try:
                                whoTeamId = None
                                if comment.body.find("{") != -1:
                                    who = comment.body[
                                        comment.body.find("{")
                                        + 1 : comment.body.find("}")
                                    ].lower()
                                else:
                                    who = None

                                params = {
                                    "hydrate": "team(division)",
                                    "fields": "records,standingsType,teamRecords,team,name,division,id,nameShort,abbreviation,runDifferential",
                                }
                                if who in [
                                    "all",
                                    "nle",
                                    "nlw",
                                    "nlc",
                                    "ale",
                                    "alw",
                                    "alc",
                                    "nl",
                                    "al",
                                ]:
                                    if who == "all":
                                        params.update({"leagueId": "103,104"})
                                    elif who in [
                                        "nle",
                                        "nlw",
                                        "nlc",
                                        "ale",
                                        "alw",
                                        "alc",
                                    ]:
                                        params.update(
                                            {
                                                "leagueId": "103"
                                                if who[0] == "a"
                                                else "104"
                                            }
                                        )
                                    elif who in ["nl", "al"]:
                                        params.update(
                                            {
                                                "leagueId": "103"
                                                if who == "al"
                                                else "104"
                                            }
                                        )
                                else:
                                    whoTeamId = statsapi.lookup_team(who)[0]["id"]
                                    teamInfo = statsapi.get(
                                        "team", {"teamId": whoTeamId}
                                    )
                                    whoDivId = teamInfo["teams"][0]["division"]["id"]
                                    whoLeagueId = teamInfo["teams"][0]["league"]["id"]
                                    params.update({"leagueId": whoLeagueId})

                                r = statsapi.get("standings", params)

                                rundiff = ""
                                divisions = {}

                                for y in r["records"]:
                                    for x in (
                                        x
                                        for x in y["teamRecords"]
                                        if who == "all"
                                        or who
                                        == x["team"]["division"]["abbreviation"].lower()
                                        or (
                                            whoTeamId
                                            and whoDivId == x["team"]["division"]["id"]
                                        )
                                        or who in ["al", "nl"]
                                    ):
                                        if (
                                            x["team"]["division"]["id"]
                                            not in divisions.keys()
                                        ):
                                            divisions.update(
                                                {
                                                    x["team"]["division"]["id"]: {
                                                        "div_name": x["team"][
                                                            "division"
                                                        ]["name"],
                                                        "teams": [],
                                                    }
                                                }
                                            )

                                        team = {
                                            "name": x["team"]["name"],
                                            "run_diff": x["runDifferential"],
                                        }
                                        if (
                                            whoTeamId == x["team"]["id"]
                                            or not whoTeamId
                                        ):
                                            divisions[x["team"]["division"]["id"]][
                                                "teams"
                                            ].append(team)

                                for div in divisions.values():
                                    if not whoTeamId:
                                        rundiff += div["div_name"] + "\n"

                                    for t in div["teams"]:
                                        rundiff += "{name:<21}: {run_diff:^5} run(s)\n".format(
                                            **t
                                        )

                                    rundiff += "\n"

                                replyText += "\n    {}".format(
                                    rundiff.replace("\n", "\n    ")
                                )
                            except Exception as e:
                                self.log.error(
                                    "Error generating response for rundiff: {}".format(
                                        e
                                    )
                                )
                                self.comments[comment.id]["errors"].append(
                                    "Error generating response for rundiff: {}".format(
                                        e
                                    )
                                )

                        if replyText != "":
                            try:
                                latest_reply = comment.reply(
                                    replyText + "\n\n" + self.replyFooter
                                    if len(self.replyFooter) > 0
                                    else ""
                                )
                                self.comments[comment.id].update(
                                    {"reply": latest_reply}
                                )
                                latest_reply.disable_inbox_replies()
                                self.log.info(
                                    "Replied with comment id {} and disabled inbox replies.".format(
                                        latest_reply
                                    )
                                )
                                self.dbc.execute(
                                    "update {} set cmd=?,reply=? where comment_id=?;".format(
                                        self.dbTable
                                    ),
                                    (
                                        str(self.comments[comment.id]["cmd"]),
                                        str(latest_reply),
                                        str(comment.id),
                                    ),
                                )
                            except Exception as e:
                                self.log.error(
                                    "Error replying to comment or disabling inbox replies: {}".format(
                                        e
                                    )
                                )
                                self.comments[comment.id]["errors"].append(
                                    "Error submitting comment or disabling inbox replies: {}".format(
                                        e
                                    )
                                )

                        if len(self.comments[comment.id].get("errors")):
                            self.dbc.execute(
                                "update {} set errors=? where comment_id=?;".format(
                                    self.dbTable
                                ),
                                (
                                    str(self.comments[comment.id].get("errors")),
                                    str(comment.id),
                                ),
                            )

                        self.db.commit()
            except Exception as e:
                self.log.exception("Caught exception: {}".format(e))
                raise

            self.log.debug(
                "Checking for downvotes on {} replies...".format(
                    sum(
                        1
                        for x in self.comments
                        if self.comments[x].get("reply")
                        and not self.comments[x].get("removed")
                        and float(self.comments[x].get("date"))
                        >= time.time() - 60 * 60 * 24 * self.historicalDays
                    )
                )
            )
            for x in (
                x
                for x in self.comments
                if self.comments[x].get("reply")
                and not self.comments[x].get("removed")
                and float(self.comments[x].get("date"))
                >= time.time() - 60 * 60 * 24 * self.historicalDays
            ):
                # print('Submission: {}, reply: {}'.format(self.r.comment(x).submission, self.comments[x]['reply']))
                try:
                    self.comments[x]["reply"].refresh()
                except praw.exceptions.ClientException as e:
                    print(
                        "Error refreshing attributes for comment reply {}: {}".format(
                            self.comments[x]["reply"], e
                        )
                    )
                    if "comment does not appear to be in the comment tree" in str(e):
                        self.comments[x].update({"removed": time.time()})
                        self.dbc.execute(
                            "update {} set removed=? where comment_id=?;".format(
                                self.dbTable
                            ),
                            (str(self.comments[x].get("removed")), str(x)),
                        )

                if (
                    not self.comments[x].get("removed")
                    and self.comments[x]["reply"].score <= self.delThreshold
                ):
                    self.log.info(
                        "Deleting comment {} with score ({}) at or below threshold ({})...".format(
                            self.comments[x]["reply"],
                            self.comments[x]["reply"].score,
                            self.delThreshold,
                        )
                    )
                    try:
                        self.comments[x]["reply"].delete()
                        self.comments[x].update({"removed": time.time()})
                        self.dbc.execute(
                            "update {} set removed=? where comment_id=?;".format(
                                self.dbTable
                            ),
                            (str(self.comments[x].get("removed")), str(x)),
                        )
                    except Exception as e:
                        self.log.error("Error deleting downvoted comment: {}".format(e))
                        self.comments[x]["errors"].append(
                            "Error deleting downvoted comment: {}".format(e)
                        )

            self.db.commit()

            limits = self.r.auth.limits
            if limits.get("remaining") < 60:
                self.log.warning(
                    "Approaching Reddit API rate limit, sleeping for a minute... {}".format(
                        limits
                    )
                )
                time.sleep(60)
            else:
                self.log.debug("Reddit API limits: {}".format(limits))

        return

    def lookup_player(self, keyword):
        """Check statsapi.lookup_player() and if no results, try other MLB source.
        Stats API only returns active players.
        """
        players = statsapi.lookup_player(keyword)
        if len(players):
            return players[0]["id"]

        else:
            r = requests.get(
                "http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=%27mlb%27&name_part=%27{}%25%27".format(
                    keyword
                )
            )
            if r.status_code not in [200, 201]:
                self.log.error(
                    "Error looking up player from alternate MLB source. Status code: {}.".format(
                        r.status_code
                    )
                )
                return ""
            else:
                return (
                    r.json()["search_player_all"]["queryResults"]["row"]["player_id"]
                    if r.json()["search_player_all"]["queryResults"]["totalSize"] == "1"
                    else r.json()["search_player_all"]["queryResults"]["row"][0][
                        "player_id"
                    ]
                )


def run(bot=None, settings=None):
    tl.log = logger.init_logger(
        logger_name="redball.bots." + threading.current_thread().name,
        log_to_console=settings.get("Logging", {}).get("LOG_TO_CONSOLE", True),
        log_to_file=settings.get("Logging", {}).get("LOG_TO_FILE", True),
        log_path=redball.LOG_PATH,
        log_file="{}.log".format(threading.current_thread().name),
        file_log_level=settings.get("Logging", {}).get("FILE_LOG_LEVEL", "DEBUG"),
        log_retention=settings.get("Logging", {}).get("LOG_RETENTION", 7),
        console_log_level=settings.get("Logging", {}).get("CONSOLE_LOG_LEVEL", "INFO"),
        clear_first=True,
        propagate=settings.get("Logging", {}).get("PROPAGATE", False),
    )

    mlbbot = StatBot(settings, bot)
    mlbbot.run()
