#!/usr/bin/env python
# encoding=utf-8
"""MLB Game Thread Bot
by Todd Roberts
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError
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

import pyprowl
import statsapi

from . import plaw

__version__ = "1.0.0"

GENERIC_DATA_LOCK = threading.Lock()
GAME_DATA_LOCK = threading.Lock()


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
            "Game Thread Bot v{} received settings: {}. Template path: {}".format(
                __version__, self.settings, self.BOT_TEMPLATE_PATH
            )
        )

        # Check db for tables and create if necessary
        self.dbTablePrefix = self.settings.get("Database").get(
            "dbTablePrefix", "gdt{}_".format(self.bot.id)
        )
        self.build_tables()

        # Initialize Lemmy API connection
        self.init_lemmy()

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
        if self.settings.get("MLB", {}).get("GAME_DATE_OVERRIDE", "") != "":
            # Bot config says to treat specified date as 'today'
            todayOverrideFlag = True
        else:
            todayOverrideFlag = False

        # Initialize var to old info about weekly thread
        # This should be separate from other threads because
        # it doesn't turn over daily
        self.weekly = {}

        while redball.SIGNAL is None and not self.bot.STOP:
            # This is the daily loop
            # Refresh settings
            if settings_date != datetime.today().strftime("%Y-%m-%d"):
                self.refresh_settings()
                settings_date = datetime.today().strftime("%Y-%m-%d")

            # Get info about configured team
            if self.settings.get("MLB", {}).get("TEAM", "") == "":
                self.log.critical("No team selected! Set MLB > TEAM in Bot Config.")
                self.bot.STOP = True
                break

            self.myTeam = self.get_team(
                self.settings.get("MLB", {}).get("TEAM", "").split("|")[1],
                s=datetime.now().strftime(
                    "%Y"
                ),  # band-aid due to MLB defaulting team page to 2021 season in July 2020
            )
            self.log.info("Configured team: {}".format(self.myTeam["name"]))

            if todayOverrideFlag:
                todayOverrideFlag = (
                    False  # Only override once, then go back to current date
                )
                self.log.info(
                    "Overriding game date per GAME_DATE_OVERRIDE setting [{}].".format(
                        self.settings["MLB"]["GAME_DATE_OVERRIDE"]
                    )
                )
                try:
                    todayObj = datetime.strptime(
                        self.settings["MLB"]["GAME_DATE_OVERRIDE"], "%Y-%m-%d"
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
            self.log.debug("Today is {}".format(self.today["Y-m-d"]))

            # Get season state
            self.seasonState = self.get_seasonState(self.myTeam["id"])
            self.log.debug("Season state: {}".format(self.seasonState))

            # Get today's games
            todayGamePks = self.get_gamePks(t=self.myTeam["id"], d=self.today["Y-m-d"])
            self.THREADS = {}  # Clear yesterday's threads
            self.activeGames = {}  # Clear yesterday's flags
            self.commonData = {}  # Clear data dict every day to save memory
            self.collect_data(0)  # Collect generic data

            if len(todayGamePks) == 0:
                # Off day thread
                self.log.info("No games today!")
                self.off_day()  # Start the off day thread update process and enter a loop
                if redball.SIGNAL is not None or self.bot.STOP:
                    break
            else:
                self.log.info(
                    "Found {} game(s) for today: {}".format(
                        len(todayGamePks), todayGamePks
                    )
                )
                # Initialize activeGames and THREADS dicts (will hold game info and thread lemmy objects)
                for x in todayGamePks:
                    self.activeGames.update(
                        {x: {"STOP_FLAG": False, "POST_STOP_FLAG": False}}
                    )
                    self.THREADS.update({x: {}})

                self.activeGames.update(
                    {"gameday": {"STOP_FLAG": False}}
                )  # Game day thread is not specific to a gamePk

                self.log.debug("activeGames: {}".format(self.activeGames))

                for pk in todayGamePks:
                    self.commonData.update({pk: {"gamePk": pk}})

                # Collect data for all games
                self.collect_data(todayGamePks)

                # Check if all MLB games are postponed (league is suspended)
                if not next(
                    (
                        True
                        for x in self.commonData[0]["leagueSchedule"]
                        if x["status"]["codedGameState"] != "D"
                    ),
                    False,
                ):
                    # All games are postponed -- assume league is suspended
                    self.log.info(
                        "All of today's MLB games are postponed. Assuming the league is suspended and treating as off day..."
                    )
                    self.commonData.update({"seasonSuspended": True})
                    # Remove game data from cache since we're treating as off day
                    self.activeGames.pop("gameday")
                    for pk in todayGamePks:
                        self.commonData.pop(pk)
                        self.activeGames.pop(pk)

                    self.off_day()
                else:
                    if not self.settings.get("Game Day Thread", {}).get(
                        "ENABLED", True
                    ):
                        self.log.info("Game day thread disabled.")
                        self.activeGames["gameday"].update({"STOP_FLAG": True})
                    else:
                        # Spawn a thread to wait for post time and then keep game day thread updated
                        self.THREADS.update(
                            {
                                "GAMEDAY_THREAD": threading.Thread(
                                    target=self.gameday_thread_update_loop,
                                    args=(todayGamePks,),
                                    name="bot-{}-{}-gameday".format(
                                        self.bot.id, self.bot.name.replace(" ", "-")
                                    ),
                                    daemon=True,
                                )
                            }
                        )
                        self.THREADS["GAMEDAY_THREAD"].start()
                        self.log.debug(
                            "Started game day thread {}.".format(
                                self.THREADS["GAMEDAY_THREAD"]
                            )
                        )

                    # Game thread update processes
                    for (
                        pk
                    ) in (
                        todayGamePks
                    ):  # Loop through gamePks since each game gets its own thread
                        if self.settings.get("Game Thread", {}).get("ENABLED", True):
                            # Spawn separate thread to wait for post time and then keep game thread updated
                            self.THREADS[pk].update(
                                {
                                    "GAME_THREAD": threading.Thread(
                                        target=self.game_thread_update_loop,
                                        args=(pk,),
                                        name="bot-{}-{}-game-{}".format(
                                            self.bot.id,
                                            self.bot.name.replace(" ", "-"),
                                            pk,
                                        ),
                                        daemon=True,
                                    )
                                }
                            )
                            self.THREADS[pk]["GAME_THREAD"].start()
                            self.log.debug(
                                "Started game thread {}.".format(
                                    self.THREADS[pk]["GAME_THREAD"]
                                )
                            )
                        else:
                            self.log.info(
                                "Game thread is disabled! [pk: {}]".format(pk)
                            )
                            self.activeGames[pk].update({"STOP_FLAG": True})

                        if self.settings.get("Post Game Thread", {}).get(
                            "ENABLED", True
                        ):
                            # Spawn separate thread to wait for game to be final and then submit and keep post game thread updated
                            self.THREADS[pk].update(
                                {
                                    "POSTGAME_THREAD": threading.Thread(
                                        target=self.postgame_thread_update_loop,
                                        args=(pk,),
                                        name="bot-{}-{}-postgame-{}".format(
                                            self.bot.id,
                                            self.bot.name.replace(" ", "-"),
                                            pk,
                                        ),
                                        daemon=True,
                                    )
                                }
                            )
                            self.THREADS[pk]["POSTGAME_THREAD"].start()
                            self.log.debug(
                                "Started post game thread {}.".format(
                                    self.THREADS[pk]["POSTGAME_THREAD"]
                                )
                            )
                        else:
                            self.log.info(
                                "Post game thread is disabled! [pk: {}]".format(pk)
                            )
                            self.activeGames[pk].update({"POST_STOP_FLAG": True})

                    # Loop over active games, make sure submit/update and comment threads are running
                    while (
                        len(
                            [
                                {k: v}
                                for k, v in self.activeGames.items()
                                if not v.get("STOP_FLAG", True)
                                or not v.get("POST_STOP_FLAG", True)
                            ]
                        )
                        > 0
                        and redball.SIGNAL is None
                        and not self.bot.STOP
                    ):
                        for pk in (
                            pk
                            for pk in self.activeGames
                            if not self.activeGames[pk]["STOP_FLAG"]
                            and isinstance(pk, int)
                            and pk > 0
                        ):
                            # Check submit/update thread for game thread
                            try:
                                if not self.settings.get("Game Thread", {}).get(
                                    "ENABLED", True
                                ):
                                    # Game thread is disabled, so don't start an update thread...
                                    pass
                                elif (
                                    pk > 0
                                    and not self.activeGames[pk]["STOP_FLAG"]
                                    and self.THREADS[pk].get("GAME_THREAD")
                                    and isinstance(
                                        self.THREADS[pk]["GAME_THREAD"],
                                        threading.Thread,
                                    )
                                    and self.THREADS[pk]["GAME_THREAD"].is_alive()
                                ):
                                    self.log.debug(
                                        "Game thread for game {} looks fine...".format(
                                            pk
                                        )
                                    )  # debug - need this here to see if the condition is working when the thread crashes
                                    # pass
                                elif pk > 0 and self.activeGames[pk]["STOP_FLAG"]:
                                    # Game thread is already done
                                    pass
                                else:
                                    raise Exception(
                                        "Game {} thread update process is not running!".format(
                                            pk
                                        )
                                    )
                            except Exception as e:
                                if "is not running" in str(e):
                                    self.log.error(
                                        "Game {} thread update process is not running. Attempting to start.".format(
                                            pk
                                        )
                                    )
                                    self.error_notification(
                                        f"Game {pk} thread update process is not running"
                                    )
                                    self.THREADS[pk].update(
                                        {
                                            "GAME_THREAD": threading.Thread(
                                                target=self.game_thread_update_loop,
                                                args=(pk,),
                                                name="bot-{}-{}-game-{}".format(
                                                    self.bot.id,
                                                    self.bot.name.replace(" ", "-"),
                                                    pk,
                                                ),
                                                daemon=True,
                                            )
                                        }
                                    )
                                    self.THREADS[pk]["GAME_THREAD"].start()
                                    self.log.debug(
                                        "Started game thread {}.".format(
                                            self.THREADS[pk]["GAME_THREAD"]
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
                                    pk > 0
                                    and not self.activeGames[pk]["POST_STOP_FLAG"]
                                    and self.THREADS[pk].get("POSTGAME_THREAD")
                                    and isinstance(
                                        self.THREADS[pk]["POSTGAME_THREAD"],
                                        threading.Thread,
                                    )
                                    and self.THREADS[pk]["POSTGAME_THREAD"].is_alive()
                                ):
                                    self.log.debug(
                                        "Post game thread for game {} looks fine...".format(
                                            pk
                                        )
                                    )  # debug - need this here to see if the condition is working when the thread crashes
                                    # pass
                                elif pk > 0 and self.activeGames[pk]["POST_STOP_FLAG"]:
                                    # Post game thread is already done
                                    pass
                                else:
                                    raise Exception(
                                        "Post game {} thread update process is not running!".format(
                                            pk
                                        )
                                    )
                            except Exception as e:
                                if "is not running" in str(e):
                                    self.log.error(
                                        "Post game {} thread update process is not running. Attempting to start.".format(
                                            pk
                                        )
                                    )
                                    self.error_notification(
                                        f"Game {pk} post game thread update process is not running"
                                    )
                                    self.THREADS[pk].update(
                                        {
                                            "POSTGAME_THREAD": threading.Thread(
                                                target=self.postgame_thread_update_loop,
                                                args=(pk,),
                                                name="bot-{}-{}-postgame-{}".format(
                                                    self.bot.id,
                                                    self.bot.name.replace(" ", "-"),
                                                    pk,
                                                ),
                                                daemon=True,
                                            )
                                        }
                                    )
                                    self.THREADS[pk]["POSTGAME_THREAD"].start()
                                    self.log.debug(
                                        "Started post game thread {}.".format(
                                            self.THREADS[pk]["POSTGAME_THREAD"]
                                        )
                                    )
                                else:
                                    raise

                            # Check comment thread
                            try:
                                if not self.settings.get("Game Thread", {}).get(
                                    "ENABLED", True
                                ) or not self.settings.get("Comments", {}).get(
                                    "ENABLED", True
                                ):
                                    # Game thread or commenting is disabled, so don't start a comment thread...
                                    pass
                                elif (
                                    pk > 0
                                    and not self.activeGames[pk]["STOP_FLAG"]
                                    and self.THREADS[pk].get("COMMENT_THREAD")
                                    and isinstance(
                                        self.THREADS[pk]["COMMENT_THREAD"],
                                        threading.Thread,
                                    )
                                    and self.THREADS[pk]["COMMENT_THREAD"].is_alive()
                                ):
                                    self.log.debug(
                                        "Comment thread for game {} looks fine...".format(
                                            pk
                                        )
                                    )  # debug - need this here to see if the condition is working when the thread crashes
                                    pass
                                elif pk > 0 and not self.activeGames[pk].get(
                                    "gameThread"
                                ):
                                    # Game thread isn't posted yet, so comment process should not be running
                                    self.log.debug(
                                        "Not starting comment process because game thread is not posted."
                                    )
                                    pass
                                elif pk > 0 and self.activeGames[pk]["STOP_FLAG"]:
                                    # Game thread is already done
                                    self.log.debug(
                                        "Not starting comment process because game thread is already done updating."
                                    )
                                    pass
                                elif self.commonData.get(pk, {}).get(
                                    "schedule", {}
                                ).get("status", {}).get(
                                    "abstractGameCode"
                                ) == "F" or self.commonData.get(
                                    pk, {}
                                ).get(
                                    "schedule", {}
                                ).get(
                                    "status", {}
                                ).get(
                                    "codedGameState"
                                ) in [
                                    "C",
                                    "D",
                                    "U",
                                    "T",
                                ]:
                                    # Game is over, so don't add any comments
                                    self.log.debug(
                                        "Not starting comment process because game is over."
                                    )
                                    pass
                                else:
                                    raise Exception(
                                        "Game {} comment process is not running!".format(
                                            pk
                                        )
                                    )
                            except Exception as e:
                                if "is not running" in str(e):
                                    self.log.error(
                                        "Game {} comment process is not running. Attempting to start.".format(
                                            pk
                                        )
                                    )
                                    self.error_notification(
                                        f"Game {pk} comment process is not running"
                                    )
                                    self.THREADS[pk].update(
                                        {
                                            "COMMENT_THREAD": threading.Thread(
                                                target=self.monitor_game_plays,
                                                args=(
                                                    pk,
                                                    self.activeGames[pk]["gameThread"],
                                                ),
                                                name="bot-{}-{}-game-{}-comments".format(
                                                    self.bot.id,
                                                    self.bot.name.replace(" ", "-"),
                                                    pk,
                                                ),
                                                daemon=True,
                                            )
                                        }
                                    )
                                    self.THREADS[pk]["COMMENT_THREAD"].start()
                                    self.log.debug(
                                        "Started comment thread {}.".format(
                                            self.THREADS[pk]["COMMENT_THREAD"]
                                        )
                                    )
                                else:
                                    raise

                        # Make sure game day thread update process is running
                        try:
                            if not self.settings.get("Game Day Thread", {}).get(
                                "ENABLED", True
                            ):
                                # Game day thread is disabled, so don't start an update thread...
                                pass
                            elif (
                                not self.activeGames["gameday"]["STOP_FLAG"]
                                and self.THREADS.get("GAMEDAY_THREAD")
                                and isinstance(
                                    self.THREADS["GAMEDAY_THREAD"], threading.Thread
                                )
                                and self.THREADS["GAMEDAY_THREAD"].is_alive()
                            ):
                                self.log.debug(
                                    "Game day update thread looks fine..."
                                )  # debug - need this here to see if the condition is working when the thread crashes
                                # pass
                            elif self.activeGames["gameday"]["STOP_FLAG"]:
                                # Game day thread is already done
                                pass
                            else:
                                raise Exception(
                                    "Game day thread update process is not running!"
                                )
                        except Exception as e:
                            if "is not running" in str(e):
                                self.log.error(
                                    "Game day thread update process is not running. Attempting to start. Error: {}".format(
                                        e
                                    )
                                )
                                self.error_notification(
                                    "Game day thread update process is not running"
                                )
                                self.THREADS.update(
                                    {
                                        "GAMEDAY_THREAD": threading.Thread(
                                            target=self.gameday_thread_update_loop,
                                            args=(todayGamePks,),
                                            name="bot-{}-{}-gameday".format(
                                                self.bot.id,
                                                self.bot.name.replace(" ", "-"),
                                            ),
                                            daemon=True,
                                        )
                                    }
                                )
                                self.THREADS["GAMEDAY_THREAD"].start()
                                self.log.debug(
                                    "Started game day thread {}.".format(
                                        self.THREADS["GAMEDAY_THREAD"]
                                    )
                                )
                            else:
                                raise

                        if (
                            len(
                                [
                                    {k: v}
                                    for k, v in self.activeGames.items()
                                    if not v.get("STOP_FLAG", True)
                                    or not v.get("POST_STOP_FLAG", True)
                                ]
                            )
                            > 0
                        ):
                            # There are still games pending/in progress
                            self.log.debug(
                                "Active games/threads: {}".format(
                                    [
                                        k
                                        for k, v in self.activeGames.items()
                                        if not v.get("STOP_FLAG", True)
                                        or not v.get("POST_STOP_FLAG", True)
                                    ]
                                )
                            )
                            self.log.debug(
                                "Active threads: {}".format(
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
        if (
            self.seasonState.startswith("off") or self.seasonState == "post:out"
        ) and self.settings.get("Off Day Thread", {}).get("SUPPRESS_OFFSEASON", True):
            self.log.info("Suppressing off day thread during offseason.")
            self.activeGames.update({"off": {"STOP_FLAG": True}})
        elif not self.settings.get("Off Day Thread", {}).get("ENABLED", True):
            self.log.info("Off day thread disabled.")
            self.activeGames.update({"off": {"STOP_FLAG": True}})
        else:
            # Spawn a thread to wait for post time and then keep off day thread updated
            self.activeGames.update(
                {"off": {"STOP_FLAG": False}}
            )  # Off day thread is not specific to a gamePk
            self.THREADS.update(
                {
                    "OFFDAY_THREAD": threading.Thread(
                        target=self.off_thread_update_loop,
                        name="bot-{}-{}-offday".format(
                            self.bot.id, self.bot.name.replace(" ", "-")
                        ),
                        daemon=True,
                    )
                }
            )
            self.THREADS["OFFDAY_THREAD"].start()
            self.log.debug(
                "Started off day thread {}.".format(self.THREADS["OFFDAY_THREAD"])
            )

        while (
            len([{k: v} for k, v in self.activeGames.items() if not v["STOP_FLAG"]])
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            try:
                if not self.settings.get("Off Day Thread", {}).get("ENABLED", True):
                    # Off day thread is disabled, so don't start an update thread...
                    pass
                elif (
                    not self.activeGames["off"]["STOP_FLAG"]
                    and self.THREADS.get("OFFDAY_THREAD")
                    and isinstance(self.THREADS["OFFDAY_THREAD"], threading.Thread)
                    and self.THREADS["OFFDAY_THREAD"].is_alive()
                ):
                    self.log.debug(
                        "Off day update thread looks fine..."
                    )  # debug - need this here to see if the condition is working when the thread crashes
                    # pass
                elif self.activeGames["off"]["STOP_FLAG"]:
                    # Off day thread is already done
                    pass
                else:
                    raise Exception("Off day thread update process is not running!")
            except Exception as e:
                self.log.error(
                    "Off day thread update process is not running. Attempting to start. (Error: {})".format(
                        e
                    )
                )
                self.error_notification("Off day thread update process is not running")
                self.THREADS.update(
                    {
                        "OFFDAY_THREAD": threading.Thread(
                            target=self.off_thread_update_loop,
                            name="bot-{}-{}-offday".format(
                                self.bot.id, self.bot.name.replace(" ", "-")
                            ),
                            daemon=True,
                        )
                    }
                )
                self.THREADS["OFFDAY_THREAD"].start()
                self.log.debug(
                    "Started off day thread {}.".format(self.THREADS["OFFDAY_THREAD"])
                )

            if (
                len(
                    [
                        {k: v}
                        for k, v in self.activeGames.items()
                        if not v.get("STOP_FLAG", False)
                        or not v.get("POST_STOP_FLAG", False)
                    ]
                )
                > 0
            ):
                # There are still active threads
                self.log.debug(
                    "Active games/threads: {}".format(
                        [
                            k
                            for k, v in self.activeGames.items()
                            if not v["STOP_FLAG"] or not v.get("POST_STOP_FLAG", True)
                        ]
                    )
                )
                self.log.debug(
                    "Active threads: {}".format(
                        [
                            t
                            for t in threading.enumerate()
                            if t.name.startswith(
                                "bot-{}-{}".format(
                                    self.bot.id, self.bot.name.replace(" ", "-")
                                )
                            )
                        ]
                    )
                )
                self.sleep(30)
            else:
                break

    def off_thread_update_loop(self):
        skipFlag = None  # Will be set later if off day thread edit should be skipped

        # Check/wait for time to submit off day thread
        self.activeGames["off"].update(
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
        while (
            datetime.today() < self.activeGames["off"]["postTime_local"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            if (
                self.activeGames["off"]["postTime_local"] - datetime.today()
            ).total_seconds() > 3600:
                self.log.info(
                    "Off day thread should not be posted for a long time ({}). Sleeping for an hour...".format(
                        self.activeGames["off"]["postTime_local"]
                    )
                )
                self.sleep(3600)
            elif (
                self.activeGames["off"]["postTime_local"] - datetime.today()
            ).total_seconds() > 1800:
                self.log.info(
                    "Off day thread post time is still more than 30 minutes away ({}). Sleeping for a half hour...".format(
                        self.activeGames["off"]["postTime_local"]
                    )
                )
                self.sleep(1800)
            else:
                self.log.info(
                    "Off day thread post time is approaching ({}). Sleeping until then...".format(
                        self.activeGames["off"]["postTime_local"]
                    )
                )
                self.sleep(
                    (
                        self.activeGames["off"]["postTime_local"] - datetime.today()
                    ).total_seconds()
                )

        if redball.SIGNAL is not None or self.bot.STOP:
            return

        # Unsticky stale threads
        if self.settings.get("Reddit", {}).get("STICKY", False):
            """
            # Make sure the subreddit's sticky posts are marked as stale
            try:
                sticky1 = self.subreddit.sticky(1)
                if sticky1.author == self.reddit.user.me() and sticky1 not in self.staleThreads:
                    self.staleThreads.append(sticky1)

                sticky2 = self.subreddit.sticky(2)
                if sticky2.author == self.reddit.user.me() and sticky2 not in self.staleThreads:
                    self.staleThreads.append(sticky2)
            except Exception:
                # Exception likely due to no post being stickied (or only one), so ignore it...
                pass
            """
            if len(self.staleThreads):
                self.unsticky_threads(self.staleThreads)
                self.staleThreads = []

        # Check DB for existing off day thread
        oq = "select * from {}threads where gamePk = {} and type='off' and deleted=0;".format(
            self.dbTablePrefix, self.today["Ymd"]
        )
        offThread = rbdb.db_qry(oq, closeAfter=True, logg=self.log)

        offDayThread = None
        if len(offThread) > 0:
            self.log.info(
                "Off Day Thread found in database [{}].".format(offThread[0]["id"])
            )
            offDayThread = self.lemmy.getPost(offThread[0]["id"])
            if not offDayThread["creator"]["name"]:
                self.log.warning("Off day thread appears to have been deleted.")
                q = "update {}threads set deleted=1 where id='{}';".format(
                    self.dbTablePrefix, offDayThread["post"]["id"]
                )
                u = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
                if isinstance(u, str):
                    self.log.error(
                        "Error marking thread as deleted in database: {}".format(u)
                    )

                offDayThread = None
            else:
                if offDayThread["post"]["body"].find("\n\nLast Updated") != -1:
                    offDayThreadText = offDayThread["post"]["body"][
                        0 : offDayThread["post"]["body"].find("\n\nLast Updated:")
                    ]
                elif offDayThread["post"]["body"].find("\n\nPosted") != -1:
                    offDayThreadText = offDayThread["post"]["body"][
                        0 : offDayThread["post"]["body"].find("\n\nPosted:")
                    ]
                else:
                    offDayThreadText = offDayThread["post"]["body"]

                self.activeGames["off"].update(
                    {
                        "offDayThreadText": offDayThreadText,
                        "offDayThread": offDayThread,
                        "offDayThreadTitle": offDayThread["post"]["name"]
                        if offDayThread not in [None, False]
                        else None,
                    }
                )
                # Only sticky when posting the thread
                if self.settings.get('Reddit',{}).get('STICKY',False): self.sticky_thread(offDayThread)

        if not offDayThread:
            (offDayThread, offDayThreadText) = self.prep_and_post(
                "off",
                postFooter="""

