"""redball bot management platform

Created by Todd Roberts

https://github.com/toddrob99/redball
"""

import argparse
import cherrypy
import os
import sys
import threading
import time
import tzlocal

from . import bot, config, database, logger, version

__version__ = version.VERSION
"""Installed version of redball"""

APP_NAME = "redball"

parser = argparse.ArgumentParser(
    prog="redball",
    description="Start redball bot management platform. See https://github.com/toddrob99/redball for details.",
)
parser.add_argument(
    "--verbose",
    "-v",
    action="store_true",
    dest="verbose",
    help="Enable debug logging to console for startup",
)
parser.add_argument(
    "--quiet",
    "-q",
    action="store_true",
    dest="quiet",
    help="Disable console logging for startup",
)
parser.add_argument(
    "--suppress",
    "-s",
    action="store_true",
    dest="suppress_bots",
    help="Prevent bots from running on startup (override auto run setting)",
)
parser.add_argument(
    "--dev",
    "-D",
    action="store_true",
    dest="dev",
    help="Enable developer mode, which adds detail to error pages in the web interface and enables debug logging for mako, praw, requests, and urllib3",
)
parser.add_argument(
    "--port",
    "-p",
    type=int,
    dest="port",
    help="Specify custom port for web interface (default: 8080)",
)
parser.add_argument(
    "--data",
    "-d",
    type=str,
    dest="data_path",
    help="Specify path where database files are stored (default is /data relative to redball.py).",
)
parser.add_argument(
    "--log",
    "-l",
    type=str,
    dest="log_path",
    help="Specify path where log files should be stored (default is /logs relative to redball.py).",
)
args = parser.parse_args()

cwd = os.path.dirname(os.path.realpath(__file__))
pardir = os.path.abspath(os.path.join(cwd, os.pardir))
LOG_PATH = os.path.join(pardir, "logs") if not args.log_path else args.log_path
DB_PATH = os.path.join(pardir, "data") if not args.data_path else args.data_path
BOT_PATH = os.path.join(pardir, "bots")
DB_FILE = os.path.join(DB_PATH, "redball.db")
WEB_ROOT = os.path.join(pardir, "web")
TEMPLATE_PATH = os.path.join(pardir, "web", "templates")

logSettings = {
    "LOG_TO_CONSOLE": not args.quiet,
    "LOG_TO_FILE": True,
    "CONSOLE_LOG_LEVEL": "DEBUG" if args.verbose else "INFO",
    "FILE_LOG_LEVEL": "DEBUG",
}
log = logger.init_logger(
    logger_name="",
    log_to_console=logSettings["LOG_TO_CONSOLE"],
    log_to_file=logSettings["LOG_TO_FILE"],
    log_path=LOG_PATH,
    log_file="redball.log",
    file_log_level=logSettings["FILE_LOG_LEVEL"],
    console_log_level=logSettings["CONSOLE_LOG_LEVEL"],
    clear_first=True,
)

WEB_THREAD = None
OVERWATCH_THREAD = None
SCHEDULER = None
DB_LOCK = threading.Lock()
HTTPS_SERVER = None
LOGGED_IN_USERS = {}
SIGNAL = None
DEV = False
BOTS = {}


