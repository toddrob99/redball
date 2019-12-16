#!/usr/bin/env python

import binascii
from datetime import datetime, timedelta
import hashlib
import json
import os
import time

import redball
from redball import config, database, logger

log = logger.get_logger(logger_name="redball.user", log_level="DEBUG", propagate=True)


def hash_password(pw, salt=None):
    # Much of this came from https://www.vitoshacademy.com/hashing-passwords-in-python/
    salt = (
        hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        if not salt
        else salt.encode("ascii")
    )
    pwHash = binascii.hexlify(
        hashlib.pbkdf2_hmac("sha512", pw.encode("utf-8"), salt, 100000)
    )
    return (salt + pwHash).decode("ascii")


def check_password(pw, hash):
    return hash_password(pw, hash[:64]) == hash


def validate_password(realm, username, password):
    """This method is used for basic authentication
    """
    hash = get_user_info(userid=username, field="password")
    if check_password(password, hash):
        log.debug(
            "User {} successfully authenticated for access to the web UI.".format(
                username
            )
        )
        if not check_privilege(username, "rb_web", refresh=True,):
            log.warning(
                "User [{}] has insufficient privileges for access to web UI.".format(
                    username,
                )
            )
            return False
        else:
            return True


def get_user_info(userid=None, apikey=None, uid=None, field=None, sensitive=True):
    # userid = rb_users.userid
    # apikey = rb_users.apikey
    # uid = rb_users.id
    # return dict of user info, or empty dict if user not found
    # or list of dicts if run with no parameters
    # field not supported without userid, apikey, or uid
    q = "SELECT * FROM rb_users WHERE 1=1"
    local_args = tuple()
    if userid:
        if sensitive:
            q += " AND userid=?"
        else:
            q += " AND userid like ?"
        local_args += (userid,)

    if uid:
        q += " AND id=?"
        local_args += (uid,)

    if apikey:
        q += " AND apikey=?"
        local_args += (apikey,)

    result = database.db_qry(
        (q, local_args), fetchone=True if len(local_args) > 0 else False, logg=log
    )
    if isinstance(result, dict):
        if field == "privileges":
            return result.get(field, "[]")
        elif field:
            return result.get(field, "")
        elif not userid and not uid and not apikey:
            return [result]
        else:
            return result
    elif isinstance(result, list):
        # field not supported for multiple records
        return result
    else:
        if field == "privileges":
            return "[]"
        elif field:
            return ""
        else:
            return {}


