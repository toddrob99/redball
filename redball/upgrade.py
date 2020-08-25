#!/usr/bin/env python

from redball import database, logger
import time

log = logger.get_logger(
    logger_name="redball.upgrade", log_level="DEBUG", propagate=True
)


def upgrade_database(toVer=None):
    # toVer = database version to upgrade to
    # returns True if version is satisfactory, False if error
    toVer = toVer if toVer else max(upgradeScripts.keys())
    fromVer = database.get_database_version(logg=log)
    origVer = fromVer

    if fromVer == toVer:
        log.info("Database is up to date (version: {})!".format(fromVer))
        return True
    elif fromVer > toVer:
        log.warning(
            "Current version ({}) is higher than requested version ({}). Someting's wrong but there's nothing to upgrade...".format(
                fromVer, toVer
            )
        )
        return True
    else:
        log.info(
            "Current database version {}; desired version: {}.".format(fromVer, toVer)
        )
        log.info("Creating a backup of the database...")
        database.backup_database(logg=log, manual=False)

        con = database.get_con(logg=log)
        cur = database.get_cur(con=con, logg=log)
        while fromVer < toVer:
            # Apply upgrade scripts one version at a time until the database is up-to-date
            log.info(
                "Upgrading database from version {} to version {}...".format(
                    fromVer, fromVer + 1
                )
            )
            if len(upgradeScripts.get(fromVer + 1, [])) > 0:
                results = database.db_qry(
                    query=upgradeScripts[fromVer + 1],
                    con=con,
                    cur=cur,
                    commit=False,
                    closeAfter=False,
                    logg=log,
                )
                if None in results:
                    log.error(
                        "One or more database upgrade queries failed: {}".format(
                            results
                        )
                    )
                    # Upgrade scripts failed. Do not commit and do not continue.
                    return False
                else:
                    con.commit()
                    fromVer += 1
                    log.debug("Database upgraded to version {}.".format(fromVer))

        if origVer != toVer:
            # Upgrade happened, so let's clean up the db and run an integrity check
            database.db_qry(
                query="VACUUM;",
                con=con,
                cur=cur,
                commit=False,
                closeAfter=False,
                logg=log,
            )
            database.db_qry(
                query="PRAGMA INTEGRITY_CHECK;",
                con=con,
                cur=cur,
                commit=False,
                closeAfter=False,
                logg=log,
            )

        con.close()
        log.debug("Database upgrade process is complete.")
        return True


