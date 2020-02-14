#!/usr/bin/env python

import logging
import logging.handlers
import os
import sys
import time

cwd = os.path.dirname(os.path.realpath(__file__))
pardir = os.path.abspath(os.path.join(cwd, os.pardir))
LOG_PATH = os.path.join(pardir, "logs")


def get_logger(logger_name, log_level="INFO", propagate=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, log_level.upper(), 30))
    logger.propagate = propagate

    return logger


def clear_handlers(logger=None):
    if not logger:
        logger = logging.getLogger()

    for h in list(logger.handlers):
        logger.removeHandler(h)


def add_handlers(
    logger,
    log_to_console=True,
    log_to_file=True,
    log_path=LOG_PATH,
    log_file=None,
    file_log_level="INFO",
    console_log_level="INFO",
    clear_first=True,
):
    if clear_first:
        clear_handlers(logger)

    formatter = logging.Formatter(
        "%(asctime)s :: %(levelname)8s :: %(threadName)s(%(thread)d) :: %(module)s(%(lineno)d) :: %(funcName)s :: %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S %p",
    )

    # Set up file logging
    if log_to_file and log_file:
        for i in [2, 1, 0]:
            try:
                if not os.path.exists(log_path):
                    os.makedirs(log_path)

                file_handler = logging.handlers.TimedRotatingFileHandler(
                    os.path.join(log_path, log_file),
                    when="midnight",
                    interval=1,
                    backupCount=7,
                )
                file_handler.setLevel(
                    getattr(logging, file_log_level.upper(), 30)
                    if file_log_level
                    else logging.INFO
                )
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
                break
            except IOError as e:
                if i >= 1:
                    print(
                        "Error creating file log handler! Will retry {} more time(s); sleeping 3 seconds... Error: {}".format(
                            i, e
                        )
                    )
                else:
                    print(
                        "Could not create file log handler. There will be no logging to file. Continuing in 3 seconds... Error: {}".format(
                            e
                        )
                    )
                    log_file = None
                    log_to_file = False

                time.sleep(3)

    # Set up console logging
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(
            getattr(logging, console_log_level.upper(), 30)
            if console_log_level
            else logging.INFO
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return True


def init_logger(
    logger_name=None,
    log_to_console=True,
    log_to_file=True,
    log_path=LOG_PATH,
    log_file=None,
    file_log_level="INFO",
    console_log_level="INFO",
    clear_first=True,
    propagate=False,
):
    log_to_console = (
        (log_to_console.lower() == "true")
        if isinstance(log_to_console, str)
        else log_to_console
    )
    log_to_file = (
        (log_to_file.lower() == "true") if isinstance(log_to_file, str) else log_to_file
    )
    propagate = (
        (propagate.lower() == "true") if isinstance(propagate, str) else propagate
    )

    logger = get_logger(
        logger_name=logger_name,
        log_level=(
            file_log_level
            if getattr(logging, file_log_level.upper(), 30)
            < getattr(logging, console_log_level.upper(), 30)
            else console_log_level
        ),
        propagate=propagate,
    )
    add_handlers(
        logger=logger,
        log_to_console=log_to_console,
        log_to_file=log_to_file,
        log_path=log_path,
        log_file=log_file,
        file_log_level=file_log_level,
        console_log_level=console_log_level,
        clear_first=clear_first,
    )

    if log_file and log_to_file:
        logger.info(
            "Logging started! Log file: {}".format(os.path.join(log_path, log_file))
        )
    else:
        logger.info("Logging started!")

    return logger
