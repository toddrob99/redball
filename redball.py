"""redball bot management platform

Created by Todd Roberts

https://github.com/toddrob99/redball
"""

from apscheduler.schedulers.background import BackgroundScheduler
import os
import sys
import signal
import threading
import tzlocal

import redball

signal.signal(signal.SIGINT, redball.signal_handler)
signal.signal(signal.SIGTERM, redball.signal_handler)
if sys.platform == "win32":
    signal.signal(signal.SIGBREAK, redball.signal_handler)

if __name__ == "__main__":
    # Honor command line arguments
    import argparse

    parser = argparse.ArgumentParser(
        prog="redball",
        description="Start redball bot management platform. See https://github.com/toddrob99/redball for details.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        dest="verbose",
        help="Enable debug logging for startup",
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

    # Read config and re-initialize logging
    redball.startup(
        dev=args.dev,
        suppress_bots=args.suppress_bots,
        data_path=args.data_path,
        log_path=args.log_path,
    )

    # Start web server
    from redball import webserver

    if args.port:
        web_port = args.port
        redball.log.debug("Using port {} from args...".format(args.port))
    elif os.environ.get('PORT'):
        web_port = int(os.environ["PORT"])
        redball.log.debug("Using port {} from environment variables...".format(os.environ['PORT']))
    else:
        web_port = None

    redball.WEB_THREAD = threading.Thread(
        target=webserver.init_webserver, args=(web_port,), name="rb-web", daemon=True
    )
    redball.WEB_THREAD.start()

    # Start overwatch thread to keep bots running
    redball.OVERWATCH_THREAD = threading.Thread(
        target=redball.overwatch, name="rb-overwatch", daemon=True
    )
    redball.OVERWATCH_THREAD.start()

    # Set up task scheduler
    redball.SCHEDULER = BackgroundScheduler(
        timezone=tzlocal.get_localzone()
        if str(tzlocal.get_localzone()) != "local"
        else "America/New_York"
    )
    redball.SCHEDULER.start()

    # Schedule task to back up DB
    from redball import database

    redball.SCHEDULER.add_job(database.backup_database, "cron", hour=3, minute=33)

    # And now we wait for a signal to exit
    redball.stay_alive()
