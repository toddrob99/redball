#!/usr/bin/env python

from datetime import datetime
import os
import json
import sqlite3
import time
import uuid

import redball
from redball import config, logger, upgrade

log = logger.get_logger(
    logger_name="redball.database", log_level="DEBUG", propagate=True
)


def get_con(logg=log, dbFile=None):
    if not os.path.isdir(redball.DB_PATH):
        try:
            logg.info("The data directory does not exist. Attempting to create it...")
            os.mkdir(redball.DB_PATH)
        except Exception as e:
            logg.error("Error creating data directory: {}.".format(e))
            raise

    try:
        logg.debug(
            "Connecting to database {}".format(dbFile if dbFile else redball.DB_FILE)
        )
        con = sqlite3.connect(dbFile if dbFile else redball.DB_FILE, timeout=30)
        con.execute("PRAGMA journal_mode = off;")
        con.row_factory = dict_factory
        return con
    except sqlite3.Error as e:
        logg.error("Error connecting to database: {}".format(e))
        raise


def get_cur(con=None, logg=log):
    if not con:
        con = get_con(logg=logg)

    try:
        return con.cursor()
    except sqlite3.Error as e:
        logg.error("Error obtaining database cursor: {}".format(e))
        raise

    return None


def db_qry(
    query, con=None, cur=None, fetchone=False, commit=False, closeAfter=False, logg=log
):
    if not con:
        con = get_con(logg=logg)

    if not cur:
        cur = get_cur(con, logg=logg)

    if isinstance(query, str) or isinstance(query, tuple):
        query = [query]

    results = []
    for q in query:
        args = []
        if isinstance(q, tuple):
            args = q[1]
            q = q[0]
            if isinstance(args, str):
                args = (args,)

        try:
            logg.debug("q: {}, args: {}".format(q, args))
            with redball.DB_LOCK:
                if len(args):
                    r = cur.execute(q, args)
                else:
                    r = cur.execute(q)

                if fetchone:
                    results.append(r.fetchone())
                else:
                    results.append(r.fetchall())
        except sqlite3.Error as e:
            logg.error("Error executing database query ({}): {}".format(q, e))
            results.append("ERROR: {}".format(e))

    if commit:
        con.commit()

    if closeAfter:
        con.close()

    if len(query) == 1:
        res = results[0]
    else:
        res = results

    logg.debug("Query result: {}.".format(res))
    return res


