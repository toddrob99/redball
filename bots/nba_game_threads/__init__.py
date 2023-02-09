#!/usr/bin/env python
# encoding=utf-8
"""NBA Game Thread Bot
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

from . import pynbaapi
import pyprowl
import twitter

import praw

__version__ = "1.1.1"

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
            "NBA Game Thread Bot v{} received settings: {}. Template path: {}".format(
                __version__, self.settings, self.BOT_TEMPLATE_PATH
            )
        )

        # Check db for tables and create if necessary
        self.dbTablePrefix = self.settings.get("Database").get(
            "dbTablePrefix", "nba_gdt{}_".format(self.bot.id)
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

        self.team_timezone = self.settings.get("Bot", {}).get(
            "TEAM_TIMEZONE", "America/New_York"
        )

        settings_date = datetime.today().strftime("%Y-%m-%d")
        if self.settings.get("NBA", {}).get("GAME_DATE_OVERRIDE", "") != "":
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

            # (Re-)Initialize NBA API
            self.log.debug(
                f"Initializing NBA API with pynbaapi v{pynbaapi.__version__.__version__}"
            )
            self.nba = pynbaapi.nba.NBA(
                f"NBAGameThreads/{__version__} (platform; redball/{redball.__version__})"
            )

            # Get info about configured team
            if self.settings.get("NBA", {}).get("TEAM", "") == "":
                self.log.critical("No team selected! Set NBA > TEAM in Bot Config.")
                self.bot.STOP = True
                break

            self.myTeamId = int(
                self.settings.get("NBA", {}).get("TEAM", "").split("|")[1]
            )
            self.log.debug(f"{self.myTeamId=}")
            self.myTeam = self.nba.team(self.myTeamId)
            if not self.myTeam:
                self.log.critical(
                    "Unable to look up team info! Check NBA > TEAM in Bot Config."
                )
                self.bot.STOP = True
                break
            self.log.info(f"Configured team: {str(self.myTeam)}")

            if todayOverrideFlag:
                self.log.info(
                    "Overriding game date per GAME_DATE_OVERRIDE setting [{}].".format(
                        self.settings["NBA"]["GAME_DATE_OVERRIDE"]
                    )
                )
                try:
                    todayObj = datetime.strptime(
                        self.settings["NBA"]["GAME_DATE_OVERRIDE"], "%Y-%m-%d"
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
                "obj": todayObj,
            }
            self.today.update(
                {
                    "season": todayObj.strftime("%Y")
                    if int(todayObj.strftime("%m")) >= 9
                    else str(int(todayObj.strftime("%Y")) - 1)
                }
            )
            self.log.debug(
                f"Today is {self.today['Y-m-d']}. Season: {self.today['season']}."
            )

            if todayOverrideFlag:
                todayOverrideFlag = (
                    False  # Only override once, then go back to current date
                )

            # Standings
            standings = self.nba.standings(self.today["season"])

            # Other division teams
            self.otherDivisionTeamIds = [
                t.teamid
                for t in standings.standings
                if t.division == self.myTeam.team_info.team_division
                and t.teamid != self.myTeam.team_info.team_id
            ]
            self.log.debug(f"{self.otherDivisionTeamIds=}")

            # Other conference teams
            self.otherConferenceTeamIds = [
                t.teamid
                for t in standings.standings
                if t.conference == self.myTeam.team_info.team_conference
                and t.teamid != self.myTeam.team_info.team_id
            ]
            self.log.debug(f"{self.otherConferenceTeamIds=}")

            # Get today's games
            todayScoreboard = self.nba.scoreboard(self.today["Y-m-d"])
            todayMyGames = [
                x
                for x in todayScoreboard.scoreboard.games
                if self.myTeamId in [x.away_team.team_id, x.home_team.team_id]
            ]
            todayOtherDivisionGames = [
                x
                for x in todayScoreboard.scoreboard.games
                if x.game_id != [g.game_id for g in todayMyGames]
                and (
                    x.away_team.team_id in self.otherDivisionTeamIds
                    or x.home_team.team_id in self.otherDivisionTeamIds
                )
            ]
            todayOtherConferenceGames = [
                x
                for x in todayScoreboard.scoreboard.games
                if x.game_id not in [g.game_id for g in todayMyGames]
                and (
                    x.away_team.team_id in self.otherConferenceTeamIds
                    or x.home_team.team_id in self.otherConferenceTeamIds
                )
            ]
            todayAllOtherGames = [
                x
                for x in todayScoreboard.scoreboard.games
                if self.myTeamId not in [x.away_team.team_id, x.home_team.team_id]
            ]
            self.log.debug(f"Today's game(s): {str(todayMyGames)}")
            if len(todayMyGames) > 1:
                self.log.warning(
                    f"Multiple games found, but only one game supported per day: {[g.game_id for g in todayMyGames]}"
                )
            self.log.debug(
                f"{len(todayOtherDivisionGames)=}, {len(todayAllOtherGames)=}"
            )

            # (Re-)Initialize dict to hold game data
            self.allData = {
                "today": self.today,
                "myTeam": self.myTeam,
                "otherDivisionTeamIds": self.otherDivisionTeamIds,
                "otherConferenceTeamIds": self.otherConferenceTeamIds,
                "todayMyGames": todayMyGames,
                "todayAllOtherGames": todayAllOtherGames,
                "todayOtherDivisionGames": todayOtherDivisionGames,
                "todayOtherConferenceGames": todayOtherConferenceGames,
                "teamSubs": self.teamSubs,
                "teamSubsById": self.teamSubsById,
            }
            # Initialize vars to hold data about reddit and process threads
            self.stopFlags = {}
            """ Holds flags to indicate when reddit threads should stop updating """
            self.THREADS = {"off": None, "tailgate": None, "game": None, "post": None}
            """ Holds process threads that will post/monitor/update each reddit thread """
            self.threadCache = {"off": {}, "tailgate": {}, "game": {}, "post": {}}
            """ Holds reddit threads and related data """

            if not len(todayMyGames):
                # It's not a game day
                self.log.info("No games today!")
                self.stopFlags.update({"off": False})
                self.allData.update(
                    {
                        "game_id": "off",
                        "next_game": self.nba.next_game(
                            self.myTeamId, self.today["season"], self.today["obj"]
                        ),
                    }
                )
                self.off_day()
                if redball.SIGNAL is not None or self.bot.STOP:
                    break
            else:
                self.stopFlags.update(
                    {
                        "tailgate": False,
                        "game": False,
                        "post": False,
                    }
                )
                game_id = todayMyGames[0].game_id
                self.log.info("IT'S GAME DAY!")
                self.log.debug(f"Gathering initial data for game_id [{game_id}]...")
                box_summary = self.nba.boxscore_summary(game_id)
                box_traditional = self.nba.boxscore_traditional(game_id)
                try:
                    box_live = self.nba.api.from_url(
                        f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{self.allData['game_id']}.json"
                    )
                except Exception as e:
                    self.log.debug(f"Exception retrieving live box from cdn: {e}")
                    box_live = None
                boxscore = {
                    "summary": box_summary,
                    "traditional": box_traditional,
                    "live": box_live,
                }
                homeAway = (
                    "home"
                    if boxscore["summary"].box_score_summary.home_team_id
                    == self.myTeamId
                    else "away"
                    if boxscore["summary"].box_score_summary.away_team_id
                    == self.myTeamId
                    else None
                )
                oppHomeAway = "home" if homeAway == "away" else "away"
                self.log.debug(f"My team is [{homeAway}] (homeAway)")
                oppTeam = self.nba.team(
                    boxscore["summary"].box_score_summary.home_team_id
                    if homeAway == "away"
                    else boxscore["summary"].box_score_summary.away_team_id
                )
                oppTeamId = oppTeam.team_info.team_id
                self.log.debug(f"oppTeamId: {oppTeamId}")
                self.log.debug(f"oppTeam: {str(oppTeam)}")
                gameTime = self.convert_timezone(  # Convert Zulu to my team TZ
                    datetime.strptime(
                        boxscore["summary"].box_score_summary.game_time_utc,
                        "%Y-%m-%dT%H:%M:%SZ",
                    ),
                    self.team_timezone,
                )
                gameTime_local = self.convert_timezone(  # Convert Zulu to my team TZ
                    datetime.strptime(
                        boxscore["summary"].box_score_summary.game_time_utc,
                        "%Y-%m-%dT%H:%M:%SZ",
                    ),
                    "local",
                )
                self.log.debug(
                    f"gameTime (my team TZ): {gameTime}; gameTime_local: {gameTime_local}"
                )
                standings = self.nba.standings(self.today["season"])

                # Initialize var to hold game data throughout the day
                self.allData.update(
                    {
                        "game_id": game_id,
                        "homeAway": homeAway,
                        "oppTeam": oppTeam,
                        "oppTeamId": oppTeamId,
                        "oppHomeAway": oppHomeAway,
                        "gameTime": {
                            "bot": gameTime_local,
                            "myTeam": gameTime,
                        },
                        "game": boxscore,
                        "standings": standings,
                    }
                )
                """ Holds data about current day games, including detailed data for my team's game """
                self.allData.update(
                    {
                        "gameStatus": self.game_status(),
                        "gameStatusText": self.game_status_text(),
                    }
                )
                if redball.DEV:
                    self.log.debug(f"allData: {self.allData}")

                # Check DB for gameId
                gq = f"select * from {self.dbTablePrefix}games where gameId = '{game_id}' and gameDate = '{self.today['Y-m-d']}';"
                dbGames = rbdb.db_qry(gq, closeAfter=True, logg=self.log)

                if dbGames and len(dbGames) > 0:
                    self.log.debug(f"Game [{game_id}] is already in the database.")
                else:
                    # Add game to DB
                    q = (
                        f"insert into {self.dbTablePrefix}games (gameId, gameDate, dateAdded) "
                        f"values ('{game_id}', '{self.today['Y-m-d']}', {time.time()});"
                    )
                    rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)

                # Tailgate Thread
                if not self.settings.get("Tailgate Thread", {}).get("ENABLED", True):
                    self.log.info("Tailgate thread disabled.")
                    self.stopFlags.update({"tailgate": True})
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

                for g in todayMyGames:
                    # Game thread update processes
                    if self.settings.get("Game Thread", {}).get("ENABLED", True):
                        # Spawn separate thread to wait for post time and then keep game thread updated
                        self.THREADS.update(
                            {
                                "game": threading.Thread(
                                    target=self.game_thread_update_loop,
                                    args=(g.game_id,),
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
                    for g in todayMyGames:
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
                                            args=(g.game_id,),
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
                                    "Started game thread {}.".format(
                                        self.THREADS["game"]
                                    )
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

    def off_day(self):
        skipFlag = None  # Will be set later if off thread edit should be skipped

        # Check/wait for time to submit off thread
        self.threadCache["off"].update(
            {
                "postTime_local": datetime.strptime(
                    datetime.today().strftime(
                        "%Y-%m-%d "
                        + self.settings.get("Off Day Thread", {}).get(
                            "POST_TIME", "05:00"
                        )
                    ),
                    "%Y-%m-%d %H:%M",
                )
            }
        )
        self.log.debug(
            "Off Day thread post time: {}".format(
                self.threadCache["off"]["postTime_local"]
            )
        )
        while (
            datetime.today() < self.threadCache["off"]["postTime_local"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            if (
                self.threadCache["off"]["postTime_local"] - datetime.today()
            ).total_seconds() > 3600:
                self.log.info(
                    "Off Day thread should not be posted for a long time ({}). Sleeping for an hour...".format(
                        self.threadCache["off"]["postTime_local"]
                    )
                )
                self.sleep(3600)
            elif (
                self.threadCache["off"]["postTime_local"] - datetime.today()
            ).total_seconds() > 1800:
                self.log.info(
                    "Off Day thread post time is still more than 30 minutes away ({}). Sleeping for a half hour...".format(
                        self.threadCache["off"]["postTime_local"]
                    )
                )
                self.sleep(1800)
            else:
                self.log.info(
                    "Off Day thread post time is approaching ({}). Sleeping until then...".format(
                        self.threadCache["off"]["postTime_local"]
                    )
                )
                self.sleep(
                    (
                        self.threadCache["off"]["postTime_local"] - datetime.today()
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

        # Check if off thread already posted (record in threads table with type='off' for today's game_id)
        tgq = f"select * from {self.dbTablePrefix}threads where type='off' and gameId = 'off' and gameDate = '{self.today['Y-m-d']}' and deleted=0;"
        tgThread = rbdb.db_qry(tgq, closeAfter=True, logg=self.log)

        offThread = None
        if len(tgThread) > 0:
            self.log.info(f"Off Day thread found in database [{tgThread[0]['id']}].")
            offThread = self.reddit.submission(tgThread[0]["id"])
            if not offThread.author:
                self.log.warning("Off Day thread appears to have been deleted.")
                q = "update {}threads set deleted=1 where id='{}';".format(
                    self.dbTablePrefix, offThread.id
                )
                u = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
                if isinstance(u, str):
                    self.log.error(
                        "Error marking thread as deleted in database: {}".format(u)
                    )

                offThread = None
            else:
                if offThread.selftext.find("\n\n^^^Last ^^^Updated") != -1:
                    offThreadText = offThread.selftext[
                        0 : offThread.selftext.find("\n\n^^^Last ^^^Updated:")
                    ]
                elif offThread.selftext.find("\n\n^^^Posted") != -1:
                    offThreadText = offThread.selftext[
                        0 : offThread.selftext.find("\n\n^^^Posted:")
                    ]
                else:
                    offThreadText = offThread.selftext

                self.threadCache["off"].update(
                    {
                        "text": offThreadText,
                        "thread": offThread,
                        "title": offThread.title
                        if offThread not in [None, False]
                        else None,
                    }
                )
                # Only sticky when posting the thread
                # if self.settings.get('Reddit',{}).get('STICKY',False): self.sticky_thread(offThread)

        if not offThread:
            # Submit off thread
            (offThread, offThreadText) = self.prep_and_post(
                "off",
                postFooter="""

^^^Posted: ^^^"""
                + self.convert_timezone(
                    datetime.utcnow(),
                    self.team_timezone,
                ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z")
                + ", ^^^Update ^^^Interval: ^^^{} ^^^Minutes".format(
                    self.settings.get("Off Day Thread", {}).get("UPDATE_INTERVAL", 5)
                ),
            )
            self.threadCache["off"].update(
                {
                    "text": offThreadText,
                    "thread": offThread,
                    "title": offThread.title
                    if offThread not in [None, False]
                    else None,
                }
            )
            skipFlag = True
        else:
            self.threadCache["off"].update({"thread": offThread})

        while (
            not self.stopFlags["off"] and redball.SIGNAL is None and not self.bot.STOP
        ):
            # Keep off thread updated
            if skipFlag:
                # Skip check/edit since skip flag is set
                skipFlag = None
                self.log.debug(
                    "Skip flag is set, off thread was just submitted/edited and does not need to be checked."
                )
            else:
                try:
                    # Update data
                    self.collect_data()
                    # self.log.debug('data passed into render_template: {}'.format(self.allData))#debug
                    text = self.render_template(
                        thread="off",
                        templateType="thread",
                        data=self.allData,
                        settings=self.settings,
                        convert_timezone=self.convert_timezone,
                    )
                    self.log.debug("Rendered off thread text: {}".format(text))
                    if text != self.threadCache["off"].get("text") and text != "":
                        self.threadCache["off"].update({"text": text})
                        text += (
                            """

^^^Last ^^^Updated: ^^^"""
                            + self.convert_timezone(
                                datetime.utcnow(),
                                self.team_timezone,
                            ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z")
                            + ", ^^^Update ^^^Interval: ^^^{} ^^^Minutes".format(
                                self.settings.get("Off Day Thread", {}).get(
                                    "UPDATE_INTERVAL", 5
                                )
                            )
                        )
                        self.threadCache["off"]["thread"].edit(text)
                        self.log.info("Off Day thread edits submitted.")
                        self.count_check_edit(
                            self.threadCache["off"]["thread"].id, "NA", edit=True
                        )
                        self.log_last_updated_date_in_db(
                            self.threadCache["off"]["thread"].id
                        )
                    elif text == "":
                        self.log.info(
                            "Skipping off thread edit since thread text is blank..."
                        )
                    else:
                        self.log.info("No changes to off thread.")
                        self.count_check_edit(
                            self.threadCache["off"]["thread"].id, "NA", edit=False
                        )
                except Exception as e:
                    self.log.error("Error editing off thread: {}".format(e))
                    self.error_notification("Error editing off thread")

            update_off_thread_until = self.settings.get("Off Day Thread", {}).get(
                "UPDATE_UNTIL", "All conference games are final"
            )
            if update_off_thread_until not in [
                "Do not update",
                "All division games are final",
                "All conference games are final",
                "All NBA games are final",
            ]:
                # Unsupported value, use default
                update_off_thread_until = "All conference games are final"

            if not self.settings.get("Off Day Thread", {}).get("ENABLED", True):
                # Off Day thread is already posted, but disabled. Don't update it.
                self.log.info(
                    "Stopping off thread update loop because off thread is disabled."
                )
                self.stopFlags.update({"off": True})
                break
            elif update_off_thread_until == "Do not update":
                # Setting says not to update
                self.log.info(
                    "Stopping off thread update loop per UPDATE_UNTIL setting."
                )
                self.stopFlags.update({"off": True})
                break
            elif update_off_thread_until == "All division games are final":
                if not next(  # All division games are final
                    (
                        True
                        for x in self.allData["todayOtherDivisionGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping off thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"off": True})
                    break
            elif update_off_thread_until == "All conference games are final":
                if not next(  # All conference games are final
                    (
                        True
                        for x in self.allData["todayOtherConferenceGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # Conference games are all final
                    self.log.info(
                        "All conference games are final. Stopping off thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"off": True})
                    break
            elif update_off_thread_until == "All NBA games are final":
                if not next(  # All NBA games are final
                    (
                        True
                        for x in self.allData["todayAllOtherGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # NBA games are all final
                    self.log.info(
                        "All NBA games are final. Stopping off thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"off": True})
                    break

            self.log.debug(
                "Off Day thread stop criteria not met ({}).".format(
                    update_off_thread_until
                )
            )  # debug - need this to tell if logic is working

            # Update interval is in minutes (seconds for game thread only)
            tgtWait = self.settings.get("off Thread", {}).get("UPDATE_INTERVAL", 5)
            if tgtWait < 1:
                tgtWait = 1
            self.log.info("Sleeping for {} minutes...".format(tgtWait))
            self.sleep(tgtWait * 60)

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        # Mark off thread as stale
        if self.threadCache["off"].get("thread"):
            self.staleThreads.append(self.threadCache["off"]["thread"])

        self.log.debug("Ending off update thread...")
        return

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

        # Check if tailgate thread already posted (record in threads table with type='tailgate' for today's game_id)
        tgq = f"select * from {self.dbTablePrefix}threads where type='tailgate' and gameId = '{self.allData['game_id']}' and gameDate = '{self.today['Y-m-d']}' and deleted=0;"
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
                    self.team_timezone,
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
                        convert_timezone=self.convert_timezone,
                    )
                    self.log.debug("Rendered tailgate thread text: {}".format(text))
                    if text != self.threadCache["tailgate"].get("text") and text != "":
                        self.threadCache["tailgate"].update({"text": text})
                        text += (
                            """

^^^Last ^^^Updated: ^^^"""
                            + self.convert_timezone(
                                datetime.utcnow(),
                                self.team_timezone,
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
                "All conference games are final",
                "All NBA games are final",
            ]:
                # Unsupported value, use default
                update_tailgate_thread_until = "Game thread is posted"

            if (
                update_tailgate_thread_until == "Game thread is posted"
                and not self.settings.get("Game Thread", {}).get("ENABLED", True)
            ):
                # Tailgate thread UPDATE_UNTIL will never be met
                self.log.warning(
                    "Tailgate thread set to update until game thread is posted, but game thread is disabled! Tailgate thread will not be updated."
                )
                update_tailgate_thread_until = "Do not update"

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
                    self.game_status() >= 3 or "PPD" in self.game_status_text()
                ) and not next(  # And all division games are final
                    (
                        True
                        for x in self.allData["todayOtherDivisionGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping tailgate thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"tailgate": True})
                    break
            elif update_tailgate_thread_until == "All conference games are final":
                if (  # This game is final
                    self.game_status() >= 3 or "PPD" in self.game_status_text()
                ) and not next(  # And all conference games are final
                    (
                        True
                        for x in self.allData["todayOtherConferenceGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # Conference games are all final
                    self.log.info(
                        "All conference games are final. Stopping tailgate thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"tailgate": True})
                    break
            elif update_tailgate_thread_until == "All NBA games are final":
                if (  # This game is final
                    self.game_status() >= 3 or "PPD" in self.game_status_text()
                ) and not next(  # All NBA games are final
                    (
                        True
                        for x in self.allData["todayAllOtherGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # NBA games are all final
                    self.log.info(
                        "All NBA games are final. Stopping tailgate thread update loop per UPDATE_UNTIL setting."
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

    def game_thread_update_loop(self, game_id):
        skipFlag = (
            None  # Will be set later if game thread submit/edit should be skipped
        )

        # Check if game thread is already posted
        gq = "select * from {}threads where type='game' and gameId = '{}' and gameDate = '{}' and deleted=0;".format(
            self.dbTablePrefix, game_id, self.today["Y-m-d"]
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
                if self.game_status() >= 3 or "PPD" in self.game_status_text():
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
                            "Game status: {}; skipping game thread...".format(
                                self.game_status_text(),
                            )
                        )
                        skipFlag = True
                    break
                elif self.game_status() == 2:
                    # Game is already in live status, so submit the game thread!
                    self.log.info(
                        "It's technically not time to submit the game thread yet, but the game status is already 2. Proceeding..."
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
                        self.team_timezone,
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
                    convert_timezone=self.convert_timezone,
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
                            self.team_timezone,
                        ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z")
                    )
                    self.threadCache["game"]["thread"].edit(text)
                    self.log.info("Edits submitted for game thread.")
                    self.count_check_edit(
                        self.threadCache["game"]["thread"].id,
                        self.game_status(),
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
                        self.game_status(),
                        edit=False,
                    )

            update_game_thread_until = self.settings.get("Game Thread", {}).get(
                "UPDATE_UNTIL", ""
            )
            if update_game_thread_until not in [
                "Do not update",
                "My team's game is final",
                "All division games are final",
                "All conference games are final",
                "All NBA games are final",
            ]:
                # Unsupported value, use default
                update_game_thread_until = "My team's game is final"

            if update_game_thread_until == "Do not update":
                # Setting says not to update
                self.log.info(
                    "Stopping game thread update loop per UPDATE_UNTIL setting."
                )
                self.stopFlags.update({"game": True})
                break
            elif update_game_thread_until == "My team's game is final":
                if self.game_status() >= 3 or "PPD" in self.game_status_text():
                    # My team's game is final
                    self.log.info(
                        "My team's game is final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"game": True})
                    break
            elif update_game_thread_until == "All division games are final":
                if (  # This game is final
                    self.game_status() >= 3 or "PPD" in self.game_status_text()
                ) and not next(  # And all division games are final
                    (
                        True
                        for x in self.allData["todayOtherDivisionGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"game": True})
                    break
            elif update_game_thread_until == "All conference games are final":
                if (  # This game is final
                    self.game_status() >= 3 or "PPD" in self.game_status_text()
                ) and not next(  # And all conference games are final
                    (
                        True
                        for x in self.allData["todayOtherConferenceGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # Conference games are all final
                    self.log.info(
                        "All conference games are final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"game": True})
                    break
            elif update_game_thread_until == "All NBA games are final":
                if (  # This game is final
                    self.game_status() >= 3 or "PPD" in self.game_status_text()
                ) and not next(  # All NBA games are final
                    (
                        True
                        for x in self.allData["todayAllOtherGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # NBA games are all final
                    self.log.info(
                        "All NBA games are final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"game": True})
                    break

            self.log.debug(
                "Game thread stop criteria not met ({}).".format(
                    update_game_thread_until
                )
            )  # debug - need this to tell if logic is working

            if self.game_status() == 2:
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
                        self.game_status_text(),
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
            if self.game_status() >= 3 or "PPD" in self.game_status_text():
                # Game is over
                self.log.info(
                    "Game is over ({}). Proceeding with post game thread...".format(
                        self.game_status_text(),
                    )
                )
                break
            elif self.stopFlags["game"]:
                # Game thread process has stopped, but game status isn't final yet... get fresh data!
                self.log.info(
                    f"Game thread process has ended, but cached game status is still ({self.allData['game']['summary'].box_score_summary.game_status}). Refreshing data..."
                )
                # Update data
                self.collect_data()
            else:
                self.log.debug(
                    "Game is not yet final ({}). Sleeping for 1 minute...".format(
                        self.game_status_text(),
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
            self.dbTablePrefix, self.allData["game_id"], self.today["Y-m-d"]
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
                    self.team_timezone,
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
                        convert_timezone=self.convert_timezone,
                    )
                    self.log.debug(f"Rendered post game thread text: {text}")
                    if text != self.threadCache["post"]["text"] and text != "":
                        self.threadCache["post"]["text"] = text
                        text += (
                            """

^^^Last ^^^Updated: ^^^"""
                            + self.convert_timezone(
                                datetime.utcnow(),
                                self.team_timezone,
                            ).strftime("%m/%d/%Y ^^^%I:%M:%S ^^^%p ^^^%Z")
                        )
                        self.threadCache["post"]["thread"].edit(text)
                        self.log.info("Post game thread edits submitted.")
                        self.log_last_updated_date_in_db(
                            self.threadCache["post"]["thread"].id
                        )
                        self.count_check_edit(
                            self.threadCache["post"]["thread"].id,
                            self.game_status(),
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
                            self.game_status(),
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
                "All conference games are final",
                "All NBA games are final",
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
                    self.game_status() >= 3 or "PPD" in self.game_status_text()
                ) and not next(  # And all division games are final
                    (
                        True
                        for x in self.allData["todayOtherDivisionGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping post game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"post": True})
                    break
            elif update_postgame_thread_until == "All conference games are final":
                if (  # This game is final
                    self.game_status() >= 3 or "PPD" in self.game_status_text()
                ) and not next(  # And all conference games are final
                    (
                        True
                        for x in self.allData["todayOtherConferenceGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # Conference games are all final
                    self.log.info(
                        "All conference games are final. Stopping post game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.stopFlags.update({"post": True})
                    break
            elif update_postgame_thread_until == "All NBA games are final":
                if (  # This game is final
                    self.game_status() >= 3 or "PPD" in self.game_status_text()
                ) and not next(  # All NBA games are final
                    (
                        True
                        for x in self.allData["todayAllOtherGames"]
                        if x.game_status < 3 and "PPD" not in x.game_status_text
                    ),
                    False,
                ):
                    # NBA games are all final
                    self.log.info(
                        "All NBA games are final. Stopping post game thread update loop per UPDATE_UNTIL setting."
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
            cache_seconds = self.settings.get("NBA", {}).get("API_CACHE_SECONDS", 5)
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
                self.log.debug(
                    f"Collecting data with pynbaapi v{pynbaapi.__version__.__version__}"
                )

            # Collect the data...
            # Get today's games
            todayScoreboard = self.nba.scoreboard(self.today["Y-m-d"])
            todayMyGames = [
                x
                for x in todayScoreboard.scoreboard.games
                if self.myTeamId in [x.away_team.team_id, x.home_team.team_id]
            ]
            todayOtherDivisionGames = [
                x
                for x in todayScoreboard.scoreboard.games
                if x.game_id != [g.game_id for g in todayMyGames]
                and (
                    x.away_team.team_id in self.otherDivisionTeamIds
                    or x.home_team.team_id in self.otherDivisionTeamIds
                )
            ]
            todayOtherConferenceGames = [
                x
                for x in todayScoreboard.scoreboard.games
                if x.game_id not in [g.game_id for g in todayMyGames]
                and (
                    x.away_team.team_id in self.otherConferenceTeamIds
                    or x.home_team.team_id in self.otherConferenceTeamIds
                )
            ]
            todayAllOtherGames = [
                x
                for x in todayScoreboard.scoreboard.games
                if self.myTeamId not in [x.away_team.team_id, x.home_team.team_id]
            ]
            if self.allData["game_id"] != "off":
                self.log.debug(
                    f"Gathering data for game_id [{self.allData['game_id']}]..."
                )
                box_summary = self.nba.boxscore_summary(self.allData["game_id"])
                box_traditional = self.nba.boxscore_traditional(self.allData["game_id"])
                try:
                    box_live = self.nba.api.from_url(
                        f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{self.allData['game_id']}.json"
                    )
                except Exception as e:
                    self.log.debug(f"Exception retrieving live box from cdn: {e}")
                    box_live = None
                boxscore = {
                    "summary": box_summary,
                    "traditional": box_traditional,
                    "live": box_live,
                }
                homeAway = (
                    "home"
                    if boxscore["summary"].box_score_summary.home_team_id
                    == self.myTeamId
                    else "away"
                    if boxscore["summary"].box_score_summary.away_team_id
                    == self.myTeamId
                    else None
                )
                oppHomeAway = "home" if homeAway == "away" else "away"
                self.log.debug(f"My team is [{homeAway}] (homeAway)")
                oppTeam = self.nba.team(
                    boxscore["summary"].box_score_summary.home_team_id
                    if homeAway == "away"
                    else boxscore["summary"].box_score_summary.away_team_id
                )
                oppTeamId = oppTeam.team_info.team_id
                self.log.debug(f"oppTeamId: {oppTeamId}")
                self.log.debug(f"oppTeam: {str(oppTeam)}")
                gameTime = self.convert_timezone(  # Convert Zulu to my team TZ
                    datetime.strptime(
                        boxscore["summary"].box_score_summary.game_time_utc,
                        "%Y-%m-%dT%H:%M:%SZ",
                    ),
                    self.team_timezone,
                )
                gameTime_local = self.convert_timezone(  # Convert Zulu to my team TZ
                    datetime.strptime(
                        boxscore["summary"].box_score_summary.game_time_utc,
                        "%Y-%m-%dT%H:%M:%SZ",
                    ),
                    "local",
                )
                self.log.debug(
                    f"gameTime (my team TZ): {gameTime}; gameTime_local: {gameTime_local}"
                )
            else:
                self.log.debug(
                    "It's an off day, so skipping game-related data retrieval."
                )
                homeAway = ""
                oppTeam = oppTeamId = oppHomeAway = gameTime_local = gameTime = None
                boxscore = None

            standings = self.nba.standings(self.today["season"])

            # Initialize var to hold game data throughout the day
            self.allData.update(
                {
                    "todayMyGames": todayMyGames,
                    "homeAway": homeAway,
                    "oppTeam": oppTeam,
                    "oppTeamId": oppTeamId,
                    "oppHomeAway": oppHomeAway,
                    "gameTime": {
                        "bot": gameTime_local,
                        "myTeam": gameTime,
                    },
                    "game": boxscore,
                    "todayOtherDivisionGames": todayOtherDivisionGames,
                    "todayOtherConferenceGames": todayOtherConferenceGames,
                    "todayAllOtherGames": todayAllOtherGames,
                    "standings": standings,
                }
            )
            self.allData.update(
                {
                    "gameStatus": self.game_status(),
                    "gameStatusText": self.game_status_text(),
                }
            )
            if self.allData["gameStatus"] >= 3 or "PPD" in str(
                self.allData["gameStatusText"]
            ):
                self.allData.update(
                    {
                        "next_game": self.nba.next_game(
                            self.myTeamId, self.today["season"], self.today["obj"]
                        )
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
        # thread = ['off', 'tailgate', 'game', 'post']
        # postFooter = text to append to post body, but not to include in return text value
        #   (normally contains a timestamp that would prevent comparison next time to check for changes)

        self.collect_data()

        try:
            title = self.render_template(
                thread=thread,
                templateType="title",
                data=self.allData,
                settings=self.settings,
                convert_timezone=self.convert_timezone,
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
            self.settings.get("Off Day Thread", {}).get("FLAIR", "")
            if thread == "off"
            else self.settings.get("Tailgate Thread", {}).get("FLAIR", "")
            if thread == "tailgate"
            else self.settings.get("Game Thread", {}).get("FLAIR", "")
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get("FLAIR", "")
            if thread == "post"
            else ""
        )
        sort = (
            self.settings.get("Off Day Thread", {}).get("SUGGESTED_SORT", "")
            if thread == "off"
            else self.settings.get("Tailgate Thread", {}).get("SUGGESTED_SORT", "new")
            if thread == "tailgate"
            else self.settings.get("Game Thread", {}).get("SUGGESTED_SORT", "new")
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get("SUGGESTED_SORT", "new")
            if thread == "post"
            else "new"
        )
        liveDiscussion = (
            self.settings.get("Off Day Thread", {}).get("LIVE_DISCUSSION", False)
            if thread == "off"
            else self.settings.get("Tailgate Thread", {}).get("LIVE_DISCUSSION", False)
            if thread == "tailgate"
            else self.settings.get("Game Thread", {}).get("LIVE_DISCUSSION", False)
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get("LIVE_DISCUSSION", False)
            if thread == "post"
            else False
        )
        lockPrevious = (
            False
            if thread in ["off", "tailgate"]
            else self.settings.get("Game Thread", {}).get("LOCK_TAILGATE_THREAD", False)
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get(
                "LOCK_GAME_THREAD", False
            )
            if thread == "post"
            else False
        )
        linkPrevious = (
            self.settings.get("Game Thread", {}).get("LINK_IN_TAILGATE_THREAD", False)
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get(
                "LINK_IN_GAME_THREAD", False
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
                    convert_timezone=self.convert_timezone,
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
                    thread, self.allData["game_id"]
                )
            )
            self.insert_thread_to_db(self.allData["game_id"], theThread, thread)

            # Check for webhooks
            for w in range(0, 10):
                s = "" if w == 0 else str(w)
                webhook_url = (
                    self.settings.get("Off Day Thread", {}).get(
                        "WEBHOOK{}_URL".format(s)
                    )
                    if thread == "off"
                    else self.settings.get("Tailgate Thread", {}).get(
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
                        convert_timezone=self.convert_timezone,
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
                    event=f"{self.myTeam.team_info.team_name} {thread.title()} Thread Posted",
                    description=f"""{self.myTeam.team_info.team_name} {thread} thread was posted to r/{self.settings["Reddit"]["SUBREDDIT"]} at {self.convert_timezone(datetime.utcfromtimestamp(theThread.created_utc),'local').strftime('%I:%M %p %Z')}\nThread title: {theThread.title}\nURL: {theThread.shortlink}""",
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
                    message = f"""{theThread.title} - Join the discussion: {theThread.shortlink} #{self.myTeam.team_info.team_name.replace(' ','')}"""
                elif thread == "tailgate":
                    message = f"""{theThread.title} - Join the discussion: {theThread.shortlink} #{self.myTeam.team_info.team_name.replace(' ','')}"""
                elif thread == "off":
                    message = f"""{theThread.title} - Join the discussion: {theThread.shortlink} #{self.myTeam.team_info.team_name.replace(' ','')}"""
                elif thread == "post":
                    message = f"""{theThread.title} - The discussion continues: {theThread.shortlink} #{self.myTeam.team_info.team_name.replace(' ','')}"""
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
            if lockPrevious or linkPrevious:
                if previousThread := (
                    self.threadCache["tailgate"].get("thread")
                    if thread == "game"
                    else self.threadCache["game"].get("thread")
                    if thread == "post"
                    else None
                ):
                    if lockPrevious:
                        try:
                            self.log.debug(
                                f"Attempting to lock {'tailgate' if thread == 'game' else 'game' if thread == 'post' else ''} thread [{previousThread.id}]..."
                            )
                            previousThread.mod.lock()
                        except Exception as e:
                            self.log.warning(
                                f"Failed to lock {'tailgate' if thread == 'game' else 'game' if thread == 'post' else ''} thread [{previousThread.id}]: {e}"
                            )

                    if linkPrevious:
                        commentText = (
                            self.settings.get("Game Thread", {}).get(
                                "TAILGATE_THREAD_MESSAGE", None
                            )
                            if thread == "game"
                            else self.settings.get("Post Game Thread", {}).get(
                                "GAME_THREAD_MESSAGE", None
                            )
                            if thread == "post"
                            else None
                        )
                        if not commentText:
                            commentText = f"{'This thread has been locked. ' if lockPrevious else ''}Please continue the discussion in the [{'game' if thread == 'game' else 'post game' if thread == 'post' else 'new'} thread](link)."

                        parsedCommentText = commentText.replace(
                            "(link)", f"({theThread.shortlink})"
                        )
                        try:
                            self.log.debug(
                                "Submitting comment in previous thread with link to new thread..."
                            )
                            lockReply = previousThread.reply(parsedCommentText)
                            self.log.debug("Distinguishing comment...")
                            lockReply.mod.distinguish(sticky=True)
                            self.log.debug(
                                f"Successfully posted a distinguished/sticky reply in {'tailgate' if thread == 'game' else 'game' if thread == 'post' else ''} thread."
                            )
                        except Exception as e:
                            self.log.warning(
                                f"Failed to submit reply with link to new thread or distinguish and sticky comment in {'tailgate' if thread == 'game' else 'game' if thread == 'post' else ''} thread: {e}"
                            )
                else:
                    self.log.debug("I did not find a previous thread to lock or link.")

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
            self.settings.get("Off Day Thread", {}).get(setting, "")
            if thread == "off"
            else self.settings.get("Tailgate Thread", {}).get(setting, "")
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
        "ATL": "/r/atlantahawks",
        "BKN": "/r/gonets",
        "BOS": "/r/bostonceltics",
        "CHA": "/r/charlottehornets",
        "CHI": "/r/chicagobulls",
        "CLE": "/r/clevelandcavs",
        "DAL": "/r/mavericks",
        "DEN": "/r/denvernuggets",
        "DET": "/r/detroitpistons",
        "GSW": "/r/warriors",
        "HOU": "/r/rockets",
        "IND": "/r/pacers",
        "LAC": "/r/laclippers",
        "LAL": "/r/lakers",
        "MEM": "/r/memphisgrizzlies",
        "MIA": "/r/heat",
        "MIL": "/r/mkebucks",
        "MIN": "/r/timberwolves",
        "NOP": "/r/nolapelicans",
        "NYK": "/r/nyknicks",
        "OKC": "/r/thunder",
        "ORL": "/r/orlandomagic",
        "PHI": "/r/sixers",
        "PHX": "/r/suns",
        "POR": "/r/ripcity",
        "SAC": "/r/kings",
        "SAS": "/r/nbaspurs",
        "TOR": "/r/torontoraptors",
        "UTA": "/r/utahjazz",
        "WAS": "/r/washingtonwizards",
    }

    teamSubsById = {
        1610612737: "/r/atlantahawks",
        1610612751: "/r/gonets",
        1610612738: "/r/bostonceltics",
        1610612766: "/r/charlottehornets",
        1610612741: "/r/chicagobulls",
        1610612739: "/r/clevelandcavs",
        1610612742: "/r/mavericks",
        1610612743: "/r/denvernuggets",
        1610612765: "/r/detroitpistons",
        1610612744: "/r/warriors",
        1610612745: "/r/rockets",
        1610612754: "/r/pacers",
        1610612746: "/r/laclippers",
        1610612747: "/r/lakers",
        1610612763: "/r/memphisgrizzlies",
        1610612748: "/r/heat",
        1610612749: "/r/mkebucks",
        1610612750: "/r/timberwolves",
        1610612740: "/r/nolapelicans",
        1610612752: "/r/nyknicks",
        1610612760: "/r/thunder",
        1610612753: "/r/orlandomagic",
        1610612755: "/r/sixers",
        1610612756: "/r/suns",
        1610612757: "/r/ripcity",
        1610612758: "/r/kings",
        1610612759: "/r/nbaspurs",
        1610612761: "/r/torontoraptors",
        1610612762: "/r/utahjazz",
        1610612764: "/r/washingtonwizards",
    }

    def game_status(self):
        if self.allData["game_id"] == "off":
            return 0
        if self.allData.get("game", {}).get("live"):
            return self.allData["game"]["live"].game.game_status
        elif len(self.allData.get("todayMyGames", [])):
            return self.allData["todayMyGames"][0].game_status
        elif self.allData.get("game", {}).get("summary"):
            return self.allData["game"]["summary"].box_score_summary.game_status
        else:
            return -1

    def game_status_text(self):
        if self.allData["game_id"] == "off":
            return 0
        if self.allData.get("game", {}).get("live"):
            return self.allData["game"]["live"].game.game_status_text.strip()
        elif len(self.allData.get("todayMyGames", [])):
            return self.allData["todayMyGames"][0].game_status_text.strip()
        elif self.allData.get("game", {}).get("summary"):
            return self.allData["game"][
                "summary"
            ].box_score_summary.game_status_text.strip()
        else:
            return ""

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
                    "id": self.myTeam.team_info.team_id,
                    "name": f"{self.myTeam.team_info.team_city} {self.myTeam.team_info.team_name}",
                    "abbreviation": self.myTeam.team_info.team_abbreviation,
                    "teamName": self.myTeam.team_info.team_name,
                    "locationName": self.myTeam.team_info.team_city,
                },
                "today": self.today,
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
                "offThread": {
                    "enabled": self.settings.get("Off Day Thread", {}).get(
                        "ENABLED", True
                    ),
                    "postTime": self.threadCache.get("off", {})
                    .get("postTime_local")
                    .strftime("%m/%d/%Y %I:%M:%S %p")
                    if isinstance(
                        self.threadCache.get("off", {}).get("postTime_local"),
                        datetime,
                    )
                    else "",
                    "posted": True
                    if self.threadCache.get("off", {}).get("thread")
                    else False,
                    "id": self.threadCache.get("off", {}).get("thread").id
                    if self.threadCache.get("off", {}).get("thread")
                    else None,
                    "url": self.threadCache.get("off", {}).get("thread").shortlink
                    if self.threadCache.get("off", {}).get("thread")
                    else None,
                    "title": self.threadCache.get("off", {}).get("title")
                    if self.threadCache.get("off", {}).get("thread")
                    else None,
                },
                "game": {
                    "gameId": self.allData.get("game_id")
                    if self.allData.get("game_id") != "off"
                    else None,
                    "status": self.game_status(),
                    "oppTeam": deepcopy(self.allData.get("oppTeam"))
                    if self.allData.get("oppTeam")
                    else None,
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
                        "text": "Today is {}.".format(
                            botStatus["today"]["Y-m-d"],
                        ),
                        "html": "Today is {}.".format(
                            botStatus["today"]["Y-m-d"],
                        ),
                        "markdown": "Today is {}.".format(
                            botStatus["today"]["Y-m-d"],
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
                ] += f"Today's game ({botStatus['game']['gameId']}): {botStatus['game']['gameTime']} {'@' if botStatus['game']['homeAway']=='away' else 'vs.'} {botStatus['game']['oppTeam'].team_info.team_name}"
                botStatus["summary"][
                    "html"
                ] += f"Today's game ({botStatus['game']['gameId']}): {botStatus['game']['gameTime']} {'@' if botStatus['game']['homeAway']=='away' else 'vs.'} {botStatus['game']['oppTeam'].team_info.team_name}"
                botStatus["summary"][
                    "markdown"
                ] += f"Today's game ({botStatus['game']['gameId']}): {botStatus['game']['gameTime']} {'@' if botStatus['game']['homeAway']=='away' else 'vs.'} {botStatus['game']['oppTeam'].team_info.team_name}"

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

                if not botStatus["offThread"]["enabled"]:
                    # Off Day thread is disabled
                    botStatus["summary"]["text"] += "\n\nOff Day thread disabled."
                    botStatus["summary"][
                        "html"
                    ] += "<br /><br /><strong>Off Day thread</strong> disabled."
                    botStatus["summary"][
                        "markdown"
                    ] += "\n\n**Off Day thread** disabled."
                else:
                    if not botStatus["offThread"]["posted"]:
                        # Thread is not posted (could be error)
                        botStatus["summary"][
                            "text"
                        ] += f"\n\nOff Day thread post time: {botStatus['offThread']['postTime']}"
                        botStatus["summary"][
                            "html"
                        ] += f"<br /><br /><strong>Off Day thread</strong> post time: {botStatus['offThread']['postTime']}"
                        botStatus["summary"][
                            "markdown"
                        ] += f"\n\n**Off Day thread** post time: {botStatus['offThread']['postTime']}"
                    else:
                        # Thread is posted
                        botStatus["summary"][
                            "text"
                        ] += f"\n\nOff Day thread: {botStatus['offThread']['title']} ({botStatus['offThread']['id']} - {botStatus['offThread']['url']})"
                        botStatus["summary"][
                            "html"
                        ] += f"<br /><br /><strong>Off Day thread</strong>: {botStatus['offThread']['title']} (<a href=\"{botStatus['offThread']['url']}\" target=\"_blank\">{botStatus['offThread']['id']}</a>)"
                        botStatus["summary"][
                            "markdown"
                        ] += f"\n\n**Off Day thread**: {botStatus['offThread']['title']} ([{botStatus['offThread']['id']}]({botStatus['offThread']['url']}))"

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