Posted: """
                + self.convert_timezone(
                    datetime.utcnow(), self.myTeam["venue"]["timeZone"]["id"]
                ).strftime("%m/%d/%Y %I:%M:%S %p %Z")
                + ", Update Interval: {} Minutes".format(
                    self.settings.get("Off Day Thread", {}).get("UPDATE_INTERVAL", 5)
                ),
            )
            self.activeGames["off"].update(
                {
                    "offDayThreadText": offDayThreadText,
                    "offDayThread": offDayThread,
                    "offDayThreadTitle": offDayThread["post"]["name"]
                    if offDayThread not in [None, False]
                    else None,
                }
            )
            skipFlag = True

        while (
            not self.activeGames["off"]["STOP_FLAG"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            # Keep off day thread updated
            if skipFlag:
                # Skip check/edit since skip flag is set
                skipFlag = None
                self.log.debug(
                    "Skip flag is set, off day thread was just submitted/edited and does not need to be checked."
                )
            else:
                try:
                    # Update generic data for division games and no-no/perfect game watch
                    self.collect_data(0)
                    # self.log.debug('data passed into render_template: {}'.format(self.commonData))#debug
                    text = self.render_template(
                        thread="off",
                        templateType="thread",
                        data=self.commonData,
                        settings=self.settings,
                    )
                    self.log.debug("Rendered off day thread text: {}".format(text))
                    if (
                        text != self.activeGames["off"]["offDayThreadText"]
                        and text != ""
                    ):
                        self.activeGames["off"].update({"offDayThreadText": text})
                        text += (
                            """