upgradeScripts = {
    1: [
        "UPDATE rb_meta SET val='1', lastUpdate='{}' WHERE key='dbVersion';".format(
            time.time()
        ),
    ],
    2: [
        # Add system config settings: category: Prowl, keys: ERROR_API_KEY, ERROR_PRIORITY
        """INSERT OR IGNORE INTO rb_config (category,key,description,type,val,options,subkeys,parent_key,read_only)
        VALUES
            ('Prowl','ERROR_API_KEY','API Key for platform error notifications','str','""','[]','["ERROR_PRIORITY"]','','False'),
            ('Prowl','ERROR_PRIORITY','Error notification priority (leave blank to disable)','str','""','["","-2","-1","0","1","2"]','[]','ERROR_API_KEY','False');""",
        # Add settings to game_thread bots: category: Prowl, keys: ERROR_API_KEY, ERROR_PRIORITY, THREAD_POSTED_API_KEY, THREAD_POSTED_PRIORITY
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Prowl','ERROR_API_KEY','API Key for sending error notifications to Prowl.','str','""','[]','["ERROR_PRIORITY"]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Prowl','ERROR_PRIORITY','Priority when sending error notifications to Prowl (leave blank to disable).','str','""','["","-2","-1","0","1","2"]','[]','ERROR_API_KEY','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Prowl','THREAD_POSTED_API_KEY','API Key for sending thread posted notifications to Prowl.','str','""','[]','["THREAD_POSTED_PRIORITY","THREAD_POSTED_TEMPLATE"]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Prowl','THREAD_POSTED_PRIORITY','Priority when sending thread posted notifications to Prowl (leave blank to disable).','str','""','["","-2","-1","0","1","2"]','[]','THREAD_POSTED_API_KEY','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        # Remove defaultSettings from rb_botTypes (copy data to temp table and rebuild)
        """CREATE TABLE IF NOT EXISTS rb_botTypes_temp (
            id integer primary key autoincrement,
            name text unique,
            description text not null,
            moduleName text not null
        );""",
        """INSERT INTO rb_botTypes_temp
            SELECT id, name, description, moduleName
                FROM rb_botTypes
        ;""",
        "DROP TABLE rb_botTypes;",
        """CREATE TABLE IF NOT EXISTS rb_botTypes (
            id integer primary key autoincrement,
            name text unique,
            description text not null,
            moduleName text not null
        );""",
        """INSERT INTO rb_botTypes
            SELECT * FROM rb_botTypes_temp
        ;""",
        "DROP TABLE rb_botTypes_temp;",
        # Add system config setting: category: Logging, key: LOG_RETENTION
        """INSERT OR IGNORE INTO rb_config (category, key, description, type, val, options, subkeys, parent_key, read_only)
            VALUES ('Logging', 'LOG_RETENTION', 'Log File Retention (Days)', 'int', 7, '[]', '[]', 'LOG_TO_FILE', 'False');""",
        """UPDATE rb_config set subkeys='["FILE_LOG_LEVEL","LOG_RETENTION"]' WHERE category='Logging' AND key='LOG_TO_FILE';""",
        # Add setting to all bots: category: Logging, key: LOG_RETENTION
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Logging','LOG_RETENTION','Log File Retention (Days).','int',7,'[]','[]','LOG_TO_FILE','','False'
                FROM rb_bots b, bots
            )
        SELECT * FROM bots;""",
        """UPDATE rb_botConfig SET subkeys='["FILE_LOG_LEVEL","LOG_RETENTION"]' WHERE category='Logging' and key='LOG_TO_FILE';""",
        # Add settings to game thread bots: category: Twitter, keys: TWEET_THREAD_POSTED, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Twitter','TWEET_THREAD_POSTED','Tweet when threads are posted (see wiki for info)','bool','false','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Twitter','CONSUMER_KEY','Twitter Consumer Key (see wiki)','str','""','[]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Twitter','CONSUMER_SECRET','Twitter Consumer Secret (see wiki)','str','""','[]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Twitter','ACCESS_TOKEN','Twitter Access Token (see wiki)','str','""','[]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Twitter','ACCESS_SECRET','Twitter Access Secret (see wiki)','str','""','[]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        # Update DB version to 2
        "UPDATE rb_meta SET val='2', lastUpdate='{}' WHERE key='dbVersion';".format(
            time.time()
        ),
    ],
    3: [
        # Add setting to game thread bots: categories: [Weekly Thread, Off Day Thread, Game Day Thread, Game Thread, Post Game Thread], key: LIVE_DISCUSSION
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Weekly Thread','LIVE_DISCUSSION','Submit post as `live discussions` instead of traditional comment threads on new Reddit (old Reddit will still show traditional comment threads).','bool','false','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Off Day Thread','LIVE_DISCUSSION','Submit post as `live discussions` instead of traditional comment threads on new Reddit (old Reddit will still show traditional comment threads).','bool','false','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Game Day Thread','LIVE_DISCUSSION','Submit post as `live discussions` instead of traditional comment threads on new Reddit (old Reddit will still show traditional comment threads).','bool','false','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Game Thread','LIVE_DISCUSSION','Submit post as `live discussions` instead of traditional comment threads on new Reddit (old Reddit will still show traditional comment threads).','bool','false','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Post Game Thread','LIVE_DISCUSSION','Submit post as `live discussions` instead of traditional comment threads on new Reddit (old Reddit will still show traditional comment threads).','bool','false','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        # Update DB version to 3
        "UPDATE rb_meta SET val='3', lastUpdate='{}' WHERE key='dbVersion';".format(
            time.time()
        ),
    ],
    4: [
        # Drop *games table from game thread bots
        # Create temp table to hold table names
        "CREATE TABLE temp_gamesTableNames (tableName text not null);",
        # Insert *games tables for game thread bots into temp table
        """INSERT OR IGNORE INTO temp_gamesTableNames (tableName)
        WITH RECURSIVE
            bots(tableName) AS (
            VALUES(NULL)
            UNION
            SELECT 'rb_bot_' || b.id || '_games' as tableName
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * from bots;""",
        # Set writable_schema = 1 to allow deleting tables via sqlite_master
        "PRAGMA writable_schema = 1;",
        # Drop *games tables for game thread bots listed in temp table
        "DELETE FROM sqlite_master WHERE tbl_name in (SELECT * FROM temp_gamesTableNames);",
        # Set writable_schema back to 0
        "PRAGMA writable_schema = 0;",
        # Delete temp table
        "DROP TABLE temp_gamesTableNames;",
        # Update DB version to 4
        "UPDATE rb_meta SET val='4', lastUpdate='{}' WHERE key='dbVersion';".format(
            time.time()
        ),
    ],
    5: [
        # Change display name of game thread bot type to include MLB
        """UPDATE rb_botTypes SET description='MLB Game Threads' WHERE name='game-threads';""",
        # Add NFL Game Threads bot type
        """INSERT OR IGNORE INTO rb_botTypes (name, description, moduleName)
            VALUES
            ('nfl-game-threads', 'NFL Game Threads', 'nfl_game_threads')
        ;""",
        # Update DB version to 5
        "UPDATE rb_meta SET val='5', lastUpdate='{}' WHERE key='dbVersion';".format(
            time.time()
        ),
    ],
    6: [
        # Add settings to game thread bots: Game Thread > LOCK_GAMEDAY_THREAD
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Game Thread','LOCK_GAMEDAY_THREAD','Lock game day thread when the game thread is submitted.','bool','false','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        # Add settings to game thread bots: Game Thread > LINK_IN_GAMEDAY_THREAD
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Game Thread','LINK_IN_GAMEDAY_THREAD','Post a stickied comment in the game day thread, linking to the game thread, when the game thread is submitted. Add a setting with key=GAMEDAY_THREAD_MESSAGE to override the comment text; use markdown format for the link and just put (link)--e.g. [game thread](link).','bool','true','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        # Add settings to game thread bots: Post Game Thread > LOCK_GAME_THREAD
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Post Game Thread','LOCK_GAME_THREAD','Lock game thread when the post game thread is submitted.','bool','false','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        # Add settings to game thread bots: Post Game Thread > LINK_IN_GAME_THREAD
        """INSERT OR IGNORE INTO rb_botConfig (botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system)
        WITH RECURSIVE
            bots(botId,category,key,description,type,val,options,subkeys,parent_key,read_only,system) AS (
            VALUES(0,null,null,null,null,null,null,null,null,null,null)
            UNION
            SELECT b.id,'Post Game Thread','LINK_IN_GAME_THREAD','Post a stickied comment in the game thread, linking to the post game thread, when the post game thread is submitted. Add a setting with key=GAME_THREAD_MESSAGE to override the comment text; use markdown format for the link and just put (link)--e.g. [post game thread](link).','bool','true','[true, false]','[]','','','False'
                FROM rb_botTypes bt, bots INNER JOIN rb_bots b ON bt.id = b.botType AND bt.moduleName='game_threads'
            )
        SELECT * FROM bots;""",
        # Update DB version to 6
        "UPDATE rb_meta SET val='6', lastUpdate='{}' WHERE key='dbVersion';".format(
            time.time()
        ),
    ],
    7: [
        # Add Duplicate Comment Removal bot type
        """INSERT OR IGNORE INTO rb_botTypes (name, description, moduleName)
            VALUES
            ('duplicate-link-removal', 'Duplicate Link Removal', 'duplicate_link_removal')
        ;""",
        # Update DB version to 7
        "UPDATE rb_meta SET val='7', lastUpdate='{}' WHERE key='dbVersion';".format(
            time.time()
        ),
    ],
}
