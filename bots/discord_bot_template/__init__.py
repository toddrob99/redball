#!/usr/bin/env python
""" Discord Bot Template
by Todd Roberts
"""

import time
import threading

import redball
from redball import logger

import asyncio
import discord

__version__ = "1.0.0"

tl = threading.local()

CHECKMARK = "\N{WHITE HEAVY CHECK MARK}"
CROSSMARK = "\N{CROSS MARK}"


def run(bot, settings):
    # Start logging
    tl.log = logger.init_logger(
        logger_name="redball.bots." + threading.current_thread().name,
        log_to_console=str(
            settings.get("Logging", {}).get("LOG_TO_CONSOLE", True)
        ).lower()
        == "true",
        log_to_file=str(settings.get("Logging", {}).get("LOG_TO_FILE", True)).lower()
        == "true",
        log_path=redball.LOG_PATH,
        log_file="{}.log".format(threading.current_thread().name),
        file_log_level=settings.get("Logging", {}).get("FILE_LOG_LEVEL"),
        log_retention=settings.get("Logging", {}).get("LOG_RETENTION", 7),
        console_log_level=settings.get("Logging", {}).get("CONSOLE_LOG_LEVEL"),
        clear_first=True,
        propagate=settings.get("Logging", {}).get("PROPAGATE", False),
    )
    tl.log.debug("Bot received settings: {}".format(settings))
    # Spawn a separate thread for the Discord bot
    # So it will run as a daemon and end when the
    # main thread sends a stop signal
    botThread = threading.Thread(
        target=runTheBot,
        args=(settings, tl.log),
        name=f"{threading.current_thread().name}-discord",
        daemon=True,
    )
    botThread.start()
    i = 0  # This is used inside the sample loop to log 'still alive' entries every 60 cycles
    while True:  # This loop keeps the bot running
        if (
            redball.SIGNAL is None and not bot.STOP
        ):  # Make sure the main thread hasn't sent a stop command
            i = i + 1
            if i == 60:  # Log that you're still running every 60 seconds
                tl.log.debug("Still alive...")
                i = 0
            time.sleep(1)
        else:  # If main thread has said to stop, we stop!
            tl.log.info("Bot {} (id={}) exiting...".format(bot.name, bot.id))
            break  # Exit the infinite loop to stop the bot


def runTheBot(settings, log):
    asyncio.set_event_loop(asyncio.new_event_loop())
    discord = DiscordClient()
    discord.cmdPrefix = settings.get("Bot", {}).get("COMMAND_PREFIX", "g!")
    discord.log = log
    discord.run(settings.get("Bot", {}).get("DISCORD_TOKEN"))


class DiscordClient(discord.Client):
    async def on_ready(self):
        self.log.debug(f"Logged in to discord as {self.user.name} / {self.user.id}.")

    async def on_message(self, msg):
        if msg.author.id == self.user.id:
            return

        if msg.content.startswith(self.cmdPrefix):
            self.log.debug(f"Received message: {msg}")
            # Check message for known command and process the request
            # Template just adds a checkmark reaction to all messages
            # regardless of command, as long as the prefix matches
            await msg.add_reaction(CHECKMARK)
