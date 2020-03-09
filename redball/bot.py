#!/usr/bin/env python

import importlib
import json
import os
import threading

import redball
from redball import config, database, logger, user

log = logger.get_logger(logger_name="redball.bots", log_level="DEBUG", propagate=True)


class Bot(object):
    def __init__(self, botId=None, botInfo=None, create=False):
        self.STOP = False
        self.detailedState = {"summary": {"text": "", "html": "", "markdown": ""}}
        if botInfo:
            if create:
                self.id = self.create_bot(
                    botInfo["name"],
                    botInfo["botType"],
                    botInfo["autoRun"],
                    botInfo.get("redditAuth", ""),
                )
                if not isinstance(self.id, int):
                    self.__del__()
            else:
                self.id = botInfo["id"]
                self.name = botInfo["name"]
                self.botType = botInfo["botType"]
                self.autoRun = botInfo["autoRun"]
                self.redditAuth = botInfo.get("redditAuth")
        elif botId:
            self.id = botId
            botInfo = get_bots(botId)
            self.name = botInfo["name"]
            self.botType = botInfo["botType"]
            self.autoRun = botInfo["autoRun"]
            self.redditAuth = botInfo.get("redditAuth")
        else:
            raise ValueError(
                "Either botId or botInfo must be provided to instantiate a bot."
            )

    def __del__(self):
        if redball.BOTS and redball.BOTS.get(str(self.id)):
            redball.BOTS.pop(str(self.id))
        self.thread = None

    def start(self):
        if self.isRunning():
            log.info("Bot {} (id={}) already running.".format(self.name, self.id))
        else:
            botType = config.get_botTypes(self.botType)
            try:
                log.debug(
                    "Attempting to import bot module: {}...".format(
                        botType["moduleName"]
                    )
                )
                self.botMod = importlib.import_module(
                    "bots.{}".format(botType["moduleName"]), "redball"
                )
            except ImportError as e:
                log.debug(
                    "Failed to import from bots directory, trying global import... (Error: {})".format(
                        e
                    )
                )
                try:
                    self.botMod = importlib.import_module(botType["moduleName"])
                    log.debug("Successfully imported bot module.")
                except Exception as e:
                    log.error("Error importing global bot module: {}".format(e))
                    return False

            log.info("Starting bot {} (id={}).".format(self.name, self.id))
            botArgs = self.get_config()
            self.thread = threading.Thread(
                target=self.botMod.run,
                args=(self, botArgs),
                name="bot-{}-{}".format(self.id, self.name.replace(" ", "-")),
                daemon=True,
            )
            self.STOP = False
            self.thread.start()

        return True

    def stop(self):
        if self.isRunning():
            log.info("Stopping bot {} (id={}).".format(self.name, self.id))
            self.STOP = True
            return True
        else:
            log.info(
                "Received stop signal for {} bot {} (id={}) but bot is not running.".format(
                    self.botType, self.name, self.id
                )
            )
            return False

    def isRunning(self):
        try:
            self.thread
        except AttributeError:
            self.thread = None

        if isinstance(self.thread, threading.Thread) and self.thread.isAlive():
            return True
        else:
            return False

    def refresh_info(self):
        botInfo = get_bots(self.id)
        if self.name != botInfo["name"]:
            self.name = botInfo["name"]
            if self.isRunning():
                self.thread.name = "bot-{}-{}".format(
                    self.id, self.name.replace(" ", "-")
                )

        self.botType = botInfo["botType"]
        self.autoRun = botInfo["autoRun"]
        self.redditAuth = botInfo["redditAuth"]

        return True

    def update_info(self, **kwargs):
        local_args = tuple()
        q = "UPDATE rb_bots set"
        fields = []
        if kwargs.get("name"):
            fields.append(" name=?")
            local_args += (kwargs["name"],)

        if kwargs.get("botType"):
            fields.append(" botType=?")
            local_args += (int(kwargs["botType"]),)

        if kwargs.get("autoRun"):
            fields.append(" autoRun=?")
            local_args += (kwargs["autoRun"],)

        if kwargs.get("redditAuth"):
            fields.append(" redditAuth=?")
            local_args += (kwargs["redditAuth"],)

        q += ",".join(fields)
        q += " WHERE id=?"
        local_args += (self.id,)
        if q == "UPDATE rb_bots set WHERE id=?":
            return "ERROR: Nothing provided to update."

        query = (q, local_args)
        result = database.db_qry(query, commit=True, closeAfter=True)
        if result in ["", []]:
            self.refresh_info()

        return result

    def delete_bot(self):
        con = database.get_con()
        cur = database.get_cur(con)

        queries = [
            ("DELETE FROM rb_bots WHERE id=?;", (self.id,)),
            ("DELETE FROM rb_botConfig WHERE botId=?;", (self.id,)),
            (
                "DELETE FROM rb_privileges WHERE privilege like 'rb_bot_{}_%';".format(
                    self.id
                )
            ),
        ]
        botConfigTables = database.db_qry(
            "select name from sqlite_master where type='table' and name like 'rb_bot_{}_%';".format(
                self.id
            ),
            con=con,
            cur=cur,
            commit=False,
            closeAfter=False,
        )
        if isinstance(botConfigTables, dict):
            for v in botConfigTables.values():
                queries.append(("DROP TABLE {};", (v,)))

        result = database.db_qry(queries, commit=True, closeAfter=True)
        if isinstance(result, list):
            user.remove_privilege("rb_bot_{}_ro".format(self.id))
            user.remove_privilege("rb_bot_{}_startstop".format(self.id))
            user.remove_privilege("rb_bot_{}_rw".format(self.id))
            self.__del__()

        return result

    def create_bot(self, name, botType, autoRun, redditAuth):
        con = database.get_con()
        cur = database.get_cur(con)

        query = (
            "INSERT INTO rb_bots (name,botType,autoRun,redditAuth) values (?,?,?,?);",
            (name, botType, autoRun, redditAuth),
        )
        result = database.db_qry(query, con=con, cur=cur)
        if isinstance(result, str) and result.find("ERROR") != -1:
            con.commit()
            con.close()
            return result
        else:
            insert_id = database.db_qry(
                "SELECT last_insert_rowid() as id;", con=con, cur=cur
            )[0]["id"]
            log.info(
                "Created bot with id: {}. Inserting default settings...".format(
                    insert_id
                )
            )
            self.id = insert_id
            self.name = name
            self.botType = botType
            self.autoRun = autoRun
            self.redditAuth = redditAuth

            config.add_default_bot_config(insert_id, con, cur)

            botTypeInfo = config.get_botTypes(botType)
            defaultSettingsFile = os.path.join(redball.BOT_PATH, f"{botTypeInfo['moduleName']}_config.json")
            log.debug(f"Default settings file for botType {botTypeInfo['name']}: {defaultSettingsFile}")
            if os.path.isfile(defaultSettingsFile):
                try:
                    with open(defaultSettingsFile) as f:
                        defaultSettings = json.load(f)
                except Exception as e:
                    log.error(
                        f"Error occurred while loading default config for [{botTypeInfo['description']}] bot type from json file [{defaultSettingsFile}]: {e}."
                    )
                    defaultSettings = {}

                if len(defaultSettings):
                    log.debug(f"Loaded default settings for botType {botTypeInfo['name']}: {defaultSettings}. Adding to bot {insert_id}...")
                    result = config.add_bot_config(
                        botId=insert_id,
                        multi=defaultSettings,
                        replace=True,
                        con=con,
                        cur=cur,
                        commit=False,
                        closeAfter=False,
                    )
                else:
                    log.debug(f"No default settings found in the json file for botType {botTypeInfo['name']}.")
            else:
                log.warning(f"No default settings json file found for [{botTypeInfo['description']}] bot type.")

            # Create privileges and grant to creator
            q = """INSERT INTO rb_privileges ('privilege', 'description')
                VALUES
                ('rb_bot_{}_ro', 'Read-only access to bot id {}.'),
                ('rb_bot_{}_startstop', 'Access to start and stop bot id {}.'),
                ('rb_bot_{}_rw', 'Full access to bot id {}.')
            ;""".format(
                insert_id, insert_id, insert_id, insert_id, insert_id, insert_id
            )
            database.db_qry(q, con=con, cur=cur)

            con.commit()
            con.close()

            return insert_id

    def get_config(self):
        redditInfo = config.get_redditAuths(self.redditAuth)
        cfg = {
            "Database": {
                "dbPath": redball.DB_PATH,
                "dbFile": redball.DB_FILE,
                "dbTablePrefix": "rb_bot_{}_".format(self.id),
            },
            "Reddit Auth": {
                "reddit_clientId": redditInfo["reddit_appId"],
                "reddit_clientSecret": redditInfo["reddit_appSecret"],
                "reddit_refreshToken": redditInfo["reddit_refreshToken"],
            },
        }
        for x in (x for x in config.get_bot_config(self.id)):
            if x.get("category", "Default") not in cfg.keys():
                cfg.update({x.get("category", "Default"): {}})

            cfg[x["category"]].update({x["key"]: x["val"]})

        return cfg


