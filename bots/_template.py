#!/usr/bin/env python

import time
import threading

import redball
from redball import logger

def run(bot, settings):
    global log # Make logger available to the whole module
    # Start logging
    log = logger.init_logger(logger_name=threading.current_thread().name, log_to_console=str(settings.get('Logging',{}).get('LOG_TO_CONSOLE',True)).lower()=='true', log_to_file=str(settings.get('Logging',{}).get('LOG_TO_FILE',True)).lower()=='true', log_path=redball.LOG_PATH, log_file='{}.log'.format(threading.current_thread().name), file_log_level=settings.get('Logging',{}).get('FILE_LOG_LEVEL'), console_log_level=settings.get('Logging',{}).get('CONSOLE_LOG_LEVEL'), clear_first=True, cploggers=False, propagate=False)
    log.debug('Bot received settings: {}'.format(settings))
    # Initialize vars and do one-time setup steps
    i = 0 # This is used inside the sample loop to log 'still alive' entries every 10 cycles
    while True: # This loop keeps the bot running
        if redball.SIGNAL is None and not bot.STOP: # Make sure the main thread hasn't sent a stop command
            # THIS IS WHERE YOU DO YOUR THING:
            i = i+1
            if i == 10: # Log that you're still running every 10 minutes
                log.debug('Still alive...')
                i = 0
            time.sleep(1)
        else: # If main thread has said to stop, we stop!
            log.info('Bot {} (id={}) exiting...'.format(bot.name, bot.id))
            break # Exit the infinite loop to stop the bot
