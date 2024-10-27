#!/usr/bin/env python

import json
import praw
from praw.util.token_manager import BaseTokenManager
from threading import Lock
import uuid

import redball
from redball import database, logger

log = logger.get_logger(logger_name="redball.config", log_level="DEBUG", propagate=True)


def get_sys_config(category=None, key=None, includeChildren=False):
    query = "SELECT * FROM rb_config WHERE 1=1"
    local_args = tuple()
    if category and key:
        query += " AND (category=? AND key=?)"
        local_args += (category, key)
    elif category:
        query += " AND category=?"
        local_args += (category,)
    elif key:
        query += " AND key=?"
        local_args += (key,)

    if includeChildren and key:
        query += " OR parent_key=?"
        local_args += (key,)

    query += " ORDER BY category ASC;"

    if len(local_args):
        config = database.db_qry((query, local_args))
    else:
        config = database.db_qry(query)

    # Deserialize val, options, and subkeys
    if isinstance(config, list):
        for c in config:
            c.update(
                {
                    "val": deserialize_key(c["val"], c["type"]),
                    "options": deserialize_key(c["options"]),
                    "subkeys": deserialize_key(c["subkeys"]),
                }
            )
    elif isinstance(config, dict):
        config.update(
            {
                "val": deserialize_key(config["val"], config["type"]),
                "options": deserialize_key(config["options"]),
                "subkeys": deserialize_key(config["subkeys"]),
            }
        )

    return config


def serialize_key(key):
    # Nothing special for now, but use a function
    # to allow additional processing in the future
    return json.dumps(key)


def deserialize_key(key, dataType=None):
    d = json.loads(key)
    # All config values are stored in a text column,
    # so cast to int if that's the dataType specified.
    # Other data types will convert as expected.
    if dataType == "int":
        return int(d)
    elif dataType == "list":
        return [x.strip() for x in d.split(",")]

    return d


def update_config(data):
    if isinstance(data, list):
        con = database.get_con()
        cur = database.get_cur(con)
        for item in data:
            if item.get("type") == "bool":
                item["val"] = (
                    item["val"]
                    if isinstance(item["val"], bool)
                    else (item["val"].lower() == "true")
                )
            elif item.get("type") == "int":
                item["val"] = int(item["val"])

            query = (
                "UPDATE rb_config SET val = ? WHERE category = ? and key = ?;",
                (serialize_key(item["val"]), item["category"], item["key"]),
            )
            log.debug(
                "Result: {}".format(database.db_qry(query=query, con=con, cur=cur))
            )
        con.commit()
        con.close()
    else:
        if data.get("type") == "bool":
            data["val"] = (
                data["val"]
                if isinstance(data["val"], bool)
                else (data["val"].lower() == "true")
            )
            if data.get("options") in ("", [], None):
                data["options"] = [True, False]
        elif data.get("type") == "int":
            data["val"] = int(data["val"])

        query = (
            "UPDATE rb_config SET val = ? WHERE category = ? and key = ?;",
            (serialize_key(data["val"]), data["category"], data["key"]),
        )
        database.db_qry(query, commit=True, closeAfter=True)

    return True


def get_bot_config(
    botId,
    category=None,
    key=None,
    includeChildren=False,
    confId=None,
    excludeSysFields=False,
    sortByCategory=False,
):
    query = "SELECT * FROM rb_botConfig WHERE botId=?"
    local_args = (botId,)
    if confId:
        query += " AND id=?"
        local_args += (confId,)

    if category and key:
        query += " AND (category=? AND key=?)"
        local_args += (category, key)
    elif category:
        query += " AND category=?"
        local_args += (category,)
    elif key:
        query += " AND key=?"
        local_args += (key,)

    if includeChildren and key:
        query += " OR parent_key=?"
        local_args += (key,)

    query += " ORDER BY category ASC;"

    if len(local_args):
        config = database.db_qry((query, local_args))
    else:
        config = database.db_qry(query)

    if excludeSysFields:
        # Remove system fields
        for x in config:
            x.pop("read_only")
            x.pop("system")

    for x in config:
        x.update(
            {
                "val": deserialize_key(x["val"], x["type"]),
                "subkeys": deserialize_key(x["subkeys"]),
                "options": deserialize_key(x["options"]),
            }
        )

    sortedConfig = {}
    if sortByCategory:
        for cat in set(c["category"] for c in config):
            sortedConfig.update({cat: []})
            log.debug("sortedConfig after adding cat: {}".format(sortedConfig))
            for a in (a for a in config if a["category"] == cat):
                sortedConfig[cat].append(a)

        for x in sortedConfig:
            for y in sortedConfig[x]:
                y.pop("category")

        return sortedConfig

    return config