def create_user(**kwargs):
    con = database.get_con()
    cur = database.get_cur(con)

    if kwargs.get("userid") in [None, ""]:
        return "User ID cannot be blank."
    elif kwargs.get("password") and kwargs["password"] != kwargs.get(
        "confirm_password"
    ):
        return "Password and confirmation do not match."
    elif kwargs.get("password") in [None, ""]:
        return "Password cannot be blank."

    if kwargs.get("name") in [None, ""]:
        kwargs.update({"name": kwargs["userid"].capitalize()})

    if kwargs.get("privileges") in [None, ""]:
        kwargs.update({"privileges": []})

    query = (
        """INSERT INTO rb_users
                (userid, name, password, email, reddit_userid, privileges, lastUpdate)
                VALUES
                (?,?,?,?,?,?,?)
            ;""",
        (
            kwargs["userid"],
            kwargs["name"],
            hash_password(kwargs["password"]),
            kwargs["email"],
            kwargs["reddit_userid"],
            config.serialize_key(kwargs["privileges"]),
            time.time(),
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
                "Created user ({}) with id: {}.".format(kwargs["userid"], insert_id)
            )
        else:
            insert_id = "ERROR: Failed to insert record."

        con.commit()
        con.close()
        return insert_id


def update_user(id, **kwargs):
    local_args = tuple()
    q = "UPDATE rb_users set"
    fields = []

    if kwargs.get("apikey") is not None:
        # apikey gets updated by itself
        fields.append(" apikey=?")
        local_args += (kwargs["apikey"],)
    else:
        if kwargs.get("userid") in [None, ""]:
            return "User ID cannot be blank."

        if kwargs.get("name") in [None, ""]:
            kwargs.update({"name": kwargs["userid"].capitalize()})

        if kwargs.get("privileges") in [None, ""]:
            kwargs.update({"privileges": []})

        if kwargs.get("userid") is not None:
            fields.append(" userid=?")
            local_args += (kwargs["userid"],)

        if kwargs.get("name") is not None:
            fields.append(" name=?")
            local_args += (kwargs["name"],)

        if kwargs.get("email") is not None:
            fields.append(" email=?")
            local_args += (kwargs["email"],)

        if kwargs.get("reddit_userid") is not None:
            fields.append(" reddit_userid=?")
            local_args += (kwargs["reddit_userid"],)

        if kwargs.get("privileges") is not None:
            fields.append(" privileges=?")
            local_args += (config.serialize_key(kwargs["privileges"]),)

    fields.append(" lastUpdate=?")
    local_args += (time.time(),)

    q += ",".join(fields)
    q += " WHERE id=?"
    local_args += (int(id),)
    if q == "UPDATE rb_users set WHERE id=?":
        return True

    query = (q, local_args)
    result = database.db_qry(query, commit=True, closeAfter=True)
    if isinstance(result, str):
        return result
    else:
        return True


def delete_user(id):
    query = ("DELETE FROM rb_users WHERE id=?;", (id,))
    result = database.db_qry(query, commit=True, closeAfter=True)
    return result


def refresh_user_privileges(userid):
    # userid = rb_users.userid
    if userid in ["", "None"] or userid not in redball.LOGGED_IN_USERS.keys():
        log.warning(
            "Can't refresh privileges because user appears to not be logged in: [{}]".format(
                userid
            )
        )
        return

    redball.LOGGED_IN_USERS[userid].update(
        {
            "PRIVS": json.loads(get_user_info(userid=userid).get("privileges", "[]")),
            "privDate": time.time(),
        }
    )


def check_privilege(userid, privilege, refresh=False, checkAll=True):
    # userid = rb_users.userid
    # privilege = rb_privileges.privilege
    # refresh = True to force pull of privileges from DB, False to use cache
    # checkAll = set to False to require privileges on specific object
    # (e.g. don't consider rb_bot_all_* if required priv is rb_bot_1_*)
    # return True if user has exact privilege or higher for same object
    # e.g. if user has rb_bot_all_rw and privilege=rb_bot_1_rw
    # or user has rb_bot_1_rw and privilege = rb_bot_1_ro
    # return False if user does not have required privilege
    if userid is None or privilege in ["", None]:
        return False

    if (
        refresh
        or not redball.LOGGED_IN_USERS.get(userid, {}).get("PRIVS")
        or datetime.fromtimestamp(
            redball.LOGGED_IN_USERS.get(userid, {}).get("privDate")
        )
        <= datetime.today() - timedelta(seconds=3)
    ):
        log.debug("Refreshing privileges...")
        refresh_user_privileges(userid)

    log.debug("checking user {} privilege: {}".format(userid, privilege))  # debug
    if privilege in redball.LOGGED_IN_USERS[userid]["PRIVS"]:
        # User has the exact privilege required
        return True
    elif (
        (
            privilege[-2:] == "ro"
            and privilege[:-2] + "rw" in redball.LOGGED_IN_USERS[userid]["PRIVS"]
        )
        or (
            privilege[-2:] == "ro"
            and privilege[:-2] + "startstop" in redball.LOGGED_IN_USERS[userid]["PRIVS"]
        )
        or (
            privilege[-9:] == "startstop"
            and privilege[:-9] + "rw" in redball.LOGGED_IN_USERS[userid]["PRIVS"]
        )
    ):
        # User has the read-write privilege for the object
        # where read-only or startstop privilege is required
        # or user has startstop privilege where read-only is required
        return True
    elif (
        checkAll
        and privilege.startswith("rb_bot_")
        and "all" not in privilege
        and "create" not in privilege
        and check_privilege(
            userid, "rb_bot_all" + privilege[7 + privilege[7:].find("_") :]
        )
    ):
        # User has required privilege for all bots, including the required bot
        return True
    elif privilege.startswith("rb_bot_all") and sum(
        1
        for x in redball.BOTS.keys()
        if check_privilege(
            userid,
            "rb_bot_{}{}".format(redball.BOTS[x].id, privilege[10:]),
            checkAll=False,
        )
    ) == len(redball.BOTS.keys()):
        # User has required privilege for all bots individually
        # which satisfies the requirement for bot_all
        return True
    elif (
        privilege not in ["rb_api", "rb_web"]
        and "rb_admin" in redball.LOGGED_IN_USERS[userid]["PRIVS"]
    ):
        # User has admin privilege which gives full access to all
        # except api and web UI which must be allowed separately
        return True

    return False


def remove_privilege(privilege):
    # privilege = rb_privilege.privilege
    # Removes the privilege from all users

    # Remove from redball.LOGGED_IN_USERS[x]['PRIVS']
    for x in redball.LOGGED_IN_USERS:
        if privilege in x:
            x.pop(x.index(privilege))

    # Remove from rb_users.privileges
    con = database.get_con()
    cur = database.get_cur(con)

    users = database.db_qry(
        "SELECT id,privileges FROM rb_users;", con=con, cur=cur, logg=log
    )
    queries = []
    for x in users:
        p = json.loads(x["privileges"])
        if privilege in p:
            p.pop(p.index(privilege))
            queries.append(
                (
                    "UPDATE rb_users SET privileges = ? WHERE id = ?;",
                    (json.dumps(p), x["id"]),
                )
            )

    if len(queries):
        database.db_qry(
            queries, con=con, cur=cur, commit=True, closeAfter=True, logg=log
        )
    else:
        con.close()


def get_privileges():
    # Return list of privileges from rb_privileges
    q = "SELECT * FROM rb_privileges;"
    result = database.db_qry(q, closeAfter=True, logg=log)
    if isinstance(result, str):
        return []
    elif isinstance(result, dict):
        return [result]
    else:
        return result


def log_login(uid):
    database.db_qry(
        (
            "UPDATE rb_users set lastLogin=?, loginCount=loginCount+1 where id=?",
            (time.time(), uid),
        ),
        commit=True,
        closeAfter=True,
    )


def mask_apikey(apikey):
    if not apikey or len(apikey) == 0:
        return ""
    else:
        return "{}{}".format("*" * 20, apikey[-4:])
