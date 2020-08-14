#!/usr/bin/env python

import cherrypy
import json
import os
import sys
import time
import traceback
import urllib.parse
import uuid

from mako.lookup import TemplateLookup
from mako import exceptions

import redball
from redball import bot, config as rbConfig, database, logger, user

log = logger.get_logger(
    logger_name="redball.webserver", log_level="DEBUG", propagate=True
)


def serve_page(templateName, **kwargs):
    """Look up and render template
    """
    lookup = TemplateLookup(directories=[redball.TEMPLATE_PATH])
    try:
        template = lookup.get_template(templateName)
        return template.render(**kwargs)
    except Exception:
        cherrypy.response.status = 500
        if redball.DEV:
            return exceptions.html_error_template().render(**kwargs)
        else:
            args = {
                "title": "Error: 500 Internal Server Error",
                "errors": "Sorry! An error has occurred while rendering the web template.",
            }
            return lookup.get_template("error.mako").render(**args)


def init_webserver(port=None):
    webSettings = rbConfig.get_sys_config(category="Web/Security")
    proxy_on = next(x["val"] for x in webSettings if x["key"] == "HTTP_PROXY")
    socket_port = (
        port
        if port
        else next(int(x["val"]) for x in webSettings if x["key"] == "HTTP_PORT")
    )
    https_on = next(x["val"] for x in webSettings if x["key"] == "USE_HTTPS")
    https_port = next(int(x["val"]) for x in webSettings if x["key"] == "HTTPS_PORT")
    https_cert = next(x["val"] for x in webSettings if x["key"] == "HTTPS_CERT")
    https_key = next(x["val"] for x in webSettings if x["key"] == "HTTPS_KEY")
    https_chain = next((x["val"] for x in webSettings if x["key"] == "HTTPS_CHAIN"), "")
    http_disallow = next(x["val"] for x in webSettings if x["key"] == "HTTPS_ONLY")
    auth_type = next(x["val"] for x in webSettings if x["key"] == "AUTH_TYPE")
    session_timeout = (
        next(int(x["val"]) for x in webSettings if x["key"] == "SESSION_TIMEOUT") * 60
    )
    secure_cookies = (proxy_on or https_on or http_disallow)
    log.info(
        "Starting web server on port {} with web root: {}{}{}...".format(
            socket_port,
            redball.WEB_ROOT,
            " and proxy support enabled" if proxy_on else "",
            " and secure cookies enabled" if secure_cookies else "",
        )
    )
    global_conf = {
        "global": {
            "server.socket_host": "0.0.0.0",
            "server.socket_port": socket_port,
            "server.thread_pool": 10,
            "engine.autoreload.on": False,
            "log.screen": False,
            "log.access_file": "",
            "log.error_file": "",
            "tools.proxy.on": proxy_on,
            "error_page.default": handle_error,
            "request.error_response": handle_error,
        }
    }
    conf = {
        "/": {
            "tools.sessions.on": True,
            "tools.sessions.timeout": session_timeout,
            "tools.sessions.secure": secure_cookies,
            "tools.encode.on": True,
            "tools.decode.on": True,
            "tools.encode.encoding": "utf-8",
        },
        "/favicon.ico": {
            "tools.staticfile.on": True,
            "tools.staticfile.filename": os.path.join(
                redball.WEB_ROOT, "img", "favicon.ico"
            ),
            "tools.caching.on": True,
            "tools.caching.force": True,
            "tools.caching.delay": 0,
            "tools.sessions.on": False,
        },
        "/images": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(redball.WEB_ROOT, "img"),
        },
        "/img": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(redball.WEB_ROOT, "img"),
        },
        "/css": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": os.path.join(redball.WEB_ROOT, "css"),
        },
    }

    if auth_type == "Basic":
        log.debug("Enabling basic authentication.")
        conf["/"].update(
            {
                "tools.auth_basic.on": True,
                "tools.auth_basic.realm": "redball",
                "tools.auth_basic.checkpassword": user.validate_password,
                "tools.auth_basic.accept_charset": "UTF-8",
            }
        )
    elif auth_type == "Form":
        log.debug("Enabling form-based authentication.")
        conf["/"].update({"tools.auth.require": True})

    api_conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": False,
            "tools.response_headers.on": True,
            "tools.response_headers.headers": [("Content-Type", "text/json")],
        }
    }
    cherrypy.config.update(global_conf)
    cherrypy.tree.mount(WebInterface(), config=conf)
    cherrypy.tree.mount(APIv1(), "/api/v1", config=api_conf)
    if https_on:
        if http_disallow:
            log.info("Disabling HTTP web server per HTTPS_ONLY setting.")
            cherrypy.server.unsubscribe()
        else:
            # Subscribe just in case HTTP was disabled before a restart
            cherrypy.server.subscribe()

        log.info(
            "Starting HTTPS web server on port {} with cert {}, key {}, and chain {}.".format(
                https_port, https_cert, https_key, https_chain
            )
        )
        try:
            from cherrypy._cpserver import Server

            redball.HTTPS_SERVER = Server()
            redball.HTTPS_SERVER.socket_host = "0.0.0.0"
            redball.HTTPS_SERVER.socket_port = https_port
            redball.HTTPS_SERVER.ssl_module = "pyopenssl"
            redball.HTTPS_SERVER.ssl_certificate = https_cert
            redball.HTTPS_SERVER.ssl_private_key = https_key
            redball.HTTPS_SERVER.ssl_certificate_chain = https_chain
            redball.HTTPS_SERVER.subscribe()
        except Exception as e:
            log.debug("Error starting HTTPS server: {}".format(e))
    elif redball.HTTPS_SERVER:
        # If restarting the web server after USE_HTTPS was changed to False,
        # we need to turn off the HTTPS web server
        redball.HTTPS_SERVER.unsubscribe()

    cherrypy.engine.start()


def restart_webServer():
    log.info("Restarting webserver...")
    cherrypy.engine.stop()
    cherrypy.server.httpserver = None
    if redball.HTTPS_SERVER:
        redball.HTTPS_SERVER.unsubscribe()

    redball.HTTPS_SERVER = None
    init_webserver()


def check_auth(*args, **kwargs):
    webSettings = rbConfig.get_sys_config(category="Web/Security")
    auth_type = next(x["val"] for x in webSettings if x["key"] == "AUTH_TYPE")
    if auth_type != "Form":
        return True

    log.debug("Checking authentication against session: {}".format(cherrypy.session.items()))
    u = cherrypy.session.get("_cp_username")
    if u:
        if not user.check_privilege(u, "rb_web", refresh=True,):
            log.warning(
                "User [{}] has insufficient privileges for access to web UI.".format(u,)
            )
            r = urllib.parse.quote(cherrypy.request.request_line.split()[1])
            raise cherrypy.HTTPRedirect(
                "/login?e=Insufficient+privileges.&r={}".format(r)
            )
        else:
            cherrypy.request.login = u
            return True
    else:
        r = urllib.parse.quote(cherrypy.request.request_line.split()[1])
        raise cherrypy.HTTPRedirect("/login?r={}".format(r))


def handle_error(**kwargs):
    args = {
        "title": "Error: {}".format(kwargs.get("status")),
        "errors": "<strong>Sorry! An error has occurred:</strong> {}".format(
            kwargs.get("message")
            if not kwargs.get("status", "").startswith("500")
            else kwargs.get("status")
        ),
        "errorcontainer_hide": "",
    }
    if redball.DEV:
        args.update(
            {"traceback": "<br />".join(traceback.format_exception(*sys.exc_info()))}
        )

    if len(kwargs) == 0:
        args.update(
            {
                "message": sys.exc_info()[1],
                "title": "Error: 500 Internal Server Error",
                "errors": "Sorry! An error has occurred. Please check the input and try again.",
                "traceback": "<br />".join(traceback.format_exception(*sys.exc_info()))
                if redball.DEV
                else "",
            }
        )
        cherrypy.response.body = bytes(
            serve_page(templateName="error.mako", **args), "utf-8"
        )
        cherrypy.response.status = 500
        return

    return serve_page(templateName="error.mako", **args)