Last Updated: """
                            + self.convert_timezone(
                                datetime.utcnow(),
                                self.myTeam["venue"]["timeZone"]["id"],
                            ).strftime("%m/%d/%Y %I:%M:%S %p %Z")
                            + ", Update Interval: {} Minutes".format(
                                self.settings.get("Off Day Thread", {}).get(
                                    "UPDATE_INTERVAL", 5
                                )
                            )
                        )
                        text = self._truncate_post(text)
                        self.lemmy.editPost(offDayThread["post"]["id"], text)
                        self.log.info("Off day thread edits submitted.")
                        self.count_check_edit(offDayThread["post"]["id"], "NA", edit=True)
                        self.log_last_updated_date_in_db(offDayThread["post"]["id"])
                    elif text == "":
                        self.log.info(
                            "Skipping off day thread edit since thread text is blank..."
                        )
                    else:
                        self.log.info("No changes to off day thread.")
                        self.count_check_edit(offDayThread["post"]["id"], "NA", edit=False)
                except Exception as e:
                    self.log.error("Error editing off day thread: {}".format(e))
                    self.error_notification("Error editing off day thread")

            update_off_thread_until = self.settings.get("Off Day Thread", {}).get(
                "UPDATE_UNTIL", "All MLB games are final"
            )
            if update_off_thread_until not in [
                "Do not update",
                "All division games are final",
                "All MLB games are final",
            ]:
                # Unsupported value, use default
                update_off_thread_until = "All MLB games are final"

            if update_off_thread_until == "Do not update":
                # Setting says not to update
                self.log.info(
                    "Stopping off day thread update loop per UPDATE_UNTIL setting."
                )
                self.activeGames["off"].update({"STOP_FLAG": True})
                break
            elif update_off_thread_until == "All division games are final":
                if not next(
                    (
                        True
                        for x in self.commonData[0]["leagueSchedule"]
                        if x["status"]["abstractGameCode"] != "F"
                        and x["status"]["codedGameState"] not in ["C", "D", "U", "T"]
                        and self.myTeam["division"]["id"]
                        in [
                            x["teams"]["away"]["team"].get("division", {}).get("id"),
                            x["teams"]["home"]["team"].get("division", {}).get("id"),
                        ]
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping off day thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames["off"].update({"STOP_FLAG": True})
                    break
            elif update_off_thread_until == "All MLB games are final":
                if not next(
                    (
                        True
                        for x in self.commonData[0]["leagueSchedule"]
                        if x["status"]["abstractGameCode"] != "F"
                        and x["status"]["codedGameState"] not in ["C", "D", "U", "T"]
                    ),
                    False,
                ):
                    # MLB games are all final
                    self.log.info(
                        "All MLB games are final. Stopping off day thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames["off"].update({"STOP_FLAG": True})
                    break

            self.log.debug(
                "Off day thread stop criteria not met ({}).".format(
                    update_off_thread_until
                )
            )  # debug - need this to tell if logic is working

            # Update interval is in minutes (seconds for game thread only)
            odtWait = self.settings.get("Off Day Thread", {}).get("UPDATE_INTERVAL", 5)
            if odtWait < 1:
                odtWait = 1
            self.log.info("Sleeping for {} minutes...".format(odtWait))
            self.sleep(odtWait * 60)

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")

        # Mark off day thread as stale so it will be unstickied tomorrow
        if offDayThread:
            self.staleThreads.append(offDayThread)

        self.log.debug("Ending off day update thread...")
        return

    def gameday_thread_update_loop(self, todayGamePks):
        pk = "gameday"  # Game day thread is not specific to a gamePk
        skipFlag = None  # Will be set later if game day thread edit should be skipped

        # Check/wait for time to submit game day thread
        self.activeGames[pk].update(
            {
                "postTime_local": datetime.strptime(
                    datetime.today().strftime(
                        "%Y-%m-%d "
                        + self.settings.get("Game Day Thread", {}).get(
                            "POST_TIME", "05:00"
                        )
                    ),
                    "%Y-%m-%d %H:%M",
                )
            }
        )
        self.log.debug(
            "Game day thread post time: {}".format(
                self.activeGames[pk]["postTime_local"]
            )
        )
        while (
            datetime.today() < self.activeGames[pk]["postTime_local"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            if (
                self.activeGames[pk]["postTime_local"] - datetime.today()
            ).total_seconds() > 3600:
                self.log.info(
                    "Game day thread should not be posted for a long time ({}). Sleeping for an hour...".format(
                        self.activeGames[pk]["postTime_local"]
                    )
                )
                self.sleep(3600)
            elif (
                self.activeGames[pk]["postTime_local"] - datetime.today()
            ).total_seconds() > 1800:
                self.log.info(
                    "Game day thread post time is still more than 30 minutes away ({}). Sleeping for a half hour...".format(
                        self.activeGames[pk]["postTime_local"]
                    )
                )
                self.sleep(1800)
            else:
                self.log.info(
                    "Game day thread post time is approaching ({}). Sleeping until then...".format(
                        self.activeGames[pk]["postTime_local"]
                    )
                )
                self.sleep(
                    (
                        self.activeGames[pk]["postTime_local"] - datetime.today()
                    ).total_seconds()
                )

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        # Unsticky stale threads
        # if self.settings.get("Reddit", {}).get("STICKY", False):
        #     """
        #     # Make sure the subreddit's sticky posts are marked as stale
        #     try:
        #         sticky1 = self.subreddit.sticky(1)
        #         if sticky1.author == self.reddit.user.me() and sticky1 not in self.staleThreads and not next((True for v in self.activeGames.values() if sticky1 in [v.get('gameThread'), v.get('postGameThread')]), None):
        #             self.log.debug('Marking {} as stale (top sticky slot).'.format(sticky1.id))
        #             self.staleThreads.append(sticky1)

        #         sticky2 = self.subreddit.sticky(2)
        #         if sticky2.author == self.reddit.user.me() and sticky2 not in self.staleThreads and not next((True for v in self.activeGames.values() if sticky2 in [v.get('gameThread'), v.get('postGameThread')]), None):
        #             self.log.debug('Marking {} as stale (bottom sticky slot).'.format(sticky2.id))
        #             self.staleThreads.append(sticky2)
        #     except Exception:
        #         # Exception likely due to no post being stickied (or only one), so ignore it...
        #         pass
        #     """

        #     if len(self.staleThreads):
        #         self.unsticky_threads(self.staleThreads)
        #         self.staleThreads = []

        # Check if game day thread already posted (record in threads table with gamePk and type='gameday' for any of today's gamePks)
        gdq = "select * from {}threads where type='gameday' and gamePk in ({}) and gameDate = '{}' and deleted=0;".format(
            self.dbTablePrefix,
            ",".join(str(i) for i in todayGamePks),
            self.today["Y-m-d"],
        )
        gdThread = rbdb.db_qry(gdq, closeAfter=True, logg=self.log)

        gameDayThread = None
        if len(gdThread) > 0:
            self.log.info(
                "Game Day Thread found in database [{}].".format(gdThread[0]["id"])
            )
            gameDayThread = self.lemmy.getPost(gdThread[0]["id"])
            if not gameDayThread["creator"]["name"]:
                self.log.warning("Game day thread appears to have been deleted.")
                q = "update {}threads set deleted=1 where id='{}';".format(
                    self.dbTablePrefix, gameDayThread["post"]["id"]
                )
                u = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
                if isinstance(u, str):
                    self.log.error(
                        "Error marking thread as deleted in database: {}".format(u)
                    )

                gameDayThread = None
            else:
                if gameDayThread["post"]["body"].find("\n\nLast Updated") != -1:
                    gameDayThreadText = gameDayThread["post"]["body"][
                        0 : gameDayThread["post"]["body"].find("\n\nLast Updated:")
                    ]
                elif gameDayThread["post"]["body"].find("\n\nPosted") != -1:
                    gameDayThreadText = gameDayThread["post"]["body"][
                        0 : gameDayThread["post"]["body"].find("\n\nPosted:")
                    ]
                else:
                    gameDayThreadText = gameDayThread["post"]["body"]

                self.activeGames[pk].update(
                    {
                        "gameDayThreadText": gameDayThreadText,
                        "gameDayThread": gameDayThread,
                        "gameDayThreadTitle": gameDayThread["post"]["name"]
                        if gameDayThread not in [None, False]
                        else None,
                    }
                )
                # Only sticky when posting the thread
                if self.settings.get('Reddit',{}).get('STICKY',False): self.sticky_thread(gameDayThread)

        # Check if post game thread is already posted, and skip game day thread if so
        if (
            sum(
                1
                for k, v in self.activeGames.items()
                if k not in [0, "weekly", "off", "gameday"] and v.get("postGameThread")
            )
            == len(self.activeGames) - 1
        ):
            # Post game thread is already posted for all games
            self.log.info(
                "Post game thread is already submitted for all games, but game day thread is not. Skipping game day thread..."
            )
            skipFlag = True
            self.activeGames[pk].update({"STOP_FLAG": True})
        else:
            # Check DB (record in pkThreads with gamePk and type='post' and gameDate=today)
            pgq = "select * from {}threads where type='post' and gamePk in ({}) and gameDate = '{}' and deleted=0;".format(
                self.dbTablePrefix,
                ",".join(
                    [
                        str(x)
                        for x in self.activeGames.keys()
                        if isinstance(x, int) and x > 0 and x != pk
                    ]
                ),
                self.today["Y-m-d"],
            )
            pgThread = rbdb.db_qry(pgq, closeAfter=True, logg=self.log)

            if len(pgThread) == len(self.activeGames) - 1:
                self.log.info(
                    "Post Game Thread found in database for all games, but game day thread not posted yet. Skipping game day thread.."
                )
                skipFlag = True
                self.activeGames[pk].update({"STOP_FLAG": True})

        if not gameDayThread and not skipFlag:
            # Submit game day thread
            (gameDayThread, gameDayThreadText) = self.prep_and_post(
                "gameday",
                todayGamePks,
                postFooter="""

Posted: """
                + self.convert_timezone(
                    datetime.utcnow(), self.myTeam["venue"]["timeZone"]["id"]
                ).strftime("%m/%d/%Y %I:%M:%S %p %Z")
                + ", Update Interval: {} Minutes".format(
                    self.settings.get("Game Day Thread", {}).get("UPDATE_INTERVAL", 5)
                ),
            )
            self.activeGames[pk].update(
                {
                    "gameDayThreadText": gameDayThreadText,
                    "gameDayThread": gameDayThread,
                    "gameDayThreadTitle": gameDayThread["post"]["name"]
                    if gameDayThread not in [None, False]
                    else None,
                }
            )
            skipFlag = True

        if gameDayThread:
            self.activeGames[pk].update({"gameDayThread": gameDayThread})
            for x in todayGamePks:
                # Associate game day thread with each of today's gamePks
                self.activeGames[x].update({"gameDayThread": gameDayThread})
                self.log.debug("Associated game day thread with gamePk {}".format(x))

        while (
            not self.activeGames[pk]["STOP_FLAG"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            # Keep game day thread updated
            if skipFlag:
                # Skip check/edit since skip flag is set
                skipFlag = None
                self.log.debug(
                    "Skip flag is set, game day thread was just submitted/edited and does not need to be checked."
                )
            else:
                try:
                    # Update data for this game
                    self.collect_data(todayGamePks)
                    # Update generic data for division games and no-no/perfect game watch
                    self.collect_data(0)
                    # self.log.debug('data passed into render_template: {}'.format(self.commonData))#debug
                    text = self.render_template(
                        thread="gameday",
                        templateType="thread",
                        data=self.commonData,
                        settings=self.settings,
                    )
                    self.log.debug("Rendered game day thread text: {}".format(text))
                    if (
                        text != self.activeGames[pk].get("gameDayThreadText")
                        and text != ""
                    ):
                        self.activeGames[pk].update({"gameDayThreadText": text})
                        text += (
                            """

Last Updated: """
                            + self.convert_timezone(
                                datetime.utcnow(),
                                self.myTeam["venue"]["timeZone"]["id"],
                            ).strftime("%m/%d/%Y %I:%M:%S %p %Z")
                            + ", Update Interval: {} Minutes".format(
                                self.settings.get("Game Day Thread", {}).get(
                                    "UPDATE_INTERVAL", 5
                                )
                            )
                        )
                        text = self._truncate_post(text)
                        self.lemmy.editPost(
                            self.activeGames[pk]["gameDayThread"]["post"]["id"],
                            body=text,
                        )
                        self.log.info("Game day thread edits submitted.")
                        self.count_check_edit(
                            self.activeGames[pk]["gameDayThread"]["post"]["id"],
                            "NA",
                            edit=True,
                        )
                        self.log_last_updated_date_in_db(
                            self.activeGames[pk]["gameDayThread"]["post"]["id"]
                        )
                    elif text == "":
                        self.log.info(
                            "Skipping game day thread edit since thread text is blank..."
                        )
                    else:
                        self.log.info("No changes to game day thread.")
                        self.count_check_edit(
                            self.activeGames[pk]["gameDayThread"]["post"]["id"],
                            "NA",
                            edit=False,
                        )
                except Exception as e:
                    self.log.error("Error editing game day thread: {}".format(e))
                    self.error_notification("Error editing game day thread")

            update_gameday_thread_until = self.settings.get("Game Day Thread", {}).get(
                "UPDATE_UNTIL", "Game thread is posted"
            )
            if update_gameday_thread_until not in [
                "Do not update",
                "Game thread is posted",
                "My team's games are final",
                "All division games are final",
                "All MLB games are final",
            ]:
                # Unsupported value, use default
                update_gameday_thread_until = "Game thread is posted"

            if not self.settings.get("Game Day Thread", {}).get("ENABLED", True):
                # Game day thread is already posted, but disabled. Don't update it.
                self.log.info(
                    "Stopping game day thread update loop because game day thread is disabled."
                )
                self.activeGames[pk].update({"STOP_FLAG": True})
                break
            elif update_gameday_thread_until == "Do not update":
                # Setting says not to update
                self.log.info(
                    "Stopping game day thread update loop per UPDATE_UNTIL setting."
                )
                self.activeGames[pk].update({"STOP_FLAG": True})
                break
            elif update_gameday_thread_until == "Game thread is posted":
                if next(
                    (
                        True
                        for k, v in self.activeGames.items()
                        if v.get("gameThread") or v.get("postGameThread")
                    ),
                    False,
                ) or next(
                    (
                        True
                        for k, v in self.commonData.items()
                        if k != 0
                        and (
                            v["schedule"]["status"]["abstractGameCode"] == "F"
                            or v["schedule"]["status"]["codedGameState"]
                            in ["C", "D", "U", "T"]
                        )
                    ),
                    False,
                ):
                    # Game thread is posted
                    self.log.info(
                        "At least one game thread is posted (or post game thread is posted, or game is final). Stopping game day thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"STOP_FLAG": True})
                    break
            elif update_gameday_thread_until == "My team's games are final":
                if not next(
                    (
                        True
                        for k, v in self.commonData.items()
                        if k != 0
                        and v["schedule"]["status"]["abstractGameCode"] != "F"
                        and v["schedule"]["status"]["codedGameState"]
                        not in ["C", "D", "U", "T"]
                    ),
                    False,
                ):
                    # My team's games are all final
                    self.log.info(
                        "My team's games are all final. Stopping game day thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"STOP_FLAG": True})
                    break
            elif update_gameday_thread_until == "All division games are final":
                if not next(
                    (
                        True
                        for x in self.commonData[0]["leagueSchedule"]
                        if x["status"]["abstractGameCode"] != "F"
                        and x["status"]["codedGameState"] not in ["C", "D", "U", "T"]
                        and self.myTeam["division"]["id"]
                        in [
                            x["teams"]["away"]["team"].get("division", {}).get("id"),
                            x["teams"]["home"]["team"].get("division", {}).get("id"),
                        ]
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping game day thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"STOP_FLAG": True})
                    break
            elif update_gameday_thread_until == "All MLB games are final":
                if not next(
                    (
                        True
                        for x in self.commonData[0]["leagueSchedule"]
                        if x["status"]["abstractGameCode"] != "F"
                        and x["status"]["codedGameState"] not in ["C", "D", "U", "T"]
                    ),
                    False,
                ):
                    # MLB games are all final
                    self.log.info(
                        "All MLB games are final. Stopping game day thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"STOP_FLAG": True})
                    break

            self.log.debug(
                "Game day thread stop criteria not met ({}).".format(
                    update_gameday_thread_until
                )
            )  # debug - need this to tell if logic is working

            # Update interval is in minutes (seconds for game thread only)
            gdtWait = self.settings.get("Game Day Thread", {}).get("UPDATE_INTERVAL", 5)
            if gdtWait < 1:
                gdtWait = 1
            self.log.info("Sleeping for {} minutes...".format(gdtWait))
            self.sleep(gdtWait * 60)

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        # Mark game day thread as stale
        if self.activeGames[pk].get("gameDayThread"):
            self.staleThreads.append(self.activeGames[pk]["gameDayThread"])

        self.log.debug("Ending gameday update thread...")
        return

    def game_thread_update_loop(self, pk):
        skipFlag = (
            None  # Will be set later if game thread submit/edit should be skipped
        )

        # Check if game thread is already posted
        gq = "select * from {}threads where type='game' and gamePk = {} and gameDate = '{}' and deleted=0;".format(
            self.dbTablePrefix, pk, self.today["Y-m-d"]
        )
        gThread = rbdb.db_qry(gq, closeAfter=True, logg=self.log)

        gameThread = None
        if len(gThread) > 0:
            self.log.info(
                "Game {} Thread found in database [{}]".format(pk, gThread[0]["id"])
            )
            gameThread = self.lemmy.getPost(gThread[0]["id"])
            if not gameThread["creator"]["name"]:
                self.log.warning("Game thread appears to have been deleted.")
                q = "update {}threads set deleted=1 where id='{}';".format(
                    self.dbTablePrefix, gameThread["post"]["id"]
                )
                u = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
                if isinstance(u, str):
                    self.log.error(
                        "Error marking thread as deleted in database: {}".format(u)
                    )

                gameThread = None
            else:
                if gameThread["post"]["body"].find("\n\nLast Updated") != -1:
                    gameThreadText = gameThread["post"]["body"][
                        0 : gameThread["post"]["body"].find("\n\nLast Updated:")
                    ]
                elif gameThread["post"]["body"].find("\n\nPosted") != -1:
                    gameThreadText = gameThread["post"]["body"][
                        0 : gameThread["post"]["body"].find("\n\nPosted:")
                    ]
                else:
                    gameThreadText = gameThread["post"]["body"]

                self.activeGames[pk].update(
                    {
                        "gameThread": gameThread,
                        "gameThreadText": gameThreadText,
                        "gameThreadTitle": gameThread["post"]["name"]
                        if gameThread not in [None, False]
                        else None,
                    }
                )
                # Only sticky when posting the thread
                # if self.settings.get('Reddit',{}).get('STICKY',False): self.sticky_thread(self.activeGames[pk]['gameThread'])

        if not gameThread:
            # Check if post game thread is already posted, and skip game thread if so
            if self.activeGames[pk].get("postGameThread"):
                # Post game thread is already known
                self.log.info(
                    "Post game thread is already submitted, but game thread is not. Skipping game thread..."
                )
                skipFlag = True
                self.activeGames[pk].update({"STOP_FLAG": True})
            else:
                # Check DB (record in pkThreads with gamePk and type='post' and gameDate=today)
                pgq = "select * from {}threads where type='post' and gamePk = {} and gameDate = '{}' and deleted=0;".format(
                    self.dbTablePrefix, pk, self.today["Y-m-d"]
                )
                pgThread = rbdb.db_qry(pgq, closeAfter=True, logg=self.log)

                if len(pgThread) > 0:
                    self.log.info(
                        "Post Game Thread found in database, but game thread not posted yet. Skipping game thread.."
                    )
                    skipFlag = True
                    self.activeGames[pk].update({"STOP_FLAG": True})

        if not gameThread and not skipFlag:
            # Determine time to post
            gameStart = self.commonData[pk]["gameTime"]["bot"]
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
            self.activeGames[pk].update(
                {
                    "postTime": min(gameStart, postBy, minBefore_time),
                    "postTime_local": min(gameStart, postBy, minBefore_time).replace(
                        tzinfo=None
                    ),
                }
            )
            self.log.debug(
                "Game {} thread post time: {} (min of Game Start: {}, Post By: {}, Min Before: {})".format(
                    pk,
                    self.activeGames[pk]["postTime"],
                    gameStart,
                    postBy,
                    minBefore_time,
                )
            )

            if (
                self.commonData[pk]["schedule"]["doubleHeader"] != "N"
                and self.commonData[pk]["schedule"]["gameNumber"] == 2
            ):
                otherGame = next(
                    (
                        v
                        for k, v in self.commonData.items()
                        if k not in [0, pk]
                        and v.get("schedule", {}).get("doubleHeader") in ["Y", "S"]
                        and v.get("schedule", {}).get("gameNumber") == 1
                    ),
                    None,
                )
                if otherGame:
                    self.log.debug(
                        "Other Game ({}) abstractGameCode: {} - codedGameState: {}".format(
                            otherGame["schedule"]["gamePk"],
                            otherGame["schedule"]["status"]["abstractGameCode"],
                            otherGame["schedule"]["status"]["codedGameState"],
                        )
                    )
                else:
                    self.log.warning("Other Game in doubleheader pair not found.")

            # Check/wait for time to submit game thread
            while (
                datetime.today() < self.activeGames[pk]["postTime_local"]
                and redball.SIGNAL is None
                and not self.bot.STOP
                and not self.activeGames[pk].get("gameThread")
            ) or (
                self.commonData[pk]["schedule"]["doubleHeader"] != "N"
                and self.commonData[pk]["schedule"]["gameNumber"] == 2
            ):
                # Refresh game status
                with GAME_DATA_LOCK:
                    self.get_gameStatus(pk, self.today["Y-m-d"])

                if self.commonData[pk]["schedule"]["status"][
                    "abstractGameCode"
                ] == "F" or self.commonData[pk]["schedule"]["status"][
                    "codedGameState"
                ] in [
                    "C",
                    "D",
                    "U",
                    "T",
                ]:
                    # codedGameState - Suspended: U, T; Cancelled: C, Postponed: D
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
                            "Game {} is {}; skipping game thread...".format(
                                pk,
                                self.commonData[pk]["schedule"]["status"][
                                    "detailedState"
                                ],
                            )
                        )
                        skipFlag = True
                    break
                elif (
                    self.commonData[pk]["schedule"]["status"]["abstractGameCode"] == "L"
                ):
                    # Game is already in live status (including warmup), so submit the game thread!
                    self.log.info(
                        "It's technically not time to submit the game {} thread yet, but the game status is Live. Proceeding...".format(
                            pk
                        )
                    )
                    break
                elif (
                    self.commonData[pk]["schedule"]["doubleHeader"] == "Y"
                    and self.commonData[pk]["schedule"]["gameNumber"] == 2
                    and (
                        self.commonData[otherGame["schedule"]["gamePk"]]["schedule"][
                            "status"
                        ]["abstractGameCode"]
                        == "F"
                        or self.commonData[otherGame["schedule"]["gamePk"]]["schedule"][
                            "status"
                        ]["codedGameState"]
                        in ["C", "D", "U", "T"]
                    )
                ):
                    # Straight doubleheader game 2 - post time doesn't matter, submit post after game 1 is final
                    # But wait 5 minutes and update common data to pull in new records
                    self.log.info(
                        "Waiting 5 minutes and then proceeding with game thread for straight doubleheader game 2 ({}) because doubleheader game 1 is {}.".format(
                            pk,
                            self.commonData[otherGame["schedule"]["gamePk"]][
                                "schedule"
                            ]["status"]["detailedState"],
                        )
                    )
                    self.sleep(300)
                    self.log.info(
                        "Proceeding with game thread for straight doubleheader game 2 ({}) because doubleheader game 1 is {}.".format(
                            pk,
                            self.commonData[otherGame["schedule"]["gamePk"]][
                                "schedule"
                            ]["status"]["detailedState"],
                        )
                    )
                    break
                elif (
                    datetime.today() > self.activeGames[pk]["postTime_local"]
                    and self.commonData[pk]["schedule"]["doubleHeader"] == "S"
                    and self.commonData[pk]["schedule"]["gameNumber"] == 2
                    and (
                        self.commonData[otherGame["schedule"]["gamePk"]]["schedule"][
                            "status"
                        ]["abstractGameCode"]
                        == "F"
                        or self.commonData[otherGame["schedule"]["gamePk"]]["schedule"][
                            "status"
                        ]["codedGameState"]
                        in ["C", "D", "U", "T"]
                    )
                ):
                    # Split doubleheader game 2 - honor post time, but only after game 1 is final
                    self.log.info(
                        "Proceeding with game thread for split doubleheader game 2 ({}) because doubleheader game 1 is {} and post time is reached.".format(
                            pk,
                            self.commonData[otherGame["schedule"]["gamePk"]][
                                "schedule"
                            ]["status"]["detailedState"],
                        )
                    )
                    break
                elif not self.settings.get("Game Thread", {}).get("ENABLED", True):
                    # Game thread is disabled
                    self.log.info("Game thread is disabled.")
                    skipFlag = True
                    break

                if (
                    self.activeGames[pk]["postTime_local"] - datetime.today()
                ).total_seconds() >= 600:
                    self.log.info(
                        "Waiting for time to submit game {} thread: {}{}. Sleeping for 10 minutes...".format(
                            pk,
                            self.activeGames[pk]["postTime"],
                            " (will hold past post time until doubleheader game 1 ({}) is final)".format(
                                otherGame["schedule"]["gamePk"]
                            )
                            if self.commonData[pk]["schedule"]["doubleHeader"] != "N"
                            and self.commonData[pk]["schedule"]["gameNumber"] != 1
                            else "",
                        )
                    )
                    self.sleep(600)
                elif (
                    (
                        self.activeGames[pk]["postTime_local"] - datetime.today()
                    ).total_seconds()
                    < 0
                    and self.commonData[pk]["schedule"]["doubleHeader"] != "N"
                    and self.commonData[pk]["schedule"]["gameNumber"] != 1
                ):
                    self.log.info(
                        "Game {} thread post time has passed, but holding until doubleheader game 1 ({}) is final (currently {}). Sleeping for 5 minutes....".format(
                            pk,
                            otherGame["schedule"]["gamePk"],
                            self.commonData[otherGame["schedule"]["gamePk"]][
                                "schedule"
                            ]["status"]["detailedState"],
                        )
                    )
                    self.sleep(300)
                else:
                    self.log.info(
                        "Game {} thread should be posted soon, sleeping until then ({})...".format(
                            pk, self.activeGames[pk]["postTime"]
                        )
                    )
                    self.sleep(
                        (
                            self.activeGames[pk]["postTime_local"] - datetime.today()
                        ).total_seconds()
                    )

            if redball.SIGNAL is not None or self.bot.STOP:
                self.log.debug("Caught a stop signal...")
                return

            # Unsticky stale threads
            if self.settings.get("Reddit", {}).get("STICKY", False):
                # Make sure game day thread is marked as stale, since we want the game thread to be sticky instead
                if (
                    self.activeGames.get("gameday", {}).get("gameDayThread")
                    and self.activeGames["gameday"]["gameDayThread"]
                    not in self.staleThreads
                ):
                    self.staleThreads.append(
                        self.activeGames["gameday"]["gameDayThread"]
                    )

                if len(self.staleThreads):
                    self.unsticky_threads(self.staleThreads)
                    self.staleThreads = []

            if skipFlag or not self.settings.get("Game Thread", {}).get(
                "ENABLED", True
            ):
                # Skip game thread since skip flag is set or game thread is disabled
                if self.settings.get("Game Thread", {}).get("ENABLED", True):
                    self.log.info("Skipping game {} thread...".format(pk))
                else:
                    self.log.info(
                        "Game thread is disabled, so skipping for game {}...".format(pk)
                    )
            else:
                # Submit Game Thread
                self.log.info("Preparing to post game {} thread...".format(pk))
                (gameThread, gameThreadText) = self.prep_and_post(
                    "game",
                    pk,
                    postFooter="""

Posted: """
                    + self.convert_timezone(
                        datetime.utcnow(), self.myTeam["venue"]["timeZone"]["id"]
                    ).strftime("%m/%d/%Y %I:%M:%S %p %Z"),
                )
                self.activeGames[pk].update(
                    {
                        "gameThread": gameThread,
                        "gameThreadText": gameThreadText,
                        "gameThreadTitle": gameThread["post"]["name"]
                        if gameThread not in [None, False]
                        else None,
                    }
                )
            # Thread is not posted, so don't start an update loop
            if not self.activeGames[pk].get("gameThread") and self.settings.get(
                "Game Thread", {}
            ).get("ENABLED", True):
                # Game thread is enabled but failed to post
                self.log.info("Game thread not posted. Ending update loop...")
                self.activeGames[pk].update({"STOP_FLAG": True})
                return  # TODO: Determine why thread is not posted and retry if temporary issue

            skipFlag = True  # Skip first edit since the thread was just posted

        if (
            self.settings.get("Comments", {}).get("ENABLED", True)
            and self.activeGames[pk].get("gameThread")
            and not (
                self.commonData[pk]["schedule"]["status"]["abstractGameCode"] == "F"
                or self.commonData[pk]["schedule"]["status"]["codedGameState"]
                in ["C", "D", "U", "T"]
            )
        ):
            if self.THREADS[pk].get("COMMENT_THREAD") and isinstance(
                self.THREADS[pk]["COMMENT_THREAD"], threading.Thread
            ):
                # Thread is already running...
                pass
            else:
                # Spawn separate thread to submit notable play comments in game thread
                self.THREADS[pk].update(
                    {
                        "COMMENT_THREAD": threading.Thread(
                            target=self.monitor_game_plays,
                            args=(pk, self.activeGames[pk]["gameThread"]),
                            name="bot-{}-{}-game-{}-comments".format(
                                self.bot.id, self.bot.name.replace(" ", "-"), pk
                            ),
                            daemon=True,
                        )
                    }
                )
                self.THREADS[pk]["COMMENT_THREAD"].start()
                self.log.debug(
                    "Started comment thread {}.".format(
                        self.THREADS[pk]["COMMENT_THREAD"]
                    )
                )
        else:
            if not self.activeGames[pk].get("gameThread"):
                self.log.info(
                    "Game thread is not posted (even though it should be), so not starting comment process! [pk: {}]".format(
                        pk
                    )
                )
            elif self.commonData[pk]["schedule"]["status"][
                "abstractGameCode"
            ] == "F" or self.commonData[pk]["schedule"]["status"]["codedGameState"] in [
                "C",
                "D",
                "U",
                "T",
            ]:
                self.log.info(
                    "Game is over, so not starting comment process! [pk: {}]".format(pk)
                )
            else:
                self.log.info(
                    "Commenting is disabled, so not starting comment process! [pk: {}]".format(
                        pk
                    )
                )

        while (
            not self.activeGames[pk]["STOP_FLAG"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            if skipFlag:
                # Skip edit since thread was just posted
                skipFlag = None
                self.log.debug(
                    "Skip flag is set, game {} thread does not need to be edited.".format(
                        pk
                    )
                )
            else:
                # Re-generate game thread code, compare to current code, edit if different
                # Update generic data
                self.collect_data(0)
                # Update data for this game
                self.collect_data(pk)
                text = self.render_template(
                    thread="game",
                    templateType="thread",
                    data=self.commonData,
                    gamePk=pk,
                    settings=self.settings,
                )
                self.log.debug("rendered game {} thread text: {}".format(pk, text))
                if text != self.activeGames[pk].get("gameThreadText") and text != "":
                    self.activeGames[pk].update({"gameThreadText": text})
                    # Add last updated timestamp
                    text += """

Last Updated: """ + self.convert_timezone(
                        datetime.utcnow(), self.myTeam["venue"]["timeZone"]["id"]
                    ).strftime(
                        "%m/%d/%Y %I:%M:%S %p %Z"
                    )
                    text = self._truncate_post(text)
                    self.lemmy.editPost(
                        self.activeGames[pk]["gameThread"]["post"]["id"], body=text
                    )
                    self.log.info("Edits submitted for {} game thread.".format(pk))
                    self.count_check_edit(
                        self.activeGames[pk]["gameThread"]["post"]["id"],
                        self.commonData[pk]["schedule"]["status"]["statusCode"],
                        edit=True,
                    )
                    self.log_last_updated_date_in_db(
                        self.activeGames[pk]["gameThread"]["post"]["id"]
                    )
                elif text == "":
                    self.log.info(
                        "Skipping game thread {} edit since thread text is blank...".format(
                            pk
                        )
                    )
                else:
                    self.log.info("No changes to {} game thread.".format(pk))
                    self.count_check_edit(
                        self.activeGames[pk]["gameThread"]["post"]["id"],
                        self.commonData[pk]["schedule"]["status"]["statusCode"],
                        edit=False,
                    )

            update_game_thread_until = self.settings.get("Game Thread", {}).get(
                "UPDATE_UNTIL", ""
            )
            if update_game_thread_until not in [
                "Do not update",
                "My team's games are final",
                "All division games are final",
                "All MLB games are final",
            ]:
                # Unsupported value, use default
                update_game_thread_until = "All MLB games are final"

            if update_game_thread_until == "Do not update":
                # Setting says not to update
                self.log.info(
                    "Stopping game thread update loop per UPDATE_UNTIL setting."
                )
                self.activeGames[pk].update({"STOP_FLAG": True})
                break
            elif update_game_thread_until == "My team's games are final":
                if not next(
                    (
                        True
                        for x in self.activeGames.keys()
                        if isinstance(x, int)
                        and x > 0
                        and self.commonData[x]["schedule"]["status"]["abstractGameCode"]
                        != "F"
                        and self.commonData[x]["schedule"]["status"]["codedGameState"]
                        not in ["C", "D", "U", "T"]
                    ),
                    False,
                ):
                    # My team's games are all final
                    self.log.info(
                        "My team's games are all final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"STOP_FLAG": True})
                    break
            elif update_game_thread_until == "All division games are final":
                if (  # This game is final
                    self.commonData[pk]["schedule"]["status"]["abstractGameCode"] == "F"
                    or self.commonData[pk]["schedule"]["status"]["codedGameState"]
                    in [
                        "C",
                        "D",
                        "U",
                        "T",
                    ]  # Suspended: U, T; Cancelled: C, Postponed: D
                ) and not next(  # And all division games are final
                    (
                        True
                        for x in self.commonData[0]["leagueSchedule"]
                        if x["status"]["abstractGameCode"] != "F"
                        and x["status"]["codedGameState"] not in ["C", "D", "U", "T"]
                        and self.myTeam["division"]["id"]
                        in [
                            x["teams"]["away"]["team"].get("division", {}).get("id"),
                            x["teams"]["home"]["team"].get("division", {}).get("id"),
                        ]
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"STOP_FLAG": True})
                    break
            elif update_game_thread_until == "All MLB games are final":
                if (  # This game is final
                    self.commonData[pk]["schedule"]["status"]["abstractGameCode"] == "F"
                    or self.commonData[pk]["schedule"]["status"]["codedGameState"]
                    in [
                        "C",
                        "D",
                        "U",
                        "T",
                    ]  # Suspended: U, T; Cancelled: C, Postponed: D
                ) and not next(  # And all MLB games are final
                    (
                        True
                        for x in self.commonData[0]["leagueSchedule"]
                        if x["status"]["abstractGameCode"] != "F"
                        and x["status"]["codedGameState"] not in ["C", "D", "U", "T"]
                    ),
                    False,
                ):
                    # MLB games are all final
                    self.log.info(
                        "All MLB games are final. Stopping game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"STOP_FLAG": True})
                    break

            self.log.debug(
                "Game thread stop criteria not met ({}).".format(
                    update_game_thread_until
                )
            )  # debug - need this to tell if logic is working

            if self.commonData[pk]["schedule"]["status"]["detailedState"].startswith(
                "Delayed"
            ) and self.commonData[pk]["schedule"]["status"]["abstractGameCode"] not in [
                "I",
                "IZ",
                "IH",
            ]:
                # I: In Progress, IZ: Delayed: About to Resume, IH: Instant Replay
                # Update interval is in minutes (seconds only when game is live)
                gtnlWait = self.settings.get("Game Thread", {}).get(
                    "UPDATE_INTERVAL_NOT_LIVE", 1
                )
                if gtnlWait < 1:
                    gtnlWait = 1
                self.log.info(
                    "Game {} is delayed (abstractGameCode: {}, codedGameState: {}), sleeping for {} minutes...".format(
                        pk,
                        self.commonData[pk]["schedule"]["status"]["abstractGameCode"],
                        self.commonData[pk]["schedule"]["status"]["codedGameState"],
                        gtnlWait,
                    )
                )
                self.sleep(gtnlWait * 60)
            elif self.commonData[pk]["schedule"]["status"]["abstractGameCode"] == "L":
                # Update interval is in seconds (minutes for all other cases)
                gtWait = self.settings.get("Game Thread", {}).get("UPDATE_INTERVAL", 10)
                if gtWait < 1:
                    gtWait = 1
                self.log.info(
                    "Game {} is live (abstractGameCode: {}, codedGameState: {}), sleeping for {} seconds...".format(
                        pk,
                        self.commonData[pk]["schedule"]["status"]["abstractGameCode"],
                        self.commonData[pk]["schedule"]["status"]["codedGameState"],
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
                    "Game {} is not live (abstractGameCode: {}, codedGameState: {}), sleeping for {} minutes...".format(
                        pk,
                        self.commonData[pk]["schedule"]["status"]["abstractGameCode"],
                        self.commonData[pk]["schedule"]["status"]["codedGameState"],
                        gtnlWait,
                    )
                )
                self.sleep(gtnlWait * 60)

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        self.log.info("All finished with game {}!".format(pk))
        self.activeGames[pk].update({"STOP_FLAG": True})

        # Mark game thread as stale
        if self.activeGames[pk].get("gameThread"):
            self.staleThreads.append(self.activeGames[pk]["gameThread"])

        self.log.debug("Ending game update thread...")
        return

    def postgame_thread_update_loop(self, pk):
        skipFlag = (
            None  # Will be set later if post game thread submit/edit should be skipped
        )

        while redball.SIGNAL is None and not self.bot.STOP:
            if not self.settings.get("Game Thread", {}).get("ENABLED", True):
                # Game thread is disabled, so ensure we have fresh data
                self.log.info(
                    f"Game thread is disabled for game {pk}, so updating data... current status: (abstractGameCode: {self.commonData[pk]['schedule']['status']['abstractGameCode']}, codedGameState: {self.commonData[pk]['schedule']['status']['codedGameState']})"
                )
                # Update generic data
                self.collect_data(0)
                # Update data for this game
                self.collect_data(pk)
            if self.commonData[pk]["schedule"]["status"][
                "abstractGameCode"
            ] == "F" or self.commonData[pk]["schedule"]["status"]["codedGameState"] in [
                "C",
                "D",
                "U",
                "T",
            ]:
                # Suspended: U, T; Cancelled: C, Postponed: D
                # Game is over
                self.log.info(
                    "Game {} is over (abstractGameCode: {}, codedGameState: {}). Proceeding with post game thread...".format(
                        pk,
                        self.commonData[pk]["schedule"]["status"]["abstractGameCode"],
                        self.commonData[pk]["schedule"]["status"]["codedGameState"],
                    )
                )
                break
            elif self.activeGames[pk]["STOP_FLAG"] and self.settings.get(
                "Game Thread", {}
            ).get("ENABLED", True):
                # Game thread process is enabled and has stopped, but game status isn't final yet... get fresh data!
                self.log.info(
                    f"Game {pk} thread process has ended, but cached game status is still (abstractGameCode: {self.commonData[pk]['schedule']['status']['abstractGameCode']}, codedGameState: {self.commonData[pk]['schedule']['status']['codedGameState']}). Refreshing data..."
                )
                # Update generic data
                self.collect_data(0)
                # Update data for this game
                self.collect_data(pk)
            else:
                self.log.debug(
                    "Game {} is not yet final (abstractGameCode: {}, codedGameState: {}). Sleeping for 1 minute...".format(
                        pk,
                        self.commonData[pk]["schedule"]["status"]["abstractGameCode"],
                        self.commonData[pk]["schedule"]["status"]["codedGameState"],
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
                self.activeGames[pk].get("gameThread")
                and self.activeGames[pk]["gameThread"] not in self.staleThreads
            ):
                self.staleThreads.append(self.activeGames[pk]["gameThread"])

            if len(self.staleThreads):
                self.unsticky_threads(self.staleThreads)
                self.staleThreads = []

        # TODO: Skip for (straight?) doubleheader game 1?
        # TODO: Loop in case thread creation fails due to title template error or API error? At least break from update loop...
        # Game is over - check if postgame thread already posted (record in pkThreads with gamePk and type='post' and gameDate=today)
        pgq = "select * from {}threads where type='post' and gamePk = {} and gameDate = '{}' and deleted=0;".format(
            self.dbTablePrefix, pk, self.today["Y-m-d"]
        )
        pgThread = rbdb.db_qry(pgq, closeAfter=True, logg=self.log)

        postGameThread = None
        if len(pgThread) > 0:
            self.log.info(
                "Post Game Thread found in database [{}].".format(pgThread[0]["id"])
            )
            postGameThread = self.lemmy.getPost(pgThread[0]["id"])
            if not postGameThread["post"]["id"]:
                self.log.warning("Post game thread appears to have been deleted.")
                q = "update {}threads set deleted=1 where id='{}';".format(
                    self.dbTablePrefix, postGameThread["post"]["id"]
                )
                u = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
                if isinstance(u, str):
                    self.log.error(
                        "Error marking thread as deleted in database: {}".format(u)
                    )

                postGameThread = None
            else:
                if postGameThread["post"]["body"].find("\n\nLast Updated") != -1:
                    postGameThreadText = postGameThread["post"]["body"][
                        0 : postGameThread["post"]["body"].find("\n\nLast Updated:")
                    ]
                elif postGameThread["post"]["body"].find("\n\nPosted") != -1:
                    postGameThreadText = postGameThread["post"]["body"][
                        0 : postGameThread["post"]["body"].find("\n\nPosted:")
                    ]
                else:
                    postGameThreadText = postGameThread["post"]["body"]

                self.activeGames[pk].update(
                    {
                        "postGameThread": postGameThread,
                        "postGameThreadText": postGameThreadText,
                        "postGameThreadTitle": postGameThread["post"]["name"]
                        if postGameThread not in [None, False]
                        else None,
                    }
                )
                # Only sticky when posting the thread
                if self.settings.get('Reddit',{}).get('STICKY',False): self.sticky_thread(self.activeGames[pk]['postGameThread'])

        game_result = (
            "EXCEPTION"
            if self.commonData[pk]["schedule"]["status"]["codedGameState"]
            in ["C", "D", "U", "T"]  # Suspended: U, T; Cancelled: C, Postponed: D
            else "TIE"
            if self.commonData[pk]["schedule"]["teams"]["home"]["score"]
            == self.commonData[pk]["schedule"]["teams"]["away"]["score"]
            else "WIN"
            if (
                (
                    self.commonData[pk]["schedule"]["teams"]["home"]["score"]
                    > self.commonData[pk]["schedule"]["teams"]["away"]["score"]
                    and self.commonData[pk]["homeAway"] == "home"
                )
                or (
                    self.commonData[pk]["schedule"]["teams"]["home"]["score"]
                    < self.commonData[pk]["schedule"]["teams"]["away"]["score"]
                    and self.commonData[pk]["homeAway"] == "away"
                )
            )
            else "LOSS"
            if (
                (
                    self.commonData[pk]["schedule"]["teams"]["home"]["score"]
                    < self.commonData[pk]["schedule"]["teams"]["away"]["score"]
                    and self.commonData[pk]["homeAway"] == "home"
                )
                or (
                    self.commonData[pk]["schedule"]["teams"]["home"]["score"]
                    > self.commonData[pk]["schedule"]["teams"]["away"]["score"]
                    and self.commonData[pk]["homeAway"] == "away"
                )
            )
            else "EXCEPTION"
        )
        wanted_results = self.settings.get("Post Game Thread", {}).get(
            "ONLY_IF_THESE_RESULTS", ["ALL"]
        )
        if "ALL" not in wanted_results and game_result not in wanted_results:
            self.log.info(
                f"Game result: [{game_result}] is not in the list of wanted results (Post Game Thread > ONLY_IF_THESE_RESULTS): {wanted_results}, skipping post game thread..."
            )
            self.activeGames[pk].update({"POST_STOP_FLAG": True})
        elif not postGameThread:
            # Submit post game thread
            (postGameThread, postGameThreadText) = self.prep_and_post(
                "post",
                pk,
                postFooter="""

Posted: """
                + self.convert_timezone(
                    datetime.utcnow(), self.myTeam["venue"]["timeZone"]["id"]
                ).strftime("%m/%d/%Y %I:%M:%S %p %Z"),
            )
            self.activeGames[pk].update(
                {
                    "postGameThread": postGameThread,
                    "postGameThreadText": postGameThreadText,
                    "postGameThreadTitle": postGameThread["post"]["name"]
                    if postGameThread not in [None, False]
                    else None,
                }
            )
            if not postGameThread:
                self.log.info("Post game thread not posted. Ending update loop...")
                self.activeGames[pk].update({"POST_STOP_FLAG": True})
                return  # TODO: Determine why thread is not posted and retry for temporary issue

            skipFlag = True  # No need to edit since the thread was just posted

        while (
            not self.activeGames[pk]["POST_STOP_FLAG"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            # Keep the thread updated until stop threshold is reached
            if skipFlag:
                skipFlag = None
                self.log.debug(
                    "Skipping edit for post game {} thread per skip flag...".format(pk)
                )
            else:
                try:
                    # Update generic data
                    self.collect_data(0)
                    # Update data for this game
                    self.collect_data(pk)
                    text = self.render_template(
                        thread="post",
                        templateType="thread",
                        data=self.commonData,
                        gamePk=pk,
                        settings=self.settings,
                    )
                    self.log.debug(
                        "Rendered post game {} thread text: {}".format(pk, text)
                    )
                    if (
                        text != self.activeGames[pk]["postGameThreadText"]
                        and text != ""
                    ):
                        self.activeGames[pk]["postGameThreadText"] = text
                        text += """

Last Updated: """ + self.convert_timezone(
                            datetime.utcnow(), self.myTeam["venue"]["timeZone"]["id"]
                        ).strftime(
                            "%m/%d/%Y %I:%M:%S %p %Z"
                        )
                        text = self._truncate_post(text)
                        self.lemmy.editPost(
                            self.activeGames[pk]["postGameThread"]["post"]["id"],
                            body=text,
                        )

                        self.log.info("Post game {} thread edits submitted.".format(pk))
                        self.log_last_updated_date_in_db(
                            self.activeGames[pk]["postGameThread"]["post"]["id"]
                        )
                        self.count_check_edit(
                            self.activeGames[pk]["postGameThread"]["post"]["id"],
                            self.commonData[pk]["schedule"]["status"]["statusCode"],
                            edit=True,
                        )
                    elif text == "":
                        self.log.info(
                            "Skipping post game {} thread edit since thread text is blank...".format(
                                pk
                            )
                        )
                    else:
                        self.log.info("No changes to post game thread.")
                        self.count_check_edit(
                            self.activeGames[pk]["postGameThread"]["post"]["id"],
                            self.commonData[pk]["schedule"]["status"]["statusCode"],
                            edit=False,
                        )
                except Exception as e:
                    self.log.error(
                        "Error editing post game {} thread: {}".format(pk, e)
                    )
                    self.error_notification(f"Error editing {pk} post game thread")

            update_postgame_thread_until = self.settings.get(
                "Post Game Thread", {}
            ).get("UPDATE_UNTIL", "An hour after thread is posted")
            if update_postgame_thread_until not in [
                "Do not update",
                "An hour after thread is posted",
                "All division games are final",
                "All MLB games are final",
            ]:
                # Unsupported value, use default
                update_postgame_thread_until = "An hour after thread is posted"

            if update_postgame_thread_until == "Do not update":
                # Setting says not to update
                self.log.info(
                    "Stopping post game thread update loop per UPDATE_UNTIL setting."
                )
                self.activeGames[pk].update({"POST_STOP_FLAG": True})
                break
            elif update_postgame_thread_until == "An hour after thread is posted":
                if (
                        datetime.utcnow() - datetime.strptime(self.activeGames[pk]["postGameThread"]["post"]["published"],
                                                           '%Y-%m-%dT%H:%M:%S.%f')
                        >= timedelta(hours=1)
                ):
                    # Post game thread was posted more than an hour ago
                    self.log.info(
                        "Post game thread was posted an hour ago. Stopping post game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"POST_STOP_FLAG": True})
                    break
            elif update_postgame_thread_until == "All division games are final":
                if not next(
                    (
                        True
                        for x in self.commonData[0]["leagueSchedule"]
                        if x["status"]["abstractGameCode"] != "F"
                        and x["status"]["codedGameState"] not in ["C", "D", "U", "T"]
                        and self.myTeam["division"]["id"]
                        in [
                            x["teams"]["away"]["team"].get("division", {}).get("id"),
                            x["teams"]["home"]["team"].get("division", {}).get("id"),
                        ]
                    ),
                    False,
                ):
                    # Division games are all final
                    self.log.info(
                        "All division games are final. Stopping post game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"POST_STOP_FLAG": True})
                    break
            elif update_postgame_thread_until == "All MLB games are final":
                if not next(
                    (
                        True
                        for x in self.commonData[0]["leagueSchedule"]
                        if x["status"]["abstractGameCode"] != "F"
                        and x["status"]["codedGameState"] not in ["C", "D", "U", "T"]
                    ),
                    False,
                ):
                    # MLB games are all final
                    self.log.info(
                        "All MLB games are final. Stopping post game thread update loop per UPDATE_UNTIL setting."
                    )
                    self.activeGames[pk].update({"POST_STOP_FLAG": True})
                    break

            # Update interval is in minutes (seconds for game thread only)
            pgtWait = self.settings.get("Post Game Thread", {}).get(
                "UPDATE_INTERVAL", 5
            )
            if pgtWait < 1:
                pgtWait = 1
            self.log.info(
                "Post game {} thread update threshold ({}) not yet reached. Sleeping for {} minute(s)...".format(
                    pk, update_postgame_thread_until, pgtWait
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

    def monitor_game_plays(self, pk, gameThread):
        # Check if gumbo data exists for pk
        if not self.commonData.get(pk, {}).get("gumbo"):
            self.collect_data(gamePk=pk)

        if gameThread:
            gameThreadId = gameThread["post"]["id"]
        else:
            self.log.error("No game thread provided!")
            return

        myTeamBattingEvents = self.settings.get("Comments", {}).get(
            "MYTEAM_BATTING_EVENTS", []
        )
        self.log.debug(f"Monitored myTeamBattingEvents: [{myTeamBattingEvents}]")
        myTeamPitchingEvents = self.settings.get("Comments", {}).get(
            "MYTEAM_PITCHING_EVENTS", []
        )
        self.log.debug(f"Monitored myTeamPitchingEvents: [{myTeamPitchingEvents}]")
        processedAtBatRecord = self.get_processedAtBats_from_db(pk, gameThreadId)
        if not processedAtBatRecord:
            self.log.error(
                "Error retrieving processed at bat info from database. Unable to determine which at bats have already been processed. Starting at the beginning..."
            )
            processedAtBats = {}
        else:
            processedAtBats = processedAtBatRecord.get("processedAtBats", {})
            self.log.debug(
                "Loaded processedAtBats from db: {}. Full record: {}".format(
                    processedAtBats, processedAtBatRecord
                )
            )

        while (
            not self.activeGames[pk]["STOP_FLAG"]
            and redball.SIGNAL is None
            and not self.bot.STOP
        ):
            # Loop through plays that haven't yet been fully processed
            for atBat in (
                a
                for a in self.commonData[pk]["gumbo"]["liveData"]["plays"]["allPlays"]
                if a.get("atBatIndex")
                and a["atBatIndex"]
                >= max([int(k) for k in processedAtBats.keys()], default=0)
            ):
                if redball.SIGNAL is not None or self.bot.STOP:
                    self.log.debug("Breaking loop due to stop signal...")
                    break

                myTeamBatting = (
                    True
                    if (
                        atBat["about"]["isTopInning"]
                        and self.commonData.get(pk, {}).get("homeAway", "") == "away"
                    )
                    or (
                        not atBat["about"]["isTopInning"]
                        and self.commonData.get(pk, {}).get("homeAway", "") == "home"
                    )
                    else False
                )
                if not processedAtBats.get(str(atBat["atBatIndex"])):
                    # Add at bat to the tracking dict - c: isComplete, a: actionIndex (abbreviated to save DB space)
                    processedAtBats.update(
                        {str(atBat["atBatIndex"]): {"c": False, "a": []}}
                    )
                    self.log.debug(
                        f"Processing atBatIndex [{atBat['atBatIndex']}] - first time seeing this atBatIndex - actionIndex: {atBat['actionIndex']}"
                    )
                elif processedAtBats[str(atBat["atBatIndex"])]["c"]:
                    # Already finished processing this at bat
                    self.log.debug(
                        "Already processed atBatIndex {}.".format(atBat["atBatIndex"])
                    )
                    continue
                else:
                    # Processed this at bat but it wasn't complete yet
                    self.log.debug(
                        f"Processing atBatIndex [{atBat['atBatIndex']}] - prior processing state: {processedAtBats.get(str(atBat['atBatIndex']),'not found')} - actionIndex: {atBat['actionIndex']}"
                    )

                for actionIndex in (
                    x
                    for x in atBat["actionIndex"]
                    if x not in processedAtBats[str(atBat["atBatIndex"])]["a"]
                ):
                    if redball.SIGNAL is not None or self.bot.STOP:
                        self.log.debug("Breaking loop due to stop signal...")
                        break
                    # Process action
                    self.log.debug(
                        "Processing actionIndex {} for atBatIndex {}: [{}] (myTeamBatting: {}).".format(
                            actionIndex,
                            atBat["atBatIndex"],
                            atBat["playEvents"][actionIndex],
                            myTeamBatting,
                        )
                    )
                    if (
                        (
                            atBat["playEvents"][actionIndex]["details"].get(
                                "eventType",
                                atBat["playEvents"][actionIndex]["details"]
                                .get("event", "")
                                .lower()
                                .replace(" ", "_"),
                            )
                            in myTeamBattingEvents
                            and myTeamBatting
                        )
                        or (
                            atBat["playEvents"][actionIndex]["details"].get(
                                "eventType",
                                atBat["playEvents"][actionIndex]["details"]
                                .get("event", "")
                                .lower()
                                .replace(" ", "_"),
                            )
                            in myTeamPitchingEvents
                            and not myTeamBatting
                        )
                        or (
                            "scoring_play" in myTeamBattingEvents
                            and atBat["playEvents"][actionIndex]["details"].get(
                                "isScoringPlay"
                            )
                            and myTeamBatting
                        )
                        or (
                            "scoring_play" in myTeamPitchingEvents
                            and atBat["playEvents"][actionIndex]["details"].get(
                                "isScoringPlay"
                            )
                            and not myTeamBatting
                        )
                    ):
                        # Event type is wanted
                        self.log.debug(
                            "Detected {}{} event (myTeamBatting: {}).".format(
                                atBat["playEvents"][actionIndex]["details"].get(
                                    "eventType",
                                    atBat["playEvents"][actionIndex]["details"]
                                    .get("event", "")
                                    .lower()
                                    .replace(" ", "_"),
                                ),
                                "/scoring_play"
                                if atBat["playEvents"][actionIndex]["details"].get(
                                    "isScoringPlay"
                                )
                                else "",
                                myTeamBatting,
                            )
                        )
                        text = self.render_template(
                            thread="comment",
                            templateType="body",
                            data=self.commonData,
                            gamePk=pk,
                            settings=self.settings,
                            actionOrResult="action",
                            myTeamBatting=myTeamBatting,
                            atBat=atBat,
                            actionIndex=actionIndex,
                            eventType=atBat["playEvents"][actionIndex]["details"].get(
                                "eventType",
                                atBat["playEvents"][actionIndex]["details"]
                                .get("event", "")
                                .lower()
                                .replace(" ", "_"),
                            ),
                        )
                        self.log.debug("Rendered comment text: {}".format(text))
                        if text != "":
                            try:
                                commentObj = self.lemmy.submitComment(
                                    gameThreadId, text, language_id=37
                                )
                                self.log.info(
                                    "Submitted comment to game thread {} for actionIndex {} for atBatIndex {}: {}".format(
                                        gameThreadId,
                                        actionIndex,
                                        atBat["atBatIndex"],
                                        text,
                                    )
                                )
                                self.insert_comment_to_db(
                                    pk=pk,
                                    gameThreadId=gameThreadId,
                                    atBatIndex=atBat["atBatIndex"],
                                    actionIndex=actionIndex,
                                    isScoringPlay=1
                                    if atBat["playEvents"][actionIndex]["details"].get(
                                        "isScoringPlay"
                                    )
                                    else 0,
                                    eventType=atBat["playEvents"][actionIndex][
                                        "details"
                                    ].get(
                                        "eventType",
                                        atBat["playEvents"][actionIndex]["details"]
                                        .get("event", "")
                                        .lower()
                                        .replace(" ", "_"),
                                    ),
                                    myTeamBatting=1 if myTeamBatting else 0,
                                    commentId=commentObj["comment"]["id"],
                                    dateCreated=commentObj["comment"]["published"],
                                    dateUpdated=commentObj["comment"]["published"],
                                    deleted=0,
                                )
                            except Exception as e:
                                self.log.error(
                                    "Error submitting comment to game thread {} for actionIndex {} for atBatIndex {}: {}".format(
                                        gameThreadId,
                                        actionIndex,
                                        atBat["atBatIndex"],
                                        e,
                                    )
                                )
                                self.error_notification(
                                    f"Error submitting comment to game {pk} thread {gameThreadId} for actionIndex {actionIndex} of atBatIndex {atBat['atBatIndex']}"
                                )
                        else:
                            self.log.warning(
                                "Not submitting comment to game thread {} for actionIndex {} for atBatIndex {} because text is blank... ".format(
                                    gameThreadId, actionIndex, atBat["atBatIndex"]
                                )
                            )
                            self.error_notification(
                                f"Comment body is blank for game {pk} thread {gameThreadId} for actionIndex {actionIndex} of atBatIndex {atBat['atBatIndex']}"
                            )
                    else:
                        # Event not wanted
                        self.log.debug(
                            "Event {} not wanted.".format(
                                atBat["playEvents"][actionIndex]["details"].get(
                                    "eventType",
                                    atBat["playEvents"][actionIndex]["details"]
                                    .get("event", "")
                                    .lower()
                                    .replace(" ", "_"),
                                )
                            )
                        )

                    # Add actionIndex so we don't process it again
                    processedAtBats[str(atBat["atBatIndex"])]["a"].append(actionIndex)

                if atBat["about"]["isComplete"]:
                    # At bat is complete, so process the result
                    self.log.debug(
                        "Processing result for atBatIndex {}: [{}] (myTeamBatting: {}).".format(
                            atBat["atBatIndex"], atBat, myTeamBatting
                        )
                    )
                    if (
                        (
                            atBat["result"].get(
                                "eventType",
                                atBat["result"]
                                .get("event", "")
                                .lower()
                                .replace(" ", "_"),
                            )
                            in myTeamBattingEvents
                            and myTeamBatting
                        )
                        or (
                            atBat["result"].get(
                                "eventType",
                                atBat["result"]
                                .get("event", "")
                                .lower()
                                .replace(" ", "_"),
                            )
                            in myTeamPitchingEvents
                            and not myTeamBatting
                        )
                        or (
                            "scoring_play" in myTeamBattingEvents
                            and atBat["about"].get("isScoringPlay")
                            and myTeamBatting
                        )
                        or (
                            "scoring_play" in myTeamPitchingEvents
                            and atBat["about"].get("isScoringPlay")
                            and not myTeamBatting
                        )
                    ):
                        # Event type is wanted
                        self.log.debug(
                            "Detected {}{} event (myTeamBatting: {}).".format(
                                atBat["result"].get(
                                    "eventType",
                                    atBat["result"]
                                    .get("event", "")
                                    .lower()
                                    .replace(" ", "_"),
                                ),
                                "/scoring_play"
                                if atBat["about"].get("isScoringPlay")
                                else "",
                                myTeamBatting,
                            )
                        )
                        text = self.render_template(
                            thread="comment",
                            templateType="body",
                            data=self.commonData,
                            gamePk=pk,
                            settings=self.settings,
                            actionOrResult="result",
                            myTeamBatting=myTeamBatting,
                            atBat=atBat,
                            actionIndex=None,
                            eventType=atBat["result"].get(
                                "eventType",
                                atBat["result"]
                                .get("event", "")
                                .lower()
                                .replace(" ", "_"),
                            ),
                        )
                        self.log.debug("Rendered comment text: {}".format(text))
                        if text != "":
                            try:
                                commentObj = self.lemmy.submitComment(
                                    gameThreadId, text, language_id=37
                                )
                                self.log.info(
                                    "Submitted comment to game thread {} for result of atBatIndex {}: {}".format(
                                        gameThreadId, atBat["atBatIndex"], text
                                    )
                                )
                                self.insert_comment_to_db(
                                    pk=pk,
                                    gameThreadId=gameThreadId,
                                    atBatIndex=atBat["atBatIndex"],
                                    actionIndex=None,
                                    isScoringPlay=1
                                    if atBat["about"].get("isScoringPlay")
                                    else 0,
                                    eventType=atBat["result"].get(
                                        "eventType",
                                        atBat["result"]
                                        .get("event", "")
                                        .lower()
                                        .replace(" ", "_"),
                                    ),
                                    myTeamBatting=1 if myTeamBatting else 0,
                                    commentId=commentObj["comment"]["id"],
                                    dateCreated=commentObj["comment"]["published"],
                                    dateUpdated=commentObj["comment"]["published"],
                                    deleted=0,
                                )
                            except Exception as e:
                                self.log.error(
                                    "Error submitting comment to game thread {} for result of atBatIndex {}: {}".format(
                                        gameThreadId, atBat["atBatIndex"], e
                                    )
                                )
                                self.error_notification(
                                    f"Error submitting comment to game {pk} thread {gameThreadId} for result of atBatIndex {atBat['atBatIndex']}"
                                )
                        else:
                            self.log.warning(
                                "Not submitting comment to game thread {} for result of atBatIndex {} because text is blank... ".format(
                                    gameThreadId, atBat["atBatIndex"]
                                )
                            )
                            self.error_notification(
                                f"Comment body is blank for game {pk} thread {gameThreadId} for result of atBatIndex {atBat['atBatIndex']}"
                            )
                    else:
                        # Event not wanted
                        self.log.debug(
                            "Event {} not wanted.".format(
                                atBat["result"].get(
                                    "eventType",
                                    atBat["result"]
                                    .get("event", "")
                                    .lower()
                                    .replace(" ", "_"),
                                )
                            )
                        )

                    # Mark atBatIndex as processed
                    processedAtBats[str(atBat["atBatIndex"])].update({"c": True})

                # Update DB with current processedAtBats
                self.update_processedAtBats_in_db(pk, gameThreadId, processedAtBats)

            if not self.activeGames.get(pk):
                self.log.warning("Game {} is no longer being tracked!".format(pk))
                break
            elif self.activeGames[pk]["STOP_FLAG"]:
                self.log.info("Game {} thread stop flag is set.".format(pk))
                break
            elif self.commonData[pk]["schedule"]["status"]["detailedState"].startswith(
                "Delayed"
            ) and self.commonData[pk]["schedule"]["status"]["abstractGameCode"] not in [
                "I",
                "IZ",
                "IH",
            ]:
                # I: In Progress, IZ: Delayed: About to Resume, IH: Instant Replay
                # Update interval is in minutes (seconds only when game is live)
                gtnlWait = self.settings.get("Game Thread", {}).get(
                    "UPDATE_INTERVAL_NOT_LIVE", 1
                )
                if gtnlWait < 1:
                    gtnlWait = 1
                self.log.info(
                    "Game {} is delayed (abstractGameCode: {}, codedGameState: {}), sleeping for {} minutes...".format(
                        pk,
                        self.commonData[pk]["schedule"]["status"]["abstractGameCode"],
                        self.commonData[pk]["schedule"]["status"]["codedGameState"],
                        gtnlWait,
                    )
                )
                self.sleep(gtnlWait * 60)
            elif self.commonData[pk]["schedule"]["status"]["abstractGameCode"] == "L":
                # Update interval is in seconds (minutes for all other cases)
                gtWait = self.settings.get("Game Thread", {}).get("UPDATE_INTERVAL", 10)
                if gtWait < 1:
                    gtWait = 1
                self.log.info(
                    "Game {} is live (abstractGameCode: {}, codedGameState: {}), sleeping for {} seconds...".format(
                        pk,
                        self.commonData[pk]["schedule"]["status"]["abstractGameCode"],
                        self.commonData[pk]["schedule"]["status"]["codedGameState"],
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
                    "Game {} is not live (abstractGameCode: {}, codedGameState: {}), sleeping for {} minutes...".format(
                        pk,
                        self.commonData[pk]["schedule"]["status"]["abstractGameCode"],
                        self.commonData[pk]["schedule"]["status"]["codedGameState"],
                        gtnlWait,
                    )
                )
                self.sleep(gtnlWait * 60)

        if redball.SIGNAL is not None or self.bot.STOP:
            self.log.debug("Caught a stop signal...")
            return

        self.log.info("Stopping game play monitor process.")
        return

    def insert_comment_to_db(
        self,
        pk,
        gameThreadId,
        atBatIndex,
        actionIndex,
        isScoringPlay,
        eventType,
        myTeamBatting,
        commentId,
        dateCreated,
        dateUpdated,
        deleted,
    ):
        q = (
            """INSERT INTO {}comments (
                gamePk,
                gameThreadId,
                atBatIndex,
                actionIndex,
                isScoringPlay,
                eventType,
                myTeamBatting,
                commentId,
                dateCreated,
                dateUpdated,
                deleted
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?
            );""".format(
                self.dbTablePrefix
            ),
            (
                pk,
                gameThreadId,
                atBatIndex,
                actionIndex,
                isScoringPlay,
                eventType,
                myTeamBatting,
                commentId,
                dateCreated,
                dateUpdated,
                deleted,
            ),
        )
        i = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
        if isinstance(i, str):
            self.log.error("Error inserting comment into database: {}".format(i))
            return False
        else:
            return True

    def get_processedAtBats_from_db(self, pk, gameThreadId):
        sq = (
            "SELECT * FROM {}processedAtBats WHERE gamePk=? and gameThreadId=?;".format(
                self.dbTablePrefix
            )
        )
        local_args = (pk, gameThreadId)
        s = rbdb.db_qry((sq, local_args), fetchone=True, closeAfter=True, logg=self.log)
        if isinstance(s, str):
            # Error querying for existing row
            self.log.error(
                "Error querying for existing row in {}processedAtBats table for gamePk {} and threadId {}: {}".format(
                    self.dbTablePrefix, pk, gameThreadId, s
                )
            )
        elif not s:
            # Row does not exist; insert it
            self.log.debug(
                "Creating record in {}processedAtBats table...".format(
                    self.dbTablePrefix
                )
            )
            ts = time.time()
            emptyDict = json.dumps({})
            q = "insert into {}processedAtBats (gamePk, gameThreadId, processedAtBats, dateCreated, dateUpdated) values ({}, '{}', '{}', '{}', '{}');".format(
                self.dbTablePrefix,
                pk,
                gameThreadId,
                emptyDict,
                ts,
                ts,
            )

            r = rbdb.db_qry(q, commit=True, closeAfter=True, logg=self.log)
            if isinstance(r, str):
                # Error inserting/updating row
                self.log.error(
                    "Error inserting/updating row in {}processedAtBats table for gamePk {} and gameThreadId {}: {}".format(
                        self.dbTablePrefix, pk, gameThreadId, r
                    )
                )
            else:
                return {
                    "gamePk": pk,
                    "gameThreadId": gameThreadId,
                    "processedAtBats": {},
                    "dateCreated": ts,
                    "dateUpdated": ts,
                }
        else:
            # Row already exists; return the record
            s.update({"processedAtBats": json.loads(s.get("processedAtBats", "{}"))})
            self.log.debug(
                "Found record in {}processedAtBats table: {}".format(
                    self.dbTablePrefix, s
                )
            )
            return s

        return None

    def update_processedAtBats_in_db(self, pk, gameThreadId, processedAtBats):
        q = "UPDATE {}processedAtBats SET processedAtBats=?, dateUpdated=? where gamePk=? and gameThreadId=?;".format(
            self.dbTablePrefix
        )
        local_args = (json.dumps(processedAtBats), time.time(), pk, gameThreadId)
        r = rbdb.db_qry((q, local_args), commit=True, closeAfter=True, logg=self.log)
        if isinstance(r, str):
            # Error inserting/updating row
            self.log.error(
                "Error updating row in {}processedAtBats table for gamePk {} and gameThreadId {}: {}".format(
                    self.dbTablePrefix, pk, gameThreadId, r
                )
            )
        else:
            return True

        return False

    def patch_dict(self, theDict, patch):
        # theDict = dict to patch
        # patch = patch to apply to theDict
        # return patched dict
        if redball.DEV:
            self.log.debug(f"theDict to be patched: {theDict}")
            self.log.debug(f"patch to be applied: {patch}")
        for x in patch:
            self.log.debug(f"x:{patch.index(x)}, len(patch): {len(patch)}")
            for d in x.get("diff", []):
                if redball.DEV:
                    self.log.debug(f"d:{d}")

                try:
                    if d.get("op") is not None:
                        value = d.get("value")
                        if value is not None or d.get("op") == "remove":
                            path = d.get("path", "").split("/")
                            target = theDict
                            for i, p in enumerate(path[1:]):
                                if redball.DEV:
                                    self.log.debug(
                                        f"i:{i}, p:{p}, type(target):{type(target)}"
                                    )

                                if i == len(path) - 2:
                                    # end of the path--set the value
                                    if d.get("op") == "add":
                                        if isinstance(target, list):
                                            if redball.DEV:
                                                self.log.debug(
                                                    f"appending [{value}] to target; target type:{type(target)}"
                                                )

                                            target.append(value)
                                            continue
                                        elif isinstance(target, dict):
                                            if redball.DEV:
                                                self.log.debug(
                                                    f"setting target[{p}] to [{value}]; target type:{type(target)}"
                                                )

                                            target[p] = value
                                            continue
                                    elif d.get("op") == "remove":
                                        if redball.DEV:
                                            self.log.debug(
                                                f"removing target[{p}]; target type:{type(target)}, target len:{len(target if not isinstance(target, int) and not isinstance(target, bool) else '')}"
                                            )

                                        try:
                                            if isinstance(target, list):
                                                if int(p) < len(target):
                                                    target.pop(
                                                        int(p)
                                                        if isinstance(target, list)
                                                        else p
                                                    )
                                                else:
                                                    self.log.warning(
                                                        f"Index {p} does not exist in target list: {target}"
                                                    )
                                            elif isinstance(target, dict):
                                                if p in target.keys():
                                                    target.pop(p)
                                                else:
                                                    self.log.warning(
                                                        f"Key {p} does not exist in target dict: {target}"
                                                    )
                                            else:
                                                self.log.warning(
                                                    f"Not sure how to remove {p} from target: {target}"
                                                )
                                        except Exception as e:
                                            self.log.error(
                                                f"Error removing {path}: {e}"
                                            )
                                            self.error_notification(
                                                f"Error patching dict--cannot remove {path} from target [{target}]"
                                            )

                                        continue
                                    elif d.get("op") == "replace":
                                        if redball.DEV:
                                            self.log.debug(
                                                f"updating target[{p}] to [{value}]; target type:{type(target)}"
                                            )

                                        if isinstance(target, list):
                                            if len(target) > 0 and len(target) > int(p):
                                                target[int(p)] = value
                                            elif int(p) == len(target):
                                                if redball.DEV:
                                                    self.log.debug(
                                                        "op=replace, but provided index does not exist yet (it's next up); appending value to list"
                                                    )

                                                target.append(value)
                                            else:
                                                self.log.warning(
                                                    f"Data discrepancy found while patching gumbo data: List is not long enough to replace index {p} (len: {len(target)})"
                                                )
                                                return False
                                        else:
                                            target[p] = value

                                        continue
                                elif (
                                    isinstance(target, dict)
                                    and target.get(
                                        int(p) if isinstance(target, list) else p
                                    )
                                    is None
                                ) or (
                                    isinstance(target, list) and len(target) <= int(p)
                                ):
                                    # key does not exist
                                    if isinstance(path[i + 1], int):
                                        # next hop is a list
                                        if redball.DEV:
                                            self.log.debug(
                                                f"missing key, adding list for target[{p}]"
                                            )

                                        if isinstance(target, list):
                                            if len(target) == int(p):
                                                target.append([])
                                            else:
                                                self.log.warning(
                                                    f"Data discrepancy found while patching gumbo data: List is not long enough to append index [{p}] (len: {len(target)})."
                                                )
                                                return False
                                        else:
                                            target[p] = []
                                    elif i == len(path) - 3 and d.get("op") == "add":
                                        # next hop is the target key to add
                                        # do nothing, because it will be handled on the next loop
                                        if redball.DEV:
                                            self.log.debug(
                                                "missing key, but not a problem because op=add; continuing..."
                                            )
                                        continue
                                    else:
                                        # next hop is a dict
                                        if redball.DEV:
                                            self.log.debug(
                                                f"missing key, adding dict for target[{p}]"
                                            )

                                        if isinstance(target, list):
                                            if len(target) == int(p):
                                                target.append({})
                                            else:
                                                self.log.warning(
                                                    f"Data discrepancy found while patching gumbo data: List is not long enough (len: {len(target)}) to append index [{p}]."
                                                )
                                                return False
                                        else:
                                            target[p] = {}
                                # point to next key in the path
                                target = target[
                                    int(p) if isinstance(target, list) else p
                                ]
                                if redball.DEV:
                                    self.log.debug(
                                        f"type(target) after next hop: {type(target)}"
                                    )
                        else:
                            # No value to add
                            if redball.DEV:
                                self.log.debug("no value")
                    else:
                        # No op
                        if redball.DEV:
                            self.log.debug("no op")
                except Exception as e:
                    self.log.error(f"Error patching gumbo data: {e}")
                    self.error_notification(f"Error patching gumbo data: {e}")
                    return False

        self.log.debug("Patch complete.")
        return True

    def get_gameStatus(self, pk, d=None):
        # pk = gamePk, d = date ('%Y-%m-%d')
        params = {
            "sportId": 1,
            "fields": "dates,date,totalGames,games,gamePk,gameDate,status,statusCode,abstractGameCode,detailedState,abstractGameState,codedGameState,startTimeTBD",
        }
        if d:
            params.update({"date": d})
        s = self.api_call("schedule", params)
        games = s["dates"][
            next((i for i, x in enumerate(s["dates"]) if x["date"] == d), 0)
        ]["games"]
        status = games[next((i for i, x in enumerate(games) if x["gamePk"] == pk), 0)][
            "status"
        ]
        if not self.commonData.get(pk):
            self.commonData.update({pk: {"schedule": {}}})
        self.commonData[pk]["schedule"].update({"status": status})

        return True

    def get_gamePks(self, t=None, o=None, d=None, sd=None, ed=None):
        # t = teamId, o = opponentId, d = date ('%Y-%m-%d'), sd = start date, ed = end date
        params = {"sportId": 1, "fields": "dates,games,gamePk"}
        if t:
            params.update({"teamId": t})

        if o and t:
            params.update({"opponentId": o})  # opponentId not supported without teamId

        if d:
            params.update({"date": d})
        elif sd and ed:
            params.update({"startDate": sd, "endDate": ed})

        s = self.api_call("schedule", params)
        pks = []
        for date in s.get("dates", []):
            for game in date.get("games"):
                if game.get("gamePk"):
                    pks.append(game["gamePk"])

        return pks

    def get_seasonState(self, t=None):
        self.log.debug(
            f"myteam league seasondateinfo: {self.myTeam['league']['seasonDateInfo']}"
        )
        if self.settings.get("MLB", {}).get("SEASON_STATE_OVERRIDE"):
            self.log.debug("Overriding season state per SEASON_STATE_OVERRIDE setting")
            return self.settings["MLB"]["SEASON_STATE_OVERRIDE"]
        elif self.myTeam["league"]["seasonDateInfo"].get(
            "springStartDate"
        ) and datetime.strptime(
            self.myTeam["league"]["seasonDateInfo"]["springStartDate"],
            "%Y-%m-%d",
        ) <= datetime.strptime(
            self.today["Y-m-d"], "%Y-%m-%d"
        ) < datetime.strptime(
            self.myTeam["league"]["seasonDateInfo"]["regularSeasonStartDate"],
            "%Y-%m-%d",
        ):
            # Preseason (includes day or two in between pre and regular season)
            return "pre"
        elif (
            not self.myTeam["league"]["seasonDateInfo"].get("springStartDate")
            and datetime.strptime(self.today["Y-m-d"], "%Y-%m-%d")
            < datetime.strptime(
                self.myTeam["league"]["seasonDateInfo"]["regularSeasonStartDate"],
                "%Y-%m-%d",
            )
        ) or (
            datetime.strptime(self.today["Y-m-d"], "%Y-%m-%d")
            < datetime.strptime(
                self.myTeam["league"]["seasonDateInfo"]["springStartDate"],
                "%Y-%m-%d",
            )
        ):
            # Offseason (prior to season)
            return "off:before"
        elif (
            datetime.strptime(
                self.myTeam["league"]["seasonDateInfo"]["regularSeasonStartDate"],
                "%Y-%m-%d",
            )
            <= datetime.strptime(self.today["Y-m-d"], "%Y-%m-%d")
            <= datetime.strptime(
                self.myTeam["league"]["seasonDateInfo"]["regularSeasonEndDate"],
                "%Y-%m-%d",
            )
        ):
            # Regular season
            return "regular"
        elif (
            datetime.strptime(
                self.myTeam["league"]["seasonDateInfo"]["regularSeasonEndDate"],
                "%Y-%m-%d",
            )
            < datetime.strptime(self.today["Y-m-d"], "%Y-%m-%d")
            <= datetime.strptime(
                self.myTeam["league"]["seasonDateInfo"]["postSeasonEndDate"], "%Y-%m-%d"
            )
        ):
            # Postseason
            if (
                len(
                    self.get_gamePks(
                        t=t,
                        sd=self.today["Y-m-d"],
                        ed=self.myTeam["league"]["seasonDateInfo"]["postSeasonEndDate"],
                    )
                )
                > 0
            ):
                # The team is in the postseason, hooray!
                return "post:in"
            else:
                # Check if there is a game scheduled where my team is part of a TBD
                sc = self.get_schedule_data(
                    sd=self.today["Y-m-d"],
                    ed=self.myTeam["league"]["seasonDateInfo"]["postSeasonEndDate"],
                )
                all_teams = []
                for d in sc["dates"]:
                    for g in d["games"]:
                        all_teams.extend(
                            [
                                g["teams"]["away"]["team"]["name"],
                                g["teams"]["home"]["team"]["name"],
                            ]
                        )
                all_teams = set(all_teams)
                team = self.get_team(t, h="")
                team_found = next(
                    (x for x in all_teams if team["abbreviation"] in x), False
                )
                if team_found:
                    # The team is in the postseason!
                    self.log.info(
                        f"Team determined to be in the postseason based on a game scheduled with a TBD team that includes [{team['abbreviation']}] in the name: [{team_found}]."
                    )
                    return "post:in"
                else:
                    # Better luck next year...
                    return "post:out"
        elif datetime.strptime(self.today["Y-m-d"], "%Y-%m-%d") > datetime.strptime(
            self.myTeam["league"]["seasonDateInfo"]["postSeasonEndDate"], "%Y-%m-%d"
        ):
            # Offseason (after season)
            return "off:after"
        else:
            # No idea...
            return None

    def get_nextGame(self, t=None):
        # t = teamId, default will by self.myTeam['id']
        if t == self.myTeam["id"]:
            seasonState = self.seasonState
        else:
            seasonState = self.get_seasonState(t)

        if seasonState == "off:before":
            season = int(self.today["Y"])
            the_date = (
                datetime.strptime(
                    self.myTeam["league"]["seasonDateInfo"]["springStartDate"],
                    "%Y-%m-%d",
                )
                if self.myTeam["league"]["seasonDateInfo"].get("springStartDate")
                else (
                    datetime.strptime(
                        self.myTeam["league"]["seasonDateInfo"][
                            "regularSeasonStartDate"
                        ],
                        "%Y-%m-%d",
                    )
                )
            )
            start_date = (the_date - timedelta(days=3)).strftime("%Y-%m-%d")
            end_date = (the_date + timedelta(days=7)).strftime("%Y-%m-%d")
        elif seasonState in ["pre", "regular", "post:in"]:
            season = int(self.today["Y"])
            start_date = self.today["Y-m-d"]
            end_date = (
                datetime.strptime(self.today["Y-m-d"], "%Y-%m-%d") + timedelta(days=10)
            ).strftime("%Y-%m-%d")
        elif seasonState in ["post:out", "off:after"]:
            season = int(self.today["Y"]) + 1
            seasonInfo = self.api_call("seasons", {"season": season, "sportId": 1})[
                "seasons"
            ]
            if len(seasonInfo) and seasonInfo[0].get("seasonStartDate"):
                seasonInfo = seasonInfo[0]
                start_date = (
                    datetime.strptime(seasonInfo["seasonStartDate"], "%Y-%m-%d")
                    - timedelta(days=3)
                ).strftime("%Y-%m-%d")
                end_date = (
                    datetime.strptime(seasonInfo["seasonStartDate"], "%Y-%m-%d")
                    + timedelta(days=7)
                ).strftime("%Y-%m-%d")
            else:
                self.log.warning(
                    "Dates not published for {} season yet! Checking for games in next 10 days instead...".format(
                        season
                    )
                )
                start_date = self.today["Y-m-d"]
                end_date = (
                    datetime.strptime(self.today["Y-m-d"], "%Y-%m-%d")
                    + timedelta(days=10)
                ).strftime("%Y-%m-%d")
        else:
            # Don't know what to do here
            self.log.error("Unknown season state, cannot determine next game...")
            return {}

        sc = self.get_schedule_data(t=t, sd=start_date, ed=end_date)
        if len(sc["dates"]) == 0:
            # No games found
            self.log.debug("No games found!")
            return {}
        else:
            lookAfter = (
                self.commonData[max(self.commonData.keys())]["gameTime"]["utc"]
                if len(self.commonData) > 1
                else datetime.strptime(
                    (
                        datetime.strptime(self.today["Y-m-d"], "%Y-%m-%d")
                        + timedelta(days=1)
                    ).strftime("%Y-%m-%d")
                    + "T"
                    + datetime.utcnow().strftime("%H:%M:%SZ"),
                    "%Y-%m-%dT%H:%M:%SZ",
                ).replace(
                    tzinfo=pytz.utc
                )  # UTC time is in the next day
                if (
                    datetime.strptime(
                        self.today["Y-m-d"]
                        + "T"
                        + datetime.now().strftime("%H:%M:%SZ"),
                        "%Y-%m-%dT%H:%M:%SZ",
                    ).replace(tzinfo=tzlocal.get_localzone())
                    - datetime.strptime(
                        self.today["Y-m-d"]
                        + "T"
                        + datetime.utcnow().strftime("%H:%M:%SZ"),
                        "%Y-%m-%dT%H:%M:%SZ",
                    ).replace(tzinfo=pytz.utc)
                ).total_seconds()
                / 60
                / 60
                / 24
                > 0.5  # With "today" date, difference between time in UTC and local is more than 12hr
                else datetime.strptime(
                    self.today["Y-m-d"] + "T" + datetime.utcnow().strftime("%H:%M:%SZ"),
                    "%Y-%m-%dT%H:%M:%SZ",
                ).replace(
                    tzinfo=pytz.utc
                )  # Date is still the same when time is converted to UTC
            )
            self.log.debug(
                "Looking for next game starting after {} ({})...".format(
                    lookAfter,
                    "start time of game {}".format(max(self.commonData.keys()))
                    if len(self.commonData) > 1
                    else "current time",
                )
            )
            nextGame = next(
                (
                    date["games"][game_index]
                    for date in sc["dates"]
                    for game_index, game in enumerate(date["games"])
                    if datetime.strptime(
                        game["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                    ).replace(tzinfo=pytz.utc)
                    > lookAfter
                ),
                {},
            )

            if nextGame:
                nextGame.update(
                    {
                        "gameTime": {
                            "myTeam": self.convert_timezone(
                                datetime.strptime(
                                    nextGame["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                ).replace(tzinfo=pytz.utc),
                                self.myTeam["venue"]["timeZone"]["id"],
                            ),
                            "homeTeam": self.convert_timezone(
                                datetime.strptime(
                                    nextGame["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                ).replace(tzinfo=pytz.utc),
                                nextGame["venue"]["timeZone"]["id"],
                            ),
                            "bot": self.convert_timezone(
                                datetime.strptime(
                                    nextGame["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                ).replace(tzinfo=pytz.utc),
                                "local",
                            ),
                            "utc": datetime.strptime(
                                nextGame["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=pytz.utc),
                        }
                    }
                )

            self.log.debug("Found next game for team {}: {}".format(t, nextGame))

            return nextGame

        return {}

    def collect_data(self, gamePk):
        """Collect data to be available for template rendering"""

        # Need to use cached data because multiple threads will be trying to update the same data at the same time
        cache_seconds = self.settings.get("MLB", {}).get("API_CACHE_SECONDS", 5)
        if cache_seconds < 0:
            cache_seconds = 5  # Use default of 5 seconds if negative value provided

        if gamePk == 0:
            # Generic data used by all threads
            with (
                GENERIC_DATA_LOCK
            ):  # Use lock to prevent multiple threads from updating data at the same time
                if self.commonData.get(gamePk) and self.commonData[gamePk].get(
                    "lastUpdate", datetime.today() - timedelta(hours=1)
                ) >= datetime.today() - timedelta(seconds=cache_seconds):
                    self.log.debug(
                        "Using cached data for gamePk {}, updated {} seconds ago.".format(
                            gamePk,
                            (
                                datetime.today() - self.commonData[gamePk]["lastUpdate"]
                            ).total_seconds(),
                        )
                    )
                    return False
                else:
                    self.log.debug(
                        "Collecting data for gamePk {} with StatsAPI v{}".format(
                            gamePk, statsapi.__version__
                        )
                    )

                pkData = {}  # temp dict to hold the data until it's complete

                # Date that represents 'today'
                pkData.update({"today": self.today})

                # Update standings info
                pkData.update(
                    {"standings": statsapi.standings_data()}
                )  # TODO: something similar to api_call()?

                # Update schedule data for today's other games - for no-no watch & division/league scoreboard
                ls = self.get_schedule_data(
                    d=self.today["Y-m-d"],
                    h="team(division,league),linescore,flags,venue(timezone)",
                )
                pkData.update({"leagueSchedule": []})
                y = next(
                    (
                        i
                        for i, x in enumerate(ls["dates"])
                        if x["date"] == self.today["Y-m-d"]
                    ),
                    None,
                )
                if y is not None:
                    games = ls["dates"][y]["games"]
                    for (
                        x
                    ) in (
                        games
                    ):  # Include all games and filter out current gamePk when displaying
                        if x["doubleHeader"] == "Y" and x["gameNumber"] == 2:
                            # Find DH game 1
                            otherGame = next(
                                (
                                    {
                                        "gamePk": v["schedule"]["gamePk"],
                                        "gameDate": v["schedule"]["gameDate"],
                                    }
                                    for k, v in self.commonData.items()
                                    if k not in [0, "weekly", "off", "gameday"]
                                    and v.get("schedule", {}).get("gamePk")
                                    != x["gamePk"]
                                    and v.get("schedule", {}).get("doubleHeader") == "Y"
                                    and v.get("schedule", {}).get("gameNumber") == 1
                                    and v.get("schedule", {})
                                    .get("teams", {})
                                    .get("home", {})
                                    .get("team", {})
                                    .get("id")
                                    in [
                                        x.get("teams", {})
                                        .get("home", {})
                                        .get("team", {})
                                        .get("id"),
                                        x.get("teams", {})
                                        .get("away", {})
                                        .get("team", {})
                                        .get("id"),
                                    ]
                                ),
                                None,
                            )
                            self.log.debug(
                                f"Result of check for DH game 1 in commonData: {otherGame}"
                            )

                            if not otherGame:
                                # Check league schedule
                                otherGame = next(
                                    (
                                        {
                                            "gamePk": v["gamePk"],
                                            "gameDate": v["gameDate"],
                                        }
                                        for v in games
                                        if v.get("gamePk") != x["gamePk"]
                                        and v.get("doubleHeader") == "Y"
                                        and v.get("gameNumber") == 1
                                        and v.get("teams", {})
                                        .get("home", {})
                                        .get("team", {})
                                        .get("id")
                                        in [
                                            x.get("teams", {})
                                            .get("home", {})
                                            .get("team", {})
                                            .get("id"),
                                            x.get("teams", {})
                                            .get("away", {})
                                            .get("team", {})
                                            .get("id"),
                                        ]
                                    ),
                                    None,
                                )
                                self.log.debug(
                                    f"Result of check for DH game 1 in leagueSchedule: {otherGame}"
                                )

                            if not otherGame:
                                # Get schedule data from MLB
                                self.log.debug(
                                    f"Getting schedule data for team id [{self.myTeam['id']}] and date [{self.today['Y-m-d']}]..."
                                )
                                sched = self.api_call(
                                    "schedule",
                                    {
                                        "sportId": 1,
                                        "date": self.today["Y-m-d"],
                                        "teamId": self.myTeam["id"],
                                        "fields": "dates,date,games,gamePk,gameDate,doubleHeader,gameNumber",
                                    },
                                )
                                schedGames = sched["dates"][
                                    next(
                                        (
                                            i
                                            for i, y in enumerate(sched["dates"])
                                            if y["date"] == self.today["Y-m-d"]
                                        ),
                                        0,
                                    )
                                ]["games"]
                                otherGame = next(
                                    (
                                        v
                                        for v in schedGames
                                        if v.get("gamePk") != x["gamePk"]
                                        and v.get("doubleHeader") == "Y"
                                        and v.get("gameNumber") == 1
                                    ),
                                    None,
                                )
                                self.log.debug(
                                    f"Result of check for DH game 1 in MLB schedule data: {otherGame}"
                                )

                            if otherGame:
                                # Replace gameDate for straight doubleheader game 2 to reflect game 1 + 3 hours
                                self.log.debug(f"DH Game 1: {otherGame['gamePk']}")
                                x["gameDate"] = (
                                    datetime.strptime(
                                        otherGame["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                    ).replace(tzinfo=pytz.utc)
                                    + timedelta(hours=3)
                                ).strftime("%Y-%m-%dT%H:%M:%SZ")
                                self.log.info(
                                    f"Replaced game time for DH Game 2 [{x['gamePk']}] to 3 hours after Game 1 [{otherGame['gamePk']}] game time: [{x['gameDate']}]"
                                )
                            else:
                                self.log.debug(
                                    f"Failed to find DH game 1 for DH game 2 [{x['gamePk']}]"
                                )

                        # Convert game time to myTeam's timezone as well as local (homeTeam's) timezone
                        x.update(
                            {
                                "gameTime": {
                                    "myTeam": self.convert_timezone(
                                        datetime.strptime(
                                            x["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                        ).replace(tzinfo=pytz.utc),
                                        self.myTeam["venue"]["timeZone"]["id"],
                                    ),
                                    "bot": self.convert_timezone(
                                        datetime.strptime(
                                            x["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                        ).replace(tzinfo=pytz.utc),
                                        "local",
                                    ),
                                    "utc": datetime.strptime(
                                        x["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                    ).replace(tzinfo=pytz.utc),
                                }
                            }
                        )
                        if x["venue"].get("timeZone", {}).get("id"):
                            x["gameTime"].update(
                                {
                                    "homeTeam": self.convert_timezone(
                                        datetime.strptime(
                                            x["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                        ).replace(tzinfo=pytz.utc),
                                        self.myTeam["venue"]["timeZone"]["id"],
                                    ),
                                }
                            )
                        else:
                            self.log.warn(
                                f"Game {x['gamePk']} has no venue timezone. Using myTeam timezone in place of home team timezone."
                            )
                            x["gameTime"].update(
                                {
                                    "homeTeam": self.convert_timezone(
                                        datetime.strptime(
                                            x["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                        ).replace(tzinfo=pytz.utc),
                                        x["venue"]["timeZone"]["id"],
                                    ),
                                }
                            )
                        pkData["leagueSchedule"].append(x)
                else:
                    self.log.debug("There are no games at all today.")

                # self.myTeam - updated daily
                pkData.update({"myTeam": self.myTeam})

                # My team's season state
                pkData["myTeam"].update({"seasonState": self.seasonState})

                # My team's next game
                pkData["myTeam"].update(
                    {"nextGame": self.get_nextGame(self.myTeam["id"])}
                )

                # Include team community dict
                pkData.update({"teamSubs": self.teamSubs})

                # Team leaders (hitting, pitching)
                # Team stats
                # Last / next game schedule info
                # Last game recap/highlights/score/decisions
                # Next opponent team info/record/standings

                pkData.update({"lastUpdate": datetime.today()})

                # Make the data available
                self.commonData.update({gamePk: pkData})
        else:
            # gamePk was provided, update game-specific data
            # Get generic data if it doesn't exist
            if not self.commonData.get(0):
                self.collect_data(0)

            with (
                GAME_DATA_LOCK
            ):  # Use lock to prevent multiple threads from updating data at the same time
                # Update game-specific data
                if not isinstance(gamePk, list):
                    gamePks = [gamePk]
                else:
                    gamePks = [x for x in gamePk]

                if len(gamePks) == 0:
                    self.log.warning("No gamePks to collect data for.")
                    return False
                
                for pk in gamePks[:]:
                    if self.commonData.get(pk) and self.commonData[pk].get(
                        "lastUpdate", datetime.today() - timedelta(hours=1)
                    ) >= datetime.today() - timedelta(seconds=cache_seconds):
                        self.log.debug(
                            "Using cached data for gamePk {}, updated {} seconds ago.".format(
                                pk,
                                (
                                    datetime.today() - self.commonData[pk]["lastUpdate"]
                                ).total_seconds(),
                            )
                        )
                        gamePks.remove(pk)
                    else:
                        self.log.debug(
                            "Collecting data for gamePk {} with StatsAPI v{}".format(
                                pk, statsapi.__version__
                            )
                        )

                if len(gamePks) == 0:
                    self.log.debug("Using cached data for all gamePks.")
                    return False

                self.log.debug("Getting schedule data for gamePks: {}".format(gamePks))
                s = self.get_schedule_data(
                    ",".join(str(i) for i in gamePks), self.today["Y-m-d"]
                )
                for pk in gamePks:
                    self.log.debug("Collecting data for pk: {}".format(pk))
                    pkData = {}  # temp dict to hold the data until it's complete

                    # Schedule data includes status, highlights, weather, broadcasts, probable pitchers, officials, and team info (incl. score)
                    games = s["dates"][
                        next(
                            (
                                i
                                for i, x in enumerate(s["dates"])
                                if x["date"] == self.today["Y-m-d"]
                            ),
                            0,
                        )
                    ]["games"]
                    game = games[
                        next((i for i, x in enumerate(games) if x["gamePk"] == pk), 0)
                    ]
                    pkData.update({"schedule": game})
                    self.log.debug("Appended schedule for pk {}".format(pk))

                    if game["doubleHeader"] == "Y" and game["gameNumber"] == 2:
                        # Find DH game 1
                        otherGame = next(
                            (
                                {
                                    "gamePk": v["schedule"]["gamePk"],
                                    "gameDate": v["schedule"]["gameDate"],
                                }
                                for k, v in self.commonData.items()
                                if k not in [0, "weekly", "off", "gameday"]
                                and v.get("schedule", {}).get("gamePk")
                                != game["gamePk"]
                                and v.get("schedule", {}).get("doubleHeader") == "Y"
                                and v.get("schedule", {}).get("gameNumber") == 1
                                and self.myTeam["id"]
                                in [
                                    v.get("teams", {})
                                    .get("home", {})
                                    .get("team", {})
                                    .get("id"),
                                    v.get("teams", {})
                                    .get("away", {})
                                    .get("team", {})
                                    .get("id"),
                                ]
                            ),
                            None,
                        )
                        self.log.debug(
                            f"Result of check for DH game 1 in commonData: {otherGame}"
                        )

                        if not otherGame:
                            # Check league schedule
                            otherGame = next(
                                (
                                    {"gamePk": v["gamePk"], "gameDate": v["gameDate"]}
                                    for v in self.commonData.get(0, {}).get(
                                        "leagueSchedule", []
                                    )
                                    if v.get("gamePk") != game["gamePk"]
                                    and v.get("doubleHeader") == "Y"
                                    and v.get("gameNumber") == 1
                                    and self.myTeam["id"]
                                    in [
                                        v.get("teams", {})
                                        .get("home", {})
                                        .get("team", {})
                                        .get("id"),
                                        v.get("teams", {})
                                        .get("away", {})
                                        .get("team", {})
                                        .get("id"),
                                    ]
                                ),
                                None,
                            )
                            self.log.debug(
                                f"Result of check for DH game 1 in leagueSchedule: {otherGame}"
                            )

                        if not otherGame:
                            # Get schedule data from MLB
                            self.log.debug(
                                f"Getting schedule data for team id [{self.myTeam['id']}] and date [{self.today['Y-m-d']}]..."
                            )
                            sched = self.api_call(
                                "schedule",
                                {
                                    "sportId": 1,
                                    "date": self.today["Y-m-d"],
                                    "teamId": self.myTeam["id"],
                                    "fields": "dates,date,games,gamePk,gameDate,doubleHeader,gameNumber",
                                },
                            )
                            schedGames = sched["dates"][
                                next(
                                    (
                                        i
                                        for i, x in enumerate(sched["dates"])
                                        if x["date"] == self.today["Y-m-d"]
                                    ),
                                    0,
                                )
                            ]["games"]
                            otherGame = next(
                                (
                                    v
                                    for v in schedGames
                                    if v.get("gamePk") != game["gamePk"]
                                    and v.get("doubleHeader") == "Y"
                                    and v.get("gameNumber") == 1
                                ),
                                None,
                            )
                            self.log.debug(
                                f"Result of check for DH game 1 in MLB schedule data: {otherGame}"
                            )

                        if otherGame:
                            # Replace gameDate for straight doubleheader game 2 to reflect game 1 + 3 hours
                            self.log.debug(f"DH Game 1: {otherGame['gamePk']}")
                            game["gameDate"] = (
                                datetime.strptime(
                                    otherGame["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                ).replace(tzinfo=pytz.utc)
                                + timedelta(hours=3)
                            ).strftime("%Y-%m-%dT%H:%M:%SZ")
                            self.log.info(
                                f"Replaced game time for DH Game 2 [{game['gamePk']}] to 3 hours after Game 1 [{otherGame['gamePk']}] game time: [{game['gameDate']}] -- pkData['schedule']['gameDate']: [{pkData['schedule']['gameDate']}]"
                            )
                        else:
                            self.log.debug(
                                f"Failed to find DH game 1 for DH game 2 [{game['gamePk']}]"
                            )
                    # Store game time in myTeam's timezone as well as local (homeTeam's) timezone
                    pkData.update(
                        {
                            "gameTime": {
                                "myTeam": self.convert_timezone(
                                    datetime.strptime(
                                        pkData["schedule"]["gameDate"],
                                        "%Y-%m-%dT%H:%M:%SZ",
                                    ).replace(tzinfo=pytz.utc),
                                    self.commonData[0]["myTeam"]["venue"]["timeZone"][
                                        "id"
                                    ],
                                ),
                                "homeTeam": self.convert_timezone(
                                    datetime.strptime(
                                        pkData["schedule"]["gameDate"],
                                        "%Y-%m-%dT%H:%M:%SZ",
                                    ).replace(tzinfo=pytz.utc),
                                    pkData["schedule"]["venue"]["timeZone"]["id"],
                                ),
                                "bot": self.convert_timezone(
                                    datetime.strptime(
                                        pkData["schedule"]["gameDate"],
                                        "%Y-%m-%dT%H:%M:%SZ",
                                    ).replace(tzinfo=pytz.utc),
                                    "local",
                                ),
                                "utc": datetime.strptime(
                                    pkData["schedule"]["gameDate"], "%Y-%m-%dT%H:%M:%SZ"
                                ).replace(tzinfo=pytz.utc),
                            }
                        }
                    )
                    self.log.debug("Added gameTime for pk {}".format(pk))

                    # Store a key to indicate if myTeam is home or away
                    pkData.update(
                        {
                            "homeAway": "home"
                            if game["teams"]["home"]["team"]["id"] == self.myTeam["id"]
                            else "away"
                        }
                    )
                    self.log.debug("Added homeAway for pk {}".format(pk))

                    # Team info for opponent - same info as myTeam, but stored in pk dict because it's game-specific
                    pkData.update(
                        {
                            "oppTeam": self.get_team(
                                game["teams"]["away"]["team"]["id"]
                                if pkData["homeAway"] == "home"
                                else game["teams"]["home"]["team"]["id"]
                            )
                        }
                    )
                    self.log.debug("Added oppTeam for pk {}".format(pk))

                    # Update gumbo data
                    gumboParams = {
                        "gamePk": pk,
                        "hydrate": "credits,alignment,flags",
                    }
                    # Get updated list of timestamps
                    self.log.debug("Getting timestamps for pk {}".format(pk))
                    timestamps = self.api_call("game_timestamps", {"gamePk": pk})
                    if (
                        not self.commonData.get(pk, {}).get("gumbo")
                        or (
                            self.commonData[pk]["gumbo"]
                            .get("metaData", {})
                            .get("timeStamp", "")
                            == ""
                            or self.commonData[pk]["gumbo"]["metaData"]["timeStamp"]
                            not in timestamps
                            or len(timestamps)
                            - timestamps.index(
                                self.commonData[pk]["gumbo"]["metaData"]["timeStamp"]
                            )
                            > 3
                        )
                        or (
                            self.settings.get("Bot", {}).get(
                                "FULL_GUMBO_WHEN_FINAL", True
                            )
                            and (
                                self.commonData.get(pk, {})
                                .get("schedule", {})
                                .get("status", {})
                                .get("abstractGameCode")
                                == "F"
                                or self.commonData.get(pk, {})
                                .get("schedule", {})
                                .get("status", {})
                                .get("codedGameState")
                                in [
                                    "C",
                                    "D",
                                    "U",
                                    "T",
                                ]
                            )
                        )
                    ):
                        # Get full gumbo
                        self.log.debug("Getting full gumbo data for pk {}".format(pk))
                        gumbo = self.api_call("game", gumboParams)
                    else:
                        self.log.debug(
                            f"Latest timestamp from StatsAPI: {timestamps[-1]}; latest timestamp in gumbo cache: {self.commonData[pk]['gumbo'].get('metaData', {}).get('timeStamp')} for pk {pk}"
                        )

                        gumbo = self.commonData[pk].get("gumbo", {})
                        if len(timestamps) == 0 or timestamps[-1] == gumbo.get(
                            "metaData", {}
                        ).get("timeStamp"):
                            # We're up to date
                            self.log.debug(
                                "Gumbo data is up to date for pk {}".format(pk)
                            )
                        else:
                            # Get diff patch to bring us up to date
                            self.log.debug(
                                "Getting gumbo diff patch for pk {}".format(pk)
                            )
                            diffPatch = self.api_call(
                                "game_diff",
                                {
                                    "gamePk": pk,
                                    "startTimecode": gumbo["metaData"]["timeStamp"],
                                    "endTimecode": timestamps[-1:],
                                },
                                force=True,
                            )  # use force=True due to MLB-StatsAPI bug #31
                            # Check if patch is actually the full gumbo data
                            if isinstance(diffPatch, dict) and diffPatch.get("gamePk"):
                                # Full gumbo data was returned
                                self.log.debug(
                                    f"Full gumbo data was returned instead of a patch for pk {pk}. No need to patch!"
                                )
                                gumbo = diffPatch
                            else:
                                # Patch the dict
                                self.log.debug(
                                    "Patching gumbo data for pk {}".format(pk)
                                )
                                if self.patch_dict(
                                    self.commonData[pk]["gumbo"], diffPatch
                                ):  # Patch in place
                                    # True result —- patching was successful
                                    gumbo = self.commonData[pk][
                                        "gumbo"
                                    ]  # Carry forward
                                else:
                                    # Get full gumbo
                                    self.log.debug(
                                        "Since patching encountered an error, getting full gumbo data for pk {}".format(
                                            pk
                                        )
                                    )
                                    gumbo = self.api_call("game", gumboParams)

                    # Include gumbo data
                    pkData.update({"timestamps": timestamps, "gumbo": gumbo})
                    self.log.debug("Added gumbo data for pk {}".format(pk))

                    # Formatted Boxscore Info
                    pkData.update({"boxscore": self.format_boxscore_data(gumbo)})
                    self.log.debug("Added boxscore for pk {}".format(pk))

                    # Update hitter stats vs. probable pitchers - only prior to game start if data already exists
                    if (
                        not pkData.get("awayBattersVsProb")
                        and not pkData.get("homeBattersVsProb")
                    ) or (
                        (
                            pkData["schedule"]["status"]["abstractGameCode"] != "L"
                            or pkData["schedule"]["status"]["statusCode"] == "PW"
                        )
                        and pkData["schedule"]["status"]["abstractGameCode"] != "F"
                    ):
                        self.log.debug(
                            "Adding batter vs probable pitchers for pk {}".format(pk)
                        )
                        pkData.update(
                            {
                                "awayBattersVsProb": self.get_batter_stats_vs_pitcher(
                                    batters=pkData.get("gumbo", {})
                                    .get("liveData", {})
                                    .get("boxscore", {})
                                    .get("teams", {})
                                    .get("away", {})
                                    .get("batters", []),
                                    pitcher=pkData["schedule"]["teams"]["home"]
                                    .get("probablePitcher", {})
                                    .get("id", 0),
                                ),
                                "homeBattersVsProb": self.get_batter_stats_vs_pitcher(
                                    batters=pkData.get("gumbo", {})
                                    .get("liveData", {})
                                    .get("boxscore", {})
                                    .get("teams", {})
                                    .get("home", {})
                                    .get("batters", []),
                                    pitcher=pkData["schedule"]["teams"]["away"]
                                    .get("probablePitcher", {})
                                    .get("id", 0),
                                ),
                            }
                        )

                    # Opponent last game recap/score/decisions/highlights if not against myTeam (only if doesn't already exist in data dict)

                    # Probable pitcher career stats vs. team - can't find the data for this
                    # pkData.update({'awayProbVsTeamStats':self.get_pitching_stats_vs_team()})
                    # pkData.update({'homeProbVsTeamStats':self.get_pitching_stats_vs_team()})

                    pkData.update({"lastUpdate": datetime.today()})
                    self.log.debug("Added lastUpdate for pk {}".format(pk))

                    # Make the data available
                    self.commonData.update({pk: pkData})
                    self.log.debug("Updated commonData with data for pk {}".format(pk))

        if redball.DEV:
            self.log.debug(
                "Data available for threads: {}".format(self.commonData)
            )  # debug

        return True

    def format_boxscore_data(self, gumbo):
        """Adapted from MLB-StatsAPI module.
        Given gumbo data, format lists of batters, pitchers, and other boxscore data
        """

        boxData = {}
        """boxData holds the dict to be returned"""

        # Add away column headers
        awayBatters = [
            {
                "namefield": gumbo["gameData"]["teams"]["away"]["teamName"]
                + " Batters",
                "ab": "AB",
                "r": "R",
                "h": "H",
                "rbi": "RBI",
                "bb": "BB",
                "k": "K",
                "lob": "LOB",
                "avg": "AVG",
                "ops": "OPS",
                "personId": 0,
                "substitution": False,
                "note": "",
                "name": gumbo["gameData"]["teams"]["away"]["teamName"] + " Batters",
                "position": "",
                "obp": "OBP",
                "slg": "SLG",
                "battingOrder": "",
            }
        ]
        for batterId_int in [
            x
            for x in gumbo["liveData"]["boxscore"]["teams"]["away"]["batters"]
            if gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                "ID" + str(x)
            ].get("battingOrder")
        ]:
            batterId = str(batterId_int)
            namefield = (
                str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["battingOrder"]
                )[0]
                if str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["battingOrder"]
                )[-1]
                == "0"
                else "   "
            )
            namefield += " " + gumbo["liveData"]["boxscore"]["teams"]["away"][
                "players"
            ]["ID" + batterId]["stats"]["batting"].get("note", "")
            namefield += (
                gumbo["gameData"]["players"]["ID" + batterId]["boxscoreName"]
                + "  "
                + gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                    "ID" + batterId
                ]["position"]["abbreviation"]
            )
            batter = {
                "namefield": namefield,
                "ab": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["atBats"]
                ),
                "r": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["runs"]
                ),
                "h": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["hits"]
                ),
                "rbi": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["rbi"]
                ),
                "bb": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["baseOnBalls"]
                ),
                "k": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["strikeOuts"]
                ),
                "lob": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["leftOnBase"]
                ),
                "avg": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["seasonStats"]["batting"]["avg"]
                ),
                "ops": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["seasonStats"]["batting"]["ops"]
                ),
                "personId": batterId_int,
                "battingOrder": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["battingOrder"]
                ),
                "substitution": False
                if str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["battingOrder"]
                )[-1]
                == "0"
                else True,
                "note": gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                    "ID" + batterId
                ]["stats"]["batting"].get("note", ""),
                "name": gumbo["gameData"]["players"]["ID" + batterId]["boxscoreName"],
                "position": gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                    "ID" + batterId
                ]["position"]["abbreviation"],
                "obp": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["seasonStats"]["batting"]["obp"]
                ),
                "slg": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + batterId
                    ]["seasonStats"]["batting"]["slg"]
                ),
            }
            awayBatters.append(batter)

        # Add home column headers
        homeBatters = [
            {
                "namefield": gumbo["gameData"]["teams"]["home"]["teamName"]
                + " Batters",
                "ab": "AB",
                "r": "R",
                "h": "H",
                "rbi": "RBI",
                "bb": "BB",
                "k": "K",
                "lob": "LOB",
                "avg": "AVG",
                "ops": "OPS",
                "personId": 0,
                "substitution": False,
                "note": "",
                "name": gumbo["gameData"]["teams"]["home"]["teamName"] + " Batters",
                "position": "",
                "obp": "OBP",
                "slg": "SLG",
                "battingOrder": "",
            }
        ]
        for batterId_int in [
            x
            for x in gumbo["liveData"]["boxscore"]["teams"]["home"]["batters"]
            if gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                "ID" + str(x)
            ].get("battingOrder")
        ]:
            batterId = str(batterId_int)
            namefield = (
                str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["battingOrder"]
                )[0]
                if str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["battingOrder"]
                )[-1]
                == "0"
                else "   "
            )
            namefield += " " + gumbo["liveData"]["boxscore"]["teams"]["home"][
                "players"
            ]["ID" + batterId]["stats"]["batting"].get("note", "")
            namefield += (
                gumbo["gameData"]["players"]["ID" + batterId]["boxscoreName"]
                + "  "
                + gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                    "ID" + batterId
                ]["position"]["abbreviation"]
            )
            batter = {
                "namefield": namefield,
                "ab": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["atBats"]
                ),
                "r": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["runs"]
                ),
                "h": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["hits"]
                ),
                "rbi": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["rbi"]
                ),
                "bb": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["baseOnBalls"]
                ),
                "k": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["strikeOuts"]
                ),
                "lob": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["stats"]["batting"]["leftOnBase"]
                ),
                "avg": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["seasonStats"]["batting"]["avg"]
                ),
                "ops": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["seasonStats"]["batting"]["ops"]
                ),
                "personId": batterId_int,
                "battingOrder": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["battingOrder"]
                ),
                "substitution": False
                if str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["battingOrder"]
                )[-1]
                == "0"
                else True,
                "note": gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                    "ID" + batterId
                ]["stats"]["batting"].get("note", ""),
                "name": gumbo["gameData"]["players"]["ID" + batterId]["boxscoreName"],
                "position": gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                    "ID" + batterId
                ]["position"]["abbreviation"],
                "obp": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["seasonStats"]["batting"]["obp"]
                ),
                "slg": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + batterId
                    ]["seasonStats"]["batting"]["slg"]
                ),
            }
            homeBatters.append(batter)

        boxData.update({"awayBatters": awayBatters})
        boxData.update({"homeBatters": homeBatters})

        # Add away team totals
        boxData.update(
            {
                "awayBattingTotals": {
                    "namefield": "Totals",
                    "ab": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "batting"
                        ]["atBats"]
                    ),
                    "r": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "batting"
                        ]["runs"]
                    ),
                    "h": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "batting"
                        ]["hits"]
                    ),
                    "rbi": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "batting"
                        ]["rbi"]
                    ),
                    "bb": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "batting"
                        ]["baseOnBalls"]
                    ),
                    "k": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "batting"
                        ]["strikeOuts"]
                    ),
                    "lob": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "batting"
                        ]["leftOnBase"]
                    ),
                    "avg": "",
                    "ops": "",
                    "obp": "",
                    "slg": "",
                    "name": "Totals",
                    "position": "",
                    "note": "",
                    "substitution": False,
                    "battingOrder": "",
                    "personId": 0,
                }
            }
        )
        # Add home team totals
        boxData.update(
            {
                "homeBattingTotals": {
                    "namefield": "Totals",
                    "ab": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "batting"
                        ]["atBats"]
                    ),
                    "r": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "batting"
                        ]["runs"]
                    ),
                    "h": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "batting"
                        ]["hits"]
                    ),
                    "rbi": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "batting"
                        ]["rbi"]
                    ),
                    "bb": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "batting"
                        ]["baseOnBalls"]
                    ),
                    "k": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "batting"
                        ]["strikeOuts"]
                    ),
                    "lob": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "batting"
                        ]["leftOnBase"]
                    ),
                    "avg": "",
                    "ops": "",
                    "obp": "",
                    "slg": "",
                    "name": "Totals",
                    "position": "",
                    "note": "",
                    "substitution": False,
                    "battingOrder": "",
                    "personId": 0,
                }
            }
        )

        # Get batting notes
        awayBattingNotes = {}
        for n in gumbo["liveData"]["boxscore"]["teams"]["away"]["note"]:
            awayBattingNotes.update(
                {len(awayBattingNotes): n["label"] + "-" + n["value"]}
            )

        homeBattingNotes = {}
        for n in gumbo["liveData"]["boxscore"]["teams"]["home"]["note"]:
            homeBattingNotes.update(
                {len(homeBattingNotes): n["label"] + "-" + n["value"]}
            )

        boxData.update({"awayBattingNotes": awayBattingNotes})
        boxData.update({"homeBattingNotes": homeBattingNotes})

        # Get pitching box
        # Add away column headers
        awayPitchers = [
            {
                "namefield": gumbo["gameData"]["teams"]["away"]["teamName"]
                + " Pitchers",
                "ip": "IP",
                "h": "H",
                "r": "R",
                "er": "ER",
                "bb": "BB",
                "k": "K",
                "hr": "HR",
                "era": "ERA",
                "p": "P",
                "s": "S",
                "name": gumbo["gameData"]["teams"]["away"]["teamName"] + " Pitchers",
                "personId": 0,
                "note": "",
            }
        ]
        for pitcherId_int in gumbo["liveData"]["boxscore"]["teams"]["away"]["pitchers"]:
            if pitcherId_int == 0:
                self.log.warning("Invalid pitcher id found: 0")
                continue

            pitcherId = str(pitcherId_int)
            namefield = gumbo["gameData"]["players"]["ID" + pitcherId]["boxscoreName"]
            namefield += (
                "  "
                + gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                    "ID" + pitcherId
                ]["stats"]["pitching"].get("note", "")
                if gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                    "ID" + pitcherId
                ]["stats"]["pitching"].get("note")
                else ""
            )
            pitcher = {
                "namefield": namefield,
                "ip": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["inningsPitched"]
                ),
                "h": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["hits"]
                ),
                "r": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["runs"]
                ),
                "er": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["earnedRuns"]
                ),
                "bb": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["baseOnBalls"]
                ),
                "k": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["strikeOuts"]
                ),
                "hr": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["homeRuns"]
                ),
                "p": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"].get(
                        "pitchesThrown",
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                            "ID" + pitcherId
                        ]["stats"]["pitching"].get("numberOfPitches", 0),
                    )
                ),
                "s": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["strikes"]
                ),
                "era": str(
                    gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                        "ID" + pitcherId
                    ]["seasonStats"]["pitching"]["era"]
                ),
                "name": gumbo["gameData"]["players"]["ID" + pitcherId]["boxscoreName"],
                "personId": pitcherId_int,
                "note": gumbo["liveData"]["boxscore"]["teams"]["away"]["players"][
                    "ID" + pitcherId
                ]["stats"]["pitching"].get("note", ""),
            }
            awayPitchers.append(pitcher)

        boxData.update({"awayPitchers": awayPitchers})

        # Add home column headers
        homePitchers = [
            {
                "namefield": gumbo["gameData"]["teams"]["home"]["teamName"]
                + " Pitchers",
                "ip": "IP",
                "h": "H",
                "r": "R",
                "er": "ER",
                "bb": "BB",
                "k": "K",
                "hr": "HR",
                "era": "ERA",
                "p": "P",
                "s": "S",
                "name": gumbo["gameData"]["teams"]["home"]["teamName"] + " Pitchers",
                "personId": 0,
                "note": "",
            }
        ]
        for pitcherId_int in gumbo["liveData"]["boxscore"]["teams"]["home"]["pitchers"]:
            if pitcherId_int == 0:
                self.log.warning("Invalid pitcher id found: 0")
                continue

            pitcherId = str(pitcherId_int)
            namefield = gumbo["gameData"]["players"]["ID" + pitcherId]["boxscoreName"]
            namefield += (
                "  "
                + gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                    "ID" + pitcherId
                ]["stats"]["pitching"].get("note", "")
                if gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                    "ID" + pitcherId
                ]["stats"]["pitching"].get("note")
                else ""
            )
            pitcher = {
                "namefield": namefield,
                "ip": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["inningsPitched"]
                ),
                "h": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["hits"]
                ),
                "r": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["runs"]
                ),
                "er": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["earnedRuns"]
                ),
                "bb": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["baseOnBalls"]
                ),
                "k": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["strikeOuts"]
                ),
                "hr": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["homeRuns"]
                ),
                "p": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"].get(
                        "pitchesThrown",
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                            "ID" + pitcherId
                        ]["stats"]["pitching"].get("numberOfPitches", 0),
                    )
                ),
                "s": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["stats"]["pitching"]["strikes"]
                ),
                "era": str(
                    gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                        "ID" + pitcherId
                    ]["seasonStats"]["pitching"]["era"]
                ),
                "name": gumbo["gameData"]["players"]["ID" + pitcherId]["boxscoreName"],
                "personId": pitcherId_int,
                "note": gumbo["liveData"]["boxscore"]["teams"]["home"]["players"][
                    "ID" + pitcherId
                ]["stats"]["pitching"].get("note", ""),
            }
            homePitchers.append(pitcher)

        boxData.update({"homePitchers": homePitchers})

        # Get away team totals
        boxData.update(
            {
                "awayPitchingTotals": {
                    "namefield": "Totals",
                    "ip": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "pitching"
                        ]["inningsPitched"]
                    ),
                    "h": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "pitching"
                        ]["hits"]
                    ),
                    "r": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "pitching"
                        ]["runs"]
                    ),
                    "er": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "pitching"
                        ]["earnedRuns"]
                    ),
                    "bb": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "pitching"
                        ]["baseOnBalls"]
                    ),
                    "k": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "pitching"
                        ]["strikeOuts"]
                    ),
                    "hr": str(
                        gumbo["liveData"]["boxscore"]["teams"]["away"]["teamStats"][
                            "pitching"
                        ]["homeRuns"]
                    ),
                    "p": "",
                    "s": "",
                    "era": "",
                    "name": "Totals",
                    "personId": 0,
                    "note": "",
                }
            }
        )

        # Get home team totals
        boxData.update(
            {
                "homePitchingTotals": {
                    "namefield": "Totals",
                    "ip": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "pitching"
                        ]["inningsPitched"]
                    ),
                    "h": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "pitching"
                        ]["hits"]
                    ),
                    "r": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "pitching"
                        ]["runs"]
                    ),
                    "er": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "pitching"
                        ]["earnedRuns"]
                    ),
                    "bb": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "pitching"
                        ]["baseOnBalls"]
                    ),
                    "k": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "pitching"
                        ]["strikeOuts"]
                    ),
                    "hr": str(
                        gumbo["liveData"]["boxscore"]["teams"]["home"]["teamStats"][
                            "pitching"
                        ]["homeRuns"]
                    ),
                    "p": "",
                    "s": "",
                    "era": "",
                    "name": "Totals",
                    "personId": 0,
                    "note": "",
                }
            }
        )

        # Get game info
        boxData.update({"gameBoxInfo": gumbo["liveData"]["boxscore"].get("info", [])})

        return boxData

    def get_batter_stats_vs_pitcher(self, batters, pitcher):
        # batters = list of personIds, pitcher = personId
        if batters == [] or pitcher == 0:
            return []
        params = {
            "personIds": ",".join([str(x) for x in batters]),
            "hydrate": "stats(group=[hitting],type=[vsPlayer],opposingPlayerId={},sportId=1)".format(
                pitcher
            ),
        }
        r = self.api_call("people", params)

        return r["people"]

    def get_pitching_stats_vs_team(self, personId, teamId):
        # Not working yet--can't find endpoint to return career pitching stats vs. team
        params = {
            "personIds": personId,
            "hydrate": "stats(group=[pitching],type=[vsTeamTotal],opposingTeamId={},sportId=1)".format(
                teamId
            ),
        }
        vsTeamStats = self.api_call("people", params)
        return vsTeamStats["people"][0]["stats"][0]["splits"][0]["stat"]

    def get_schedule_data(
        self,
        pks=None,
        d=None,
        sd=None,
        ed=None,
        t=None,
        h="team(division,league),game(content(editorial(preview),decisions,gamenotes,highlights(highlights))),linescore,scoringplays,probablePitcher(note),broadcasts(all),venue(timezone),weather,officials,flags",
    ):
        # pks = single gamePk or comma-separated list (string), d = date ('%Y-%m-%d'), sd = start date, ed = end date,
        # t = teamId, h = hydration(s)
        # "hydrations" : [ "team", "tickets", "game(content)", "game(content(all))", "game(content(media(all)))", "game(content(editorial(all)))", "game(content(highlights(all)))", "game(content(editorial(preview)))", "game(content(editorial(recap)))", "game(content(editorial(articles)))", "game(content(editorial(wrap)))", "game(content(media(epg)))", "game(content(media(milestones)))", "game(content(highlights(scoreboard)))", "game(content(highlights(scoreboardPreview)))", "game(content(highlights(highlights)))", "game(content(highlights(gamecenter)))", "game(content(highlights(milestone)))", "game(content(highlights(live)))", "game(content(media(featured)))", "game(content(summary))", "game(content(gamenotes))", "game(tickets)", "game(atBatTickets)", "game(promotions)", "game(atBatPromotions)", "game(sponsorships)", "linescore", "decisions", "scoringplays", "broadcasts", "broadcasts(all)", "radioBroadcasts", "metadata", "game(seriesSummary)", "seriesStatus", "event(performers)", "event(promotions)", "event(timezone)", "event(tickets)", "event(venue)", "event(designations)", "event(game)", "event(status)", "venue", "weather", "gameInfo", "officials", "probableOfficials" ]
        # team(division,league),game(content(editorial(preview),gamenotes,highlights(highlights))),linescore,decisions,probablePitcher(note),broadcasts(all),venue(timezone),weather,officials,flags
        params = {"sportId": 1}
        if pks:
            params.update({"gamePks": pks})
        if d:
            params.update({"date": d})
        elif sd and ed:
            params.update({"startDate": sd, "endDate": ed})
        if t:
            params.update({"teamId": t})
        if h:
            params.update({"hydrate": h})
        s = self.api_call("schedule", params)
        return s

    def get_team(self, t, h="league,division,venue(timezone)", s=None):
        # t = teamId, h = hydrate, s = season
        params = {"teamId": t, "hydrate": h}
        if s:
            params.update({"season": s})

        return self.api_call("team", params)["teams"][0]

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

    def insert_thread_to_db(self, pk, threadId, threadType):
        # pk = gamePk (or list of gamePks), threadId = thread object returned from Reddit (OFF+date for off day threads), threadType = ['gameday', 'game', 'post', 'off', 'weekly']
        q = "insert or ignore into {}threads (gamePk, type, gameDate, id, dateCreated, dateUpdated) values".format(
            self.dbTablePrefix
        )
        if isinstance(pk, list):
            for k in pk:
                if q[:-1] == ")":
                    q += ","
                q += " ({}, '{}', '{}', '{}', {}, {})".format(
                    k,
                    threadType,
                    self.today["Y-m-d"],
                    threadId,
                    time.time(),
                    time.time(),
                )
        else:
            q += " ({}, '{}', '{}', '{}', {}, {})".format(
                pk, threadType, self.today["Y-m-d"], threadId, time.time(), time.time()
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

    def prep_and_post(self, thread, pk=None, postFooter=None):
        # thread = ['weekly', 'off', 'gameday', 'game', 'post']
        # pk = gamePk or list of gamePks
        # postFooter = text to append to post body, but not to include in return text value
        #   (normally contains a timestamp that would prevent comparison next time to check for changes)

        # Collect data for the game(s), or skip if no pk provided (generic data collected at start of daily loop)
        if pk:
            self.collect_data(pk)

        try:
            title = self.render_template(
                thread=thread,
                templateType="title",
                data=self.commonData,
                gamePk=pk,
                settings=self.settings,
            )
            self.log.debug("Rendered {} title: {}".format(thread, title))
        except Exception as e:
            self.log.error("Error rendering {} title: {}".format(thread, e))
            title = None
            self.error_notification(f"Error rendering title for {thread} thread")

        sticky = self.settings.get("Reddit", {}).get("STICKY", False) is True
        title_mod = (
            self.settings.get("Weekly Thread", {}).get("TITLE_MOD", "")
            if thread == "weekly"
            else self.settings.get("Off Day Thread", {}).get("TITLE_MOD", "")
            if thread == "off"
            else self.settings.get("Game Day Thread", {}).get("TITLE_MOD", "")
            if thread == "gameday"
            else self.settings.get("Game Thread", {}).get("TITLE_MOD", "")
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get("TITLE_MOD", "")
            if thread == "post"
            else ""
        )
        if "upper" in title_mod.lower():
            title = title.upper()
            self.log.info(
                f"Converted {thread} title to upper case per TITLE_MOD setting: [{title}]"
            )
        if "lower" in title_mod.lower():
            title = title.lower()
            self.log.info(
                f"Converted {thread} title to lower case per TITLE_MOD setting: [{title}]"
            )
        if "title" in title_mod.lower():
            title = title.title()
            self.log.info(
                f"Converted {thread} title to title case per TITLE_MOD setting: [{title}]"
            )
        if "nospaces" in title_mod.lower():
            title = title.replace(" ", "")
            self.log.info(
                f"Removed spaces from {thread} title per TITLE_MOD setting: [{title}]"
            )

        # Check if post already exists
        theThread = None
        text = ""
        try:
            for p in self.lemmy.listPosts():
                if (
                    p["creator"]["name"] == self.lemmy.username
                    and p["post"]["name"] == title
                ):
                    # Found existing thread...
                    self.log.info("Found an existing {} thread...".format(thread))
                    theThread = p
                    if theThread["post"]["body"].find("\n\nLast Updated") != -1:
                        text = theThread["post"]["body"][
                            0 : theThread["post"]["body"].find("\n\nLast Updated:")
                        ]
                    elif theThread["post"]["body"].find("\n\nPosted") != -1:
                        text = theThread["post"]["body"][
                            0 : theThread["post"]["body"].find("\n\nPosted:")
                        ]
                    else:
                        text = theThread["post"]["body"]

                    if sticky:
                        self.sticky_thread(theThread)

                    break
        except Exception as e:
            self.log.error("Error checking community for existing posts: {}".format(e))
            self.error_notification("Error checking community for existing posts")

        if not theThread:
            try:
                text = self.render_template(
                    thread=thread,
                    templateType="thread",
                    data=self.commonData,
                    gamePk=pk,
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
                theThread = self.submit_lemmy_post(
                    title=title,
                    text=fullText,
                    sticky=sticky,
                )
                self.log.info("Submitted {} thread: ({}).".format(thread, theThread))
            except Exception as e:
                self.log.error("Error submitting {} thread: {}".format(thread, e))
                theThread = None
                self.error_notification(f"Error submitting {thread} thread")

        if theThread:
            if isinstance(pk, list):
                self.log.debug(
                    "List of gamePks to associate in DB with {} thread: {}...".format(
                        thread, pk
                    )
                )
                for x in pk:
                    self.log.debug(
                        "Inserting {} thread into DB for game {}...".format(thread, x)
                    )
                    self.insert_thread_to_db(x, theThread["post"]["id"], thread)
            elif pk:
                self.log.debug(
                    "Inserting {} thread into DB for game {}...".format(thread, pk)
                )
                self.insert_thread_to_db(pk, theThread["post"]["id"], thread)
            else:
                self.log.debug(
                    "Inserting {} thread into db as {}...".format(
                        thread, self.today["Ymd"]
                    )
                )
                self.insert_thread_to_db(
                    int(self.today["Ymd"]), theThread["post"]["id"], thread
                )

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
                    event=f"{self.myTeam['teamName']} {thread.title()} Thread Posted",
                    description=f"""{self.myTeam['teamName']} {thread} thread was posted to c/{self.settings["Lemmy"]["COMMUNITY_NAME"]} at {self.convert_timezone(datetime.utcfromtimestamp(theThread.created_utc),'local').strftime('%I:%M %p %Z')}\nThread title: {theThread.title}\nURL: {theThread.shortlink}""",
                    priority=prowlPriority,
                    url=theThread.shortlink,
                    appName=f"redball - {self.bot.name}",
                )
        else:
            self.log.warning("No thread object present. Something went wrong!")

        return (theThread, text)

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

    def submit_lemmy_post(
        self,
        title,
        text,
        sub=None,
        sticky=False,
    ):
        if sub:
            community = self.lemmy.getCommunity(sub)
        else:
            community = self.lemmy.community

        title = title.strip("\n")
        text = self._truncate_post(text)
        post = self.lemmy.submitPost(
            title=title,
            body=text,
        )
        self.log.info("Thread ({}) submitted: {}".format(title, post))

        if sticky:
            self.lemmy.stickyPost(post["post"]["id"])

        return post

    def render_template(self, thread, templateType, **kwargs):
        setting = "{}_TEMPLATE".format(templateType.upper())
        template = (
            self.settings.get("Weekly Thread", {}).get(setting, "")
            if thread == "weekly"
            else self.settings.get("Off Day Thread", {}).get(setting, "")
            if thread == "off"
            else self.settings.get("Game Day Thread", {}).get(setting, "")
            if thread == "gameday"
            else self.settings.get("Game Thread", {}).get(setting, "")
            if thread == "game"
            else self.settings.get("Post Game Thread", {}).get(setting, "")
            if thread == "post"
            else self.settings.get("Comments", {}).get(setting, "")
            if thread == "comment"
            else ""
        )
        try:
            template = self.LOOKUP.get_template(template)
            return template.render(**kwargs)
        except Exception:
            self.log.error(
                "Error rendering template [{}] for {} {}. Falling back to default template. Error: {}".format(
                    template.filename,
                    thread,
                    templateType,
                    mako.exceptions.text_error_template().render(),
                )
            )
            self.error_notification(
                f"Error rendering {thread} {templateType} template [{template.filename}]"
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
        self.log.info("Stickying thread [{}]...".format(thread["post"]["id"]))
        try:
            self.lemmy.stickyPost(thread["post"]["id"])
            self.log.info("Thread [{}] stickied...".format(thread["post"]["id"]))
        except Exception:
            self.log.warning(
                "Sticky of thread [{}] failed. Check mod privileges or the thread may have already been sticky.".format(
                    thread["post"]["id"]
                )
            )

    def unsticky_threads(self, threads):
        for t in threads:
            try:
                self.log.debug(
                    "Attempting to unsticky thread [{}]".format(t["post"]["id"])
                )
                self.lemmy.unStickyPost(t["post"]["id"])
            except Exception:
                self.log.debug(
                    "Unsticky of thread [{}] failed. Check mod privileges or the thread may not have been sticky.".format(
                        t.id
                    )
                )

    def api_call(self, endpoint, params, retries=-1, force=False):
        s = {}
        while retries != 0:
            try:
                s = statsapi.get(endpoint, params, force=force)
                break
            except Exception as e:
                if retries == 0:
                    self.log.error(
                        "Error encountered while querying StatsAPI. Continuing. Error: {}".format(
                            e
                        )
                    )
                elif retries > 0:
                    retries -= 1
                    self.log.error(
                        "Error encountered while querying StatsAPI. Retrying in 30 seconds ({} additional retries remaining). Error: {}".format(
                            retries, e
                        )
                    )
                    self.sleep(30)
                else:
                    self.log.error(
                        "Error encountered while querying StatsAPI. Retrying in 30 seconds. Error: {}".format(
                            e
                        )
                    )
                    self.sleep(30)

        return s

    def build_tables(self):
        queries = []
        queries.append(
            """CREATE TABLE IF NOT EXISTS {}threads (
                gamePk integer not null,
                type text not null,
                gameDate text not null,
                id text not null,
                dateCreated text not null,
                dateUpdated text not null,
                deleted integer default 0,
                unique (gamePk, type, id, gameDate, deleted)
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

        queries.append(
            """CREATE TABLE IF NOT EXISTS {}processedAtBats (
                id integer primary key autoincrement,
                gamePk integer not null,
                gameThreadId text not null,
                processedAtBats text not null,
                dateCreated text not null,
                dateUpdated text not null
            );""".format(
                self.dbTablePrefix
            )
        )

        queries.append(
            """CREATE TABLE IF NOT EXISTS {}comments (
                id integer primary key autoincrement,
                gamePk integer not null,
                gameThreadId text not null,
                atBatIndex integer not null,
                actionIndex integer,
                isScoringPlay integer,
                eventType text,
                myTeamBatting integer,
                commentId text not null,
                dateCreated text not null,
                dateUpdated text not null,
                deleted integer default 0
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
            self.init_lemmy()

        self.log.debug("Refreshed settings: {}".format(self.settings))

    def init_lemmy(self):
        self.log.debug(f"Initiating Lemmy API with plaw")
        with redball.REDDIT_AUTH_LOCKS[str(self.bot.redditAuth)]:
            try:
                # Check for Lemmy
                instance_name = self.settings.get("Lemmy", {}).get("INSTANCE_NAME", "")
                username = self.settings.get("Lemmy", {}).get("USERNAME", "")
                password = self.settings.get("Lemmy", {}).get("PASSWORD", "")
                community = self.settings.get("Lemmy", {}).get("COMMUNITY_NAME")

                if "" in [instance_name, username, password, community]:
                    self.log.warn("Lemmy not fully configured")

                self.lemmy = plaw.Lemmy(instance_name, username, password)
                self.community = self.lemmy.getCommunity(community)
            except Exception as e:
                self.log.error(
                    "Error encountered attempting to initialize Lemmy: {}".format(e)
                )
                self.error_notification("Error initializing Lemmy")
                raise

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
        142: "/c/minnesotatwins@fanaticus.social",
        145: "/c/whitesox@fanaticus.social",
        116: "/c/motorcitykitties@fanaticus.social",
        118: "/c/kcroyals@fanaticus.social",
        114: "/c/clevelandguardians@fanaticus.social",
        140: "/c/texasrangers@fanaticus.social",
        117: "/c/astros@fanaticus.social",
        133: "/c/oaklandathletics@fanaticus.social",
        108: "/c/angelsbaseball@fanaticus.social",
        136: "/c/mariners@fanaticus.social",
        111: "/c/redsox@fanaticus.social",
        147: "/c/nyyankees@fanaticus.social",
        141: "/c/torontobluejays@fanaticus.social",
        139: "/c/tampabayrays@fanaticus.social",
        110: "/c/orioles@fanaticus.social",
        138: "/c/cardinals@fanaticus.social",
        113: "/c/reds@fanaticus.social",
        134: "/c/buccos@fanaticus.social",
        112: "/c/chicubs@fanaticus.social",
        158: "/c/brewers@fanaticus.social",
        137: "/c/sfgiants@fanaticus.social",
        109: "/c/azdiamondbacks@fanaticus.social",
        115: "/c/coloradorockies@fanaticus.social",
        119: "/c/dodgers@fanaticus.social",
        135: "/c/padres@fanaticus.social",
        143: "/c/phillies@fanaticus.social",
        121: "/c/newyorkmets@fanaticus.social",
        146: "/c/miamimarlins@fanaticus.social",
        120: "/c/nationals@fanaticus.social",
        144: "/c/braves@fanaticus.social",
        0: "/c/baseball@fanaticus.social",
        "mlb": "/c/baseball@fanaticus.social",
    }

    def bot_state(self):
        """Return current state...
        Current date being monitored
        Games being monitored with current status
        Threads pending and post time
        Threads posted
        """
        try:
            botStatus = {
                "lastUpdated": datetime.today().strftime("%m/%d/%Y %I:%M:%S %p"),
                "myTeam": {
                    "id": self.myTeam["id"],
                    "name": self.myTeam["name"],
                    "shortName": self.myTeam["shortName"],
                    "teamName": self.myTeam["teamName"],
                    "link": self.myTeam["link"],
                },
                "today": self.today,
                "seasonState": self.seasonState,
                "weeklyThread": {
                    "enabled": self.settings.get("Weekly Thread", {}).get(
                        "ENABLED", True
                    )
                    and (
                        (
                            (
                                self.seasonState.startswith("off")
                                or self.seasonState == "post:out"
                            )
                            and self.settings.get("Weekly Thread", {}).get(
                                "OFFSEASON_ONLY", True
                            )
                        )
                        or not self.settings.get("Weekly Thread", {}).get(
                            "OFFSEASON_ONLY", True
                        )
                    ),
                    "postTime": self.weekly.get("postTime_local").strftime(
                        "%m/%d/%Y %I:%M:%S %p"
                    )
                    if isinstance(self.weekly.get("postTime_local"), datetime)
                    else "",
                    "posted": True if self.weekly.get("weeklyThread") else False,
                    "id": self.weekly.get("weeklyThread")["post"]["id"]
                    if self.weekly.get("weeklyThread")
                    else None,
                    "url": self.weekly.get("weeklyThread")["post"]["ap_id"]
                    if self.weekly.get("weeklyThread")
                    else None,
                    "title": self.weekly.get("weeklyThreadTitle")
                    if self.weekly.get("weeklyThread")
                    else None,
                },
                "offDayThread": {
                    "enabled": self.settings.get("Off Day Thread", {}).get(
                        "ENABLED", True
                    ),
                    "postTime": self.activeGames.get("off", {})
                    .get("postTime_local")
                    .strftime("%m/%d/%Y %I:%M:%S %p")
                    if isinstance(
                        self.activeGames.get("off", {}).get("postTime_local"), datetime
                    )
                    else "",
                    "posted": True
                    if self.activeGames.get("off", {}).get("offDayThread")
                    else False,
                    "id": self.activeGames.get("off", {}).get("offDayThread")["post"][
                        "id"
                    ]
                    if self.activeGames.get("off", {}).get("offDayThread")
                    else None,
                    "url": self.activeGames.get("off", {}).get("offDayThread")["post"][
                        "ap_id"
                    ]
                    if self.activeGames.get("off", {}).get("offDayThread")
                    else None,
                    "title": self.activeGames.get("off", {}).get("offDayThreadTitle")
                    if self.activeGames.get("off", {}).get("offDayThread")
                    else None,
                },
                "gameDayThread": {
                    "enabled": self.settings.get("Game Day Thread", {}).get(
                        "ENABLED", True
                    ),
                    "postTime": self.activeGames.get("gameday", {})
                    .get("postTime_local")
                    .strftime("%m/%d/%Y %I:%M:%S %p")
                    if isinstance(
                        self.activeGames.get("gameday", {}).get("postTime_local"),
                        datetime,
                    )
                    else "",
                    "posted": True
                    if self.activeGames.get("gameday", {}).get("gameDayThread")
                    else False,
                    "id": self.activeGames.get("gameday", {}).get("gameDayThread")[
                        "post"
                    ]["id"]
                    if self.activeGames.get("gameday", {}).get("gameDayThread")
                    else None,
                    "url": self.activeGames.get("gameday", {}).get("gameDayThread")[
                        "post"
                    ]["ap_id"]
                    if self.activeGames.get("gameday", {}).get("gameDayThread")
                    else None,
                    "title": self.activeGames.get("gameday", {}).get(
                        "gameDayThreadTitle"
                    )
                    if self.activeGames.get("gameday", {}).get("gameDayThread")
                    else None,
                },
                "games": [
                    {
                        k: {
                            "gamePk": k,
                            "status": self.commonData[k]["schedule"]["status"],
                            "oppTeam": self.commonData[k]["oppTeam"],
                            "homeAway": self.commonData[k]["homeAway"],
                            "threads": {
                                "game": {
                                    "enabled": self.settings.get("Game Thread", {}).get(
                                        "ENABLED", True
                                    ),
                                    "postTime": v.get("postTime_local").strftime(
                                        "%m/%d/%Y %I:%M:%S %p"
                                    )
                                    if isinstance(v.get("postTime_local"), datetime)
                                    else "",
                                    "posted": True if v.get("gameThread") else False,
                                    "id": v.get("gameThread")["post"]["id"]
                                    if v.get("gameThread")
                                    else None,
                                    "url": v.get("gameThread")["post"]["ap_id"]
                                    if v.get("gameThread")
                                    else None,
                                    "title": v.get("gameThreadTitle")
                                    if v.get("gameThread")
                                    else None,
                                },
                                "post": {
                                    "enabled": self.settings.get(
                                        "Post Game Thread", {}
                                    ).get("ENABLED", True),
                                    "posted": True
                                    if v.get("postGameThread")
                                    else False,
                                    "id": v.get("postGameThread")["post"]["id"]
                                    if v.get("postGameThread")
                                    else None,
                                    "url": v.get("postGameThread")["post"]["ap_id"]
                                    if v.get("postGameThread")
                                    else None,
                                    "title": v.get("postGameThreadTitle")
                                    if v.get("postGameThread")
                                    else None,
                                },
                            },
                        }
                    }
                    for k, v in self.activeGames.items()
                    if isinstance(k, int) and k > 0
                ],
            }
            botStatus["myTeam"].pop("nextGame", None)  # Not used, junks up the log

            botStatus.update(
                {
                    "summary": {
                        "text": "Today is {}. Season state: {}.".format(
                            botStatus["today"]["Y-m-d"], botStatus["seasonState"]
                        ),
                        "html": "Today is {}. Season state: {}.".format(
                            botStatus["today"]["Y-m-d"], botStatus["seasonState"]
                        ),
                        "markdown": "Today is {}. Season state: {}.".format(
                            botStatus["today"]["Y-m-d"], botStatus["seasonState"]
                        ),
                    }
                }
            )

            # Weekly thread
            botStatus["summary"]["text"] += "\n\nWeekly thread{}".format(
                " disabled."
                if not botStatus["weeklyThread"]["enabled"]
                else " suppressed except during off season."
                if self.settings.get("Weekly Thread", {}).get("OFFSEASON_ONLY", True)
                and not (
                    botStatus["seasonState"].startswith("off")
                    or botStatus["seasonState"] == "post:out"
                )
                else " failed to post (check log for error)"
                if not botStatus["weeklyThread"]["posted"]
                and datetime.strptime(
                    botStatus["weeklyThread"]["postTime"], "%m/%d/%Y %I:%M:%S %p"
                )
                < datetime.today()
                else " post time: {}".format(botStatus["weeklyThread"]["postTime"])
                if not botStatus["weeklyThread"]["posted"]
                else ": {} ({} - {})".format(
                    botStatus["weeklyThread"]["title"],
                    botStatus["weeklyThread"]["id"],
                    botStatus["weeklyThread"]["url"],
                )
            )
            botStatus["summary"][
                "html"
            ] += "<br /><br /><strong>Weekly thread</strong>{}".format(
                " disabled."
                if not botStatus["weeklyThread"]["enabled"]
                else " suppressed except during off season."
                if self.settings.get("Weekly Thread", {}).get("OFFSEASON_ONLY", True)
                and not (
                    botStatus["seasonState"].startswith("off")
                    or botStatus["seasonState"] == "post:out"
                )
                else " failed to post (check log for error)"
                if not botStatus["weeklyThread"]["posted"]
                and datetime.strptime(
                    botStatus["weeklyThread"]["postTime"], "%m/%d/%Y %I:%M:%S %p"
                )
                < datetime.today()
                else " post time: {}".format(botStatus["weeklyThread"]["postTime"])
                if not botStatus["weeklyThread"]["posted"]
                else ': {} (<a href="{}" target="_blank">{}</a>)'.format(
                    botStatus["weeklyThread"]["title"],
                    botStatus["weeklyThread"]["url"],
                    botStatus["weeklyThread"]["id"],
                )
            )
            botStatus["summary"]["markdown"] += "\n\n**Weekly thread**{}".format(
                " disabled."
                if not botStatus["weeklyThread"]["enabled"]
                else " suppressed except during off season."
                if self.settings.get("Weekly Thread", {}).get("OFFSEASON_ONLY", True)
                and not (
                    botStatus["seasonState"].startswith("off")
                    or botStatus["seasonState"] == "post:out"
                )
                else " failed to post (check log for error)"
                if not botStatus["weeklyThread"]["posted"]
                and datetime.strptime(
                    botStatus["weeklyThread"]["postTime"], "%m/%d/%Y %I:%M:%S %p"
                )
                < datetime.today()
                else " post time: {}".format(botStatus["weeklyThread"]["postTime"])
                if not botStatus["weeklyThread"]["posted"]
                else ": {} ([{}]({}))".format(
                    botStatus["weeklyThread"]["title"],
                    botStatus["weeklyThread"]["id"],
                    botStatus["weeklyThread"]["url"],
                )
            )

            if len(botStatus["games"]) == 0:
                # Off Day
                botStatus["summary"][
                    "text"
                ] += "\n\nToday is an off day{}.\n\nOff day thread{}".format(
                    " (Season Suspended)"
                    if self.commonData.get("seasonSuspended")
                    else "",
                    " disabled."
                    if not botStatus["offDayThread"]["enabled"]
                    else " suppressed during off season."
                    if self.settings.get("Off Day Thread", {}).get(
                        "SUPPRESS_OFFSEASON", True
                    )
                    and (
                        botStatus["seasonState"].startswith("off")
                        or botStatus["seasonState"] == "post:out"
                    )
                    else " failed to post (check log for error)"
                    if not botStatus["offDayThread"]["posted"]
                    and datetime.strptime(
                        botStatus["offDayThread"]["postTime"], "%m/%d/%Y %I:%M:%S %p"
                    )
                    < datetime.today()
                    else " post time: {}".format(botStatus["offDayThread"]["postTime"])
                    if not botStatus["offDayThread"]["posted"]
                    else ": {} ({} - {})".format(
                        botStatus["offDayThread"]["title"],
                        botStatus["offDayThread"]["id"],
                        botStatus["offDayThread"]["url"],
                    ),
                )
                botStatus["summary"][
                    "html"
                ] += "<br /><br />Today is an off day{}.<br /><br /><strong>Off day thread</strong>{}".format(
                    " (<strong>Season Suspended</strong>)"
                    if self.commonData.get("seasonSuspended")
                    else "",
                    " disabled."
                    if not botStatus["offDayThread"]["enabled"]
                    else " suppressed during off season."
                    if self.settings.get("Off Day Thread", {}).get(
                        "SUPPRESS_OFFSEASON", True
                    )
                    and (
                        botStatus["seasonState"].startswith("off")
                        or botStatus["seasonState"] == "post:out"
                    )
                    else " failed to post (check log for error)"
                    if not botStatus["offDayThread"]["posted"]
                    and datetime.strptime(
                        botStatus["offDayThread"]["postTime"], "%m/%d/%Y %I:%M:%S %p"
                    )
                    < datetime.today()
                    else " post time: {}".format(botStatus["offDayThread"]["postTime"])
                    if not botStatus["offDayThread"]["posted"]
                    else ': {} (<a href="{}" target="_blank">{}</a>)'.format(
                        botStatus["offDayThread"]["title"],
                        botStatus["offDayThread"]["url"],
                        botStatus["offDayThread"]["id"],
                    ),
                )
                botStatus["summary"][
                    "markdown"
                ] += "\n\nToday is an off day{}.\n\n**Off day thread**{}".format(
                    " (**Season Suspended**)"
                    if self.commonData.get("seasonSuspended")
                    else "",
                    " disabled."
                    if not botStatus["offDayThread"]["enabled"]
                    else " suppressed during off season."
                    if self.settings.get("Off Day Thread", {}).get(
                        "SUPPRESS_OFFSEASON", True
                    )
                    and (
                        botStatus["seasonState"].startswith("off")
                        or botStatus["seasonState"] == "post:out"
                    )
                    else " failed to post (check log for error)"
                    if not botStatus["offDayThread"]["posted"]
                    and datetime.strptime(
                        botStatus["offDayThread"]["postTime"], "%m/%d/%Y %I:%M:%S %p"
                    )
                    < datetime.today()
                    else " post time: {}".format(botStatus["offDayThread"]["postTime"])
                    if not botStatus["offDayThread"]["posted"]
                    else ": {} ([{}]({}))".format(
                        botStatus["offDayThread"]["title"],
                        botStatus["offDayThread"]["id"],
                        botStatus["offDayThread"]["url"],
                    ),
                )
            else:
                # Game Day
                botStatus["summary"][
                    "text"
                ] += "\n\nI am monitoring {} game{}: {}.".format(
                    len(botStatus["games"]),
                    "s" if len(botStatus["games"]) > 1 else "",
                    [k for x in botStatus["games"] for k, v in x.items()],
                )
                botStatus["summary"][
                    "html"
                ] += "<br /><br />I am monitoring <strong>{} game{}</strong>: {}.".format(
                    len(botStatus["games"]),
                    "s" if len(botStatus["games"]) > 1 else "",
                    [k for x in botStatus["games"] for k, v in x.items()],
                )
                botStatus["summary"][
                    "markdown"
                ] += "\n\nI am monitoring **{} game{}**: {}.".format(
                    len(botStatus["games"]),
                    "s" if len(botStatus["games"]) > 1 else "",
                    [k for x in botStatus["games"] for k, v in x.items()],
                )

                botStatus["summary"]["text"] += "\n\nGame Day Thread{}.".format(
                    " disabled"
                    if not botStatus["gameDayThread"]["enabled"]
                    else " skipped or failed to post (check log for error)"
                    if not botStatus["gameDayThread"]["posted"]
                    and datetime.strptime(
                        botStatus["gameDayThread"]["postTime"], "%m/%d/%Y %I:%M:%S %p"
                    )
                    < datetime.today()
                    else " post time: {}".format(botStatus["gameDayThread"]["postTime"])
                    if not botStatus["gameDayThread"]["posted"]
                    else ": {} ({} - {})".format(
                        botStatus["gameDayThread"]["title"],
                        botStatus["gameDayThread"]["id"],
                        botStatus["gameDayThread"]["url"],
                    )
                )
                botStatus["summary"][
                    "html"
                ] += "<br /><br /><strong>Game Day Thread</strong>{}.".format(
                    " disabled"
                    if not botStatus["gameDayThread"]["enabled"]
                    else " skipped or failed to post (check log for error)"
                    if not botStatus["gameDayThread"]["posted"]
                    and datetime.strptime(
                        botStatus["gameDayThread"]["postTime"], "%m/%d/%Y %I:%M:%S %p"
                    )
                    < datetime.today()
                    else " post time: {}".format(botStatus["gameDayThread"]["postTime"])
                    if not botStatus["gameDayThread"]["posted"]
                    else ': {} (<a href="{}" target="_blank">{}</a>)'.format(
                        botStatus["gameDayThread"]["title"],
                        botStatus["gameDayThread"]["url"],
                        botStatus["gameDayThread"]["id"],
                    )
                )
                botStatus["summary"]["markdown"] += "\n\n**Game Day Thread**{}.".format(
                    " disabled"
                    if not botStatus["gameDayThread"]["enabled"]
                    else " suppressed during off season."
                    if self.settings.get("Off Day Thread", {}).get(
                        "SUPPRESS_OFFSEASON", True
                    )
                    and (
                        botStatus["seasonState"].startswith("off")
                        or botStatus["seasonState"] == "post:out"
                    )
                    else " skipped or failed to post (check log for error)"
                    if not botStatus["gameDayThread"]["posted"]
                    and datetime.strptime(
                        botStatus["gameDayThread"]["postTime"], "%m/%d/%Y %I:%M:%S %p"
                    )
                    < datetime.today()
                    else " post time: {}".format(botStatus["gameDayThread"]["postTime"])
                    if not botStatus["gameDayThread"]["posted"]
                    else ": {} ([{}]({}))".format(
                        botStatus["gameDayThread"]["title"],
                        botStatus["gameDayThread"]["id"],
                        botStatus["gameDayThread"]["url"],
                    )
                )

            if len(botStatus["games"]) > 0:
                # Game and Post Game Thread(s)
                for x in botStatus["games"]:
                    for k, v in x.items():
                        botStatus["summary"]["text"] += "{}".format(
                            "\n\n{} ({}):\nGame thread{}{}".format(
                                k,
                                v.get("status", {}).get(
                                    "detailedState", "Unknown Status"
                                ),
                                " disabled."
                                if not v["threads"]["game"]["enabled"]
                                else " skipped"
                                if v["threads"]["game"].get("postTime", "") == ""
                                and not v["threads"]["game"]["posted"]
                                else " not posted (check log for errors; this is normal if DH Game 2)"
                                if not v["threads"]["game"]["posted"]
                                and datetime.strptime(
                                    v["threads"]["game"]["postTime"],
                                    "%m/%d/%Y %I:%M:%S %p",
                                )
                                < datetime.today()
                                else " post time: {}.".format(
                                    v["threads"]["game"]["postTime"]
                                )
                                if not v["threads"]["game"]["posted"]
                                else ": {} ({} - {})".format(
                                    v["threads"]["game"]["title"],
                                    v["threads"]["game"]["id"],
                                    v["threads"]["game"]["url"],
                                ),
                                "\n\nPost game thread: {} ({} - {}).".format(
                                    v["threads"]["post"]["title"],
                                    v["threads"]["post"]["id"],
                                    v["threads"]["post"]["url"],
                                )
                                if v["threads"]["post"]["posted"]
                                else "\n\nPost game thread disabled."
                                if not v["threads"]["post"]["enabled"]
                                else "",
                            )
                        )

                for x in botStatus["games"]:
                    for k, v in x.items():
                        botStatus["summary"]["html"] += "{}".format(
                            "<br /><br /><strong>{}</strong> ({}):<br /><strong>Game thread</strong>{}{}".format(
                                k,
                                v.get("status", {}).get(
                                    "detailedState", "Unknown Status"
                                ),
                                " disabled."
                                if not v["threads"]["game"]["enabled"]
                                else " skipped"
                                if v["threads"]["game"].get("postTime", "") == ""
                                and not v["threads"]["game"]["posted"]
                                else " not posted (check log for errors; this is normal if DH Game 2)"
                                if not v["threads"]["game"]["posted"]
                                and datetime.strptime(
                                    v["threads"]["game"]["postTime"],
                                    "%m/%d/%Y %I:%M:%S %p",
                                )
                                < datetime.today()
                                else " post time: {}.".format(
                                    v["threads"]["game"]["postTime"]
                                )
                                if not v["threads"]["game"]["posted"]
                                else ': {} (<a href="{}" target="_blank">{}</a>)'.format(
                                    v["threads"]["game"]["title"],
                                    v["threads"]["game"]["url"],
                                    v["threads"]["game"]["id"],
                                ),
                                '<br /><br /><strong>Post game thread</strong>: {} (<a href="{}" target="_blank">{}</a>).'.format(
                                    v["threads"]["post"]["title"],
                                    v["threads"]["post"]["url"],
                                    v["threads"]["post"]["id"],
                                )
                                if v["threads"]["post"]["posted"]
                                else "<br /><br /><strong>Post game thread</strong> disabled."
                                if not v["threads"]["post"]["enabled"]
                                else "",
                            )
                        )

                for x in botStatus["games"]:
                    for k, v in x.items():
                        botStatus["summary"]["markdown"] += "{}".format(
                            "\n\n**{}** ({}):\n\n**Game thread**{}{}".format(
                                k,
                                v.get("status", {}).get(
                                    "detailedState", "Unknown Status"
                                ),
                                " disabled."
                                if not v["threads"]["game"]["enabled"]
                                else " skipped"
                                if v["threads"]["game"].get("postTime", "") == ""
                                and not v["threads"]["game"]["posted"]
                                else " not posted (check log for errors; this is normal if DH Game 2)"
                                if not v["threads"]["game"]["posted"]
                                and datetime.strptime(
                                    v["threads"]["game"]["postTime"],
                                    "%m/%d/%Y %I:%M:%S %p",
                                )
                                < datetime.today()
                                else " post time: {}.".format(
                                    v["threads"]["game"]["postTime"]
                                )
                                if not v["threads"]["game"]["posted"]
                                else ": {} ([{}]({}))".format(
                                    v["threads"]["game"]["title"],
                                    v["threads"]["game"]["id"],
                                    v["threads"]["game"]["url"],
                                ),
                                "\n\n**Post game thread**: {} ([{}]({})).".format(
                                    v["threads"]["post"]["title"],
                                    v["threads"]["post"]["id"],
                                    v["threads"]["post"]["url"],
                                )
                                if v["threads"]["post"]["posted"]
                                else "\n\n>**Post game thread** disabled."
                                if not v["threads"]["post"]["enabled"]
                                else "",
                            )
                        )

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

    def _truncate_post(self, text):
        warning_text = " \  # Truncated, post length limit reached."
        max_length = self.settings.get("Lemmy", {}).get("POST_CHARACTER_LIMIT", 10000) - len(warning_text)
        if len(text) >= max_length:
            new_text = text[0:max_length - 1]
            new_text += warning_text
        else:
            new_text = text
        return new_text