def update_bot_config(botId, data):
    if isinstance(data, dict):
        data = [data]

    if isinstance(data, list):
        con = database.get_con()
        cur = database.get_cur(con)
        for item in data:
            if item.get("id"):
                q = "UPDATE rb_botConfig SET"
                local_args = tuple()
                for k, v in item.items():
                    if q[-1:] == "?":
                        q += ","
                    q += " {}=?".format(k)
                    local_args += (v,)
                q += " WHERE botId=? and id=?;"
                local_args += (botId, item["id"])
                query = (q, local_args)
            else:
                if item.get("type") == "bool":
                    item["val"] = (
                        item["val"]
                        if isinstance(item["val"], bool)
                        else (item["val"].lower() == "true")
                    )
                elif item.get("type") == "int":
                    item["val"] = int(item["val"])

                query = (
                    "UPDATE rb_botConfig SET val = ? WHERE category = ? and key = ? and botId=?;",
                    (serialize_key(item["val"]), item["category"], item["key"], botId),
                )
            log.debug(
                "Result: {}".format(database.db_qry(query=query, con=con, cur=cur))
            )

        con.commit()
        con.close()
    else:
        query = (
            "UPDATE rb_config SET val = ? WHERE category = ? and key = ?;",
            (serialize_key(data["val"]), data["category"], data["key"]),
        )
        database.db_qry(query, commit=True, closeAfter=True)

    return True


def add_bot_config(
    botId,
    category=None,
    key=None,
    val=None,
    description="",
    dataType="str",
    options="",
    subkeys="",
    parent_key="",
    multi=None,
    replace=False,
    clean=False,
    con=None,
    cur=None,
    commit=True,
    closeAfter=True,
):
    if clean:
        log.debug("Clearing config for bot id {} per clean parameter".format(botId))
        delete_bot_config(botId, category, key, all=True)

    if replace:
        log.debug("Replacing existing values...")
        q = "INSERT OR REPLACE INTO rb_botConfig (botId, category, key, val, description, type, options, subkeys, parent_key, system) VALUES "
    else:
        log.debug("Preserving existing values...")
        q = "INSERT OR IGNORE INTO rb_botConfig (botId, category, key, val, description, type, options, subkeys, parent_key, system) VALUES "

    if isinstance(multi, dict):
        log.debug(f"Multiple [{len(multi)}] config categories provided.")
        query = []
        for k, v in multi.items():
            log.debug(
                f"Generating query for category [{k}] containing [{len(multi[k])}] items..."
            )
            local_args = tuple()
            q2 = q
            for z in v:
                if z.get("type") == "bool":
                    z["val"] = (
                        z["val"]
                        if isinstance(z["val"], bool)
                        else (z["val"].lower() == "true")
                    )
                    if z.get("options") in ("", [], None):
                        z["options"] = [True, False]
                elif z.get("type") == "int":
                    z["val"] = int(z["val"])

                if len(local_args):
                    q2 += ", "

                q2 += "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                local_args += (
                    int(botId),
                    k,
                    z["key"],
                    serialize_key(z["val"]),
                    z.get("description", ""),
                    z.get("type", "str"),
                    serialize_key(z.get("options"))
                    if z.get("options") not in ["", None]
                    else "[]",
                    serialize_key(z.get("subkeys"))
                    if z.get("subkeys") not in ["", None]
                    else "[]",
                    z.get("parent_key", ""),
                    "True"
                    if k == "Logging"
                    and z["key"]
                    in [
                        "LOG_TO_FILE",
                        "FILE_LOG_LEVEL",
                        "LOG_TO_CONSOLE",
                        "CONSOLE_LOG_LEVEL",
                        "PROPAGATE",
                    ]
                    else "False",
                )

            q2 += ";"
            query.append((q2, local_args))
    else:
        if dataType == "bool":
            val = val if isinstance(val, bool) else (val.lower() == "true")
            if options in ("", [], None):
                options = [True, False]
        elif dataType == "int":
            val = int(val)

        query = (
            q + " (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (
                botId,
                category,
                key,
                serialize_key(val),
                description,
                dataType,
                serialize_key(options if isinstance(options, list) else []),
                serialize_key(subkeys if isinstance(subkeys, list) else []),
                parent_key,
                "True"
                if category == "Logging"
                and key
                in [
                    "LOG_TO_FILE",
                    "FILE_LOG_LEVEL",
                    "LOG_TO_CONSOLE",
                    "CONSOLE_LOG_LEVEL",
                    "PROPAGATE",
                ]
                else "False",
            ),
        )

    return database.db_qry(
        query, con=con, cur=cur, commit=commit, closeAfter=closeAfter
    )

    return None


