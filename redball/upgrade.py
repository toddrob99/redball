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
        # Update DB version to 2
        "UPDATE rb_meta SET val='2', lastUpdate='{}' WHERE key='dbVersion';".format(
            time.time()
        ),
    ]
}