def get_bots(botId=None):
    query = "SELECT * FROM rb_bots WHERE 1=1"
    local_args = tuple()
    fetchone = False
    if botId:
        query += " AND id=?"
        local_args = (botId,)
        fetchone = True

    query += " ORDER BY id ASC;"

    if len(local_args):
        bots = database.db_qry((query, local_args), fetchone=fetchone)
    else:
        bots = database.db_qry(query, fetchone=fetchone)

    if isinstance(bots, list):
        for bot in bots:
            if redball.BOTS.get(str(bot["id"])):
                bot.update(
                    {
                        "status": "Running"
                        if redball.BOTS[str(bot["id"])].isRunning()
                        else "Stopped"
                    }
                )

            if (
                redball.BOTS.get(str(bot["id"]))
                and redball.BOTS[str(bot["id"])].detailedState
            ):
                bot.update(
                    {"detailedState": redball.BOTS[str(bot["id"])].detailedState}
                )
    elif isinstance(bots, dict):
        if redball.BOTS.get(str(bots["id"])):
            bots.update(
                {
                    "status": "Running"
                    if redball.BOTS[str(bots["id"])].isRunning()
                    else "Stopped"
                }
            )

        if (
            redball.BOTS.get(str(bots["id"]))
            and redball.BOTS[str(bots["id"])].detailedState
        ):
            bots.update({"detailedState": redball.BOTS[str(bots["id"])].detailedState})

    return bots