class WebInterface(object):
    cherrypy.tools.auth = cherrypy.Tool("before_handler", check_auth)

    @cherrypy.expose()
    def login(self, r=None, i=None, e=None, *args, **kwargs):
        if (
            rbConfig.get_sys_config(category="Web/Security", key="AUTH_TYPE")[0]["val"]
            != "Form"
        ):
            raise cherrypy.HTTPRedirect("/")

        local_args = {
            "title": "Login",
            "r": r,
            "errors": urllib.parse.unquote(e) if e else "",
            "errorcontainer_hide": "" if e else " hide",
            "info": urllib.parse.unquote(i) if i else "",
            "infocontainer_hide": "" if i else " hide",
        }
        if kwargs.get("from") == "logout":
            local_args.update(
                {"info": "You have been logged out.", "infocontainer_hide": ""}
            )

        if kwargs.get("c") == "ip":
            local_args.update(
                {
                    "errors": "You have insufficient privileges to access the web interface.",
                    "errorcontainer_hide": "",
                }
            )

        if kwargs.get("action") == "login":
            if (
                kwargs.get("login|userid", "") == ""
                or kwargs.get("login|password", "") == ""
            ):
                local_args.update(
                    {
                        "errors": "Please enter your user id and password.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                u = user.get_user_info(userid=kwargs["login|userid"], sensitive=False)
                if not u.get('userid'):
                    log.debug("Invalid userid [{}]".format(kwargs["login|userid"]))
                    local_args.update(
                        {
                            "errors": "Your user id and password do not match our records. Please try again.",
                            "errorcontainer_hide": "",
                        }
                    )
                else:
                    userid = u["userid"]
                    pwh = u["password"]
                    if user.check_password(kwargs["login|password"], pwh):
                        log.debug(
                            "User [{}] successfully authenticated for access to the web interface.".format(
                                userid
                            )
                        )
                        local_args.update(
                            {
                                "info": "You have successfully logged in as {}. Welcome!".format(
                                    userid
                                ),
                                "infocontainer_hide": "",
                            }
                        )
                        cherrypy.session.regenerate()
                        cherrypy.session.update(
                            {"_cp_username": userid, "_cp_loginTime": time.time()}
                        )
                        cherrypy.request.login = userid
                        redball.LOGGED_IN_USERS.update(
                            {
                                userid: {
                                    "PRIVS": user.get_user_info(
                                        userid=userid, field="privileges"
                                    ),
                                    "privDate": time.time(),
                                }
                            }
                        )
                        user.log_login(u["id"])
                        if r:
                            log.debug("redirecting to {}".format(r))
                            raise cherrypy.HTTPRedirect(urllib.parse.unquote(r))
                        else:
                            raise cherrypy.HTTPRedirect("/")
                    else:
                        local_args.update(
                            {
                                "errors": "Your user id and password do not match our records. Please try again.",
                                "errorcontainer_hide": "",
                            }
                        )

        return serve_page(templateName="login.mako", **local_args)

    @cherrypy.expose()
    def logout(self, *args, **kwargs):
        if (
            rbConfig.get_sys_config(category="Web/Security", key="AUTH_TYPE")[0]["val"]
            != "Form"
        ):
            raise cherrypy.HTTPRedirect("/")

        u = cherrypy.session.get("_cp_username")
        cherrypy.session.clear()
        cherrypy.request.login = None
        if u in redball.LOGGED_IN_USERS.keys():
            redball.LOGGED_IN_USERS.pop(u)

        raise cherrypy.HTTPRedirect("/login?from=logout")

    @cherrypy.expose(["home", "status", "index"])
    @cherrypy.tools.auth()
    def bots(self, bot_id=None, *args, **kwargs):
        local_args = {
            "title": "Bot Status",
            "bot_id": bot_id,
            "errors": "",
            "errorcontainer_hide": " hide",
            "info": "",
            "infocontainer_hide": " hide",
        }
        if kwargs.get("action") == "start" and bot_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_startstop".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received start command for bot id {}, but user [{}] has insufficient privileges: {}.".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            elif redball.BOTS[bot_id].isRunning():
                log.info(
                    "Received start command for bot id {}, but bot is already running.".format(
                        bot_id
                    )
                )
                local_args.update(
                    {
                        "info": "Bot {} (id={}) is already running.".format(
                            redball.BOTS[bot_id].name, redball.BOTS[bot_id].id
                        ),
                        "infocontainer_hide": "",
                    }
                )
                if not kwargs.get("singleBot"):
                    local_args.update({"bot_id": None})
            else:
                log.info("Received start command for bot id {}.".format(bot_id))
                redball.BOTS[bot_id].start()
                local_args.update(
                    {
                        "info": "Start signal sent to bot {} (id={}).".format(
                            redball.BOTS[bot_id].name, redball.BOTS[bot_id].id
                        ),
                        "infocontainer_hide": "",
                    }
                )
                if not kwargs.get("singleBot"):
                    local_args.update({"bot_id": None})
        elif kwargs.get("action") == "stop" and bot_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_startstop".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received stop command for bot id {}, but user [{}] has insufficient privileges: {}.".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            elif not redball.BOTS[bot_id].isRunning():
                log.info(
                    "Received stop command for bot id {}, but bot is not running.".format(
                        bot_id
                    )
                )
                local_args.update(
                    {
                        "info": "Bot {} (id={}) is not running.".format(
                            redball.BOTS[bot_id].name, redball.BOTS[bot_id].id
                        ),
                        "infocontainer_hide": "",
                    }
                )
                if not kwargs.get("singleBot"):
                    local_args.update({"bot_id": None})
            else:
                log.info("Received stop command for bot id {}.".format(bot_id))
                redball.BOTS[bot_id].stop()
                local_args.update(
                    {
                        "info": "Stop signal sent to bot {} (id={}).".format(
                            redball.BOTS[bot_id].name, redball.BOTS[bot_id].id
                        ),
                        "infocontainer_hide": "",
                    }
                )
                if not kwargs.get("singleBot"):
                    local_args.update({"bot_id": None})
        elif kwargs.get("action") == "create":
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_bot_create", refresh=True
            ):
                log.warning(
                    "Received create bot command, but user [{}] has insufficient privileges: {}.".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                newBot = bot.Bot(
                    botInfo={
                        "name": kwargs["bot_name"],
                        "botType": kwargs["bot_type"],
                        "autoRun": kwargs["bot_autoRun"],
                        "redditAuth": kwargs["bot_redditAuth"],
                    },
                    create=True,
                )
                if isinstance(newBot.id, str):
                    local_args.update({"errors": newBot.id, "errorcontainer_hide": ""})
                else:
                    if cherrypy.session.get("_cp_username") != "authOff":
                        redball.BOTS.update({str(newBot.id): newBot})
                        # Grant rw access to the bot creator
                        redball.LOGGED_IN_USERS[cherrypy.session.get("_cp_username")][
                            "PRIVS"
                        ].append("rb_bot_{}_rw".format(newBot.id))
                        q = (
                            "UPDATE rb_users SET privileges = ? WHERE userid=?;",
                            (
                                json.dumps(
                                    redball.LOGGED_IN_USERS[
                                        cherrypy.session.get("_cp_username")
                                    ]["PRIVS"]
                                ),
                                cherrypy.session.get("_cp_username"),
                            ),
                        )
                        database.db_qry(q, commit=True, closeAfter=True)
        elif kwargs.get("action") == "delete" and bot_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_rw".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received delete command for bot id {}, but user [{}] has insufficient privileges ({}).".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                redball.BOTS[bot_id].delete_bot()
                raise cherrypy.HTTPRedirect("/")
        elif kwargs.get("action") == "edit" and bot_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_ro".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received edit command for bot id {}, but user [{}] has insufficient privileges ({}).".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                local_args.update(
                    {
                        "title": "Bot Setup - {}".format(redball.BOTS[bot_id].name),
                        "bot_id": bot_id,
                    }
                )
        elif kwargs.get("action") == "cancel" and bot_id:
            raise cherrypy.HTTPRedirect("/")
        elif kwargs.get("action") == "save_bot" and bot_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_rw".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received save command for bot id {}, but user [{}] has insufficient privileges ({}).".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                redball.BOTS[bot_id].update_info(
                    name=kwargs["bot_name"],
                    botType=kwargs["bot_type"],
                    autoRun=kwargs["bot_autoRun"],
                    redditAuth=kwargs["bot_redditAuth"],
                )
                local_args.update(
                    {
                        "title": "Bot Setup - {}".format(redball.BOTS[bot_id].name),
                        "bot_id": bot_id,
                        "info": "Bot settings saved.",
                        "infocontainer_hide": "",
                    }
                )
        elif kwargs.get("action") == "save_botConfig":
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_rw".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received save config command for bot id {}, but user [{}] has insufficient privileges ({}).".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                data = []
                for k, v in kwargs.items():
                    if k in [
                        "type",
                        "action",
                        "botConfig_addVal",
                        "botConfig_addDataType",
                    ]:
                        continue
                    if k == "botConfig_addKey":
                        if v != "":
                            rbConfig.add_bot_config(
                                botId=bot_id,
                                category=kwargs["type"],
                                key=v,
                                val=kwargs["botConfig_addVal"],
                                dataType=kwargs["botConfig_addDataType"],
                            )
                        else:
                            continue
                    else:
                        cat_key = k.split("|")
                        data.append(
                            {
                                "category": cat_key[0],
                                "key": cat_key[1],
                                "val": v,
                                "type": cat_key[2],
                            }
                        )
                rbConfig.update_bot_config(bot_id, data)
                local_args.update(
                    {
                        "info": "{} settings saved.".format(kwargs["type"]),
                        "infocontainer_hide": "",
                    }
                )
        elif kwargs.get("action") == "botConfig_add_cat":
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_rw".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received add category command for bot id {}, but user [{}] has insufficient privileges ({}).".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                rbConfig.add_bot_config(
                    botId=bot_id,
                    category=kwargs["botConfig_add_cat_name"],
                    key=kwargs["botConfig_add_cat_key"],
                    val=kwargs["botConfig_add_cat_val"],
                    dataType=kwargs["botConfig_add_cat_dataType"],
                )
        elif kwargs.get("action", "").find("del_botConfig---") != -1:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_rw".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received delete config command for bot id {}, but user [{}] has insufficient privileges ({}).".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                cat_key = kwargs.get("action").split("---")[1].split("|")
                rbConfig.delete_bot_config(bot_id, cat_key[0], cat_key[1])
        elif kwargs.get("action") == "botConfig_upload":
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_rw".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received upload config command for bot id {}, but user [{}] has insufficient privileges ({}).".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                upFile = kwargs.get("botConfig_upload_file")
                if not upFile:
                    local_args.update(
                        {
                            "errors": "Please select file to upload.",
                            "errorcontainer_hide": "",
                        }
                    )
                else:
                    bodyLen = int(cherrypy.request.headers["Content-Length"])
                    if bodyLen > 0:
                        try:
                            fileContents = json.loads(
                                kwargs.get("botConfig_upload_file")
                                .file.read(bodyLen)
                                .decode("utf-8")
                            )
                            log.debug(
                                "replace: {}, fileContents: {}".format(
                                    kwargs.get("botConfig_upload_replace"), fileContents
                                )
                            )
                            result = rbConfig.add_bot_config(
                                botId=bot_id,
                                multi=fileContents,
                                replace=str(
                                    kwargs.get("botConfig_upload_replace", "false")
                                ).lower()
                                == "true",
                                clean=str(
                                    kwargs.get("botConfig_upload_clean", "false")
                                ).lower()
                                == "true",
                            )
                            if isinstance(result, str):
                                # Insert query failed
                                local_args.update(
                                    {
                                        "errors": "Error inserting creating configuration settings: {}.".format(
                                            result
                                        ),
                                        "errorcontainer_hide": "",
                                    }
                                )
                            else:
                                local_args.update(
                                    {
                                        "info": "File imported successfully.{}".format(
                                            " Settings not included in file have been deleted."
                                            if str(
                                                kwargs.get(
                                                    "botConfig_upload_clean", "false"
                                                )
                                            ).lower()
                                            == "true"
                                            else " Existing values overwritten."
                                            if str(
                                                kwargs.get(
                                                    "botConfig_upload_replace", "false"
                                                )
                                            ).lower()
                                            == "true"
                                            else " Existing values preserved."
                                        ),
                                        "infocontainer_hide": "",
                                    }
                                )
                        except Exception as e:
                            log.error("Error processing imported file: {}".format(e))
                            local_args.update(
                                {
                                    "errors": "Error processing file. Please ensure it is in JSON format and try again.",
                                    "errorcontainer_hide": "",
                                }
                            )
        elif kwargs.get("action") == "botConfig_export":
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"),
                "rb_bot_{}_ro".format(bot_id),
                refresh=True,
            ):
                log.warning(
                    "Received export config command for bot id {}, but user [{}] has insufficient privileges ({}).".format(
                        bot_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                allConfig = rbConfig.get_bot_config(bot_id)
                cleanConfig = {}
                for x in allConfig:
                    if not cleanConfig.get(x["category"]):
                        cleanConfig.update({x["category"]: []})

                    cleanConfig[x["category"]].append(
                        {
                            "key": x["key"],
                            "description": x["description"],
                            "type": x["type"],
                            "val": x["val"] if x["type"] != "list" else ", ".join(x["val"]),
                            "options": x["options"],
                            "subkeys": x["subkeys"],
                            "parent_key": x["parent_key"],
                        }
                    )

                cherrypy.response.headers[
                    "Content-Disposition"
                ] = 'attachment; filename="bot{}_config.json"'.format(bot_id)
                return json.dumps(cleanConfig, indent=4)

        return serve_page(templateName="bots.mako", **local_args)

    @cherrypy.expose()
    @cherrypy.tools.auth()
    def botstatus(self, botId=None):
        if botId:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_bot_{}_ro".format(botId)
            ):
                return "{}"

            return json.dumps(
                {botId: "Running" if redball.BOTS[botId].isRunning() else "Stopped"}
            )
        else:
            botStatus = {}
            for b in redball.BOTS.values():
                if user.check_privilege(
                    cherrypy.session.get("_cp_username"), "rb_bot_{}_ro".format(b.id)
                ):
                    botStatus.update({b.id: "Running" if b.isRunning() else "Stopped"})

            return json.dumps(botStatus)

    @cherrypy.expose()
    @cherrypy.tools.auth()
    def botdetailedstate(self, botId=None):
        if botId:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_bot_{}_ro".format(botId)
            ):
                return "{}"

            return json.dumps(
                {
                    botId: redball.BOTS[botId].detailedState["summary"]
                    if redball.BOTS[botId].detailedState
                    else ""
                }
            )
        else:
            botState = {}
            for b in redball.BOTS.values():
                if user.check_privilege(
                    cherrypy.session.get("_cp_username"), "rb_bot_{}_ro".format(b.id)
                ):
                    botState.update(
                        {b.id: b.detailedState["summary"] if b.detailedState else ""}
                    )

            return json.dumps(botState)

    @cherrypy.expose()
    @cherrypy.tools.auth()
    def inuse(self, botType_id=None, redditAuth_id=None):
        if not user.check_privilege(
            cherrypy.session.get("_cp_username"), "rb_config_ro"
        ):
            return "ERROR"
        elif botType_id:
            count = rbConfig.in_use(botTypeId=botType_id)
            return json.dumps(
                {"count": str(count) if isinstance(count, int) else "ERROR"}
            )
        elif redditAuth_id:
            count = rbConfig.in_use(redditAuthId=redditAuth_id)
            return json.dumps(
                {"count": str(count) if isinstance(count, int) else "ERROR"}
            )
        else:
            return "ERROR"

    @cherrypy.expose()
    @cherrypy.tools.auth()
    def config(
        self,
        botType_id=None,
        redditAuth_id=None,
        user_id=None,
        i=None,
        e=None,
        *args,
        **kwargs
    ):
        local_args = {
            "title": "System Configuration",
            "botType_id": botType_id,
            "redditAuth_id": redditAuth_id,
            "user_id": user_id,
            "errors": urllib.parse.unquote(e) if e else "",
            "errorcontainer_hide": "" if e else " hide",
            "info": urllib.parse.unquote(i) if i else "",
            "infocontainer_hide": "" if i else " hide",
        }

        if kwargs.get("action") is not None:
            log.debug("Config action: {}".format(kwargs["action"]))

        if kwargs.get("action") == "save_sysConfig":
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_rw"
            ):
                log.warning(
                    "Received save config command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                data = []
                logSettings = {}
                for k, v in kwargs.items():
                    if k in ["type", "action"]:
                        continue
                    cat_key = k.split("|")
                    data.append(
                        {
                            "category": cat_key[0],
                            "key": cat_key[1],
                            "val": v,
                            "type": cat_key[2],
                        }
                    )
                    if cat_key[0] == "Logging":
                        logSettings.update({cat_key[1]: v})
                rbConfig.update_config(data)
                local_args.update(
                    {
                        "info": "{} settings saved.".format(kwargs["type"]),
                        "infocontainer_hide": "",
                    }
                )
                if kwargs["type"] == "Logging":
                    log.info(
                        "Reinitializing loggers with updated settings... {}".format(
                            logSettings
                        )
                    )
                    redball.log = logger.init_logger(
                        logger_name="",
                        log_to_console=logSettings["LOG_TO_CONSOLE"],
                        log_to_file=logSettings["LOG_TO_FILE"],
                        log_path=redball.LOG_PATH,
                        log_file="redball.log",
                        file_log_level=logSettings["FILE_LOG_LEVEL"],
                        log_retention=logSettings["LOG_RETENTION"],
                        console_log_level=logSettings["CONSOLE_LOG_LEVEL"],
                        clear_first=True,
                    )
                    logger.init_logger(
                        logger_name="cherrypy.access",
                        log_to_console=logSettings["LOG_TO_CONSOLE"],
                        log_to_file=logSettings["LOG_TO_FILE"],
                        log_path=redball.LOG_PATH,
                        log_file="cherrypy.access.log",
                        file_log_level=logSettings["FILE_LOG_LEVEL"],
                        log_retention=logSettings["LOG_RETENTION"],
                        console_log_level=logSettings["CONSOLE_LOG_LEVEL"],
                        clear_first=True,
                    )
                    logger.init_logger(
                        logger_name="cherrypy.error",
                        log_to_console=logSettings["LOG_TO_CONSOLE"],
                        log_to_file=logSettings["LOG_TO_FILE"],
                        log_path=redball.LOG_PATH,
                        log_file="cherrypy.error.log",
                        file_log_level=logSettings["FILE_LOG_LEVEL"],
                        log_retention=logSettings["LOG_RETENTION"],
                        console_log_level=logSettings["CONSOLE_LOG_LEVEL"],
                        clear_first=True,
                    )
                    logger.init_logger(
                        logger_name="statsapi",
                        log_to_console=logSettings["LOG_TO_CONSOLE"],
                        log_to_file=logSettings["LOG_TO_FILE"],
                        log_path=redball.LOG_PATH,
                        log_file="statsapi.log",
                        file_log_level=logSettings["FILE_LOG_LEVEL"],
                        log_retention=logSettings["LOG_RETENTION"],
                        console_log_level=logSettings["CONSOLE_LOG_LEVEL"],
                        clear_first=True,
                    )
                elif kwargs["type"] == "Web/Security":
                    log.info("Restarting webserver...")
                    restart_webServer()
        elif kwargs.get("action") == "create_botType":
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_rw"
            ):
                log.warning(
                    "Received create bot type command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                result = rbConfig.create_botType(
                    description=kwargs["botType_description"],
                    moduleName=kwargs["botType_moduleName"],
                )
                if isinstance(result, str):
                    local_args.update({"errors": result, "errorcontainer_hide": ""})
                elif result == 0:
                    local_args.update(
                        {
                            "errors": "Bot type creation failed for unknown reason.",
                            "errorcontainer_hide": "",
                        }
                    )
        elif kwargs.get("action") == "delete_botType" and botType_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_rw"
            ):
                log.warning(
                    "Received delete bot type command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                rbConfig.delete_botType(botType_id)
                raise cherrypy.HTTPRedirect("/config")
        elif kwargs.get("action") == "edit_botType" and botType_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_ro"
            ):
                log.warning(
                    "Received edit bot type command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                local_args.update(
                    {
                        "title": "{} - Edit Bot Type".format(local_args["title"]),
                        "botType_id": botType_id,
                    }
                )
        elif kwargs.get("action") == "cancel":
            raise cherrypy.HTTPRedirect("/config")
        elif kwargs.get("action") == "save_botType" and botType_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_rw"
            ):
                log.warning(
                    "Received save bot type command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                rbConfig.update_botType(
                    id=botType_id,
                    description=kwargs["botType_description"],
                    moduleName=kwargs["botType_moduleName"],
                )
                raise cherrypy.HTTPRedirect("/config")
        elif kwargs.get("action") == "create_redditAuth":
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_rw"
            ):
                log.warning(
                    "Received create reddit auth command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                result = rbConfig.create_redditAuth(
                    description=kwargs["redditAuth_description"],
                    reddit_appId=kwargs["redditAuth_redditAppId"],
                    reddit_appSecret=kwargs["redditAuth_redditAppSecret"],
                    reddit_scopes=kwargs["redditAuth_redditScopes"],
                    reddit_refreshToken=kwargs.get("redditAuth_redditRefreshToken", ""),
                )
                if isinstance(result, str):
                    local_args.update({"errors": result, "errorcontainer_hide": ""})
                elif result == 0:
                    local_args.update(
                        {
                            "errors": "Reddit Authorization creation failed for unknown reason.",
                            "errorcontainer_hide": "",
                        }
                    )
        elif kwargs.get("action") == "delete_redditAuth" and redditAuth_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_rw"
            ):
                log.warning(
                    "Received delete reddit auth command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                rbConfig.delete_redditAuth(redditAuth_id)
                raise cherrypy.HTTPRedirect("/config")
        elif kwargs.get("action") == "edit_redditAuth" and redditAuth_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_ro"
            ):
                log.warning(
                    "Received edit reddit auth command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                local_args.update(
                    {
                        "title": "{} - Edit Reddit Auth".format(local_args["title"]),
                        "redditAuth_id": redditAuth_id,
                    }
                )
        elif kwargs.get("action") == "save_redditAuth" and redditAuth_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_rw"
            ):
                log.warning(
                    "Received save reddit auth command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                rbConfig.update_redditAuth(
                    id=redditAuth_id,
                    description=kwargs["redditAuth_description"],
                    reddit_appId=kwargs["redditAuth_redditAppId"],
                    reddit_appSecret=kwargs["redditAuth_redditAppSecret"],
                    reddit_scopes=kwargs["redditAuth_redditScopes"],
                    reddit_refreshToken=kwargs.get("redditAuth_redditRefreshToken", ""),
                )
                raise cherrypy.HTTPRedirect("/config")
        elif kwargs.get("action") == "authorize_redditAuth" and redditAuth_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_config_rw"
            ):
                log.warning(
                    "Received authorize reddit auth command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                log.debug(
                    "Received reddit auth request for redditAuth_id: {}.".format(
                        redditAuth_id
                    )
                )
                url = rbConfig.authorize_redditAuth(int(redditAuth_id))
                if url:
                    local_args.update(
                        {
                            "info": 'Log in to Reddit as your bot user, and <a href="{}" target="_new">click here</a> to authorize access to your bot account.'.format(
                                url
                            ),
                            "infocontainer_hide": "",
                        }
                    )
                else:
                    raise cherrypy.HTTPRedirect("/config")
        elif kwargs.get("action") == "create_user":
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_user_rw"
            ):
                log.warning(
                    "Received create user command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                result = user.create_user(
                    userid=kwargs.get("user_userid", ""),
                    password=kwargs.get("user_password", ""),
                    confirm_password=kwargs.get("user_passwordConfirm", ""),
                    name=kwargs.get("user_name", ""),
                    email=kwargs.get("user_email", ""),
                    reddit_userid=kwargs.get("user_reddit_userid", ""),
                    privileges=kwargs.get("user_privileges", []),
                )
                if isinstance(result, str):
                    local_args.update({"errors": result, "errorcontainer_hide": ""})
                elif result == 0:
                    local_args.update(
                        {
                            "errors": "User creation failed for unknown reason.",
                            "errorcontainer_hide": "",
                        }
                    )
                else:
                    local_args.update(
                        {
                            "info": "User created successfully.",
                            "infocontainer_hide": "",
                        }
                    )
        elif kwargs.get("action") == "edit_user" and user_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_user_ro"
            ):
                log.warning(
                    "Received edit user {} command, but user [{}] has insufficient privileges ({}).".format(
                        user_id,
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                local_args.update(
                    {
                        "title": "{} - Edit User".format(local_args["title"]),
                        "user_id": user_id,
                    }
                )
        elif kwargs.get("action") == "save_user" and user_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_user_rw"
            ):
                log.warning(
                    "Received save user command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                result = user.update_user(
                    id=user_id,
                    userid=kwargs["user_userid"],
                    name=kwargs["user_name"],
                    email=kwargs["user_email"],
                    reddit_userid=kwargs["user_reddit_userid"],
                    privileges=kwargs.get("user_privileges", []),
                )
                raise cherrypy.HTTPRedirect(
                    "/config?{}".format(
                        "i=Changes+saved+successfully."
                        if result is True
                        else "e=Changes+not+saved.+{}".format(
                            urllib.parse.quote(result)
                        )
                    )
                )
        elif kwargs.get("action") == "delete_user" and user_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_user_rw"
            ):
                log.warning(
                    "Received delete user command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                # Check if user_id is the only user,
                # or only user with access to web UI
                users = user.get_user_info()
                if (
                    isinstance(users, dict)
                    and users["id"] == user_id
                    or isinstance(users, list)
                    and len(users) == 1
                ):
                    # Don't delete the last user
                    local_args.update(
                        {
                            "errors": "Sorry, I can't let you delete the last user.",
                            "errorcontainer_hide": "",
                        }
                    )
                elif isinstance(users, list) and [
                    x["userid"] for x in users if "rb_web" in x["privileges"]
                ] == [user_id]:
                    # Don't delete the last user with access to the web UI
                    local_args.update(
                        {
                            "errors": "Sorry, I can't let you delete the last user with access to the web UI.",
                            "errorcontainer_hide": "",
                        }
                    )
                else:
                    result = user.delete_user(user_id)
                    if result == []:
                        raise cherrypy.HTTPRedirect(
                            "/config?i=User+successfully+deleted."
                        )
                    else:
                        log.error("Error deleting user {}: {}".format(user_id, result))
                        local_args.update(
                            {
                                "errors": "An error occurred while deleting the user.",
                                "errorcontainer_hide": "",
                            }
                        )
        elif kwargs.get("action") == "generate_user_apikey" and user_id:
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_apikeys_rw"
            ):
                log.warning(
                    "Received save user command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                result = user.update_user(id=user_id, apikey=uuid.uuid4().hex,)
                raise cherrypy.HTTPRedirect(
                    "/config?{}".format(
                        "i=API+key+generated+successfully."
                        if result is True
                        else "e=Error+generating+and+saving+API+key.+{}".format(
                            urllib.parse.quote(result)
                        )
                    )
                )

        return serve_page(templateName="config.mako", **local_args)

    @cherrypy.expose()
    @cherrypy.tools.auth()
    def logs(self, *args, **kwargs):
        local_args = {
            "title": "Logs",
            "errors": "",
            "errorcontainer_hide": " hide",
            "info": "",
            "infocontainer_hide": " hide",
        }
        if kwargs.get("action") == "downloadLog" and kwargs.get("logId"):
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_log_ro"
            ):
                log.warning(
                    "Received download log command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                logFile = os.path.join(redball.LOG_PATH, kwargs["logId"])
                if any(
                    x for x in ["\\", "/", ":", ".."] if x in kwargs["logId"]
                ) or not os.path.isfile(logFile):
                    local_args.update(
                        {"errors": "Invalid log specified.", "errorcontainer_hide": ""}
                    )
                else:
                    log.debug("Serving up log file: {}".format(logFile))
                    return cherrypy.lib.static.serve_file(
                        logFile, "application/x-download", "attachment", kwargs["logId"]
                    )
        elif kwargs.get("action") == "deleteLog" and kwargs.get("logId"):
            if not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_log_rw"
            ):
                log.warning(
                    "Received delete log command, but user [{}] has insufficient privileges ({}).".format(
                        cherrypy.session.get("_cp_username"),
                        redball.LOGGED_IN_USERS.get(
                            cherrypy.session.get("_cp_username"), {}
                        ).get("PRIVS", []),
                    )
                )
                local_args.update(
                    {
                        "errors": "You have insufficient privileges to perform the requested action.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                logFile = os.path.join(redball.LOG_PATH, kwargs["logId"])
                if (
                    any(x for x in ["\\", "/", ":", ".."] if x in kwargs["logId"])
                    or not os.path.isfile(logFile)
                    or kwargs["logId"] not in os.listdir(redball.LOG_PATH)
                ):
                    local_args.update(
                        {"errors": "Invalid log specified.", "errorcontainer_hide": ""}
                    )
                else:
                    try:
                        os.remove(logFile)
                        local_args.update(
                            {
                                "info": "Log file [{}] deleted successfully.".format(
                                    kwargs["logId"]
                                ),
                                "infocontainer_hide": "",
                            }
                        )
                    except Exception:
                        local_args.update(
                            {
                                "errors": "Error deleting log. Ensure the log is not actively being written to.",
                                "errorcontainer_hide": "",
                            }
                        )

        return serve_page(templateName="logs.mako", **local_args)

    @cherrypy.expose()
    @cherrypy.tools.auth()
    def password(self, user_id=None, *args, **kwargs):
        if rbConfig.get_sys_config(category="Web/Security", key="AUTH_TYPE")[0][
            "val"
        ] not in ["Form", "Basic"]:
            # Authentication not enabled
            raise cherrypy.HTTPRedirect("/")

        local_args = {
            "title": "Change Password",
            "user_id": user_id,
            "errors": "",
            "errorcontainer_hide": " hide",
            "info": "",
            "infocontainer_hide": " hide",
        }

        if (
            user_id
            and int(user_id)
            != int(
                user.get_user_info(
                    userid=cherrypy.session.get("_cp_username"), field="id"
                )
            )
            and not user.check_privilege(
                cherrypy.session.get("_cp_username"), "rb_user_rw"
            )
        ):
            log.warning(
                "Received change password command (with user_id specified), but user [{}] has insufficient privileges ({}).".format(
                    cherrypy.session.get("_cp_username"),
                    redball.LOGGED_IN_USERS.get(
                        cherrypy.session.get("_cp_username"), {}
                    ).get("PRIVS", []),
                )
            )
            user_id = None
            local_args.update(
                {
                    "user_id": user_id,
                    "errors": "You have insufficient privileges to perform the requested action.",
                    "errorcontainer_hide": "",
                }
            )

        u = user.get_user_info(uid=user_id)
        if not u:
            user_id = None
            local_args.update(
                {
                    "user_id": user_id,
                    "errors": "The specified user id was not found. Defaulting to your user id.",
                    "errorcontainer_hide": "",
                }
            )
        elif kwargs.get("action") == "changePassword":
            if not (
                kwargs.get("password|current")
                and kwargs.get("password|new")
                and kwargs.get("password|confirm")
            ):
                local_args.update(
                    {"errors": "Please complete all fields.", "errorcontainer_hide": ""}
                )
            elif kwargs["password|new"] != kwargs["password|confirm"]:
                local_args.update(
                    {
                        "errors": "New password and confirmation do not match.",
                        "errorcontainer_hide": "",
                    }
                )
            elif not cherrypy.session.get("_cp_username"):
                local_args.update(
                    {"errors": "Unable to authenticate you.", "errorcontainer_hide": ""}
                )
            elif not user.check_password(
                kwargs["password|current"],
                user.get_user_info(
                    userid=cherrypy.session["_cp_username"], field="password"
                ),
            ):
                local_args.update(
                    {
                        "errors": "Incorrect current password entered.",
                        "errorcontainer_hide": "",
                    }
                )
            else:
                pwq = (
                    "UPDATE rb_users set password=? where id=?;",
                    (user.hash_password(kwargs["password|new"]), u["id"],),
                )
                pwresult = database.db_qry(pwq, commit=True, closeAfter=True)
                if isinstance(pwresult, str):
                    local_args.update(
                        {
                            "errors": "Error executing database query to update password: {}.".format(
                                pwresult
                            ),
                            "errorcontainer_hide": "",
                        }
                    )
                else:
                    local_args.update(
                        {
                            "info": "Password updated successfully.",
                            "infocontainer_hide": "",
                        }
                    )

        return serve_page(templateName="password.mako", **local_args)

    @cherrypy.expose()
    @cherrypy.tools.auth()
    def authorize(self, *args, **kwargs):
        if not user.check_privilege(
            cherrypy.session.get("_cp_username"), "rb_config_rw"
        ):
            log.warning(
                "Received reddit authorization callback, but user [{}] has insufficient privileges ({}).".format(
                    cherrypy.session.get("_cp_username"),
                    redball.LOGGED_IN_USERS.get(
                        cherrypy.session.get("_cp_username"), {}
                    ).get("PRIVS", []),
                )
            )
            return serve_page(
                templateName="config.mako",
                botType_id=None,
                redditAuth_id=None,
                user_id=None,
                title="System Configuration",
                errors="You have insufficient privileges to perform the requested action",
                errorcontainer_hide="",
            )

        if not kwargs.get("state") or not kwargs.get("code"):
            return False

        result = rbConfig.callBack_redditAuth(
            state=kwargs["state"], code=kwargs["code"]
        )
        if result:
            return serve_page(
                templateName="config.mako",
                botType_id=None,
                redditAuth_id=None,
                user_id=None,
                title="System Configuration",
                info="Successfully updated Reddit refresh token.",
                infocontainer_hide="",
            )
        elif isinstance(result, str):
            return serve_page(
                templateName="config.mako",
                botType_id=None,
                redditAuth_id=None,
                user_id=None,
                title="System Configuration",
                errors="Error retrieving Reddit refresh token: {}".format(result),
                errorcontainer_hide="",
            )
        else:
            return serve_page(
                templateName="config.mako",
                botType_id=None,
                redditAuth_id=None,
                user_id=None,
                title="System Configuration",
                errors="Error retrieving Reddit refresh token.",
                errorcontainer_hide="",
            )


@cherrypy.expose
class APIv1(object):
    def GET(self, *args, **kwargs):
        log.debug(
            "Received API call via GET method. args: {}, kwargs: {}".format(
                args, kwargs
            )
        )
        response = {}
        errors = []
        if kwargs.get("apikey") and self._authorize(kwargs["apikey"]):
            u = user.get_user_info(apikey=kwargs["apikey"])
            if len(args):
                try:
                    if args[0].lower() == "bots":
                        if len(args) == 1:
                            # Get all bots
                            response.update(
                                {
                                    "bots": [
                                        b
                                        for b in bot.get_bots()
                                        if user.check_privilege(
                                            u["userid"], "rb_bot_{}_ro".format(b["id"])
                                        )
                                    ]
                                }
                            )
                        elif len(args) == 2:
                            # Bot id specified
                            if not user.check_privilege(
                                u["userid"], "rb_bot_{}_ro".format(args[1])
                            ):
                                log.warning(
                                    "Received API call for bot {}, but user [{}] has insufficient privileges ({}).".format(
                                        args[1], u["userid"], u["privileges"],
                                    )
                                )
                                # Insufficient privileges
                                errors.append(self._status(403))
                                return self._prep(errors=errors)
                            else:
                                bt = bot.get_bots(args[1])
                                bt.update(
                                    {
                                        "config": rbConfig.get_bot_config(
                                            args[1],
                                            excludeSysFields=True,
                                            sortByCategory=True,
                                        )
                                    }
                                )
                                response.update({"bots": [bt]})
                        elif len(args) == 3:
                            # Bot id and attribute specified
                            if not user.check_privilege(
                                u["userid"], "rb_bot_{}_ro".format(args[1])
                            ):
                                log.warning(
                                    "Received API call for bot {}, but user [{}] has insufficient privileges ({}).".format(
                                        args[1], u["userid"], u["privileges"],
                                    )
                                )
                                # Insufficient privileges
                                errors.append(self._status(403))
                                return self._prep(errors=errors)
                            else:
                                if args[2] == "config":
                                    response.update(
                                        {
                                            "bots": [
                                                {
                                                    "id": args[1],
                                                    "config": rbConfig.get_bot_config(
                                                        args[1],
                                                        excludeSysFields=True,
                                                        sortByCategory=True,
                                                    ),
                                                }
                                            ]
                                        }
                                    )
                                else:
                                    response.update(
                                        {
                                            "bots": [
                                                {
                                                    "id": args[1],
                                                    args[2]: bot.get_bots(args[1])[
                                                        args[2]
                                                    ],
                                                }
                                            ]
                                        }
                                    )
                        elif len(args) == 4:
                            # Bot id and attribute specified
                            if not user.check_privilege(
                                u["userid"], "rb_bot_{}_ro".format(args[1])
                            ):
                                log.warning(
                                    "Received API call for bot {}, but user [{}] has insufficient privileges ({}).".format(
                                        args[1], u["userid"], u["privileges"],
                                    )
                                )
                                # Insufficient privileges
                                errors.append(self._status(403))
                                return self._prep(errors=errors)
                            else:
                                if args[2] == "config":
                                    response.update(
                                        {
                                            "bots": [
                                                {
                                                    "id": args[1],
                                                    "config": rbConfig.get_bot_config(
                                                        args[1],
                                                        confId=args[3],
                                                        excludeSysFields=True,
                                                        sortByCategory=True,
                                                    ),
                                                }
                                            ]
                                        }
                                    )
                                else:
                                    # Invalid arg(s)
                                    errors.append(self._status(400))
                                    return self._prep(errors=errors)
                        else:
                            # Too many args
                            errors.append(self._status(400))
                            return self._prep(errors=errors)
                    elif args[0].lower() == "bottypes":
                        if not user.check_privilege(u["userid"], "rb_config_ro"):
                            log.warning(
                                "Received API call for system config, but user [{}] has insufficient privileges ({}).".format(
                                    u["userid"], u["privileges"],
                                )
                            )
                            # Insufficient privileges
                            errors.append(self._status(403))
                            return self._prep(errors=errors)
                        else:
                            if len(args) == 1:
                                # Get all bot types
                                response.update({"botTypes": rbConfig.get_botTypes()})
                            elif len(args) == 2:
                                # BotType id specified
                                response.update(
                                    {"botTypes": [rbConfig.get_botTypes(args[1])]}
                                )
                            elif len(args) == 3:
                                # BotType id and attribute specified
                                response.update(
                                    {
                                        "botTypes": [
                                            {
                                                "id": args[1],
                                                args[2]: rbConfig.get_botTypes(args[1])[
                                                    args[2]
                                                ],
                                            }
                                        ]
                                    }
                                )
                            else:
                                # Too many args
                                errors.append(self._status(400))
                                return self._prep(errors=errors)
                    elif args[0].lower() == "redditauths":
                        if not user.check_privilege(u["userid"], "rb_config_ro"):
                            log.warning(
                                "Received API call for system config, but user [{}] has insufficient privileges ({}).".format(
                                    u["userid"], u["privileges"],
                                )
                            )
                            # Insufficient privileges
                            errors.append(self._status(403))
                            return self._prep(errors=errors)
                        else:
                            if len(args) == 1:
                                # Get all reddit auths
                                response.update(
                                    {"redditAuths": rbConfig.get_redditAuths()}
                                )
                            elif len(args) == 2:
                                # Reddit auth id specified
                                response.update(
                                    {"redditAuths": [rbConfig.get_redditAuths(args[1])]}
                                )
                            elif len(args) == 3:
                                # Reddit auth id and attribute specified
                                response.update(
                                    {
                                        "redditAuths": [
                                            {
                                                "id": args[1],
                                                args[2]: rbConfig.get_redditAuths(
                                                    args[1]
                                                )[args[2]],
                                            }
                                        ]
                                    }
                                )
                            else:
                                # Too many args
                                errors.append(self._status(400))
                                return self._prep(errors=errors)
                    else:
                        errors.append(self._status(400))
                        return self._prep(errors=errors)
                except Exception as e:
                    # Exception encountered while processing request
                    log.debug("Error processing API call: {}".format(e))
                    if redball.DEV:
                        raise

                    errors.append(self._status(500))
                    return self._prep(errors=errors)
            else:
                # No endpoint specified
                errors.append(self._status(400))
                return self._prep(errors=errors)

            return self._prep(response=response, errors=errors)
        else:
            # Missing or bad API Key
            errors.append(self._status(401))
            return self._prep(errors=errors)

    def POST(self, *args, **kwargs):
        log.debug(
            "Received API call via POST method. args: {}, kwargs: {}".format(
                args, kwargs
            )
        )
        response = {}
        errors = []
        if kwargs.get("apikey") and self._authorize(kwargs["apikey"]):
            u = user.get_user_info(apikey=kwargs["apikey"])
            if len(args):
                try:
                    if args[0].lower() == "bots":
                        if len(args) == 1:
                            if not user.check_privilege(u["userid"], "rb_bot_create"):
                                log.warning(
                                    "Received API call for create bot, but user [{}] has insufficient privileges ({}).".format(
                                        u["userid"], u["privileges"],
                                    )
                                )
                                # Insufficient privileges
                                errors.append(self._status(403))
                                return self._prep(errors=errors)
                            else:
                                # Check for required kwargs and create the bot
                                newBot = bot.Bot(
                                    botInfo={
                                        "name": kwargs["name"],
                                        "botType": kwargs["botType"],
                                        "autoRun": kwargs["autoRun"],
                                        "redditAuth": kwargs.get("redditAuth", ""),
                                    },
                                    create=True,
                                )
                                if isinstance(newBot.id, str):
                                    # Exception encountered while processing request
                                    log.debug(
                                        "Error creating new bot via API call: {}".format(
                                            newBot.id
                                        )
                                    )
                                    errors.append(self._status(500))
                                else:
                                    redball.BOTS.update({str(newBot.id): newBot})
                                    response.update({"bots": [{"id": newBot.id}]})
                                    # Grant rw access to the bot creator
                                    redball.LOGGED_IN_USERS[
                                        cherrypy.session.get("_cp_username")
                                    ]["PRIVS"].append("rb_bot_{}_rw".format(newBot.id))
                                    q = (
                                        "UPDATE rb_users SET privileges = ? WHERE userid=?;",
                                        (
                                            json.dumps(
                                                redball.LOGGED_IN_USERS[
                                                    cherrypy.session.get("_cp_username")
                                                ]["PRIVS"]
                                            ),
                                            cherrypy.session.get("_cp_username"),
                                        ),
                                    )
                                    database.db_qry(q, commit=True, closeAfter=True)
                        elif len(args) == 3:
                            if not user.check_privilege(
                                u["userid"], "rb_bot_{}_rw".format(args[1])
                            ):
                                log.warning(
                                    "Received API call for to post config for bot {}, but user [{}] has insufficient privileges ({}).".format(
                                        args[1], u["userid"], u["privileges"],
                                    )
                                )
                                # Insufficient privileges
                                errors.append(self._status(403))
                                return self._prep(errors=errors)
                            else:
                                # Additional argument included (should be /api/v1/bots/<bot_id>/config)
                                if args[2] == "config":
                                    # Create config setting(s) for given bot (args[1] should be botId)
                                    # check for json payload
                                    bodyLen = int(
                                        cherrypy.request.headers["Content-Length"]
                                    )
                                    if bodyLen > 0:
                                        postBody = json.loads(
                                            cherrypy.request.body.read(bodyLen)
                                        )
                                        log.debug("POST body: {}".format(postBody))
                                        result = rbConfig.add_bot_config(
                                            botId=args[1], multi=postBody, replace=False
                                        )
                                        if isinstance(result, str):
                                            # Insert query failed
                                            errors.append(self._status(400))
                                    else:
                                        result = rbConfig.add_bot_config(
                                            botId=args[1],
                                            category=kwargs["category"],
                                            key=kwargs["key"],
                                            val=kwargs["val"],
                                            description=kwargs.get("description", ""),
                                            type=kwargs.get("type", "str"),
                                            options=kwargs.get("options", ""),
                                            subkeys=kwargs.get("subkeys", ""),
                                            parent_key=kwargs.get("parent_key", ""),
                                            replace=False,
                                        )
                                else:
                                    # Unsupported/extra arg
                                    errors.append(self._status(414))
                        else:
                            # Too many args
                            errors.append(self._status(414))
                    elif args[0].lower() == "bottypes":
                        if not user.check_privilege(u["userid"], "rb_config_rw"):
                            log.warning(
                                "Received API call to create bot type, but user [{}] has insufficient privileges ({}).".format(
                                    u["userid"], u["privileges"],
                                )
                            )
                            # Insufficient privileges
                            errors.append(self._status(403))
                            return self._prep(errors=errors)
                        else:
                            if len(args) == 1:
                                # Check for required kwargs and create the botType
                                result = rbConfig.create_botType(
                                    description=kwargs["description"],
                                    moduleName=kwargs["moduleName"],
                                )
                                if isinstance(result, str) or result == 0:
                                    # Exception encountered while processing request
                                    log.debug(
                                        "Error creating new bot type via API call: {}".format(
                                            result
                                        )
                                    )
                                    errors.append(self._status(500))
                                else:
                                    response.update({"botTypes": [{"id": result}]})
                            else:
                                # Too many args
                                errors.append(self._status(414))
                    elif args[0].lower() == "redditauths":
                        if not user.check_privilege(u["userid"], "rb_config_rw"):
                            log.warning(
                                "Received API call to create reddit auth, but user [{}] has insufficient privileges ({}).".format(
                                    u["userid"], u["privileges"],
                                )
                            )
                            # Insufficient privileges
                            errors.append(self._status(403))
                            return self._prep(errors=errors)
                        else:
                            if len(args) == 1:
                                # Check for required kwargs and create the redditAuth
                                result = rbConfig.create_redditAuth(
                                    description=kwargs["description"],
                                    reddit_appId=kwargs["reddit_appId"],
                                    reddit_appSecret=kwargs["reddit_appSecret"],
                                    reddit_scopes=kwargs["reddit_scopes"],
                                    reddit_refreshToken=kwargs.get(
                                        "reddit_refreshToken", ""
                                    ),
                                )
                                if isinstance(result, str) or result == 0:
                                    # Exception encountered while processing request
                                    log.debug(
                                        "Error creating new reddit auth via API call: {}".format(
                                            result
                                        )
                                    )
                                    errors.append(self._status(500))
                                else:
                                    response.update({"redditAuths": [{"id": result}]})
                            else:
                                # Too many args
                                errors.append(self._status(414))
                except Exception as e:
                    # Exception encountered while processing request
                    log.debug("Error processing API call: {}".format(e))
                    if redball.DEV:
                        raise

                    errors.append(self._status(500))
            else:
                # No endpoint specified
                errors.append(self._status(400))
        else:
            # Missing or bad API Key
            errors.append(self._status(401))

        return self._prep(response=response, errors=errors)

    def PUT(self, *args, **kwargs):
        log.debug(
            "Received API call via PUT method. args: {}, kwargs: {}".format(
                args, kwargs
            )
        )
        response = {}
        errors = []
        if kwargs.get("apikey") and self._authorize(kwargs["apikey"]):
            u = user.get_user_info(apikey=kwargs["apikey"])
            if len(args):
                try:
                    if args[0].lower() == "bots":
                        if len(args) > 1 and not redball.BOTS.get(args[1]):
                            errors.append(self._status(404))
                        elif len(args) == 2:
                            if not user.check_privilege(
                                u["userid"], "rb_bot_{}_rw".format(args[1])
                            ):
                                log.warning(
                                    "Received API call to edit bot {}, but user [{}] has insufficient privileges ({}).".format(
                                        args[1], u["userid"], u["privileges"],
                                    )
                                )
                                # Insufficient privileges
                                errors.append(self._status(403))
                                return self._prep(errors=errors)
                            else:
                                # Check for required kwargs and update the bot
                                result = redball.BOTS[args[1]].update_info(
                                    name=kwargs.get("name"),
                                    botType=kwargs.get("botType"),
                                    autoRun=kwargs.get("autoRun"),
                                    redditAuth=kwargs.get("redditAuth"),
                                )
                                if result == "ERROR: Nothing provided to update.":
                                    errors.append(self._status(400))
                        elif len(args) == 3:
                            # args[1] should be botId and args[2] should be [start, stop, config]
                            if args[2].lower() in ["start", "stop"]:
                                if not user.check_privilege(
                                    u["userid"], "rb_bot_{}_startstop".format(args[1])
                                ):
                                    log.warning(
                                        "Received API call to start/stop bot {}, but user [{}] has insufficient privileges ({}).".format(
                                            args[1], u["userid"], u["privileges"],
                                        )
                                    )
                                    # Insufficient privileges
                                    errors.append(self._status(403))
                                    return self._prep(errors=errors)
                                else:
                                    result = (
                                        redball.BOTS[args[1]].stop()
                                        if args[2].lower() == "stop"
                                        else redball.BOTS[args[1]].start()
                                    )
                                    if not result:
                                        errors.append(
                                            "Bot {} is not running.".format(args[1])
                                        )
                                    response.update({"result": result})
                            elif args[2].lower() == "config":
                                if not user.check_privilege(
                                    u["userid"], "rb_bot_{}_rw".format(args[1])
                                ):
                                    log.warning(
                                        "Received API call to modify bot {} config, but user [{}] has insufficient privileges ({}).".format(
                                            args[1], u["userid"], u["privileges"],
                                        )
                                    )
                                    # Insufficient privileges
                                    errors.append(self._status(403))
                                    return self._prep(errors=errors)
                                else:
                                    # check for json payload
                                    bodyLen = int(
                                        cherrypy.request.headers["Content-Length"]
                                    )
                                    if bodyLen > 0:
                                        putBody = json.loads(
                                            cherrypy.request.body.read(bodyLen)
                                        )
                                        log.debug("PUT body: {}".format(putBody))
                                        result = rbConfig.add_bot_config(
                                            botId=args[1], multi=putBody, replace=True
                                        )
                                        if isinstance(result, str):
                                            # Insert query failed
                                            errors.append(self._status(400))
                                    else:
                                        # No data in request body
                                        errors.append(self._status(400))
                            else:
                                # Invalid arg(s)
                                errors.append(self._status(400))
                        elif len(args) == 4:
                            if args[2].lower() == "config":
                                if not user.check_privilege(
                                    u["userid"], "rb_bot_{}_rw".format(args[1])
                                ):
                                    log.warning(
                                        "Received API call to modify bot {} config, but user [{}] has insufficient privileges ({}).".format(
                                            args[1], u["userid"], u["privileges"],
                                        )
                                    )
                                    # Insufficient privileges
                                    errors.append(self._status(403))
                                    return self._prep(errors=errors)
                                else:
                                    # Update a given botConfigId
                                    data = {"id": args[3]}
                                    for k, v in kwargs.items():
                                        if k != "apikey":
                                            data.update({k: v})
                                    result = rbConfig.update_bot_config(
                                        botId=args[1], data=data
                                    )
                        else:
                            # Too many args
                            errors.append(self._status(414))
                    elif args[0].lower() == "bottypes":
                        if not user.check_privilege(u["userid"], "rb_config_rw"):
                            log.warning(
                                "Received API call to modify a bot type, but user [{}] has insufficient privileges ({}).".format(
                                    u["userid"], u["privileges"],
                                )
                            )
                            # Insufficient privileges
                            errors.append(self._status(403))
                            return self._prep(errors=errors)
                        else:
                            if len(args) == 2:
                                # Check for required kwargs and update the botType
                                result = rbConfig.update_botType(
                                    id=args[1],
                                    description=kwargs.get("description"),
                                    moduleName=kwargs.get("moduleName"),
                                )
                                if result == "ERROR: Nothing provided to update.":
                                    errors.append(self._status(400))
                            else:
                                # Too many or not enough args
                                errors.append(self._status(400))
                    elif args[0].lower() == "redditauths":
                        if not user.check_privilege(u["userid"], "rb_config_rw"):
                            log.warning(
                                "Received API call to modify a reddit authorization, but user [{}] has insufficient privileges ({}).".format(
                                    u["userid"], u["privileges"],
                                )
                            )
                            # Insufficient privileges
                            errors.append(self._status(403))
                            return self._prep(errors=errors)
                        else:
                            if len(args) == 2:
                                # Check for required kwargs and update the reddit auth
                                result = rbConfig.update_redditAuth(
                                    id=args[1],
                                    description=kwargs.get("description"),
                                    reddit_appId=kwargs.get("reddit_appId"),
                                    reddit_appSecret=kwargs.get("reddit_appSecret"),
                                    reddit_scopes=kwargs.get("reddit_scopes"),
                                    reddit_refreshToken=kwargs.get(
                                        "reddit_refreshToken"
                                    ),
                                )
                                if result == "ERROR: Nothing provided to update.":
                                    errors.append(self._status(400))
                            else:
                                # Too many or not enough args
                                errors.append(self._status(400))
                except Exception as e:
                    # Exception encountered while processing request
                    log.debug("Error processing API call: {}".format(e))
                    if redball.DEV:
                        raise

                    errors.append(self._status(500))
            else:
                # No endpoint specified
                errors.append(self._status(400))
        else:
            # Missing or bad API Key
            errors.append(self._status(401))

        return self._prep(response=response, errors=errors)

    def DELETE(self, *args, **kwargs):
        log.debug(
            "Received API call via DELETE method. args: {}, kwargs: {}".format(
                args, kwargs
            )
        )
        response = {}
        errors = []
        if kwargs.get("apikey") and self._authorize(kwargs["apikey"]):
            u = user.get_user_info(apikey=kwargs["apikey"])
            if len(args):
                try:
                    if args[0].lower() == "bots":
                        if not user.check_privilege(
                            u["userid"], "rb_bot_{}_rw".format(args[1])
                        ):
                            log.warning(
                                "Received API call to delete bot {} (or its configuration), but user [{}] has insufficient privileges ({}).".format(
                                    args[1], u["userid"], u["privileges"],
                                )
                            )
                            # Insufficient privileges
                            errors.append(self._status(403))
                            return self._prep(errors=errors)
                        else:
                            if len(args) == 2:
                                # Delete the bot
                                redball.BOTS[str(args[1])].delete_bot()
                            elif len(args) == 3:
                                if args[2] == "config":
                                    # Delete all config for given bot
                                    result = rbConfig.delete_bot_config(
                                        botId=args[1], all=True
                                    )
                                    if isinstance(result, str):
                                        errors.append(self._status(400))
                                else:
                                    # Invalid arg(s)
                                    errors.append(self._status(400))
                            elif len(args) == 4:
                                if args[2] == "config":
                                    # Delete specified bot config for given bot
                                    result = rbConfig.delete_bot_config(
                                        botId=args[1], confId=args[3]
                                    )
                                    if isinstance(result, str):
                                        errors.append(self._status(400))
                                else:
                                    # Invalid arg(s)
                                    errors.append(self._status(400))
                            else:
                                # Too many or not enough args
                                errors.append(self._status(400))
                    elif args[0].lower() == "bottypes":
                        if not user.check_privilege(u["userid"], "rb_config_rw"):
                            log.warning(
                                "Received API call to delete bot type {}, but user [{}] has insufficient privileges ({}).".format(
                                    args[1], u["userid"], u["privileges"],
                                )
                            )
                            # Insufficient privileges
                            errors.append(self._status(403))
                            return self._prep(errors=errors)
                        else:
                            if len(args) == 2:
                                # Delete the botType
                                rbConfig.delete_botType(args[1])
                            else:
                                # Too many or not enough args
                                errors.append(self._status(400))
                    elif args[0].lower() == "redditauths":
                        if not user.check_privilege(u["userid"], "rb_config_rw"):
                            log.warning(
                                "Received API call to delete reddit authorization {}, but user [{}] has insufficient privileges ({}).".format(
                                    args[1], u["userid"], u["privileges"],
                                )
                            )
                            # Insufficient privileges
                            errors.append(self._status(403))
                            return self._prep(errors=errors)
                        else:
                            if len(args) == 2:
                                # Delete the redditAuth
                                rbConfig.delete_redditAuth(args[1])
                            else:
                                # Too many or not enough args
                                errors.append(self._status(400))
                except Exception:
                    # Exception encountered while processing request
                    if redball.DEV:
                        raise

                    errors.append(self._status(500))
            else:
                # No endpoint specified
                errors.append(self._status(400))
        else:
            # Missing or bad API Key
            errors.append(self._status(401))

        return self._prep(response=response, errors=errors)

    @cherrypy.expose(["OPTIONS", "HEAD"])
    def PATCH(self, *args, **kwargs):
        log.debug(
            "Received API call via unsupported PATCH/OPTIONS/HEAD method. args: {}, kwargs: {}".format(
                args, kwargs
            )
        )
        response = {}
        errors = [self._status(405)]
        return self._prep(response=response, errors=errors)

    def _authorize(self, key):
        if key in ["", None]:
            return False

        u = user.get_user_info(apikey=key)
        if u in [None, {}]:
            return False

        if u["userid"] not in redball.LOGGED_IN_USERS.keys():
            redball.LOGGED_IN_USERS.update(
                {u["userid"]: {"PRIVS": u["privileges"], "privDate": time.time()}}
            )

        if not user.check_privilege(u.get("userid"), "rb_api"):
            log.warning(
                "Received API call, but user [{}] has insufficient privileges ({}).".format(
                    u.get("userid"), u.get("privileges"),
                )
            )
            return False
        else:
            log.debug("API call authorized for user [{}].".format(u["userid"]))
            return True

    def _prep(self, response=None, errors=None):
        data = {
            "meta": {"api_version": 1, "timestamp": time.time()},
            "errors": "",
            "response": "",
        }
        if errors:
            data.update({"errors": errors})

        if response:
            data.update({"response": response})

        return json.dumps(data)

    def _status(self, status_code=200):
        code_lookup = {
            200: "200 OK",
            201: "201 Created",
            204: "204 No Content",
            400: "400 Bad Request",
            401: "401 Unauthorized",
            403: "403 Forbidden",
            404: "404 Not Found",
            405: "405 Method Not Allowed",
            406: "406 Not Acceptable",
            409: "409 Conflict",
            410: "410 Gone",
            414: "414 URI Too Long",
            500: "500 Internal Server Error",
            501: "501 Not Implemented",
            502: "502 Bad Gateway",
            503: "503 Service Unavailable",
        }
        if status_code >= 400:
            cherrypy.response.status = code_lookup[status_code]

        return code_lookup[status_code]