def add_default_bot_config(botId, con=None, cur=None):
    boolOptions = serialize_key([True, False])
    logLevelOptions = serialize_key(["DEBUG", "INFO", "WARNING", "ERROR"])
    sq = (
        """INSERT OR IGNORE INTO rb_botConfig (botId, category, key, description, type, val, options, subkeys, parent_key, read_only, system)
            VALUES
            (?, 'Logging', 'LOG_TO_FILE', 'Log to File', 'bool', 'true', ?, '["FILE_LOG_LEVEL"]', '', 'False', 'True'),
            (?, 'Logging', 'FILE_LOG_LEVEL', 'File Log Level', 'str', '"DEBUG"', ?, '[]', 'LOG_TO_FILE', 'False', 'True'),
            (?, 'Logging', 'LOG_TO_CONSOLE', 'Log to Console', 'bool', 'true', ?, '["CONSOLE_LOG_LEVEL"]', '', 'False', 'True'),
            (?, 'Logging', 'CONSOLE_LOG_LEVEL', 'Console Log Level', 'str', '"INFO"', ?, '[]', 'LOG_TO_CONSOLE', 'False', 'True'),
            (?, 'Logging', 'PROPAGATE', 'Propagate Logs', 'bool', 'false', ?, '[]', '', 'False', 'True')
        ;""",
        (
            botId,
            boolOptions,
            botId,
            logLevelOptions,
            botId,
            boolOptions,
            botId,
            logLevelOptions,
            botId,
            boolOptions,
        ),
    )
    sres = database.db_qry(sq, con=con, cur=cur)
    if isinstance(sres, str):
        return "Error inserting default config: {}".format(sres)
    else:
        return sres


def delete_bot_config(botId, category=None, key=None, confId=None, all=False):
    if all:
        query = ("DELETE FROM rb_botConfig WHERE botId=? and system!='True';", (botId,))
    elif confId:
        query = (
            "DELETE FROM rb_botConfig WHERE botId=? and id=? and system!='True';",
            (botId, int(confId)),
        )
    else:
        query = (
            "DELETE FROM rb_botConfig WHERE botId=? AND category=? AND key=? and system!='True';",
            (botId, category, key),
        )

    return database.db_qry(query, commit=True, closeAfter=True)


def get_botTypes(id=None):
    query = "SELECT * FROM rb_botTypes WHERE 1=1"
    local_args = tuple()
    fetchone = False
    if id:
        query += " AND id=?"
        local_args = (int(id),)
        fetchone = True

    query += " ORDER BY id ASC;"

    if len(local_args):
        types = database.db_qry((query, local_args), fetchone=fetchone)
    else:
        types = database.db_qry(query, fetchone=fetchone)

    if isinstance(types, dict):
        types = [types]

    if len(types) == 1:
        types = types[0]

    return types