def startup(suppress_bots=False, dev=False, data_path=None, log_path=None):
    global log, DB_PATH, LOG_PATH, DEV

    DEV = False
    if dev:
        log.debug("Enabling developer mode.")
        DEV = True

    if data_path is not None and data_path != DB_PATH:
        # Set custom data path
        DB_PATH = data_path
        log.info("Using custom data path: [{}].".format(DB_PATH))

    if log_path is not None and log_path != LOG_PATH:
        # Set custom log path
        LOG_PATH = log_path
        log.info("Using custom log path: [{}].".format(LOG_PATH))

    log.info("Bot timezone: {}".format(str(tzlocal.get_localzone())))

    # Initialize the DB
    database.validate_db()

    # Re-initialize logger if settings are different than defaults (most likely the case)
    updated = False
    for x in (x for x in config.get_sys_config() if x["category"] == "Logging"):
        if logSettings[x["key"]] != x["val"]:
            updated = True
            logSettings.update({x["key"]: x["val"]})

    if updated:
        log.info(
            "Reinitializing logger with updated settings... {}".format(logSettings)
        )
        log = logger.init_logger(
            logger_name="",
            log_to_console=logSettings["LOG_TO_CONSOLE"],
            log_to_file=logSettings["LOG_TO_FILE"],
            log_path=LOG_PATH,
            log_file="redball.log",
            file_log_level=logSettings["FILE_LOG_LEVEL"],
            console_log_level=logSettings["CONSOLE_LOG_LEVEL"],
            clear_first=True,
        )

    # Initialize loggers for mako, praw, requests, urllib3, cherrypy, and statsapi
    logger.get_logger("mako", "DEBUG" if DEV else "ERROR", True)
    logger.get_logger("prawcore", "DEBUG" if DEV else "ERROR", True)
    logger.get_logger("requests", "DEBUG" if DEV else "ERROR", True)
    logger.get_logger("urllib3", "DEBUG" if DEV else "ERROR", True)
    logger.init_logger(
        logger_name="cherrypy.access",
        log_to_console=logSettings["LOG_TO_CONSOLE"],
        log_to_file=logSettings["LOG_TO_FILE"],
        log_path=LOG_PATH,
        log_file="cherrypy.access.log",
        file_log_level=logSettings["FILE_LOG_LEVEL"],
        console_log_level=logSettings["CONSOLE_LOG_LEVEL"],
        clear_first=True,
    )
    logger.init_logger(
        logger_name="cherrypy.error",
        log_to_console=logSettings["LOG_TO_CONSOLE"],
        log_to_file=logSettings["LOG_TO_FILE"],
        log_path=LOG_PATH,
        log_file="cherrypy.error.log",
        file_log_level=logSettings["FILE_LOG_LEVEL"],
        console_log_level=logSettings["CONSOLE_LOG_LEVEL"],
        clear_first=True,
    )
    logger.init_logger(
        logger_name="statsapi",
        log_to_console=logSettings["LOG_TO_CONSOLE"],
        log_to_file=logSettings["LOG_TO_FILE"],
        log_path=LOG_PATH,
        log_file="statsapi.log",
        file_log_level=logSettings["FILE_LOG_LEVEL"],
        console_log_level=logSettings["CONSOLE_LOG_LEVEL"],
        clear_first=True,
    )

    # Load bot settings
    for b in database.db_qry(
        "SELECT id FROM rb_bots ORDER BY id ASC;", closeAfter=True
    ):
        BOTS.update({str(b["id"]): bot.Bot(botId=b["id"])})

    log.debug("BOTS: {}".format(BOTS))

    # Start bot threads
    if suppress_bots:
        log.info("Suppressing bot auto-run per command line argument.")

    for b in BOTS.values():
        if b.autoRun == "True":
            if suppress_bots:
                b.STOP = True
                b.thread = None
            else:
                b.start()
        else:
            b.thread = None

    return True


def overwatch():
    global SIGNAL
    while True:
        if SIGNAL is None:
            # Start any autoRun=True bots that are not running
            # Leave the bot stopped if it was manually stopped or suppressed
            for b in BOTS.values():
                if b.autoRun == "True" and not b.isRunning() and not b.STOP:
                    log.info(
                        "Bot {} (id={}) is not running but autoRun is enabled. Starting the bot...".format(
                            b.name, b.id
                        )
                    )
                    b.start()

            time.sleep(5)
        else:
            log.debug("Overwatch exiting...")
            break


def stay_alive():
    global SIGNAL
    i = 0
    while True:
        if SIGNAL is None:
            try:
                i = i + 1
                if i == 600:
                    log.debug("Still alive...")
                    i = 0

                time.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                SIGNAL = "shutdown"
        else:
            shutdown(SIGNAL)


def signal_handler(signal=None, frame=None):
    global SIGNAL
    if signal is not None:
        SIGNAL = signal
        # log.info('Received signal {}...'.format(signal))
        shutdown(signal)


def shutdown(s):
    log.info("Shutting down (signal: {})...".format(s))
    for b in BOTS.values():
        if b.isRunning():
            b.stop()

    cherrypy.engine.exit()
    sys.exit(0)
