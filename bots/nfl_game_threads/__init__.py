#!/usr/bin/env python
# encoding=utf-8
"""NFL Game Thread Bot
by Todd Roberts
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError
from copy import deepcopy
from datetime import datetime, timedelta
import json
import pytz
import requests
import sys
import traceback
import tzlocal
import time

import threading

import redball
from redball import database as rbdb, logger

import os

from mako.lookup import TemplateLookup
import mako.exceptions

from . import mynflapi
import pyprowl
import twitter

import praw

__version__ = "2.3.0"

DATA_LOCK = threading.Lock()


def run(bot, settings):
    thisBot = Bot(bot, settings)
    thisBot.run()


class Bot(object):
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        self.staleThreads = []
        self.BOT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.BOT_TEMPLATE_PATH = []
        if self.settings.get("Bot", {}).get("TEMPLATE_PATH", "") != "":
            self.BOT_TEMPLATE_PATH.append(self.settings["Bot"]["TEMPLATE_PATH"])
        self.BOT_TEMPLATE_PATH.append(os.path.join(self.BOT_PATH, "templates"))

        self.LOOKUP = TemplateLookup(directories=self.BOT_TEMPLATE_PATH)

    def run(self):
        self.log = logger.init_logger(
            logger_name="redball.bots." + threading.current_thread().name,
            log_to_console=self.settings.get("Logging", {}).get("LOG_TO_CONSOLE", True),
            log_to_file=self.settings.get("Logging", {}).get("LOG_TO_FILE", True),
            log_path=redball.LOG_PATH,
            log_file="{}.log".format(threading.current_thread().name),
            file_log_level=self.settings.get("Logging", {}).get("FILE_LOG_LEVEL"),
            log_retention=self.settings.get("Logging", {}).get("LOG_RETENTION", 7),
            console_log_level=self.settings.get("Logging", {}).get("CONSOLE_LOG_LEVEL"),
            clear_first=True,
            propagate=False,
        )
        self.log.debug(
            "NFL Game Thread Bot v{} received settings: {}. Template path: {}".format(
                __version__, self.settings, self.BOT_TEMPLATE_PATH
            )
        )

        # Check db for tables and create if necessary
        self.dbTablePrefix = self.settings.get("Database").get(
            "dbTablePrefix", "nfl_gdt{}_".format(self.bot.id)
        )
        self.build_tables()

        # Initialize Reddit API connection
        self.init_reddit()

        # Initialize scheduler
        if "SCHEDULER" in vars(self.bot):
            # Scheduler already exists, maybe bot restarted
            sch_jobs = self.bot.SCHEDULER.get_jobs()
            self.log.warning(
                f"Scheduler already exists on bot startup with the following job(s): {sch_jobs}"
            )
            # Remove all jobs and shut down so we can start fresh
            for x in sch_jobs:
                x.remove()
            try:
                self.bot.SCHEDULER.shutdown()
            except SchedulerNotRunningError as e:
                self.log.debug(f"Could not shut down scheduler because: {e}")

        self.bot.SCHEDULER = BackgroundScheduler(
            timezone=tzlocal.get_localzone()
            if str(tzlocal.get_localzone()) != "local"
            else "America/New_York"
        )
        self.bot.SCHEDULER.start()

        self.bot.detailedState = {
            "summary": {
                "text": "Starting up, please wait 1 minute...",
                "html": "Starting up, please wait 1 minute...",
                "markdown": "Starting up, please wait 1 minute...",
            }
        }  # Initialize detailed state to a wait message

        # Start a scheduled task to update self.bot.detailedState every minute
        if not next(
            (
                x
                for x in self.bot.SCHEDULER.get_jobs()
                if x.name == f"bot-{self.bot.id}-statusUpdateTask"
            ),
            None,
        ):
            self.bot.SCHEDULER.add_job(
                self.bot_state,
                "interval",
                name=f"bot-{self.bot.id}-statusUpdateTask",
                minutes=1,
            )
        else:
            self.log.debug(
                f"The bot-{self.bot.id}-statusUpdateTask scheduled job already exists."
            )

        settings_date = datetime.today().strftime("%Y-%m-%d")
        if self.settings.get("NFL", {}).get("GAME_DATE_OVERRIDE", "") != "":
            # Bot config says to treat specified date as 'today'
            todayOverrideFlag = True
        else:
            todayOverrideFlag = False

        while redball.SIGNAL is None and not self.bot.STOP:
            # This is the daily loop
            # Refresh settings
            if settings_date != datetime.today().strftime("%Y-%m-%d"):
                self.refresh_settings()
                settings_date = datetime.today().strftime("%Y-%m-%d")

            if todayOverrideFlag:
                self.log.info(
                    "Overriding game date per GAME_DATE_OVERRIDE setting [{}].".format(
                        self.settings["NFL"]["GAME_DATE_OVERRIDE"]
                    )
                )
                try:
                    todayObj = datetime.strptime(
                        self.settings["NFL"]["GAME_DATE_OVERRIDE"], "%Y-%m-%d"
                    )
                except Exception as e:
                    self.log.error(
                        "Error overriding game date. Falling back to today's date. Error: {}".format(
                            e
                        )
                    )
                    self.error_notification(
                        "Error overriding game date. Falling back to today's date"
                    )
                    todayObj = datetime.today()
            else:
                todayObj = datetime.today()

            self.today = {
                "Y-m-d": todayObj.strftime("%Y-%m-%d"),
                "Ymd": todayObj.strftime("%Y%m%d"),
                "Y": todayObj.strftime("%Y"),
            }
            self.today.update(
                {
                    "season": (
                        str(int(self.today["Y"]) - 1)
                        if int(self.today["Y-m-d"].split("-")[1]) < 4
                        else self.today["Y"]
                    )
                }
            )
            self.log.debug(
                f"Today is {self.today['Y-m-d']}. Season: {self.today['season']}."
            )

            # (Re-)Initialize NFL API
            self.log.debug(
                f"Initializing NFL API with mynflapi v{mynflapi.__version__}"
            )
            self.nfl = mynflapi.APISession(self.getNflToken())
            # Start a scheduled task to refresh NFL API token before it expires
            if not next(
                (x for x in self.bot.SCHEDULER.get_jobs() if x.name == "getNflToken"),
                None,
            ):
                self.log.debug("Scheduling getNflToken job...")
                # First check if job exists
                self.bot.SCHEDULER.add_job(
                    self.getNflToken,
                    "interval",
                    name=f"bot-{self.bot.id}-getNflToken",
                    kwargs={"nflSession": self.nfl},
                    minutes=58,
                )
            else:
                self.log.debug("The getNflToken scheduled job already exists.")

            # Get info about configured team
            if self.settings.get("NFL", {}).get("TEAM", "") == "":
                self.log.critical("No team selected! Set NFL > TEAM in Bot Config.")
                self.bot.STOP = True
                break

            self.allTeams = self.nfl.teams(season=self.today["season"])["teams"]
            self.log.debug(f"{self.allTeams=}")
            self.log.debug(
                f"{self.settings.get('NFL', {}).get('TEAM', '').split('|')[1]=}"
            )

            self.myTeam = next(
                (
                    x
                    for x in self.allTeams
                    if x["abbreviation"]
                    == self.settings.get("NFL", {}).get("TEAM", "").split("|")[1]
                ),
                None,
            )
            if not self.myTeam:
                self.log.critical(
                    "Unable to look up team info! Check NFL > TEAM in Bot Config."
                )
                self.bot.STOP = True
                break
            self.log.info("Configured team: {}".format(self.myTeam["fullName"]))
            self.log.debug(f"self.myTeam: {self.myTeam}")

            # Get other teams in my team's division
            self.otherDivisionTeams = [
                x
                for x in self.allTeams
                if x["divisionFullName"] == self.myTeam["divisionFullName"]
                and x["id"] != self.myTeam["id"]
            ]

            # Get current week and games
            if todayOverrideFlag:
                todayOverrideFlag = (
                    False  # Only override once, then go back to current date
                )

            currentWeek = self.nfl.weekByDate(self.today["Y-m-d"])
            if currentWeek.get("message"):
                self.log.error(
                    f"Error retrieving currentWeek Assuming no games today. Response: {currentWeek}"
                )
                currentWeekGames = []
            else:
                currentWeekGames = self.nfl.gamesByWeek(
                    season=currentWeek["season"],
                    week=currentWeek["week"],
                    seasonType=currentWeek["seasonType"],
                )["games"]
                self.log.debug(
                    f"Season: {currentWeek['season']}; Season Type: {currentWeek['seasonType']}; Week: {currentWeek['week']}"
                )

            # Get today's games
            todayGames = [
                g
                for g in currentWeekGames
                if self.convert_timezone(
                    datetime.strptime(g["time"], "%Y-%m-%dT%H:%M:%SZ"),
                    self.settings.get("Bot", {}).get(
                        "TEAM_TIMEZONE", "America/New_York"
                    ),
                ).strftime("%Y-%m-%d")
                == self.today["Y-m-d"]
            ]
            self.log.debug(f"Today's games: {todayGames}")
            myTeamTodayGameId = next(
                (
                    g["id"]
                    for g in todayGames
                    if self.myTeam["id"] in [g["awayTeam"]["id"], g["homeTeam"]["id"]]
                ),
                None,
            )
            self.log.debug(f"My team's game id for today: {myTeamTodayGameId}")

            otherTodayGamesDetails = {}
            for g in [g for g in todayGames if g["id"] != myTeamTodayGameId]:
                try:
                    g_details = self.nfl.gameDetails(g["id"])
                    g_details = (
                        g_details.get("data", {})
                        .get("viewer", {})
                        .get("gameDetail", {})
                    )
                except Exception as e:
                    if "404" in str(e):
                        self.log.debug(
                            f"Game detail is not published in NFL API yet for other today game [{g['id']}]: {e}"
                        )
                    else:
                        self.log.debug(
                            f"Unknown error retrieving game details for other today game [{g['id']}]: {e}"
                        )
                    g_details = {}
                otherTodayGamesDetails.update({g["id"]: g_details})

            # (Re-)Initialize dict to hold game data
            self.allData = {
                "myTeam": self.myTeam,
                "currentWeek": currentWeek,
                "currentWeekGames": currentWeekGames,
                "todayGames": todayGames,
                "gameId": myTeamTodayGameId,
                "otherDivisionTeams": self.otherDivisionTeams,
                "otherTodayGamesDetails": otherTodayGamesDetails,
            }
            # Initialize vars to hold data about reddit and process threads
            self.stopFlags = {"tailgate": False, "game": False, "post": False}
            """ Holds flags to indicate when reddit threads should stop updating """
            self.THREADS = {"tailgate": None, "game": None, "post": None}
            """ Holds process threads that will post/monitor/update each reddit thread """
            self.threadCache = {"tailgate": {}, "game": {}, "post": {}}
            """ Holds reddit threads and related data """

            isCanceled = False
            if myTeamTodayGameId:
                # Get game insights now so we can check for cancelation headlines
                gameInsights = self.nfl.gameInsights(gameId=myTeamTodayGameId)["data"][
                    "viewer"
                ]["gameInsight"]["insightsByGames"]
                isCanceled = self.isGameCanceled(gameInsights)

            if not myTeamTodayGameId or (myTeamTodayGameId and isCanceled):
                # It's not a game day
                self.log.info(
                    f"No games today!{' (Game canceled)' if isCanceled else ''}"
                )
                if redball.SIGNAL is not None or self.bot.STOP:
                    break
            else:
                self.log.info(f"IT'S GAME DAY! gameId: {myTeamTodayGameId}")
                gameById = self.nfl.gameById(gameId=myTeamTodayGameId)
                self.log.debug(f"gameById: {gameById}")
                myGameIndex = next(
                    (
                        k
                        for k, v in enumerate(todayGames)
                        if v["id"] == self.allData["gameId"]
                    ),
                    None,
                )
                homeAway = (
                    "home"
                    if todayGames[myGameIndex]["homeTeam"]["id"] == self.myTeam["id"]
                    else "away"
                    if todayGames[myGameIndex]["awayTeam"]["id"] == self.myTeam["id"]
                    else None
                )
                self.log.debug(f"My team is [{homeAway}] (homeAway)")
                oppTeam = todayGames[myGameIndex][
                    ("away" if homeAway == "home" else "home") + "Team"
                ]
                oppTeamId = oppTeam["id"]
                self.log.debug(f"oppTeamId: {oppTeamId}")
                oppTeam = self.nfl.teamById(teamId=oppTeamId)
                self.log.debug(f"oppTeam: {oppTeam}")
                gameTime = next(
                    (
                        self.convert_timezone(  # Convert Zulu to my team TZ
                            datetime.strptime(g["time"], "%Y-%m-%dT%H:%M:%SZ"),
                            self.settings.get("Bot", {}).get(
                                "TEAM_TIMEZONE", "America/New_York"
                            ),
                        )
                        .replace(tzinfo=None)
                        .isoformat()  # Convert back to tz-naive
                        for g in todayGames
                        if g["id"] == myTeamTodayGameId
                    ),
                    None,
                )
                gameTime_local = next(
                    (
                        self.convert_timezone(  # Convert Zulu to my team TZ
                            datetime.strptime(g["time"], "%Y-%m-%dT%H:%M:%SZ"),
                            "local",
                        )
                        for g in todayGames
                        if g["id"] == myTeamTodayGameId
                    ),
                    None,
                )
                self.log.debug(
                    f"gameTime (my team TZ): {gameTime}; gameTime_local: {gameTime_local}"
                )
                try:
                    standings = self.nfl.standings(
                        season=currentWeek["season"],
                        seasonType=currentWeek["seasonType"],
                        week=currentWeek["week"],
                    )
                    if len(standings["weeks"]) and standings["weeks"][0].get(
                        "standings"
                    ):
                        standings = standings["weeks"][0]["standings"]
                    else:
                        standings = []
                except Exception as e:
                    self.log.error(f"Error retrieving standings: {e}")
                    standings = []
                # Initialize var to hold game data throughout the day
                self.allData.update(
                    {
                        "myTeam": self.nfl.teamById(
                            teamId=todayGames[myGameIndex][homeAway + "Team"]["id"]
                        ),
                        "myTeamRoster": self.nfl.team_roster(self.myTeam["id"])["data"][
                            "viewer"
                        ]["clubs"]["currentClubRoster"],
                        "gameInsights": gameInsights,
                        "homeAway": homeAway,
                        "oppTeam": oppTeam,
                        "oppTeamRoster": self.nfl.team_roster(oppTeam["id"])["data"][
                            "viewer"
                        ]["clubs"]["currentClubRoster"],
                        "gameTime": {
                            # "homeTeam": datetime.fromisoformat(gameTime),
                            "bot": gameTime_local,
                            "myTeam": datetime.fromisoformat(gameTime),
                        },
                        "myGameIndex": myGameIndex,
                        "standings": standings,
                    }
                )
                """ Holds data about current week games, including detailed data for my team's game """
                try:
                    gameDetails = self.nfl.gameDetails(myTeamTodayGameId)
                except Exception as e:
                    if "404" in str(e):
                        self.log.debug(
                            f"Game detail is not published in NFL API yet: {e}"
                        )
                        gameDetails = {}
                    else:
                        raise
                try:
                    gameSummary = self.nfl.gameSummaryById(self.allData["gameId"])
                except Exception as e:
                    if "404" in str(e):
                        self.log.debug(
                            f"Game summary is not published in NFL API yet: {e}"
                        )
                        gameSummary = {}
                    else:
                        raise
                self.allData.update(
                    {
                        "gameDetails": gameDetails.get("data", {})
                        .get("viewer", {})
                        .get("gameDetail", {}),
                        "gameSummary": gameSummary,
                    }
                )
                if redball.DEV:
                    self.log.debug(f"allData: {self.allData}")

                # Check DB for gameId
                gq = f"select * from {self.dbTablePrefix}games where gameId = '{self.allData['gameId']}' and gameDate = '{self.today['Y-m-d']}';"
                dbGames = rbdb.db_qry(gq, closeAfter=True, logg=self.log)

                if dbGames and len(dbGames) > 0:
                    self.log.debug("Game is already in the database.")
                else:
                    # Add game to DB
                    q = (
                        f"insert into {self.dbTablePrefix}games (gameId, gameDate, dateAdded) "
                        f"values ('{self.allData['gameId']}', '{self.today['Y-m-d']}', {time.time()});"
                    )
                    rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)

                # Tailgate Thread
                if not self.settings.get("Tailgate Thread", {}).get("ENABLED", True):
                    self.log.info("Pre thread disabled.")
                    self.stopFlags.update({"pre": True})
                else:
                    # Spawn a thread to wait for post time and then keep tailgate thread updated
                    self.THREADS.update(
                        {
                            "tailgate": threading.Thread(
                                target=self.tailgate_thread_update_loop,
                                name="bot-{}-{}-tailgate".format(
                                    self.bot.id, self.bot.name.replace(" ", "-")
                                ),
                                daemon=True,
                            )
                        }
                    )
                    self.THREADS["tailgate"].start()
                    self.log.debug(
                        "Started tailgate thread {}.".format(self.THREADS["tailgate"])
                    )

                # Game thread update processes
                if self.settings.get("Game Thread", {}).get("ENABLED", True):
                    # Spawn separate thread to wait for post time and then keep game thread updated
                    self.THREADS.update(
                        {
                            "game": threading.Thread(
                                target=self.game_thread_update_loop,
                                name="bot-{}-{}-game".format(
                                    self.bot.id,
                                    self.bot.name.replace(" ", "-"),
                                ),
                                daemon=True,
                            )
                        }
                    )
                    self.THREADS["game"].start()
                    self.log.debug(
                        "Started game thread {}.".format(self.THREADS["game"])
                    )
                else:
                    self.log.info("Game thread is disabled!")
                    self.stopFlags.update({"game": True})

                if self.settings.get("Post Game Thread", {}).get("ENABLED", True):
                    # Spawn separate thread to wait for game to be final and then submit and keep post game thread updated
                    self.THREADS.update(
                        {
                            "post": threading.Thread(
                                target=self.postgame_thread_update_loop,
                                name="bot-{}-{}-postgame".format(
                                    self.bot.id,
                                    self.bot.name.replace(" ", "-"),
                                ),
                                daemon=True,
                            )
                        }
                    )
                    self.THREADS["post"].start()
                    self.log.debug(
                        "Started post game thread {}.".format(self.THREADS["post"])
                    )
                else:
                    self.log.info("Post game thread is disabled!")
                    self.stopFlags.update({"post": True})

                # Loop while there are still active threads, make sure submit/update threads are running
                while (
                    next((k for k, v in self.stopFlags.items() if not v), None)
                    and redball.SIGNAL is None
                    and not self.bot.STOP
                ):
                    # Check submit/update thread for game thread
                    try:
                        if not self.settings.get("Game Thread", {}).get(
                            "ENABLED", True
                        ):
                            # Game thread is disabled, so don't start an update thread...
                            pass
                        elif (
                            not self.stopFlags["game"]
                            and self.THREADS.get("game")
                            and isinstance(
                                self.THREADS["game"],
                                threading.Thread,
                            )
                            and self.THREADS["game"].is_alive()
                        ):
                            self.log.debug(
                                "Game thread looks fine..."
                            )  # debug - need this here to see if the condition is working when the thread crashes
                            # pass
                        elif self.stopFlags["game"]:
                            # Game thread is already done
                            pass
                        else:
                            raise Exception(
                                "Game thread update process is not running!"
                            )
                    except Exception as e:
                        if "is not running" in str(e):
                            self.log.error(
                                "Game thread update process is not running. Attempting to start."
                            )
                            self.error_notification(
                                "Game thread update process is not running"
                            )
                            self.THREADS.update(
                                {
                                    "game": threading.Thread(
                                        target=self.game_thread_update_loop,
                                        name="bot-{}-{}-game".format(
                                            self.bot.id,
                                            self.bot.name.replace(" ", "-"),
                                        ),
                                        daemon=True,
                                    )
                                }
                            )
                            self.THREADS["game"].start()
                            self.log.debug(
                                "Started game thread {}.".format(self.THREADS["game"])
                            )
                        else:
                            raise

                    # Check submit/update thread for post game thread
                    try:
                        if not self.settings.get("Post Game Thread", {}).get(
                            "ENABLED", True
                        ):
                            # Post game thread is disabled, so don't start an update thread...
                            pass
                        elif (
                            not self.stopFlags["post"]
                            and self.THREADS.get("post")
                            and isinstance(
                                self.THREADS["post"],
                                threading.Thread,
                            )
                            and self.THREADS["post"].is_alive()
                        ):
                            self.log.debug(
                                "Post game thread looks fine..."
                            )  # debug - need this here to see if the condition is working when the thread crashes
                            # pass
                        elif self.stopFlags["post"]:
                            # Post game thread is already done
                            pass
                        else:
                            raise Exception(
                                "Post game thread update process is not running!"
                            )
                    except Exception as e:
                        if "is not running" in str(e):
                            self.log.error(
                                "Post game thread update process is not running. Attempting to start."
                            )
                            self.error_notification(
                                "Post game thread update process is not running"
                            )
                            self.THREADS.update(
                                {
                                    "post": threading.Thread(
                                        target=self.postgame_thread_update_loop,
                                        name="bot-{}-{}-postgame".format(
                                            self.bot.id,
                                            self.bot.name.replace(" ", "-"),
                                        ),
                                        daemon=True,
                                    )
                                }
                            )
                            self.THREADS["post"].start()
                            self.log.debug(
                                "Started post game thread {}.".format(
                                    self.THREADS["post"]
                                )
                            )
                        else:
                            raise

                    # Make sure tailgate thread update process is running
                    try:
                        if not self.settings.get("Tailgate Thread", {}).get(
                            "ENABLED", True
                        ):
                            # Tailgate thread is disabled, so don't start an update thread...
                            pass
                        elif (
                            not self.stopFlags["tailgate"]
                            and self.THREADS.get("tailgate")
                            and isinstance(self.THREADS["tailgate"], threading.Thread)
                            and self.THREADS["tailgate"].is_alive()
                        ):
                            self.log.debug(
                                "Tailgate update thread looks fine..."
                            )  # debug - need this here to see if the condition is working when the thread crashes
                            # pass
                        elif self.stopFlags["tailgate"]:
                            # Tailgate thread is already done
                            pass
                        else:
                            raise Exception(
                                "Tailgate thread update process is not running!"
                            )
                    except Exception as e:
                        if "is not running" in str(e):
                            self.log.error(
                                "Tailgate thread update process is not running. Attempting to start. Error: {}".format(
                                    e
                                )
                            )
                            self.error_notification(
                                "Tailgate thread update process is not running"
                            )
                            self.THREADS.update(
                                {
                                    "tailgate": threading.Thread(
                                        target=self.tailgate_thread_update_loop,
                                        name="bot-{}-{}-tailgate".format(
                                            self.bot.id,
                                            self.bot.name.replace(" ", "-"),
                                        ),
                                        daemon=True,
                                    )
                                }
                            )
                            self.THREADS["tailgate"].start()
                            self.log.debug(
                                "Started tailgate thread {}.".format(
                                    self.THREADS["tailgate"]
                                )
                            )
                        else:
                            raise

                    if next((k for k, v in self.stopFlags.items() if not v), None):
                        # There are still threads pending/in progress
                        self.log.debug(
                            "Thread(s) with negative stop flags: {}".format(
                                [k for k, v in self.stopFlags.items() if not v]
                            )
                        )
                        self.log.debug(
                            "Active update process threads: {}".format(
                                [
                                    t
                                    for t in threading.enumerate()
                                    if t.name.startswith(
                                        "bot-{}-{}".format(
                                            self.bot.id,
                                            self.bot.name.replace(" ", "-"),
                                        )
                                    )
                                ]
                            )
                        )
                        self.sleep(30)
                    else:
                        break

                if redball.SIGNAL is not None or self.bot.STOP:
                    break

            self.log.info("All done for today! Going into end of day loop...")
            self.eod_loop(self.today["Y-m-d"])

        self.bot.SCHEDULER.shutdown()
        self.log.info("Bot {} (id={}) exiting...".format(self.bot.name, self.bot.id))
        self.bot.detailedState = {
            "lastUpdated": datetime.today().strftime("%m/%d/%Y %I:%M:%S %p"),
            "summary": {
                "text": "Bot has been stopped.",
                "html": "Bot has been stopped.",
                "markdown": "Bot has been stopped.",
            },
        }

    def tailgate_thread_update_loop(self):
        skipFlag = None  # Will be set later if tailgate thread edit should be skipped

        # Check/wait for time to submit tailgate thread
        self.threadCache["tailgate"].update(
            {
                "postTime_local": datetime.strptime(
                    datetime.today().strftime(
                        "%Y-%m-%d "
                        + self.settings.get("Tailgate Thread", {}).get(
                            "POST_TIME", "05:00"
                        )
                    ),
                    "%Y-%m-%d %H:%M",
                )
            }
        )
        self.log.debug(
            "Tailgate thread post time: {}".format(
                self.threadCache["tailgate"]["postTime_local"]
            )
        )
        while (
            datetime.today() < self.threadCache["tailgate"]["postTime_local"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            if (
                self.threadCache["tailgate"]["postTime_local"] - datetime.today()
            ).total_seconds() > 3600:
                self.log.info(
                    "Tailgate thread should not be posted for a long time ({}). Sleeping for an hour...".format(
                        self.threadCache["tailgate"]["postTime_local"]
                    )
                )
                self.sleep(3600)
            elif (
                self.threadCache["tailgate"]["postTime_local"] - datetime.today()
            ).total_seconds() > 1800:
                self.log.info(
                    "Tailgate thread post time is still more than 30 minutes away ({}). Sleeping for a half hour...".format(
                        self.threadCache["tailgate"]["postTime_local"]
                    )
                )
                self.sleep(1800)
            else:
                self.log.info(
                    "Tailgate thread post time is approaching ({}). Sleeping until then...".format(
                        self.threadCache["tailgate"]["postTime_local"]
                    )
                )
                self.sleep(
                    (
                        self.threadCache["tailgate"]["postTime_local"]
                        - datetime.today()
                    ).total_seconds()
                )

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        # Unsticky stale threads
        if self.settings.get("Reddit", {}).get("STICKY", False):
            if len(self.staleThreads):
                self.unsticky_threads(self.staleThreads)
                self.staleThreads = []

        # Check if tailgate thread already posted (record in threads table with type='tailgate' for today's gameId)
        tgq = f"select * from {self.dbTablePrefix}threads where type='tailgate' and gameId = '{self.allData['gameId']}' and gameDate = '{self.today['Y-m-d']}' and deleted=0;"
        tgThread = rbdb.db_qry(tgq, closeAfter=True, logg=self.log)

        tailgateThread = None
        if len(tgThread) > 0:
            self.log.info(f"Tailgate thread found in database [{tgThread[0]['id']}].")
            tailgateThread = self.reddit.submission(tgThread[0]["id"])
            if not tailgateThread.author:
                self.log.warning("Tailgate thread appears to have been deleted.")
                q = "update {}threads set deleted=1 where id='{}';".format(
                    self.dbTablePrefix, tailgateThread.id
                )
                u = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
                if isinstance(u, str):
                    self.log.error(
                        "Error marking thread as deleted in database: {}".format(u)
                    )

                tailgateThread = None
            else:
                if tailgateThread.selftext.find("\n\n^^^Last ^^^Updated") != -1:
                    tailgateThreadText = tailgateThread.selftext[
                        0 : tailgateThread.selftext.find("\n\n^^^Last ^^^Updated:")
                    ]
                elif tailgateThread.selftext.find("\n\n^^^Posted") != -1:
                    tailgateThreadText = tailgateThread.selftext[
                        0 : tailgateThread.selftext.find("\n\n^^^Posted:")
                    ]
                else:
                    tailgateThreadText = tailgateThread.selftext

                self.threadCache["tailgate"].update(
                    {
                        "text": tailgateThreadText,
                        "thread": tailgateThread,
                        "title": tailgateThread.title
                        if tailgateThread not in [None, False]
                        else None,
                    }
                )
                # Only sticky when posting the thread
                # if self.settings.get('Reddit',{}).get('STICKY',False): self.sticky_thread(tailgateThread)

        if not tailgateThread:
            # Submit tailgate thread
            (tailgateThread, tailgateThreadText) = self.prep_and_post(
                "tailgate",
                postFooter="""

^^^Posted: ^^^"""
                + self.convert_timezone(
                    datetime.utcnow(),
                    self.settings.get("Bot", {}).get(
                        "TEAM_TIMEZONE", "America/New_York"
                    ),
                ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z")
                + ", ^^^Update ^^^Interval: ^^^{} ^^^Minutes".format(
                    self.settings.get("Tailgate Thread", {}).get("UPDATE_INTERVAL", 5)
                ),
            )
            self.threadCache["tailgate"].update(
                {
                    "text": tailgateThreadText,
                    "thread": tailgateThread,
                    "title": tailgateThread.title
                    if tailgateThread not in [None, False]
                    else None,
                }
            )
            skipFlag = True
        else:
            self.threadCache["tailgate"].update({"thread": tailgateThread})

        while (
            not self.stopFlags["tailgate"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            # Keep tailgate thread updated
            if skipFlag:
                # Skip check/edit since skip flag is set
                skipFlag = None
                self.log.debug(
                    "Skip flag is set, tailgate thread was just submitted/edited and does not need to be checked."
                )
            else:
                try:
                    # Update data
                    self.collect_data()
                    # self.log.debug('data passed into render_template: {}'.format(self.allData))#debug
                    text = self.render_template(
                        thread="tailgate",
                        templateType="thread",
                        data=self.allData,
                        settings=self.settings,
                    )
                    self.log.debug("Rendered tailgate thread text: {}".format(text))
                    if text != self.threadCache["tailgate"].get("text") and text != "":
                        self.threadCache["tailgate"].update({"text": text})
                        text += (
                            """

^^^Last ^^^Updated: ^^^"""
                            + self.convert_timezone(
                                datetime.utcnow(),
                                self.settings.get("Bot", {}).get(
                                    "TEAM_TIMEZONE", "America/New_York"
                                ),
                            ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z")
                            + ", ^^^Update ^^^Interval: ^^^{} ^^^Minutes".format(
                                self.settings.get("Tailgate Thread", {}).get(
                                    "UPDATE_INTERVAL", 5
                                )
                            )
                        )
                        self.threadCache["tailgate"]["thread"].edit(text)
                        self.log.info("Tailgate thread edits submitted.")
                        self.count_check_edit(
                            self.threadCache["tailgate"]["thread"].id, "NA", edit=True
                        )
                        self.log_last_updated_date_in_db(
                            self.threadCache["tailgate"]["thread"].id
                        )
                    elif text == "":
                        self.log.info(
                            "Skipping tailgate thread edit since thread text is blank..."
                        )
                    else:
                        self.log.info("No changes to tailgate thread.")
                        self.count_check_edit(
                            self.threadCache["tailgate"]["thread"].id, "NA", edit=False
                        )
                except Exception as e:
                    self.log.error("Error editing tailgate thread: {}".format(e))
                    self.error_notification("Error editing tailgate thread")

            update_tailgate_thread_until = self.settings.get("Tailgate Thread", {}).get(
                "UPDATE_UNTIL", "Game thread is posted"
            )
            if update_tailgate_thread_until not in [
                "Do not update",
                "Game thread is posted",
                "All division games are final",
                "All NFL games are final",
            ]:
                # Unsupported value, use default
                update_tailgate_thread_until = "Game thread is posted"

            if not self.settings.get("Tailgate Thread", {}).get("ENABLED", True):
                # Tailgate thread is already posted, but disabled. Don't update it.
                self.log.info(
                    "Stopping tailgate thread update loop because tailgate thread is disabled."
                )
                self.stopFlags.update({"tailgate": True})
                break
            elif update_tailgate_thread_until == "Do not update":
                # Setting says not to update
                self.log.info(
                    "Stopping tailgate thread update loop per UPDATE_UNTIL setting."
                )
                self.stopFlags.update({"tailgate": True})
                break
            elif update_tailgate_thread_until == "Game thread is posted":
                if self.threadCache["game"].get("thread"):
                    # Game thread is posted
                    self.log.info(
                        "Game thread is posted. Stopping tailgate thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"tailgate": True})
                    break
            elif update_tailgate_thread_until == "All division games are final":
                if (  # This game is final
                    self.allData["gameDetails"].get("phase", "UNKNOWN")
                    in ["FINAL", "FINAL_OVERTIME", "CANCELED", "CANCELLED"]
                ) and not next(  # And all division games are final
                    (
                        True
                        for x in self.allData["todayGames"]
                        if self.allData["otherTodayGamesDetails"]
                        .get(x["id"], {})
                        .get("PHASE")
                        in ["PREGAME", "INGAME", "HALFTIME"]
                        and any(
                            (
                                True
                                for divTeam in self.otherDivisionTeams
                                if divTeam["abbreviation"]
                                in [
                                    x["visitorTeam"]["abbreviation"],
                                    x["homeTeam"]["abbreviation"],
                                ]
                            )
                        )
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping tailgate thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"tailgate": True})
                    break
            elif update_tailgate_thread_until == "All NFL games are final":
                if (  # This game is final
                    self.allData["gameDetails"].get("phase", "UNKNOWN")
                    in ["FINAL", "FINAL_OVERTIME", "CANCELED", "CANCELLED"]
                ) and not next(  # All NFL games are final
                    (
                        True
                        for x in self.allData["todayGames"]
                        if self.allData["otherTodayGamesDetails"]
                        .get(x["id"], {})
                        .get("PHASE")
                        in ["PREGAME", "INGAME", "HALFTIME"]
                    ),
                    False,
                ):
                    # NFL games are all final
                    self.log.info(
                        "All NFL games are final. Stopping tailgate thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"tailgate": True})
                    break

            self.log.debug(
                "Tailgate thread stop criteria not met ({}).".format(
                    update_tailgate_thread_until
                )
            )  # debug - need this to tell if logic is working

            # Update interval is in minutes (seconds for game thread only)
            tgtWait = self.settings.get("Tailgate Thread", {}).get("UPDATE_INTERVAL", 5)
            if tgtWait < 1:
                tgtWait = 1
            self.log.info("Sleeping for {} minutes...".format(tgtWait))
            self.sleep(tgtWait * 60)

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        # Mark tailgate thread as stale
        if self.threadCache["tailgate"].get("thread"):
            self.staleThreads.append(self.threadCache["tailgate"]["thread"])

        self.log.debug("Ending tailgate update thread...")
        return

    def game_thread_update_loop(self):
        skipFlag = (
            None  # Will be set later if game thread submit/edit should be skipped
        )

        # Check if game thread is already posted
        gq = "select * from {}threads where type='game' and gameId = '{}' and gameDate = '{}' and deleted=0;".format(
            self.dbTablePrefix, self.allData["gameId"], self.today["Y-m-d"]
        )
        gThread = rbdb.db_qry(gq, closeAfter=True, logg=self.log)

        gameThread = None
        if len(gThread) > 0:
            self.log.info("Game thread found in database [{}]".format(gThread[0]["id"]))
            gameThread = self.reddit.submission(gThread[0]["id"])
            if not gameThread.author:
                self.log.warning("Game thread appears to have been deleted.")
                q = "update {}threads set deleted=1 where id='{}';".format(
                    self.dbTablePrefix, gameThread.id
                )
                u = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
                if isinstance(u, str):
                    self.log.error(
                        "Error marking thread as deleted in database: {}".format(u)
                    )

                gameThread = None
            else:
                if gameThread.selftext.find("\n\n^^^Last ^^^Updated") != -1:
                    gameThreadText = gameThread.selftext[
                        0 : gameThread.selftext.find("\n\n^^^Last ^^^Updated:")
                    ]
                elif gameThread.selftext.find("\n\n^^^Posted") != -1:
                    gameThreadText = gameThread.selftext[
                        0 : gameThread.selftext.find("\n\n^^^Posted:")
                    ]
                else:
                    gameThreadText = gameThread.selftext

                self.threadCache["game"].update(
                    {
                        "thread": gameThread,
                        "text": gameThreadText,
                        "title": gameThread.title
                        if gameThread not in [None, False]
                        else None,
                    }
                )
                # Only sticky when posting the thread
                # if self.settings.get('Reddit',{}).get('STICKY',False): self.sticky_thread(self.threadCache['game']['thread'])

        if not gameThread:
            # Determine time to post
            gameStart = self.allData["gameTime"]["bot"]
            postBy = tzlocal.get_localzone().localize(
                datetime.strptime(
                    datetime.today().strftime(
                        "%Y-%m-%d "
                        + self.settings.get("Game Thread", {}).get("POST_BY", "23:59")
                    ),
                    "%Y-%m-%d %H:%M",
                )
            )
            minBefore = int(
                self.settings.get("Game Thread", {}).get("MINUTES_BEFORE", 180)
            )
            minBefore_time = gameStart - timedelta(minutes=minBefore)
            self.threadCache["game"].update(
                {
                    "postTime": min(gameStart, postBy, minBefore_time),
                    "postTime_local": min(gameStart, postBy, minBefore_time).replace(
                        tzinfo=None
                    ),
                }
            )
            self.log.debug(
                "Game thread post time: {} (min of Game Start: {}, Post By: {}, Min Before: {})".format(
                    self.threadCache["game"]["postTime_local"],
                    gameStart,
                    postBy,
                    minBefore_time,
                )
            )

            # Check/wait for time to submit game thread
            while (
                datetime.today() < self.threadCache["game"]["postTime_local"]
                and redball.SIGNAL is None
                and not self.bot.STOP
                and not self.threadCache["game"].get("thread")
            ):
                if self.allData["gameDetails"].get("phase", "UNKNOWN") in [
                    "FINAL",
                    "FINAL_OVERTIME",
                    "CANCELED",
                    "CANCELLED",
                ]:
                    if not self.settings.get("Post Game Thread", {}).get(
                        "ENABLED", True
                    ):
                        # Post game thread is disabled
                        if not self.settings.get("Game Thread", {}).get(
                            "ENABLED", True
                        ):
                            # Game thread is also disabled
                            skipFlag = True
                        else:
                            # Need to post game thread because post game thread is disabled
                            skipFlag = False
                    else:
                        # Post game thread is enabled, so skip game thread
                        self.log.info(
                            "Game is {}; skipping game thread...".format(
                                self.allData["gameDetails"].get("phase", "UNKNOWN"),
                            )
                        )
                        skipFlag = True
                    break
                elif self.allData["gameDetails"].get("phase", "UNKNOWN") in [
                    "INGAME",
                    "HALFTIME",
                ]:
                    # Game is already in live status (including halftime), so submit the game thread!
                    self.log.info(
                        "It's technically not time to submit the game thread yet, but the game status is INGAME/HALFTIME. Proceeding..."
                    )
                    break
                elif not self.settings.get("Game Thread", {}).get("ENABLED", True):
                    # Game thread is disabled
                    self.log.info("Game thread is disabled.")
                    skipFlag = True
                    break

                if (
                    self.threadCache["game"]["postTime_local"] - datetime.today()
                ).total_seconds() >= 600:
                    self.log.info(
                        "Waiting for time to submit game thread: {}. Sleeping for 10 minutes...".format(
                            self.threadCache["game"]["postTime_local"],
                        )
                    )
                    self.sleep(600)
                else:
                    self.log.info(
                        "Game thread should be posted soon, sleeping until then ({})...".format(
                            self.threadCache["game"]["postTime_local"]
                        )
                    )
                    self.sleep(
                        (
                            self.threadCache["game"]["postTime_local"]
                            - datetime.today()
                        ).total_seconds()
                    )

            if redball.SIGNAL is not None or self.bot.STOP:
                self.log.debug("Caught a stop signal...")
                return

            # Unsticky stale threads
            if self.settings.get("Reddit", {}).get("STICKY", False):
                # Make sure tailgate thread is marked as stale, since we want the game thread to be sticky instead
                if (
                    self.threadCache.get("tailgate", {}).get("thread")
                    and self.threadCache["tailgate"]["thread"] not in self.staleThreads
                ):
                    self.staleThreads.append(self.threadCache["tailgate"]["thread"])

                if len(self.staleThreads):
                    self.unsticky_threads(self.staleThreads)
                    self.staleThreads = []

            if skipFlag or not self.settings.get("Game Thread", {}).get(
                "ENABLED", True
            ):
                # Skip game thread since skip flag is set or game thread is disabled
                if self.settings.get("Game Thread", {}).get("ENABLED", True):
                    self.log.info("Skipping game thread...")
                else:
                    self.log.info("Game thread is disabled, so skipping...")
            else:
                # Submit Game Thread
                self.log.info("Preparing to post game thread...")
                (gameThread, gameThreadText) = self.prep_and_post(
                    "game",
                    postFooter="""

^^^Posted: ^^^"""
                    + self.convert_timezone(
                        datetime.utcnow(),
                        self.settings.get("Bot", {}).get(
                            "TEAM_TIMEZONE", "America/New_York"
                        ),
                    ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z"),
                )
                self.threadCache["game"].update(
                    {
                        "thread": gameThread,
                        "text": gameThreadText,
                        "title": gameThread.title
                        if gameThread not in [None, False]
                        else None,
                    }
                )

            # Thread is not posted, so don't start an update loop
            if not self.threadCache["game"].get("thread") and self.settings.get(
                "Game Thread", {}
            ).get("ENABLED", True):
                # Game thread is enabled but failed to post
                self.log.info("Game thread not posted. Ending update loop...")
                self.stopFlags.update({"game": True})
                return  # TODO: Determine why thread is not posted and retry if temporary issue

            skipFlag = True  # Skip first edit since the thread was just posted

        while (
            not self.stopFlags["game"] and redball.SIGNAL is None and not self.bot.STOP
        ):
            if skipFlag:
                # Skip edit since thread was just posted
                skipFlag = None
                self.log.debug(
                    "Skip flag is set, game thread does not need to be edited."
                )
            else:
                # Re-generate game thread code, compare to current code, edit if different
                # Update data
                self.collect_data()
                text = self.render_template(
                    thread="game",
                    templateType="thread",
                    data=self.allData,
                    settings=self.settings,
                )
                self.log.debug(f"rendered game thread text: {text}")
                if text != self.threadCache["game"].get("text") and text != "":
                    self.threadCache["game"].update({"text": text})
                    # Add last updated timestamp
                    text += (
                        """

^^^Last ^^^Updated: ^^^"""
                        + self.convert_timezone(
                            datetime.utcnow(),
                            self.settings.get("Bot", {}).get(
                                "TEAM_TIMEZONE", "America/New_York"
                            ),
                        ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z")
                    )
                    self.threadCache["game"]["thread"].edit(text)
                    self.log.info("Edits submitted for game thread.")
                    self.count_check_edit(
                        self.threadCache["game"]["thread"].id,
                        self.allData["gameDetails"].get("phase", "UNKNOWN"),
                        edit=True,
                    )
                    self.log_last_updated_date_in_db(
                        self.threadCache["game"]["thread"].id
                    )
                elif text == "":
                    self.log.info(
                        "Skipping game thread edit since thread text is blank..."
                    )
                else:
                    self.log.info("No changes to game thread.")
                    self.count_check_edit(
                        self.threadCache["game"]["thread"].id,
                        self.allData["gameDetails"].get("phase", "UNKNOWN"),
                        edit=False,
                    )

            update_game_thread_until = self.settings.get("Game Thread", {}).get(
                "UPDATE_UNTIL", ""
            )
            if update_game_thread_until not in [
                "Do not update",
                "My team's game is final",
                "All division games are final",
                "All NFL games are final",
            ]:
                # Unsupported value, use default
                update_game_thread_until = "All NFL games are final"

            if update_game_thread_until == "Do not update":
                # Setting says not to update
                self.log.info(
                    "Stopping game thread update loop per UPDATE_UNTIL setting."
                )
                self.stopFlags.update({"game": True})
                break
            elif update_game_thread_until == "My team's game is final":
                if self.allData["gameDetails"].get("phase", "UNKNOWN") in [
                    "FINAL",
                    "FINAL_OVERTIME",
                    "CANCELED",
                    "CANCELLED",
                ]:
                    # My team's game is final
                    self.log.info(
                        "My team's game is final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"game": True})
                    break
            elif update_game_thread_until == "All division games are final":
                if (  # This game is final
                    self.allData["gameDetails"].get("phase", "UNKNOWN")
                    in ["FINAL", "FINAL_OVERTIME", "CANCELED", "CANCELLED"]
                ) and not next(  # And all division games are final
                    (
                        True
                        for x in self.allData["todayGames"]
                        if self.allData["otherTodayGamesDetails"]
                        .get(x["id"], {})
                        .get("PHASE")
                        in ["PREGAME", "INGAME", "HALFTIME"]
                        and any(
                            (
                                True
                                for divTeam in self.otherDivisionTeams
                                if divTeam["abbreviation"]
                                in [
                                    x["visitorTeam"]["abbreviation"],
                                    x["homeTeam"]["abbreviation"],
                                ]
                            )
                        )
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"game": True})
                    break
            elif update_game_thread_until == "All NFL games are final":
                if (  # This game is final
                    self.allData["gameDetails"].get("phase", "UNKNOWN")
                    in ["FINAL", "FINAL_OVERTIME", "CANCELED", "CANCELLED"]
                ) and not next(  # All NFL games are final
                    (
                        True
                        for x in self.allData["todayGames"]
                        if self.allData["otherTodayGamesDetails"]
                        .get(x["id"], {})
                        .get("PHASE")
                        in ["PREGAME", "INGAME", "HALFTIME"]
                    ),
                    False,
                ):
                    # NFL games are all final
                    self.log.info(
                        "All NFL games are final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"game": True})
                    break

            self.log.debug(
                "Game thread stop criteria not met ({}).".format(
                    update_game_thread_until
                )
            )  # debug - need this to tell if logic is working

            if self.allData["gameDetails"].get("phase", "UNKNOWN") == "HALFTIME":
                # Game is at halftime
                # Update interval is in minutes (seconds only when game is live)
                gtnlWait = self.settings.get("Game Thread", {}).get(
                    "UPDATE_INTERVAL_NOT_LIVE", 1
                )
                if gtnlWait < 1:
                    gtnlWait = 1
                self.log.info(
                    "Game is at halftime, sleeping for {} minutes...".format(
                        gtnlWait,
                    )
                )
                self.sleep(gtnlWait * 60)
            elif self.allData["gameDetails"].get("phase", "UNKNOWN") == "INGAME":
                # Update interval is in seconds (minutes for all other cases)
                gtWait = self.settings.get("Game Thread", {}).get("UPDATE_INTERVAL", 10)
                if gtWait < 1:
                    gtWait = 1
                self.log.info(
                    "Game is live, sleeping for {} seconds...".format(
                        gtWait,
                    )
                )
                self.sleep(gtWait)
            else:
                # Update interval is in minutes (seconds only when game is live)
                gtnlWait = self.settings.get("Game Thread", {}).get(
                    "UPDATE_INTERVAL_NOT_LIVE", 1
                )
                if gtnlWait < 1:
                    gtnlWait = 1
                self.log.info(
                    "Game is not live ({}), sleeping for {} minutes...".format(
                        self.allData["gameDetails"].get("phase", "UNKNOWN"),
                        gtnlWait,
                    )
                )
                self.sleep(gtnlWait * 60)

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        self.log.info("All finished with this game!")
        self.stopFlags.update({"game": True})

        # Mark game thread as stale
        if self.threadCache["game"].get("thread"):
            self.staleThreads.append(self.threadCache["game"]["thread"])

        self.log.debug("Ending game update thread...")
        return

    def postgame_thread_update_loop(self):
        skipFlag = (
            None  # Will be set later if post game thread submit/edit should be skipped
        )

        while redball.SIGNAL is None and not self.bot.STOP:
            if self.allData["gameDetails"].get("phase", "UNKNOWN") in [
                "FINAL",
                "FINAL_OVERTIME",
                "CANCELED",
                "CANCELLED",
            ]:
                # Game is over
                self.log.info(
                    "Game is over ({}). Proceeding with post game thread...".format(
                        self.allData["gameDetails"].get("phase", "UNKNOWN"),
                    )
                )
                break
            elif self.stopFlags["game"]:
                # Game thread process has stopped, but game status isn't final yet... get fresh data!
                self.log.info(
                    f"Game thread process has ended, but cached game status is still ({self.allData['gameDetails'].get('phase', 'UNKNOWN')}). Refreshing data..."
                )
                # Update data
                self.collect_data()
            else:
                self.log.debug(
                    "Game is not yet final ({}). Sleeping for 1 minute...".format(
                        self.allData["gameDetails"].get("phase", "UNKNOWN"),
                    )
                )
                self.sleep(60)

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        # Unsticky stale threads
        if self.settings.get("Reddit", {}).get("STICKY", False):
            # Make sure game thread is marked as stale, since we want the post game thread to be sticky instead
            if (
                self.threadCache["game"].get("thread")
                and self.threadCache["game"]["thread"] not in self.staleThreads
            ):
                self.staleThreads.append(self.threadCache["game"]["thread"])

            if len(self.staleThreads):
                self.unsticky_threads(self.staleThreads)
                self.staleThreads = []

        # TODO: Loop in case thread creation fails due to title template error or API error? At least break from update loop...
        # Game is over - check if postgame thread already posted (record in db with gameId and type='post' and gameDate=today)
        pgq = "select * from {}threads where type='post' and gameId = '{}' and gameDate = '{}' and deleted=0;".format(
            self.dbTablePrefix, self.allData["gameId"], self.today["Y-m-d"]
        )
        pgThread = rbdb.db_qry(pgq, closeAfter=True, logg=self.log)

        postGameThread = None
        if len(pgThread) > 0:
            self.log.info(
                "Post Game Thread found in database [{}].".format(pgThread[0]["id"])
            )
            postGameThread = self.reddit.submission(pgThread[0]["id"])
            if not postGameThread.author:
                self.log.warning("Post game thread appears to have been deleted.")
                q = "update {}threads set deleted=1 where id='{}';".format(
                    self.dbTablePrefix, postGameThread.id
                )
                u = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
                if isinstance(u, str):
                    self.log.error(
                        "Error marking thread as deleted in database: {}".format(u)
                    )

                postGameThread = None
            else:
                if postGameThread.selftext.find("\n\n^^^Last ^^^Updated") != -1:
                    postGameThreadText = postGameThread.selftext[
                        0 : postGameThread.selftext.find("\n\n^^^Last ^^^Updated:")
                    ]
                elif postGameThread.selftext.find("\n\n^^^Posted") != -1:
                    postGameThreadText = postGameThread.selftext[
                        0 : postGameThread.selftext.find("\n\n^^^Posted:")
                    ]
                else:
                    postGameThreadText = postGameThread.selftext

                self.threadCache["post"].update(
                    {
                        "thread": postGameThread,
                        "text": postGameThreadText,
                        "title": postGameThread.title
                        if postGameThread not in [None, False]
                        else None,
                    }
                )
                # Only sticky when posting the thread
                # if self.settings.get('Reddit',{}).get('STICKY',False): self.sticky_thread(self.threadCache["post"]["thread"])

        if not postGameThread:
            # Submit post game thread
            (postGameThread, postGameThreadText) = self.prep_and_post(
                "post",
                postFooter="""

^^^Posted: ^^^"""
                + self.convert_timezone(
                    datetime.utcnow(),
                    self.settings.get("Bot", {}).get(
                        "TEAM_TIMEZONE", "America/New_York"
                    ),
                ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z"),
            )
            self.threadCache["post"].update(
                {
                    "thread": postGameThread,
                    "text": postGameThreadText,
                    "title": postGameThread.title
                    if postGameThread not in [None, False]
                    else None,
                }
            )
            if not postGameThread:
                self.log.info("Post game thread not posted. Ending update loop...")
                self.stopFlags.update({"post": True})
                return  # TODO: Determine why thread is not posted and retry for temporary issue

            skipFlag = True  # No need to edit since the thread was just posted

        while (
            not self.stopFlags["post"] and redball.SIGNAL is None and not self.bot.STOP
        ):
            # Keep the thread updated until stop threshold is reached
            if skipFlag:
                skipFlag = None
                self.log.debug("Skipping edit for post game thread per skip flag...")
            else:
                try:
                    # Update data
                    self.collect_data()
                    text = self.render_template(
                        thread="post",
                        templateType="thread",
                        data=self.allData,
                        settings=self.settings,
                    )
                    self.log.debug(f"Rendered post game thread text: {text}")
                    if text != self.threadCache["post"]["text"] and text != "":
                        self.threadCache["post"]["text"] = text
                        text += (
                            """

^^^Last ^^^Updated: ^^^"""
                            + self.convert_timezone(
                                datetime.utcnow(),
                                self.settings.get("Bot", {}).get(
                                    "TEAM_TIMEZONE", "America/New_York"
                                ),
                            ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z")
                        )
                        self.threadCache["post"]["thread"].edit(text)
                        self.log.info("Post game thread edits submitted.")
                        self.log_last_updated_date_in_db(
                            self.threadCache["post"]["thread"].id
                        )
                        self.count_check_edit(
                            self.threadCache["post"]["thread"].id,
                            self.allData["gameDetails"].get("phase", "UNKNOWN"),
                            edit=True,
                        )
                    elif text == "":
                        self.log.info(
                            "Skipping post game thread edit since thread text is blank..."
                        )
                    else:
                        self.log.info("No changes to post game thread.")
                        self.count_check_edit(
                            self.threadCache["post"]["thread"].id,
                            self.allData["gameDetails"].get("phase", "UNKNOWN"),
                            edit=False,
                        )
                except Exception as e:
                    self.log.error("Error editing post game thread: {}".format(e))
                    self.error_notification("Error editing post game thread")

            update_postgame_thread_until = self.settings.get(
                "Post Game Thread", {}
            ).get("UPDATE_UNTIL", "An hour after thread is posted")
            if update_postgame_thread_until not in [
                "Do not update",
                "An hour after thread is posted",
                "All division games are final",
                "All NFL games are final",
            ]:
                # Unsupported value, use default
                self.log.warning(
                    "Unsupported value detected for Post Game Thread > UPDATE_UNTIL. Using default: An hour after thread is posted."
                )
                update_postgame_thread_until = "An hour after thread is posted"

            if update_postgame_thread_until == "Do not update":
                # Setting says not to update
                self.log.info(
                    "Stopping post game thread update loop per UPDATE_UNTIL setting."
                )
                self.stopFlags.update({"post": True})
                break
            elif update_postgame_thread_until == "An hour after thread is posted":
                self.log.debug(
                    f'Thread posted: {int(self.threadCache["post"]["thread"].created_utc)}, 1 hour ago: {round(time.time()) - 3600}, minutes to go: {60 - (round((time.time() - int(self.threadCache["post"]["thread"].created_utc)) / 60))}'
                )
                if (
                    int(self.threadCache["post"]["thread"].created_utc)
                    <= int(time.time()) - 3600
                ):
                    # Post game thread was posted more than an hour ago
                    self.log.info(
                        "Post game thread was posted an hour ago. Stopping post game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"post": True})
                    break
            elif update_postgame_thread_until == "All division games are final":
                if (  # This game is final
                    self.allData["gameDetails"].get("phase", "UNKNOWN")
                    in ["FINAL", "FINAL_OVERTIME", "CANCELED", "CANCELLED"]
                ) and not next(  # And all division games are final
                    (
                        True
                        for x in self.allData["todayGames"]
                        if self.allData["otherTodayGamesDetails"]
                        .get(x["id"], {})
                        .get("PHASE")
                        in ["PREGAME", "INGAME", "HALFTIME"]
                        and any(
                            (
                                True
                                for divTeam in self.otherDivisionTeams
                                if divTeam["abbreviation"]
                                in [
                                    x["visitorTeam"]["abbreviation"],
                                    x["homeTeam"]["abbreviation"],
                                ]
                            )
                        )
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping post game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"post": True})
                    break
            elif update_postgame_thread_until == "All NFL games are final":
                if (  # This game is final
                    self.allData["gameDetails"].get("phase", "UNKNOWN")
                    in ["FINAL", "FINAL_OVERTIME", "CANCELED", "CANCELLED"]
                ) and not next(  # All NFL games are final
                    (
                        True
                        for x in self.allData["todayGames"]
                        if self.allData["otherTodayGamesDetails"]
                        .get(x["id"], {})
                        .get("PHASE")
                        in ["PREGAME", "INGAME", "HALFTIME"]
                    ),
                    False,
                ):
                    # NFL games are all final
                    self.log.info(
                        "All NFL games are final. Stopping post game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"post": True})
                    break

            # Update interval is in minutes (seconds for game thread only)
            pgtWait = self.settings.get("Post Game Thread", {}).get(
                "UPDATE_INTERVAL", 5
            )
            if pgtWait < 1:
                pgtWait = 1
            self.log.info(
                "Post game thread update threshold ({}) not yet reached. Sleeping for {} minute(s)...".format(
                    update_postgame_thread_until, pgtWait
                )
            )
            self.sleep(pgtWait * 60)

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        # Mark post game thread as stale if sticky is enabled
        if postGameThread:
            self.staleThreads.append(postGameThread)
        self.log.debug("Ending post game update thread...")
        return  # All done with this game!

    def collect_data(self):
        """Collect data to be available for template rendering"""
        with DATA_LOCK:
            # Need to use cached data because multiple threads will be trying to update the same data at the same time
            cache_seconds = self.settings.get("NFL", {}).get("API_CACHE_SECONDS", 5)
            if cache_seconds < 0:
                cache_seconds = 5  # Use default of 5 seconds if negative value provided

            if self.allData.get(
                "lastUpdate", datetime.today() - timedelta(hours=1)
            ) >= datetime.today() - timedelta(seconds=cache_seconds):
                self.log.debug(
                    "Using cached data, updated {} seconds ago.".format(
                        (datetime.today() - self.allData["lastUpdate"]).total_seconds(),
                    )
                )
                return False
            else:
                self.log.debug(f"Collecting data with mynflapi v{mynflapi.__version__}")

            # Check NFL API Token
            self.checkNflToken(self.nfl)

            # Collect the data...
            currentWeekGames = self.nfl.gamesByWeek(
                season=self.allData["currentWeek"]["season"],
                week=self.allData["currentWeek"]["week"],
                seasonType=self.allData["currentWeek"]["seasonType"],
            )["games"]
            todayGames = [
                g
                for g in currentWeekGames
                if self.convert_timezone(
                    datetime.strptime(g["time"], "%Y-%m-%dT%H:%M:%SZ"),
                    self.settings.get("Bot", {}).get(
                        "TEAM_TIMEZONE", "America/New_York"
                    ),
                ).strftime("%Y-%m-%d")
                == self.today["Y-m-d"]
            ]
            myGameIndex = next(
                (
                    k
                    for k, v in enumerate(todayGames)
                    if v["id"] == self.allData["gameId"]
                ),
                None,
            )
            self.log.debug(f"self.allData['gameId']: {self.allData['gameId']}")
            otherTodayGamesDetails = {}
            for g in [g for g in todayGames if g["id"] != self.allData["gameId"]]:
                try:
                    g_details = self.nfl.gameDetails(g["id"])
                    g_details = (
                        g_details.get("data", {})
                        .get("viewer", {})
                        .get("gameDetail", {})
                    )
                except Exception as e:
                    if "404" in str(e):
                        self.log.debug(
                            f"Game detail is not published in NFL API yet for other today game [{g['id']}]: {e}"
                        )
                    else:
                        self.log.debug(
                            f"Unknown error retrieving game details for other today game [{g['id']}]: {e}"
                        )
                    g_details = {}
                otherTodayGamesDetails.update({g["id"]: g_details})
            try:
                gameDetails = self.nfl.gameDetails(self.allData["gameId"])
            except Exception as e:
                if "404" in str(e):
                    self.log.debug(f"Game detail is not published in NFL API yet: {e}")
                    gameDetails = {}
                else:
                    raise
            self.allData.update(
                {
                    "gameDetails": gameDetails.get("data", {})
                    .get("viewer", {})
                    .get("gameDetail", {}),
                    "otherTodayGamesDetails": otherTodayGamesDetails,
                }
            )
            gameInsights = self.nfl.gameInsights(gameId=self.allData["gameId"])["data"][
                "viewer"
            ]["gameInsight"]["insightsByGames"]
            gameTime = next(
                (
                    self.convert_timezone(  # Convert Zulu to my team TZ
                        datetime.strptime(g["time"], "%Y-%m-%dT%H:%M:%SZ"),
                        self.settings.get("Bot", {}).get(
                            "TEAM_TIMEZONE", "America/New_York"
                        ),
                    )
                    .replace(tzinfo=None)
                    .isoformat()  # Convert back to tz-naive
                    for g in todayGames
                    if g["id"] == self.allData["gameId"]
                ),
                None,
            )
            gameTime_local = next(
                (
                    self.convert_timezone(  # Convert Zulu to my team TZ
                        datetime.strptime(g["time"], "%Y-%m-%dT%H:%M:%SZ"),
                        "local",
                    )
                    for g in todayGames
                    if g["id"] == self.allData["gameId"]
                ),
                None,
            )
            self.log.debug(
                f"gameTime (my team TZ): {gameTime}; gameTime_local: {gameTime_local}"
            )
            try:
                standings = self.nfl.standings(
                    season=self.allData["currentWeek"]["season"],
                    seasonType=self.allData["currentWeek"]["seasonType"],
                    week=self.allData["currentWeek"]["week"],
                )
                if len(standings["weeks"]) and standings["weeks"][0].get("standings"):
                    standings = standings["weeks"][0]["standings"]
                else:
                    standings = []
            except Exception as e:
                self.log.error(f"Error retrieving standings: {e}")
                standings = []
            try:
                myGameSummary = self.nfl.gameSummaryById(self.allData["gameId"])
            except Exception as e:
                if "404" in str(e):
                    self.log.debug(f"Game summary is not published in NFL API yet: {e}")
                    myGameSummary = {}
                else:
                    raise
            try:
                allGameSummaries_raw = self.nfl.gameSummariesByWeek(
                    season=self.allData["currentWeek"]["season"],
                    seasonType=self.allData["currentWeek"]["seasonType"],
                    week=self.allData["currentWeek"]["week"],
                )
            except Exception as e:
                if "404" in str(e):
                    self.log.debug(
                        f"Game summaries are not published in NFL API yet: {e}"
                    )
                    allGameSummaries_raw = {}
                else:
                    raise
            otherWeekGameSummaries = {}
            for gs in allGameSummaries_raw.get("data", []):
                if gs["gameId"] != self.allData["gameId"]:
                    otherWeekGameSummaries.update({gs["gameId"]: gs})
            self.allData.update(
                {
                    "myTeam": self.nfl.teamById(
                        teamId=todayGames[myGameIndex][
                            self.allData["homeAway"] + "Team"
                        ]["id"]
                    ),
                    "myTeamRoster": self.nfl.team_roster(self.myTeam["id"])["data"][
                        "viewer"
                    ]["clubs"]["currentClubRoster"],
                    "oppTeam": self.nfl.teamById(teamId=self.allData["oppTeam"]["id"]),
                    "oppTeamRoster": self.nfl.team_roster(
                        self.allData["oppTeam"]["id"]
                    )["data"]["viewer"]["clubs"]["currentClubRoster"],
                    "gameInsights": gameInsights,
                    "currentWeekGames": currentWeekGames,
                    "todayGames": todayGames,
                    "gameTime": {
                        "bot": gameTime_local,
                        "myTeam": datetime.fromisoformat(gameTime),
                    },
                    "myGameIndex": myGameIndex,
                    "standings": standings,
                    "gameSummary": myGameSummary,
                    "otherWeekGameSummaries": otherWeekGameSummaries,
                    "lastUpdate": datetime.today(),
                }
            )

        if redball.DEV:
            self.log.debug(
                "Data available for threads: {}".format(self.allData)
            )  # debug

        return True

    def log_last_updated_date_in_db(self, threadId, t=None):
        # threadId = Reddit thread id that was edited, t = timestamp of edit
        q = "update {}threads set dateUpdated=? where id=?;".format(self.dbTablePrefix)
        if not t:
            t = time.time()
        localArgs = (t, threadId)
        i = rbdb.db_qry((q, localArgs), commit=True, closeAfter=True, logg=self.log)
        if isinstance(i, str):
            self.log.error("Error updating thread edit date in database: {}".format(i))
            return False
        else:
            return True

    def insert_thread_to_db(self, pk, threadId, type):
        # pk = gameId (or list of gameIds), threadId = thread object returned from Reddit (OFF+date for off day threads), type = ['tailgate', 'game', 'post']
        q = "insert or ignore into {}threads (gameId, type, gameDate, id, dateCreated, dateUpdated) values".format(
            self.dbTablePrefix
        )
        if isinstance(pk, list):
            for k in pk:
                if q[:-1] == ")":
                    q += ","
                q += " ('{}', '{}', '{}', '{}', {}, {})".format(
                    k, type, self.today["Y-m-d"], threadId, time.time(), time.time()
                )
        else:
            q += " ('{}', '{}', '{}', '{}', {}, {})".format(
                pk, type, self.today["Y-m-d"], threadId, time.time(), time.time()
            )

        q += ";"
        i = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
        if isinstance(i, str):
            self.log.error("Error inserting thread into database: {}".format(i))
            return False
        else:
            return True

    def count_check_edit(self, threadId, status, edit=False):
        # threadId = reddit thread id, status = game status (statusCode, code for detailed state)
        sq = "select checks,edits from {}thread_edits where threadId='{}' and status='{}';".format(
            self.dbTablePrefix, threadId, status
        )
        s = rbdb.db_qry(sq, closeAfter=True, logg=self.log)
        if isinstance(s, str):
            # Error querying for existing row
            self.log.error(
                "Error querying for existing row in {}thread_edits table for threadId {} and status {}: {}".format(
                    self.dbTablePrefix, threadId, status, s
                )
            )
            return False
        elif s != []:
            # Row already exists; increment edit count
            q = "update {}thread_edits set checks=checks+1,{} dateUpdated='{}' where threadId='{}' and status='{}';".format(
                self.dbTablePrefix,
                " edits=edits+1," if edit else "",
                time.time(),
                threadId,
                status,
            )
        else:
            # Row does not exist; insert it
            q = "insert into {}thread_edits (threadId, status, checks, edits, dateCreated, dateUpdated) values ('{}', '{}', {}, {}, '{}', '{}');".format(
                self.dbTablePrefix,
                threadId,
                status,
                1,
                1 if edit else 0,
                time.time(),
                time.time(),
            )

        r = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
        if isinstance(r, str):
            # Error inserting/updating row
            self.log.error(
                "Error inserting/updating row in {}thread_edits table for threadId {} and status {}: {}".format(
                    self.dbTablePrefix, threadId, status, r
                )
            )
            return False

        return True

    def prep_and_post(self, thread, postFooter=None):
        # thread = ['tailgate', 'game', 'post']
        # postFooter = text to append to post body, but not to include in return text value
        #   (normally contains a timestamp that would prevent comparison next time to check for changes)

        self.collect_data()

        try:
            title = self.render_template(
                thread=thread,
                templateType="title",
                data=self.allData,
                settings=self.settings,
            )
            self.log.debug("Rendered {} title: {}".format(thread, title))
        except Exception as e:
            self.log.error("Error rendering {} title: {}".format(thread, e))
            title = None
            self.error_notification(f"Error rendering title for {thread} thread")

        sticky = self.settings.get("Reddit", {}).get("STICKY", False) is True
        inboxReplies = (
            self.settings.get("Reddit", {}).get("INBOX_REPLIES", False) is True
        )
        flairMode = self.settings.get("Reddit", {}).get("FLAIR_MODE", "none")
        flair = (
            self.settings.get("Tailgate Thread", {}).get("FLAIR", "")
            if thread == "tailgate"
            else self.settings.get("Game Thread", {}).get("FLAIR", "")
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get("FLAIR", "")
            if thread == "post"
            else ""
        )
        sort = (
            self.settings.get("Tailgate Thread", {}).get("SUGGESTED_SORT", "new")
            if thread == "tailgate"
            else self.settings.get("Game Thread", {}).get("SUGGESTED_SORT", "new")
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get("SUGGESTED_SORT", "new")
            if thread == "post"
            else "new"
        )
        liveDiscussion = (
            self.settings.get("Tailgate Thread", {}).get("LIVE_DISCUSSION", False)
            if thread == "tailgate"
            else self.settings.get("Game Thread", {}).get("LIVE_DISCUSSION", False)
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get("LIVE_DISCUSSION", False)
            if thread == "post"
            else False
        )
        lockPrevious = (
            False
            if thread == "tailgate"
            else self.settings.get("Game Thread", {}).get("LOCK_TAILGATE_THREAD", False)
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get(
                "LOCK_GAME_THREAD", False
            )
            if thread == "post"
            else False
        )
        restrictSelfPosts = (
            False
            if thread != "tailgate"
            else self.settings.get("Tailgate Thread", {}).get(
                "RESTRICT_SELF_POSTS", False
            )
        )

        # Check if post already exists
        theThread = None
        text = ""
        try:
            for p in self.subreddit.new():
                if p.author == self.reddit.user.me() and p.title == title:
                    # Found existing thread...
                    self.log.info("Found an existing {} thread...".format(thread))
                    theThread = p
                    if theThread.selftext.find("\n\n^^^Last ^^^Updated") != -1:
                        text = theThread.selftext[
                            0 : theThread.selftext.find("\n\n^^^Last ^^^Updated:")
                        ]
                    elif theThread.selftext.find("\n\n^^^Posted") != -1:
                        text = theThread.selftext[
                            0 : theThread.selftext.find("\n\n^^^Posted:")
                        ]
                    else:
                        text = theThread.selftext

                    if sticky:
                        self.sticky_thread(theThread)

                    break
        except Exception as e:
            self.log.error("Error checking subreddit for existing posts: {}".format(e))
            self.error_notification("Error checking subreddit for existing posts")

        if not theThread:
            try:
                text = self.render_template(
                    thread=thread,
                    templateType="thread",
                    data=self.allData,
                    settings=self.settings,
                )
                self.log.debug("Rendered {} text: {}".format(thread, text))
            except Exception as e:
                self.log.error("Error rendering {} text: {}".format(thread, e))
                text = None
                self.error_notification(
                    f"{thread.title()} thread not posted due to failure rendering title or text."
                )

            if not (title and text):
                self.log.error(
                    "Thread not posted due to failure rendering title or text."
                )
                return (None, text)

            fullText = text + (postFooter if isinstance(postFooter, str) else "")

            # Submit thread
            try:
                theThread = self.submit_reddit_post(
                    title=title,
                    text=fullText,
                    inboxReplies=inboxReplies,
                    sticky=sticky,
                    flairMode=flairMode,
                    flair=flair,
                    sort=sort,
                    live_discussion=liveDiscussion,
                )
                self.log.info("Submitted {} thread: ({}).".format(thread, theThread))
            except Exception as e:
                self.log.error("Error submitting {} thread: {}".format(thread, e))
                theThread = None
                self.error_notification(f"Error submitting {thread} thread")

        if theThread:
            self.log.debug(
                "Inserting {} thread into DB for game {}...".format(
                    thread, self.allData["gameId"]
                )
            )
            self.insert_thread_to_db(self.allData["gameId"], theThread, thread)

            # Check for webhooks
            for w in range(0, 10):
                s = "" if w == 0 else str(w)
                webhook_url = (
                    self.settings.get("Tailgate Thread", {}).get(
                        "WEBHOOK{}_URL".format(s)
                    )
                    if thread == "tailgate"
                    else self.settings.get("Game Thread", {}).get(
                        "WEBHOOK{}_URL".format(s)
                    )
                    if thread == "game"
                    else self.settings.get("Post Game Thread", {}).get(
                        "WEBHOOK{}_URL".format(s)
                    )
                    if thread == "post"
                    else None
                )
                if webhook_url:
                    self.log.debug(
                        "Webhook{} URL for {} thread: [{}].".format(
                            s, thread, webhook_url
                        )
                    )
                    webhook_text = self.render_template(
                        thread=thread,
                        templateType="webhook" + s,
                        data=self.allData,
                        settings=self.settings,
                        theThread=theThread,
                    )
                    self.log.debug(
                        "Rendered {} webhook{} text: {}".format(thread, s, webhook_text)
                    )
                    if webhook_text:
                        webhook_result = self.post_webhook(webhook_url, webhook_text)
                        self.log.info(
                            "Webhook [{}] result: {}.".format(
                                webhook_url,
                                webhook_result
                                if isinstance(webhook_result, str)
                                else "success",
                            )
                        )
                else:
                    # Break the loop if no more webhook urls configured
                    break

            # Check for Prowl notification
            prowlKey = self.settings.get("Prowl", {}).get("THREAD_POSTED_API_KEY", "")
            prowlPriority = self.settings.get("Prowl", {}).get(
                "THREAD_POSTED_PRIORITY", ""
            )
            if prowlKey == "" or prowlPriority == "":
                self.log.debug("Prowl notifications are disabled or not configured.")
            else:
                self.notify_prowl(
                    apiKey=prowlKey,
                    event=f"{self.myTeam['nickName']} {thread.title()} Thread Posted",
                    description=f"""{self.myTeam['nickName']} {thread} thread was posted to r/{self.settings["Reddit"]["SUBREDDIT"]} at {self.convert_timezone(datetime.utcfromtimestamp(theThread.created_utc),'local').strftime('%I:%M %p %Z')}\nThread title: {theThread.title}\nURL: {theThread.shortlink}""",
                    priority=prowlPriority,
                    url=theThread.shortlink,
                    appName=f"redball - {self.bot.name}",
                )

            # Check for Twitter
            tConsumerKey = self.settings.get("Twitter", {}).get("CONSUMER_KEY", "")
            tConsumerSecret = self.settings.get("Twitter", {}).get(
                "CONSUMER_SECRET", ""
            )
            tAccessToken = self.settings.get("Twitter", {}).get("ACCESS_TOKEN", "")
            tAccessSecret = self.settings.get("Twitter", {}).get("ACCESS_SECRET", "")
            tweetThreadPosted = self.settings.get("Twitter", {}).get(
                "TWEET_THREAD_POSTED", False
            )
            if (
                "" in [tConsumerKey, tConsumerSecret, tAccessToken, tAccessSecret]
                or not tweetThreadPosted
            ):
                self.log.debug("Twitter disabled or not configured")
            else:
                if thread == "game":
                    message = f"""{theThread.title} - Join the discussion: {theThread.shortlink} #{self.myTeam['nickName'].replace(' ','')}"""
                elif thread == "tailgate":
                    message = f"""{theThread.title} - Join the discussion: {theThread.shortlink} #{self.myTeam['nickName'].replace(' ','')}"""
                elif thread == "post":
                    message = f"""{theThread.title} - The discussion continues: {theThread.shortlink} #{self.myTeam['nickName'].replace(' ','')}"""
                else:
                    self.log.error(f"Can't tweet about unknown thread type [{thread}]!")
                    return (None, text)

                tweetResult = self.tweet_thread(
                    message=message,
                    consumerKey=tConsumerKey,
                    consumerSecret=tConsumerSecret,
                    accessToken=tAccessToken,
                    accessSecret=tAccessSecret,
                )
                if tweetResult:
                    self.log.info("Tweet submitted successfully!")

            # Lock previous thread
            if lockPrevious:
                if threadToLock := (
                    self.threadCache["tailgate"].get("thread")
                    if thread == "game"
                    else self.threadCache["game"].get("thread")
                    if thread == "post"
                    else None
                ):
                    commentText = (
                        self.settings.get("Game Thread", {}).get("LOCK_MESSAGE", None)
                        if thread == "game"
                        else self.settings.get("Post Game Thread", {}).get(
                            "LOCK_MESSAGE", None
                        )
                        if thread == "post"
                        else None
                    )
                    if not commentText:
                        commentText = f"This thread has been locked. Please continue the discussion in the [{'game' if thread == 'game' else 'post game' if thread == 'post' else 'new'} thread](link)."
                    parsedCommentText = commentText.replace(
                        "(link)", f"({theThread.shortlink})"
                    )
                    try:
                        self.log.debug(
                            f"Attempting to lock {'tailgate' if thread == 'game' else 'game' if thread == 'post' else ''} thread [{threadToLock.id}]..."
                        )
                        threadToLock.mod.lock()
                        self.log.debug("Submitting comment with link to new thread...")
                        lockReply = threadToLock.reply(parsedCommentText)
                        self.log.debug("Distinguishing comment...")
                        lockReply.mod.distinguish(sticky=True)
                        self.log.debug(
                            "Successfully locked thread and posted a distinguished/sticky reply."
                        )
                    except Exception as e:
                        self.log.warning(
                            f"Failed to lock {'tailgate' if thread == 'game' else 'game' if thread == 'post' else ''} thread [{threadToLock.id}], submit reply with link to new thread, or distinguish and sticky comment: {e}"
                        )
                else:
                    self.log.debug("I did not find a previous thread to lock.")

            if restrictSelfPosts:
                # Disable self posts now that the thread is submitted
                self.log.debug(
                    f"Attempting to disable self posts after submitting {thread} thread..."
                )
                try:
                    self.subreddit.mod.update(link_type="link")
                    self.log.debug("Self posts disabled.")
                except Exception as e:
                    self.log.warning(
                        f"Failed to disable self posts after submitting {thread} thread: {e}"
                    )
        else:
            self.log.warning("No thread object present. Something went wrong!")

        return (theThread, text)

    def tweet_thread(
        self,
        message,
        consumerKey=None,
        consumerSecret=None,
        accessToken=None,
        accessSecret=None,
    ):
        if not consumerKey or not consumerSecret or not accessToken or not accessSecret:
            self.log.warning(
                "Can't submit tweet because Twitter settings are missing or incomplete. Check bot config."
            )
            return False

        self.log.debug("Initiating Twitter...")
        try:
            t = twitter.Api(consumerKey, consumerSecret, accessToken, accessSecret)
            self.log.debug(
                f"Authenticated Twitter user: {t.VerifyCredentials().screen_name}"
            )
            self.log.debug(f"Tweeting: {message}")
            t.PostUpdate(message)
            return True
        except Exception as e:
            self.log.error(f"Error submitting Tweet: {e}")
            self.error_notification(f"Error submitting Tweet: {e}")
            return False

    def notify_prowl(
        self, apiKey, event, description, priority=0, url=None, appName="redball"
    ):
        # Send a notification to Prowl
        p = pyprowl.Prowl(apiKey=apiKey, appName=appName)

        self.log.debug(
            f"Sending notification to Prowl with API Key: {apiKey}. Event: {event}, Description: {description}, Priority: {priority}, URL: {url}..."
        )
        try:
            p.notify(
                event=event,
                description=description,
                priority=priority,
                url=url,
            )
            self.log.info("Notification successfully sent to Prowl!")
            return True
        except Exception as e:
            self.log.error("Error sending notification to Prowl: {}".format(e))
            return False

    def error_notification(self, action):
        # Generate and send notification to Prowl for errors
        prowlKey = self.settings.get("Prowl", {}).get("ERROR_API_KEY", "")
        prowlPriority = self.settings.get("Prowl", {}).get("ERROR_PRIORITY", "")
        newline = "\n"
        if prowlKey != "" and prowlPriority != "":
            self.notify_prowl(
                apiKey=prowlKey,
                event=f"{self.bot.name} - {action}!",
                description=f"{action} for bot: [{self.bot.name}]!\n\n{newline.join(traceback.format_exception(*sys.exc_info()))}",
                priority=prowlPriority,
                appName=f"redball - {self.bot.name}",
            )

    def post_webhook(self, url, body):
        # url = url to which the data should be posted
        # body = dict or json-formatted string of data to post to the webhook url
        if isinstance(body, str):
            # We need the data to be a dict rather than json
            # so we can use the json param of requests.post().
            # Otherwise we have to set headers and stuff
            try:
                body = json.loads(body)
            except Exception as e:
                self.log.error(
                    "Failed to convert webhook template from json format. Ensure there are no line breaks or other special characters in the rendered template. Error: {}".format(
                        e
                    )
                )
                self.error_notification(
                    "Failed to convert webhook template from json format. Ensure there are no line breaks or other special characters in the rendered template"
                )
                return "Failed to convert webhook template from json format. Ensure there are no line breaks or other special characters in the rendered template. Error: {}".format(
                    e
                )

        try:
            r = requests.post(url, json=body)
            if r.status_code in [200, 204]:
                return True
            else:
                return "Request status code: {}".format(r.status_code)
        except requests.exceptions.RequestException as e:
            self.error_notification(f"Error posting to webhook [{url}]")
            return str(e)

        return False

    def submit_reddit_post(
        self,
        title,
        text,
        sub=None,
        inboxReplies=False,
        sticky=False,
        flairMode=None,
        flair=None,
        sort=None,
        live_discussion=False,
    ):
        if sub:
            subreddit = self.reddit.subreddit(sub)
        else:
            subreddit = self.subreddit

        post = subreddit.submit(
            title=title,
            selftext=text,
            send_replies=inboxReplies,
            discussion_type="CHAT" if live_discussion else None,
        )
        self.log.info("Thread ({}) submitted: {}".format(title, post))

        if sticky:
            self.sticky_thread(post)

        if flairMode == "submitter":
            if flair in [None, ""]:
                self.log.warning("FLAIR_MODE = submitter, but no flair provided...")
            else:
                self.log.info("Adding flair to submission as submitter...")
                choices = post.flair.choices()
                flairsuccess = False
                for p in choices:
                    if p["flair_text"] == flair:
                        post.flair.select(p["flair_template_id"])
                        flairsuccess = True
                if flairsuccess:
                    self.log.info("Submission flaired...")
                else:
                    self.log.error(
                        "Flair not set: could not find flair in available choices; check subreddit configuration."
                    )
        elif flairMode == "mod":
            if flair in [None, ""]:
                self.log.warning("FLAIR_MODE = mod, but no flair provided...")
            else:
                self.log.info("Adding flair to submission as mod...")
                try:
                    post.mod.flair(flair)
                    self.log.info("Submission flaired...")
                except Exception:
                    self.log.error(
                        "Failed to set flair on thread {post.id} (check mod privileges or change FLAIR_MODE to submitter), continuing..."
                    )
                    self.error_notification(
                        "Failed to set flair (check mod privileges or change FLAIR_MODE to submitter)"
                    )

        if sort not in [None, ""]:
            self.log.info("Setting suggested sort to {}...".format(sort))
            try:
                post.mod.suggested_sort(sort)
                self.log.info("Suggested sort set...")
            except Exception:
                self.log.error(
                    "Setting suggested sort failed (check mod privileges), continuing..."
                )
                self.error_notification(
                    f"Failed to set suggested sort on thread {post.id} (check mod privileges)"
                )

        return post

    def render_template(self, thread, templateType, **kwargs):
        setting = "{}_TEMPLATE".format(templateType.upper())
        templateFilename = (
            self.settings.get("Tailgate Thread", {}).get(setting, "")
            if thread == "tailgate"
            else self.settings.get("Game Thread", {}).get(setting, "")
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get(setting, "")
            if thread == "post"
            else ""
        )
        self.log.debug(f"templateFilename: {templateFilename}")
        try:
            template = self.LOOKUP.get_template(templateFilename)
            return template.render(**kwargs)
        except Exception:
            self.log.error(
                "Error rendering template [{}] for {} {}. Falling back to default template. Error: {}".format(
                    templateFilename,
                    thread,
                    templateType,
                    mako.exceptions.text_error_template().render(),
                )
            )
            self.error_notification(
                f"Error rendering {thread} {templateType} template [{templateFilename}]"
            )
            try:
                template = self.LOOKUP.get_template(
                    "{}_{}.mako".format(thread, templateType)
                )
                return template.render(**kwargs)
            except Exception:
                self.log.error(
                    "Error rendering default template for thread [{}] and type [{}]: {}".format(
                        thread,
                        templateType,
                        mako.exceptions.text_error_template().render(),
                    )
                )
                self.error_notification(
                    f"Error rendering default {thread} {templateType} template [{template.filename}]"
                )

        return ""

    def sticky_thread(self, thread):
        self.log.info("Stickying thread [{}]...".format(thread.id))
        try:
            thread.mod.sticky()
            self.log.info("Thread [{}] stickied...".format(thread.id))
        except Exception:
            self.log.warning(
                "Sticky of thread [{}] failed. Check mod privileges or the thread may have already been sticky.".format(
                    thread.id
                )
            )

    def unsticky_threads(self, threads):
        for t in threads:
            try:
                self.log.debug("Attempting to unsticky thread [{}]".format(t.id))
                t.mod.sticky(state=False)
            except Exception:
                self.log.debug(
                    "Unsticky of thread [{}] failed. Check mod privileges or the thread may not have been sticky.".format(
                        t.id
                    )
                )

    def build_tables(self):
        queries = []
        queries.append(
            """CREATE TABLE IF NOT EXISTS {}games (
                id integer primary key autoincrement,
                gameId text unique not null,
                gameDate text not null,
                dateAdded text not null
            );""".format(
                self.dbTablePrefix
            )
        )

        queries.append(
            """CREATE TABLE IF NOT EXISTS {}threads (
                gameId integer not null,
                type text not null,
                gameDate text not null,
                id text not null,
                dateCreated text not null,
                dateUpdated text not null,
                deleted integer default 0,
                unique (gameId, type, id, gameDate, deleted)
            );""".format(
                self.dbTablePrefix
            )
        )

        queries.append(
            """CREATE TABLE IF NOT EXISTS {}thread_edits (
                threadId text not null,
                status text not null,
                checks integer default 0,
                edits integer default 0,
                dateCreated text not null,
                dateUpdated text not null,
                unique (threadId, status)
            );""".format(
                self.dbTablePrefix
            )
        )

        self.log.debug(
            "Executing queries to build {} tables: {}".format(len(queries), queries)
        )
        results = rbdb.db_qry(queries, commit=True, closeAfter=True, logg=self.log)
        if None in results:
            self.log.debug("One or more queries failed: {}".format(results))
        else:
            self.log.debug("Building of tables complete. Results: {}".format(results))

        return True

    def refresh_settings(self):
        self.prevSettings = self.settings
        self.settings = self.bot.get_config()
        if self.prevSettings["Logging"] != self.settings["Logging"]:
            # reload logger
            self.log = logger.init_logger(
                logger_name="redball.bots." + threading.current_thread().name,
                log_to_console=self.settings.get("Logging", {}).get(
                    "LOG_TO_CONSOLE", True
                ),
                log_to_file=self.settings.get("Logging", {}).get("LOG_TO_FILE", True),
                log_path=redball.LOG_PATH,
                log_file="{}.log".format(threading.current_thread().name),
                file_log_level=self.settings.get("Logging", {}).get("FILE_LOG_LEVEL"),
                console_log_level=self.settings.get("Logging", {}).get(
                    "CONSOLE_LOG_LEVEL"
                ),
                clear_first=True,
                propagate=False,
            )
            self.log.info("Restarted logger with new settings")

        if (
            self.prevSettings["Reddit Auth"] != self.settings["Reddit Auth"]
            or self.prevSettings["Reddit"] != self.settings["Reddit"]
        ):
            self.log.info(
                "Detected new Reddit Authorization info. Re-initializing Reddit API..."
            )
            self.init_reddit()

        # Check here if settings have changed for other services added in the future (twitter, etc.)

        self.log.debug("Refreshed settings: {}".format(self.settings))

    def init_reddit(self):
        self.log.debug(f"Initializing Reddit API with praw v{praw.__version__}...")
        with redball.REDDIT_AUTH_LOCKS[str(self.bot.redditAuth)]:
            try:
                self.reddit = praw.Reddit(
                    client_id=self.settings["Reddit Auth"]["reddit_clientId"],
                    client_secret=self.settings["Reddit Auth"]["reddit_clientSecret"],
                    token_manager=self.bot.reddit_auth_token_manager,
                    user_agent="redball Football Game Thread Bot - https://github.com/toddrob99/redball/ - r/{}".format(
                        self.settings["Reddit"].get("SUBREDDIT", "")
                    ),
                )
            except Exception as e:
                self.log.error(
                    "Error encountered attempting to initialize Reddit: {}".format(e)
                )
                self.error_notification("Error initializing Reddit")
                raise

            scopes = [
                "identity",
                "submit",
                "edit",
                "read",
                "modposts",
                "privatemessages",
                "flair",
                "modflair",
            ]
            try:
                praw_scopes = self.reddit.auth.scopes()
            except Exception as e:
                self.log.error(
                    "Error encountered attempting to look up authorized Reddit scopes: {}".format(
                        e
                    )
                )
                self.error_notification(
                    "Error encountered attempting to look up authorized Reddit scopes"
                )
                raise

        missing_scopes = []
        self.log.debug("Reddit authorized scopes: {}".format(praw_scopes))
        try:
            if self.reddit.user.me() is None:
                raise ValueError(
                    "Failed to initialize Reddit instance--authorized user is None"
                )
            self.log.info("Reddit authorized user: {}".format(self.reddit.user.me()))
        except Exception as e:
            self.log.warning(
                "Error encountered attempting to identify authorized Reddit user (identity scope may not be authorized): {}".format(
                    e
                )
            )
            self.error_notification(
                "Error encountered attempting to identify authorized Reddit user (identity scope may not be authorized)"
            )

        for scope in scopes:
            if scope not in praw_scopes:
                missing_scopes.append(scope)

        if len(missing_scopes):
            self.log.warning(
                "Scope(s) not authorized: {}. Please check/update/re-authorize Reddit Authorization in redball System Config.".format(
                    missing_scopes
                )
            )

        self.subreddit = self.reddit.subreddit(
            self.settings.get("Reddit", {}).get("SUBREDDIT")
        )

    def eod_loop(self, today):
        # today = date that's already been finished ('%Y-%m-%d')
        # return when datetime.today().strftime('%Y-%m-%d') is not equal to today param (it's the next day)
        while redball.SIGNAL is None and not self.bot.STOP:
            # End of day loop
            if redball.SIGNAL is not None or self.bot.STOP:
                break
            elif today != datetime.today().strftime("%Y-%m-%d"):
                self.log.info("It's a brand new day!")
                break
            else:
                i = 0
                while True:
                    if redball.SIGNAL is None and not self.bot.STOP:
                        i += 1
                        if today != datetime.today().strftime("%Y-%m-%d"):
                            break
                        elif i == 600:
                            self.log.info("Still waiting for the next day...")
                            break
                        time.sleep(1)
                    else:
                        break

    def sleep(self, t):
        # t = total number of seconds to sleep before returning
        i = 0
        while redball.SIGNAL is None and not self.bot.STOP and i < t:
            i += 1
            time.sleep(1)

    def convert_timezone(self, dt, convert_to="America/New_York"):
        # dt = datetime object to convert, convert_to = timezone to convert to (e.g. 'America/New_York', or 'local' for local bot timezone)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=pytz.utc)

        if convert_to == "local":
            to_tz = tzlocal.get_localzone()
        else:
            to_tz = pytz.timezone(convert_to)

        return dt.astimezone(to_tz)

    teamSubs = {
        "ARI": "r/AZCardinals",
        "ATL": "r/falcons",
        "BAL": "r/ravens",
        "BUF": "r/buffalobills",
        "CAR": "r/panthers",
        "CHI": "r/CHIBears",
        "CIN": "r/bengals",
        "CLE": "r/Browns",
        "DAL": "r/cowboys",
        "DEN": "r/DenverBroncos",
        "DET": "r/detroitlions",
        "GB": "r/GreenBayPackers",
        "HOU": "r/Texans",
        "IND": "r/Colts",
        "JAX": "r/Jaguars",
        "KC": "r/KansasCityChiefs",
        "LA": "r/LosAngelesRams",
        "LAC": "r/Chargers",
        "LV": "r/raiders",
        "MIA": "r/miamidolphins",
        "MIN": "r/minnesotavikings",
        "NE": "r/Patriots",
        "NO": "r/Saints",
        "NYG": "r/NYGiants",
        "NYJ": "r/nyjets",
        "PHI": "r/eagles",
        "PIT": "r/steelers",
        "SEA": "r/Seahawks",
        "SF": "r/49ers",
        "TB": "r/buccaneers",
        "TEN": "r/Tennesseetitans",
        "WAS": "r/Commanders",
        0: "r/NFL",
        "nfl": "r/NFL",
    }

    def bot_state(self):
        """Return current state...
        Current date being monitored
        Game being monitored with current status
        Threads pending and post time
        Threads posted
        """
        try:
            botStatus = {
                "lastUpdated": datetime.today().strftime("%m/%d/%Y %I:%M:%S %p"),
                "myTeam": {
                    "id": self.myTeam["id"],
                    "fullName": self.myTeam["fullName"],
                    "abbreviation": self.myTeam["abbreviation"],
                    "nickName": self.myTeam["nickName"],
                    "location": self.myTeam["location"],
                },
                "today": self.today,
                "currentWeek": self.allData["currentWeek"],
                "tailgateThread": {
                    "enabled": self.settings.get("Tailgate Thread", {}).get(
                        "ENABLED", True
                    ),
                    "postTime": self.threadCache.get("tailgate", {})
                    .get("postTime_local")
                    .strftime("%m/%d/%Y %I:%M:%S %p")
                    if isinstance(
                        self.threadCache.get("tailgate", {}).get("postTime_local"),
                        datetime,
                    )
                    else "",
                    "posted": True
                    if self.threadCache.get("tailgate", {}).get("thread")
                    else False,
                    "id": self.threadCache.get("tailgate", {}).get("thread").id
                    if self.threadCache.get("tailgate", {}).get("thread")
                    else None,
                    "url": self.threadCache.get("tailgate", {}).get("thread").shortlink
                    if self.threadCache.get("tailgate", {}).get("thread")
                    else None,
                    "title": self.threadCache.get("tailgate", {}).get("title")
                    if self.threadCache.get("tailgate", {}).get("thread")
                    else None,
                },
                "game": {
                    "gameId": self.allData.get("gameId"),
                    "status": self.allData.get("gameDetails", {}).get("phase"),
                    "oppTeam": deepcopy(self.allData.get("oppTeam")),
                    "homeAway": self.allData.get("homeAway"),
                    "gameTime": self.allData["gameTime"]["myTeam"].strftime(
                        "%I:%M %p %Z"
                    )
                    if self.allData.get("gameTime", {}).get("myTeam")
                    else "Unknown game time",
                    "threads": {
                        "game": {
                            "enabled": self.settings.get("Game Thread", {}).get(
                                "ENABLED", True
                            ),
                            "postTime": self.threadCache["game"]
                            .get("postTime_local")
                            .strftime("%m/%d/%Y %I:%M:%S %p")
                            if isinstance(
                                self.threadCache["game"].get("postTime_local"), datetime
                            )
                            else "",
                            "posted": True
                            if self.threadCache["game"].get("thread")
                            else False,
                            "id": self.threadCache["game"].get("thread").id
                            if self.threadCache["game"].get("thread")
                            else None,
                            "url": self.threadCache["game"].get("thread").shortlink
                            if self.threadCache["game"].get("thread")
                            else None,
                            "title": self.threadCache["game"].get("title")
                            if self.threadCache["game"].get("thread")
                            else None,
                        },
                        "post": {
                            "enabled": self.settings.get("Post Game Thread", {}).get(
                                "ENABLED", True
                            ),
                            "posted": True
                            if self.threadCache["post"].get("thread")
                            else False,
                            "id": self.threadCache["post"].get("thread").id
                            if self.threadCache["post"].get("thread")
                            else None,
                            "url": self.threadCache["post"].get("thread").shortlink
                            if self.threadCache["post"].get("thread")
                            else None,
                            "title": self.threadCache["post"].get("title")
                            if self.threadCache["post"].get("thread")
                            else None,
                        },
                    },
                },
            }

            botStatus.update(
                {
                    "summary": {
                        "text": "Today is {}.\nCurrent Week: {} {} {}.".format(
                            botStatus["today"]["Y-m-d"],
                            botStatus["currentWeek"]["season"],
                            botStatus["currentWeek"]["seasonType"],
                            botStatus["currentWeek"]["week"],
                        ),
                        "html": "Today is {}.<br />Current Week: {} {} {}.".format(
                            botStatus["today"]["Y-m-d"],
                            botStatus["currentWeek"]["season"],
                            botStatus["currentWeek"]["seasonType"],
                            botStatus["currentWeek"]["week"],
                        ),
                        "markdown": "Today is {}.\n\nCurrent Week: {} {} {}.".format(
                            botStatus["today"]["Y-m-d"],
                            botStatus["currentWeek"]["season"],
                            botStatus["currentWeek"]["seasonType"],
                            botStatus["currentWeek"]["week"],
                        ),
                    }
                }
            )

            if botStatus["game"]["gameId"]:
                botStatus["summary"]["text"] += "\n\n"
                botStatus["summary"]["html"] += "<br /><br />"
                botStatus["summary"]["markdown"] += "\n\n"

                botStatus["summary"][
                    "text"
                ] += f"Today's game: {botStatus['game']['gameTime']} {'@' if botStatus['game']['homeAway']=='away' else 'vs.'} {botStatus['game']['oppTeam']['fullName']}"
                botStatus["summary"][
                    "html"
                ] += f"Today's game: {botStatus['game']['gameTime']} {'@' if botStatus['game']['homeAway']=='away' else 'vs.'} {botStatus['game']['oppTeam']['fullName']}"
                botStatus["summary"][
                    "markdown"
                ] += f"Today's game: {botStatus['game']['gameTime']} {'@' if botStatus['game']['homeAway']=='away' else 'vs.'} {botStatus['game']['oppTeam']['fullName']}"

                if not botStatus["tailgateThread"]["enabled"]:
                    # Tailgate thread is disabled
                    botStatus["summary"]["text"] += "\n\nTailgate thread disabled."
                    botStatus["summary"][
                        "html"
                    ] += "<br /><br /><strong>Tailgate thread</strong> disabled."
                    botStatus["summary"][
                        "markdown"
                    ] += "\n\n**Tailgate thread** disabled."
                else:
                    if not botStatus["tailgateThread"]["posted"]:
                        # Thread is not posted (could be error)
                        botStatus["summary"][
                            "text"
                        ] += f"\n\nTailgate thread post time: {botStatus['tailgateThread']['postTime']}"
                        botStatus["summary"][
                            "html"
                        ] += f"<br /><br /><strong>Tailgate thread</strong> post time: {botStatus['tailgateThread']['postTime']}"
                        botStatus["summary"][
                            "markdown"
                        ] += f"\n\n**Tailgate thread** post time: {botStatus['tailgateThread']['postTime']}"
                    else:
                        # Thread is posted
                        botStatus["summary"][
                            "text"
                        ] += f"\n\nTailgate thread: {botStatus['tailgateThread']['title']} ({botStatus['tailgateThread']['id']} - {botStatus['tailgateThread']['url']})"
                        botStatus["summary"][
                            "html"
                        ] += f"<br /><br /><strong>Tailgate thread</strong>: {botStatus['tailgateThread']['title']} (<a href=\"{botStatus['tailgateThread']['url']}\" target=\"_blank\">{botStatus['tailgateThread']['id']}</a>)"
                        botStatus["summary"][
                            "markdown"
                        ] += f"\n\n**Tailgate thread**: {botStatus['tailgateThread']['title']} ([{botStatus['tailgateThread']['id']}]({botStatus['tailgateThread']['url']}))"

                if not botStatus["game"]["threads"]["game"]["enabled"]:
                    # Game thread is disabled
                    botStatus["summary"]["text"] += "\n\nGame thread disabled."
                    botStatus["summary"][
                        "html"
                    ] += "<br /><br /><strong>Game thread</strong> disabled."
                    botStatus["summary"]["markdown"] += "\n\n**Game thread** disabled."
                else:
                    if not botStatus["game"]["threads"]["game"]["posted"]:
                        # Thread is not posted (could be error)
                        botStatus["summary"][
                            "text"
                        ] += f"\n\nGame thread post time: {botStatus['game']['threads']['game']['postTime']}"
                        botStatus["summary"][
                            "html"
                        ] += f"<br /><br /><strong>Game thread</strong> post time: {botStatus['game']['threads']['game']['postTime']}"
                        botStatus["summary"][
                            "markdown"
                        ] += f"\n\n**TailgGameate thread** post time: {botStatus['game']['threads']['game']['postTime']}"
                    else:
                        # Thread is posted
                        botStatus["summary"][
                            "text"
                        ] += f"\n\nGame thread: {botStatus['game']['threads']['game']['title']} ({botStatus['game']['threads']['game']['id']} - {botStatus['game']['threads']['game']['url']})"
                        botStatus["summary"][
                            "html"
                        ] += f"<br /><br /><strong>Game thread</strong>: {botStatus['game']['threads']['game']['title']} (<a href=\"{botStatus['game']['threads']['game']['url']}\" target=\"_blank\">{botStatus['game']['threads']['game']['id']}</a>)"
                        botStatus["summary"][
                            "markdown"
                        ] += f"\n\n**Game thread**: {botStatus['game']['threads']['game']['title']} ([{botStatus['game']['threads']['game']['id']}]({botStatus['game']['threads']['game']['url']}))"

                if not botStatus["game"]["threads"]["post"]["enabled"]:
                    # Post game thread is disabled
                    botStatus["summary"]["text"] += "\n\nPost Game thread disabled."
                    botStatus["summary"][
                        "html"
                    ] += "<br /><br /><strong>Post Game thread</strong> disabled."
                    botStatus["summary"][
                        "markdown"
                    ] += "\n\n**Post Game thread** disabled."
                elif botStatus["game"]["threads"]["post"]["posted"]:
                    # Thread is posted
                    botStatus["summary"][
                        "text"
                    ] += f"\n\nPost Game thread: {botStatus['game']['threads']['post']['title']} ({botStatus['game']['threads']['post']['id']} - {botStatus['game']['threads']['post']['url']})"
                    botStatus["summary"][
                        "html"
                    ] += f"<br /><br /><strong>Post Game thread</strong>: {botStatus['game']['threads']['post']['title']} (<a href=\"{botStatus['game']['threads']['post']['url']}\" target=\"_blank\">{botStatus['game']['threads']['post']['id']}</a>)"
                    botStatus["summary"][
                        "markdown"
                    ] += f"\n\n**Post Game thread**: {botStatus['game']['threads']['post']['title']} ([{botStatus['game']['threads']['post']['id']}]({botStatus['game']['threads']['post']['url']}))"
            else:
                # No game today
                botStatus["summary"]["text"] += "\n\nNo game today."
                botStatus["summary"]["html"] += "<br /><br />No game today."
                botStatus["summary"]["markdown"] += "\n\nNo game today."

            botStatus["summary"]["text"] += "\n\nLast Updated: {}".format(
                botStatus["lastUpdated"]
            )
            botStatus["summary"][
                "html"
            ] += "<br /><br /><strong>Last Updated</strong>: {}".format(
                botStatus["lastUpdated"]
            )
            botStatus["summary"]["markdown"] += "\n\n**Last Updated**: {}".format(
                botStatus["lastUpdated"]
            )
        except Exception as e:
            botStatus = {
                "lastUpdated": datetime.today().strftime("%m/%d/%Y %I:%M:%S %p"),
                "summary": {
                    "text": "Error retrieving bot state: {}".format(e),
                    "html": "Error retrieving bot state: {}".format(e),
                    "markdown": "Error retrieving bot state: {}".format(e),
                },
            }
            self.error_notification("Error retrieving bot state")

        self.log.debug("Bot Status: {}".format(botStatus))  # debug
        self.bot.detailedState = botStatus

    def isGameCanceled(self, gameInsights):
        if insight := next(
            (x for x in gameInsights if "canceled" in x["headline"]), None
        ):
            self.log.info(
                f"Detected that the game is canceled based on the following headline: {insight['headline']}"
            )
            return True
        else:
            return False

    def getNflToken(self, nflSession=None):
        self.log.debug("Retrieving fresh NFL API token...")
        url = "https://api.nfl.com/v1/reroute"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-domain-id": "100",
        }
        body = {
            "grant_type": "client_credentials",
        }

        try:
            r = requests.post(url, data=body, headers=headers)
            content = json.loads(r.content)
        except Exception as e:
            self.log.error(f"Caught exception requesting NFL API token: {e}")
            raise

        if nflSession:
            # Update existing NFL API session
            nflSession.token = content

        return content

    def checkNflToken(self, nfl):
        try:
            nfl.currentWeek()
        except requests.exceptions.HTTPError as e:
            if "401" in str(e):
                self.log.warning(
                    f"Invalid NFL API token detected. Requesting a new one. Error message: {e}"
                )
                self.getNflToken(nfl)
            else:
                raise