def dict_factory(cursor, row):
    """From sqlite3 documentation:
    https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.row_factory
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d


def validate_db(logg=log):
    con = get_con(logg=logg)
    cur = get_cur(con, logg=logg)

    allTables = [
        "rb_config",
        "rb_users",
        "rb_privileges",
        "rb_bots",
        "rb_botTypes",
        "rb_redditAuth",
        "rb_redditScopes",
        "rb_botConfig",
        "rb_meta",
    ]
    existingTables = db_qry(
        "select name from sqlite_master where type='table';",
        con=con,
        cur=cur,
        closeAfter=True,
        logg=logg,
    )
    missingTables = []

    for i in range(0, len(allTables)):
        if not next((x for x in existingTables if allTables[i] in x.values()), None):
            missingTables.append(allTables[i])

    if len(missingTables):
        logg.error("Missing table(s) in database: {}.".format(missingTables))
        build_tables(missingTables)
    else:
        logg.debug("Database connection and tables validated.")

    # Upgrade database
    logg.debug("Checking for database upgrades...")
    upgrade.upgrade_database()  # Not doing anything with the return value for now

    return True


def build_tables(tables, logg=log):
    queries = []

    boolOptions = json.dumps([True, False])
    logLevelOptions = json.dumps(["DEBUG", "INFO", "WARNING", "ERROR"])
    authOptions = json.dumps(["Basic", "Form", "None"])

    if "rb_config" in tables:
        # Create rb_config table to hold application configuration
        queries.append(
            """CREATE TABLE IF NOT EXISTS rb_config (
                id integer primary key autoincrement,
                category text not null,
                key text not null,
                description text not null,
                type text not null,
                val text,
                options text,
                subkeys text,
                parent_key text,
                read_only text,
                unique (category, key)
            );"""
        )

        # Set default values
        queries.append(
            (
                """INSERT OR IGNORE INTO rb_config (category, key, description, type, val, options, subkeys, parent_key, read_only)
                    VALUES
                        ('Logging', 'LOG_TO_FILE', 'Log to File', 'bool', 'true', ?, '["FILE_LOG_LEVEL"]', '', 'False'),
                        ('Logging', 'FILE_LOG_LEVEL', 'File Log Level', 'str', '"DEBUG"', ?, '[]', 'LOG_TO_FILE', 'False'),
                        ('Logging', 'LOG_TO_CONSOLE', 'Log to Console', 'bool', 'true', ?, '["CONSOLE_LOG_LEVEL"]', '', 'False'),
                        ('Logging', 'CONSOLE_LOG_LEVEL', 'Console Log Level', 'str', '"INFO"', ?, '[]', 'LOG_TO_CONSOLE', 'False'),
                        ('Web/Security', 'HTTP_ROOT', 'HTTP root for web interface (e.g. http://localhost:8087, http://127.0.0.1:8087)', 'str', '"http://localhost:8087"', '[]', '[]', '', 'False'),
                        ('Web/Security', 'HTTP_PORT', 'HTTP port for web interface', 'int', 8087, '[]', '[]', '', 'False'),
                        ('Web/Security', 'AUTH_TYPE', 'Authentication Method', 'str', '"Form"', ?, '[]', '', 'False'),
                        ('Web/Security', 'USE_HTTPS', 'Use HTTPS', 'bool', 'false', ?, '["HTTPS_KEY","HTTPS_CERT","HTTPS_CHAIN","HTTPS_PORT","HTTPS_ONLY"]', '', 'False'),
                        ('Web/Security', 'HTTPS_ONLY', 'Disable HTTP', 'bool', 'false', ?, '[]', 'USE_HTTPS', 'False'),
                        ('Web/Security', 'HTTPS_KEY', 'Private Key File Path (e.g. C:\\certs\\privkey.pem)', 'str', '""', '[]', '[]', 'USE_HTTPS', 'False'),
                        ('Web/Security', 'HTTPS_CERT', 'Certificate File Path (e.g. C:\\certs\\cert.pem)', 'str', '""', '[]', '[]', 'USE_HTTPS', 'False'),
                        ('Web/Security', 'HTTPS_CHAIN', 'Certificate Chain File Path (e.g. C:\\certs\\certchain.pem)', 'str', '""', '[]', '[]', 'USE_HTTPS', 'False'),
                        ('Web/Security', 'HTTPS_PORT', 'HTTPS Port', 'int', 443, '[]', '[]', 'USE_HTTPS', 'False'),
                        ('Web/Security', 'SESSION_TIMEOUT', 'Session Timeout (hours)', 'int', 4, '[]', '[]', '', 'False'),
                        ('Web/Security', 'HTTP_PROXY', 'Enable HTTP Proxy (support reverse proxy with SSL)', 'bool', 'false', ?, '[]', '', 'False'),
                        ('Database', 'BACKUP_DAYS', 'Retain automatic nightly database backups for N days (default: 7)', 'int', 7, '[]', '[]', '', 'False')
                ;""",
                (
                    boolOptions,
                    logLevelOptions,
                    boolOptions,
                    logLevelOptions,
                    authOptions,
                    boolOptions,
                    boolOptions,
                    boolOptions,
                ),
            )
        )

    if "rb_users" in tables:
        # Create rb_users table to hold user info
        queries.append(
            """CREATE TABLE IF NOT EXISTS rb_users (
                id integer primary key autoincrement,
                userid text not null unique,
                password text not null,
                name text,
                email text,
                reddit_userid text,
                privileges text default '[]',
                apikey text unique,
                lastUpdate text,
                lastLogin text,
                loginCount integer default 0
            );"""
        )

        # Set default values - default admin password is redball
        queries.append(
            (
                """INSERT OR IGNORE INTO rb_users (userid, password, name, email, reddit_userid, privileges, apikey, lastUpdate)
                    VALUES
                        ('admin', ?, 'Administrator', '', '', '["rb_admin", "rb_web"]', ?, ?)
                ;""",
                (
                    "07903e293c05892a5e24b8ae02a5423d053f3cdec78baa05f78b954ddf3657f7a2a14f03afbe5464147d67dccbeb04e7a0f11d75ca09cdc19a9d28873d9494772c8b8c44ee76d6bf96245fded8df207bc8e446fb17b63c3ce209ad01d6ef952a",
                    uuid.uuid4().hex,
                    time.time(),
                ),
            )
        )

    if "rb_privileges" in tables:
        # Create rb_privileges table to hold info about privileges
        queries.append(
            """CREATE TABLE IF NOT EXISTS rb_privileges (
                id integer primary key autoincrement,
                privilege text not null unique,
                description text
            );"""
        )

        # Insert default privileges -- ro/startstop/rw privs will be added for each bot
        queries.append(
            """INSERT OR IGNORE INTO rb_privileges (privilege, description)
                VALUES
                ('rb_admin', 'Full access to all areas of the application.'),
                ('rb_api', 'Allow access via api (api key required).'),
                ('rb_web', 'Allow access via web UI.'),
                ('rb_config_ro', 'Read-only access to system configuration.'),
                ('rb_config_rw', 'Full access to system configuration.'),
                ('rb_user_ro', 'Read-only access to users (req. rb_config_r*).'),
                ('rb_user_rw', 'Full access to manage users (req. rb_config_r*).'),
                ('rb_apikeys_ro', 'Read-only access to (masked) API keys (req. rb_config_r*).'),
                ('rb_apikeys_rw', 'Full access to API keys (req. rb_config_r*).'),
                ('rb_log_ro', 'Read-only access to logs.'),
                ('rb_log_rw', 'Full access to logs.'),
                ('rb_bot_create', 'Access to create a bot.'),
                ('rb_bot_all_ro', 'Read-only access to all bots.'),
                ('rb_bot_all_startstop', 'Access to start and stop all bots.'),
                ('rb_bot_all_rw', 'Full access to all bots.')
            ;"""
        )

    if "rb_bots" in tables:
        # Create rb_bots table to hold info about bots
        queries.append(
            """CREATE TABLE IF NOT EXISTS rb_bots (
                id integer primary key autoincrement,
                name text unique not null,
                botType integer not null,
                redditAuth text,
                autoRun text default 'False'
            );"""
        )

    if "rb_botTypes" in tables:
        # Create rb_botTypes table to hold info about available bot types
        queries.append(
            """CREATE TABLE IF NOT EXISTS rb_botTypes (
                id integer primary key autoincrement,
                name text unique,
                description text not null,
                moduleName text not null
            );"""
        )

        # Insert packaged bot types
        queries.append(
            """INSERT OR IGNORE INTO rb_botTypes (name, description, moduleName)
                VALUES
                ('game-threads', 'MLB Game Threads', 'game_threads'),
                ('lemmy-mlb-game-threads', 'Lemmy MLB Game Threads', 'lemmy_mlb_game_threads'),
                ('nfl-game-threads', 'NFL Game Threads', 'nfl_game_threads'),
                ('mlb-data', 'MLB Data', 'mlb_data'),
                ('comment-response', 'Comment Response', 'comment_response'),
                ('placeholder', 'Placeholder', '_template')
            ;"""
        )

    if "rb_botConfig" in tables:
        # Create rb_botConfig table to hold bot settings
        queries.append(
            """CREATE TABLE IF NOT EXISTS rb_botConfig (
                id integer primary key autoincrement,
                botId integer not null,
                category text not null,
                key text not null,
                description text,
                type text,
                val text,
                options text,
                subkeys text,
                parent_key text,
                read_only text,
                system text default 'False',
                unique (botId, category, key)
            );"""
        )

    if "rb_redditAuth" in tables:
        # Create rb_redditAuth table to hold reddit authorization info for bot to use
        queries.append(
            """CREATE TABLE IF NOT EXISTS rb_redditAuth (
                id integer primary key autoincrement,
                description text not null,
                reddit_appId text not null,
                reddit_appSecret text not null,
                reddit_scopes text not null,
                reddit_refreshToken text,
                reddit_uniqueCode text unique
            );"""
        )

        # Set default record
        queries.append(
            """INSERT OR IGNORE INTO rb_redditAuth (id, description, reddit_appId, reddit_appSecret, reddit_scopes, reddit_uniqueCode)
                VALUES
                (0, 'None', 'n/a', 'n/a', 'n/a', 'n/a')
            ;"""
        )

    if "rb_redditScopes" in tables:
        # Create rb_redditScopes table to hold a list of reddit scopes
        queries.append(
            """CREATE TABLE IF NOT EXISTS rb_redditScopes (
                id integer primary key autoincrement,
                name text not null unique,
                description text not null
            );"""
        )

        # Insert values from https://www.reddit.com/api/v1/scopes
        queries.append(
            """INSERT OR IGNORE INTO rb_redditScopes (name, description)
                VALUES
                ('creddits','Spend my reddit gold creddits on giving gold to other users.'),
                ('modcontributors','Add/remove users to approved user lists and ban/unban or mute/unmute users from subreddits I moderate.'),
                ('modmail','Access and manage modmail via mod.reddit.com.'),
                ('modconfig','Manage the configuration, sidebar, and CSS of subreddits I moderate.'),
                ('subscribe','Manage my subreddit subscriptions. Manage ---friends--- - users whose content I follow.'),
                ('structuredstyles','Edit structured styles for a subreddit I moderate.'),
                ('vote','Submit and change my votes on comments and submissions.'),
                ('wikiedit','Edit wiki pages on my behalf'),
                ('mysubreddits','Access the list of subreddits I moderate, contribute to, and subscribe to.'),
                ('submit','Submit links and comments from my account.'),
                ('modlog','Access the moderation log in subreddits I moderate.'),
                ('modposts','Approve, remove, mark nsfw, and distinguish content in subreddits I moderate.'),
                ('modflair','Manage and assign flair in subreddits I moderate.'),
                ('save','Save and unsave comments and submissions.'),
                ('modothers','Invite or remove other moderators from subreddits I moderate.'),
                ('read','Access posts and comments through my account.'),
                ('privatemessages','Access my inbox and send private messages to other users.'),
                ('report','Report content for rules violations. Hide & show individual submissions.'),
                ('identity','Access my reddit username and signup date.'),
                ('livemanage','Manage settings and contributors of live threads I contribute to.'),
                ('account','Update preferences and related account information. Will not have access to your email or password.'),
                ('modtraffic','Access traffic stats in subreddits I moderate.'),
                ('wikiread','Read wiki pages through my account'),
                ('edit','Edit and delete my comments and submissions.'),
                ('modwiki','Change editors and visibility of wiki pages in subreddits I moderate.'),
                ('modself','Accept invitations to moderate a subreddit. Remove myself as a moderator or contributor of subreddits I moderate or contribute to.'),
                ('history','Access my voting history and comments or submissions Ive saved or hidden.'),
                ('flair','Select my subreddit flair. Change link flair on my submissions.')
            ;"""
        )

    if "rb_meta" in tables:
        # Create rb_meta table to hold info about the app
        queries.append(
            """CREATE TABLE IF NOT EXISTS rb_meta (
                id integer primary key autoincrement,
                key text not null unique,
                val text not null,
                lastUpdate text
            );"""
        )

        # Insert DB Version
        queries.append(
            """INSERT OR IGNORE INTO rb_meta (key, val, lastUpdate)
                VALUES
                ('dbVersion', '1', '{}')
            ;""".format(
                time.time()
            )
        )

    logg.debug("Executing queries to build {} table(s): {}".format(tables, queries))
    results = db_qry(queries, commit=True, closeAfter=True, logg=logg)
    if None in results:
        logg.debug("One or more queries failed: {}".format(results))
    else:
        logg.debug("Building of tables complete. Results: {}".format(results))

    return True


def get_database_version(logg=log):
    result = db_qry(
        "SELECT val from rb_meta where key='dbVersion';",
        fetchone=True,
        closeAfter=True,
        logg=logg,
    )
    return int(result.get("val", 0))


def backup_database(logg=log, manual=False):
    con = get_con()
    bakFileName = "redball{}-{}.db".format(
        "-manual" if manual else "-auto", datetime.today().strftime("%Y%m%d%H%M%S")
    )
    bak = get_con(dbFile=os.path.join(redball.DB_PATH, bakFileName))
    try:
        con.backup(bak)
        logg.info("Successfully created database backup [{}].".format(bakFileName))
    except Exception as e:
        logg.error("Error backing up database: {}".format(e))

    con.close()
    bak.close()
    cleanup_db_backups(
        days=next(
            (
                x["val"]
                for x in config.get_sys_config(category="Database")
                if x["key"] == "BACKUP_DAYS"
            ),
            7,
        )
    )


def cleanup_db_backups(logg=log, backupPath=None, days=7):
    if not backupPath:
        backupPath = redball.DB_PATH

    for f in os.listdir(backupPath):
        if (
            "auto" in f
            and "manual" not in f
            and os.stat(os.path.join(backupPath, f)).st_mtime
            < time.time() - days * 86400 - 60  # Include 60 second buffer
            and os.path.isfile(os.path.join(backupPath, f))
        ):
            try:
                os.remove(os.path.join(backupPath, f))
                logg.debug("Deleted old backup [{}]".format(f))
            except Exception as e:
                logg.error("Error deleting old backup [{}]: {}.".format(f, e))