def create_botType(**kwargs):
    con = database.get_con()
    cur = database.get_cur(con)

    query = (
        """INSERT INTO rb_botTypes
                (name, description, moduleName)
                VALUES
                (?,?,?)
            ;""",
        (
            kwargs["description"].lower().strip().replace(" ", "-"),
            kwargs["description"],
            kwargs["moduleName"],
        ),
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
        if insert_id > 0:
            log.info(
                "Created botType ({}) with id: {}.".format(
                    kwargs["description"], insert_id
                )
            )
        else:
            insert_id = "ERROR: Failed to insert record."

        con.commit()
        con.close()
        return insert_id


def update_botType(id, **kwargs):
    local_args = tuple()
    q = "UPDATE rb_botTypes set"
    fields = []
    if kwargs.get("name"):
        fields.append(" name=?")
        local_args += (kwargs["name"],)

    if kwargs.get("description"):
        fields.append(" description=?")
        local_args += (kwargs["description"],)

    if kwargs.get("moduleName"):
        fields.append(" moduleName=?")
        local_args += (kwargs["moduleName"],)

    q += ",".join(fields)
    q += " WHERE id=?"
    local_args += (int(id),)
    if q == "UPDATE rb_botTypes set WHERE id=?":
        return "ERROR: Nothing provided to update."

    query = (q, local_args)
    result = database.db_qry(query, commit=True, closeAfter=True)
    return result


def delete_botType(id):
    query = ("DELETE FROM rb_botTypes WHERE id=?;", (id,))
    result = database.db_qry(query, commit=True, closeAfter=True)
    return result


def in_use(botTypeId=None, redditAuthId=None):
    query = "SELECT count(*) FROM rb_bots WHERE "
    if botTypeId:
        query = (query + "botType=?;", (botTypeId,))
    elif redditAuthId:
        query = (query + "redditAuth=?;", (redditAuthId,))
    else:
        return None

    result = database.db_qry(query, fetchone=True, closeAfter=True)
    return result["count(*)"]


def get_redditAuths(id=None):
    query = "SELECT * FROM rb_redditAuth WHERE 1=1"
    local_args = tuple()
    fetchone = False
    if id is not None:
        query += " AND id=?"
        local_args = (int(id),)
        fetchone = True

    query += " ORDER BY id ASC;"

    if len(local_args):
        auths = database.db_qry((query, local_args), fetchone=fetchone)
    else:
        auths = database.db_qry(query, fetchone=fetchone)

    return auths


def create_redditAuth(**kwargs):
    con = database.get_con()
    cur = database.get_cur(con)

    query = (
        """INSERT INTO rb_redditAuth
                (description, reddit_appId, reddit_appSecret, reddit_scopes, reddit_refreshToken, reddit_uniqueCode)
                VALUES
                (?,?,?,?,?,?)
            ;""",
        (
            kwargs["description"],
            kwargs["reddit_appId"],
            kwargs["reddit_appSecret"],
            serialize_key(kwargs["reddit_scopes"]),
            kwargs.get("reddit_refreshToken"),
            uuid.uuid4().hex,
        ),
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
        if insert_id > 0:
            log.info(
                "Created redditAuth ({}) with id: {}.".format(
                    kwargs["description"], insert_id
                )
            )
            redball.REDDIT_AUTH_LOCKS.update({str(insert_id): Lock()})
        else:
            insert_id = "ERROR: Failed to insert record."

        con.commit()
        con.close()
        return insert_id


def update_redditAuth(id, **kwargs):
    local_args = tuple()
    q = "UPDATE rb_redditAuth set"
    fields = []
    if kwargs.get("description"):
        fields.append(" description=?")
        local_args += (kwargs["description"],)

    if kwargs.get("reddit_appId"):
        fields.append(" reddit_appId=?")
        local_args += (kwargs["reddit_appId"],)

    if kwargs.get("reddit_appSecret"):
        fields.append(" reddit_appSecret=?")
        local_args += (kwargs["reddit_appSecret"],)

    if kwargs.get("reddit_scopes"):
        fields.append(" reddit_scopes=?")
        local_args += (serialize_key(kwargs["reddit_scopes"]),)

    if kwargs.get("reddit_refreshToken"):
        fields.append(" reddit_refreshToken=?")
        local_args += (kwargs["reddit_refreshToken"],)

    q += ",".join(fields)
    q += " WHERE id=?"
    local_args += (int(id),)
    if q == "UPDATE rb_redditAuth set WHERE id=?":
        return "ERROR: Nothing provided to update."

    query = (q, local_args)
    result = database.db_qry(query, commit=True, closeAfter=True)
    return result


def delete_redditAuth(id):
    query = ("DELETE FROM rb_redditAuth WHERE id=?;", (id,))
    result = database.db_qry(query, commit=True, closeAfter=True)
    return result


def authorize_redditAuth(id):
    redditAuth = get_redditAuths(id)
    log.debug("redditAuth: {}".format(redditAuth))
    if redditAuth["reddit_scopes"].find("[") == -1:
        redditAuth.update({"reddit_scopes": "[" + redditAuth["reddit_scopes"] + "]"})

    if (
        not len(redditAuth["reddit_appId"])
        or not len(redditAuth["reddit_appSecret"])
        or not len(redditAuth["reddit_scopes"])
        or not len(redditAuth["reddit_uniqueCode"])
    ):
        return False

    webConfig = get_sys_config(category="Web/Security")

    log.debug("Starting Reddit authorization process for redditAuth {}.")
    reddit = praw.Reddit(
        client_id=redditAuth["reddit_appId"],
        client_secret=redditAuth["reddit_appSecret"],
        redirect_uri="{}/authorize".format(
            next(x["val"] for x in webConfig if x["key"] == "HTTP_ROOT")
        ),
        user_agent="{} v{} - Authorizer".format(redball.APP_NAME, redball.__version__),
    )
    url = reddit.auth.url(
        deserialize_key(redditAuth["reddit_scopes"]),
        redditAuth["reddit_uniqueCode"],
        "permanent",
    )
    log.debug("Reddit authorization URL: {}".format(url))
    try:
        import webbrowser

        webbrowser.open(url)
        return url
    except Exception:
        log.debug(
            "Failed to launch web browser for Reddit authorization. Return URL instead. URL: {}".format(
                url
            )
        )
        return url


def callBack_redditAuth(state, code):
    redditAuth = database.db_qry(
        ("SELECT * FROM rb_redditAuth WHERE reddit_uniqueCode=?;", (state,)),
        fetchone=True,
    )
    if isinstance(redditAuth, str) or len(redditAuth) == 0:
        return False

    webConfig = get_sys_config(category="Web/Security")
    # Get refresh token
    log.debug(
        "Exchanging code {} for refresh token for redditAuth id {}.".format(
            code, redditAuth["id"]
        )
    )
    reddit = praw.Reddit(
        client_id=redditAuth["reddit_appId"],
        client_secret=redditAuth["reddit_appSecret"],
        redirect_uri="{}/authorize".format(
            next(x["val"] for x in webConfig if x["key"] == "HTTP_ROOT")
        ),
        user_agent="{} v{} - Callback Handler".format(
            redball.APP_NAME, redball.__version__
        ),
    )
    try:
        refreshToken = reddit.auth.authorize(code)
    except Exception as e:
        log.error("Error exchanging code for refresh token: {}".format(e))
        return "ERROR: {}".format(e)

    log.debug("Refresh token: {}.".format(refreshToken))
    upd = database.db_qry(
        (
            "UPDATE rb_redditAuth SET reddit_refreshToken=? WHERE reddit_uniqueCode=?;",
            (refreshToken, state),
        ),
        commit=True,
        closeAfter=True,
    )
    if upd in [[], [[]]]:
        return True
    else:
        return False


class RedditAuthDBTokenManager(BaseTokenManager):
    def __init__(self, redditAuthId):
        super().__init__()
        self._reddit_auth_id = redditAuthId

    def post_refresh_callback(self, authorizer):
        log.debug(f"Storing refresh token: {authorizer.refresh_token}")
        update_redditAuth(
            self._reddit_auth_id, reddit_refreshToken=authorizer.refresh_token
        )

    def pre_refresh_callback(self, authorizer):
        redditAuthInfo = get_redditAuths(self._reddit_auth_id)
        freshToken = redditAuthInfo.get("reddit_refreshToken")
        log.debug(f"Redeeming Reddit refresh token: {freshToken}")
        authorizer.refresh_token = freshToken


def get_redditScopes(id=None, name=None):
    query = "SELECT * FROM rb_redditScopes WHERE 1=1"
    local_args = tuple()
    fetchone = False
    if id:
        query += " AND id=?"
        local_args += (int(id),)
        fetchone = True

    if name:
        query += " AND name=?"
        local_args += (int(name),)
        fetchone = True

    query += " ORDER BY name ASC;"

    if len(local_args):
        types = database.db_qry((query, local_args), fetchone=fetchone)
    else:
        types = database.db_qry(query, fetchone=fetchone)

    return types
