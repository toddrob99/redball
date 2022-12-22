"""Reddit Sidebar Updater
by Todd Roberts
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError
from datetime import datetime
import json
from mako.lookup import TemplateLookup
import mako.exceptions
import os
import praw
import pyprowl
import re
import requests
import sys
import threading
import time
import traceback
import tzlocal

import redball
from redball import logger

import statsapi
from ..nba_game_threads import pynbaapi
from ..nhl_game_threads import pynhlapi
from ..nfl_game_threads import mynflapi

__version__ = "1.1"


def run(bot, settings):
    sidebar_updater_bot = SidebarUpdaterBot(bot, settings)
    sidebar_updater_bot.run()


class SidebarUpdaterBot:
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        self.BOT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.BOT_TEMPLATE_PATH = []
        if self.settings.get("Bot", {}).get("TEMPLATE_PATH", "") != "":
            self.BOT_TEMPLATE_PATH.append(self.settings["Bot"]["TEMPLATE_PATH"])
        self.BOT_TEMPLATE_PATH.append(os.path.join(self.BOT_PATH, "templates"))
        self.lookup = TemplateLookup(directories=self.BOT_TEMPLATE_PATH)

    def run(self):
        self.log = logger.init_logger(
            logger_name="redball.bots." + threading.current_thread().name,
            log_to_console=self.settings.get("Logging", {}).get("LOG_TO_CONSOLE", True),
            log_to_file=self.settings.get("Logging", {}).get("LOG_TO_FILE", True),
            log_path=redball.LOG_PATH,
            log_file="{}.log".format(threading.current_thread().name),
            file_log_level=self.settings.get("Logging", {}).get("FILE_LOG_LEVEL"),
            log_retention=self.settings.get("Logging", {}).get("LOG_RETENTION", 7),
            console_log_level=self.settings.get("Logging", {}).get("CONSOLE_LOG_LEVEL"),
            clear_first=True,
            propagate=False,
        )
        self.log.debug(
            f"Sidebar Updater Bot v{__version__} received settings: {self.settings}. Template path: {self.BOT_TEMPLATE_PATH}"
        )

        # Initialize Reddit API connection
        self.init_reddit()

        # Initialize scheduler
        if "SCHEDULER" in vars(self.bot):
            # Scheduler already exists, maybe bot restarted
            sch_jobs = self.bot.SCHEDULER.get_jobs()
            self.log.warning(
                f"Scheduler already exists on bot startup with the following job(s): {sch_jobs}"
            )
            # Remove all jobs and shut down so we can start fresh
            for x in sch_jobs:
                x.remove()
            try:
                self.bot.SCHEDULER.shutdown()
            except SchedulerNotRunningError as e:
                self.log.debug(f"Could not shut down scheduler because: {e}")

        self.bot.SCHEDULER = BackgroundScheduler(
            timezone=tzlocal.get_localzone()
            if str(tzlocal.get_localzone()) != "local"
            else "America/New_York"
        )
        self.bot.SCHEDULER.start()

        self.bot.detailedState = {
            "summary": {
                "text": "Starting up, please wait 1 minute...",
                "html": "Starting up, please wait 1 minute...",
                "markdown": "Starting up, please wait 1 minute...",
            }
        }  # Initialize detailed state to a wait message

        # Start a scheduled task to update self.bot.detailedState every minute
        self.bot.SCHEDULER.add_job(
            self.bot_state,
            "interval",
            name=f"bot-{self.bot.id}-statusUpdateTask",
            id=f"bot-{self.bot.id}-statusUpdateTask",
            minutes=1,
            replace_existing=True,
        )

        if sport := self.settings.get("Bot", {}).get("SPORT"):
            self.log.debug(f"Bot set to sport: {sport}")
            self.sport = sport
        else:
            self.log.error(
                "No sport selected! Please select a sport in the Bot > SPORT setting. Aborting..."
            )
            self.bot.STOP = True
            self.shutdown()
            return

        if self.settings.get("Old Reddit", {}).get(
            "STANDINGS_ENABLED"
        ) or self.settings.get("New Reddit", {}).get("STANDINGS_ENABLED"):
            update_interval = self.settings["Bot"].get("UPDATE_INTERVAL", 60)
            self.log.debug(
                f"Scheduling job to update reddit every [{update_interval}] minute(s). Job name: [bot-{self.bot.id}-reddit_update_task]..."
            )
            self.bot.SCHEDULER.add_job(
                func=self.update_reddit,
                trigger="interval",
                name=f"bot-{self.bot.id}-reddit_update_task",
                id=f"bot-{self.bot.id}-reddit_update_task",
                minutes=update_interval,
                replace_existing=True,
            )
            self.log.debug("Running the job to get things started...")
            self.update_reddit()
        else:
            self.log.warning("Old and New Reddit are both disabled. Nothing to do!")
            self.bot.STOP = True
            self.shutdown()
            return

        while redball.SIGNAL is None and not self.bot.STOP:
            self.sleep(60)
            self.log.debug(
                f"Scheduler jobs w/ next run times: {[(x.name, x.next_run_time) for x in self.bot.SCHEDULER.get_jobs()]}"
            )

        self.shutdown()

    def bot_state(self):
        bot_status = {
            "lastUpdated": datetime.today().strftime("%m/%d/%Y %I:%M:%S %p"),
            "summary": {
                "text": f"Subreddit: r/{self.subreddit.display_name}",
                "html": f'Subreddit: <a href="https://reddit.com/r/{self.subreddit.display_name}" target="_blank">{self.subreddit.display_name}</a>',
                "markdown": f"Subreddit: [{self.subreddit.display_name}](https://reddit.com/r/{self.subreddit.display_name})",
            },
        }
        bot_status["summary"][
            "text"
        ] += f"\n\nSport: {self.sport}\n\nOld Reddit Enabled (Standings): {self.settings.get('Old Reddit', {}).get('STANDINGS_ENABLED', False)}"
        bot_status["summary"][
            "text"
        ] += f"\n\nNew Reddit Enabled (Standings): {self.settings.get('New Reddit', {}).get('STANDINGS_ENABLED', False)}"
        bot_status["summary"][
            "html"
        ] += f"<br /><br />Sport: {self.sport}<br /><br />Old Reddit Enabled (Standings): {self.settings.get('Old Reddit', {}).get('STANDINGS_ENABLED', False)}"
        bot_status["summary"][
            "html"
        ] += f"<br /><br />New Reddit Enabled (Standings): {self.settings.get('New Reddit', {}).get('STANDINGS_ENABLED', False)}"
        bot_status["summary"][
            "markdown"
        ] += f"\n\nSport: {self.sport}\n\nOld Reddit Enabled (Standings): {self.settings.get('Old Reddit', {}).get('STANDINGS_ENABLED', False)}"
        bot_status["summary"][
            "markdown"
        ] += f"\n\nNew Reddit Enabled (Standings): {self.settings.get('New Reddit', {}).get('STANDINGS_ENABLED', False)}"
        self.log.debug(f"Bot Status: {bot_status}")
        self.bot.detailedState = bot_status

    def error_notification(self, action):
        # Generate and send notification to Prowl for errors
        prowl_key = self.settings.get("Prowl", {}).get("ERROR_API_KEY", "")
        prowl_priority = self.settings.get("Prowl", {}).get("ERROR_PRIORITY", "")
        newline = "\n"
        if prowl_key != "" and prowl_priority != "":
            self.notify_prowl(
                api_key=prowl_key,
                event=f"{self.bot.name} - {action}!",
                description=f"{action} for bot: [{self.bot.name}]!\n\n{newline.join(traceback.format_exception(*sys.exc_info()))}",
                priority=prowl_priority,
                app_name=f"redball - {self.bot.name}",
            )

    def get_nfl_token(self):
        self.log.debug("Retrieving fresh NFL API token...")
        url = "https://api.nfl.com/v1/reroute"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-domain-id": "100",
        }
        body = {
            "grant_type": "client_credentials",
        }

        try:
            r = requests.post(url, data=body, headers=headers)
            content = json.loads(r.content)
        except Exception as e:
            self.log.error(f"Caught exception requesting NFL API token: {e}")
            raise

        return content

    def init_reddit(self):
        self.log.debug(f"Initializing Reddit API with praw v{praw.__version__}...")
        with redball.REDDIT_AUTH_LOCKS[str(self.bot.redditAuth)]:
            try:
                self.reddit = praw.Reddit(
                    client_id=self.settings["Reddit Auth"]["reddit_clientId"],
                    client_secret=self.settings["Reddit Auth"]["reddit_clientSecret"],
                    token_manager=self.bot.reddit_auth_token_manager,
                    user_agent="redball Sidebar Updater Bot - https://github.com/toddrob99/redball/ - r/{}".format(
                        self.settings["Bot"].get("SUBREDDIT", "")
                    ),
                )
            except Exception as e:
                self.log.error(
                    "Error encountered attempting to initialize Reddit: {}".format(e)
                )
                self.error_notification("Error initializing Reddit")
                raise

            scopes = [
                "identity",
                "modconfig",
                "wikiread",
                "wikiedit",
            ]
            try:
                praw_scopes = self.reddit.auth.scopes()
            except Exception as e:
                self.log.error(
                    "Error encountered attempting to look up authorized Reddit scopes: {}".format(
                        e
                    )
                )
                self.error_notification(
                    "Error encountered attempting to look up authorized Reddit scopes"
                )
                raise

        missing_scopes = []
        self.log.debug("Reddit authorized scopes: {}".format(praw_scopes))
        try:
            if self.reddit.user.me() is None:
                raise ValueError(
                    "Failed to initialize Reddit instance--authorized user is None"
                )
            self.log.info("Reddit authorized user: {}".format(self.reddit.user.me()))
        except Exception as e:
            self.log.warning(
                "Error encountered attempting to identify authorized Reddit user (identity scope may not be authorized): {}".format(
                    e
                )
            )
            self.error_notification(
                "Error encountered attempting to identify authorized Reddit user (identity scope may not be authorized)"
            )

        for scope in scopes:
            if scope not in praw_scopes:
                missing_scopes.append(scope)

        if len(missing_scopes):
            self.log.error(
                "Scope(s) not authorized: {}. Please check/update/re-authorize Reddit Authorization in redball System Config.".format(
                    missing_scopes
                )
            )

        self.subreddit = self.reddit.subreddit(
            self.settings.get("Bot", {}).get("SUBREDDIT")
        )

    def notify_prowl(
        self, api_key, event, description, priority=0, url=None, app_name="redball"
    ):
        # Send a notification to Prowl
        p = pyprowl.Prowl(apiKey=api_key, appName=app_name)

        self.log.debug(
            f"Sending notification to Prowl with API Key: {api_key}. Event: {event}, Description: {description}, Priority: {priority}, URL: {url}..."
        )
        try:
            p.notify(
                event=event,
                description=description,
                priority=priority,
                url=url,
            )
            self.log.info("Notification successfully sent to Prowl!")
            return True
        except Exception as e:
            self.log.error("Error sending notification to Prowl: {}".format(e))
            return False

    def render_template(self, template_file_name, **kwargs):
        self.log.debug(f"Rendering template [{template_file_name}]...")
        try:
            template = self.lookup.get_template(template_file_name)
            rendered_text = template.render(**kwargs)
            self.log.debug(f"Rendered template [{template_file_name}]: {rendered_text}")
            return rendered_text
        except Exception as e:  # TODO: more specific exception(s) to handle
            self.log.error(
                f"Error rendering template [{template_file_name}]: {e}{mako.exceptions.text_error_template().render()}"
            )
            self.error_notification(f"Error rendering template [{template_file_name}]")
            return ""

    def shutdown(self):
        if "SCHEDULER" in vars(self.bot):
            sch_jobs = self.bot.SCHEDULER.get_jobs()
            # Remove all jobs and shut down the scheduler
            for x in sch_jobs:
                self.log.debug(f"Removing scheduled job [{x.name}]")
                x.remove()
            try:
                self.log.debug("Shutting down scheduler...")
                self.bot.SCHEDULER.shutdown()
            except SchedulerNotRunningError as e:
                self.log.debug(f"Could not shut down scheduler because: {e}")
        self.bot.STOP = True
        self.bot.detailedState = {
            "summary": {
                "text": "The bot has been shut down.",
                "html": "The bot has been shut down.",
                "markdown": "The bot has been shut down.",
            }
        }
        self.log.info("Shutting down...")

    def sleep(self, t):
        # t = total number of seconds to sleep before returning
        i = 0
        while redball.SIGNAL is None and not self.bot.STOP and i < t:
            i += 1
            time.sleep(1)

    def update_new_reddit_standings(
        self, my_team, standings, team_subs, all_teams, current_week=None
    ):
        standings_widget_name = self.settings["New Reddit"].get(
            "STANDINGS_WIDGET_NAME", "Standings"
        )
        standings_text = self.render_template(
            self.settings["New Reddit"]["STANDINGS_TEMPLATE"]
            if self.settings["New Reddit"].get("STANDINGS_TEMPLATE", "") != ""
            else f"{self.sport.lower()}_standings.mako",
            my_team=my_team,
            standings=standings,
            team_subs=team_subs,
            num_to_show=self.settings["New Reddit"].get("STANDINGS_NUM_TO_SHOW", 99),
            all_teams=all_teams,
            current_week=current_week,
            settings=self.settings["New Reddit"],
        )
        if standings_text == "":
            self.log.warning(
                "Standings text is blank, skipping widget update/creation."
            )
            return
        subreddit_widgets = self.subreddit.widgets
        subreddit_widgets.refresh()
        standings_widget = next(
            (
                x
                for x in subreddit_widgets.sidebar
                if x.shortName == standings_widget_name
            ),
            None,
        )
        if standings_widget:
            self.log.debug(
                f"Current contents of standings widget: [{standings_widget.text}]"
            )
            try:
                standings_widget.mod.update(text=standings_text)
                self.log.debug("Finished updating new reddit.")
            except Exception as e:
                self.log.error(f"Error updating standings widget: {e}")
        else:
            self.log.info(
                f"No widget found named [{standings_widget_name}]. Creating it..."
            )
            self.subreddit.widgets.mod.add_text_area(
                standings_widget_name,
                standings_text,
                styles={
                    "backgroundColor": self.settings["New Reddit"].get(
                        "STANDINGS_WIDGET_BG_COLOR", "#FFFF66"
                    ),
                    "headerColor": self.settings["New Reddit"].get(
                        "STANDINGS_WIDGET_HEADER_COLOR", "#3333EE"
                    ),
                },
            )
            self.log.debug("Finished updating new reddit (created new widget).")

    def update_old_reddit_standings(
        self, my_team, standings, team_subs, all_teams, current_week=None
    ):
        standings_text = self.render_template(
            self.settings["Old Reddit"]["STANDINGS_TEMPLATE"]
            if self.settings["Old Reddit"].get("STANDINGS_TEMPLATE", "") != ""
            else f"{self.sport.lower()}_standings.mako",
            my_team=my_team,
            standings=standings,
            team_subs=team_subs,
            num_to_show=self.settings["Old Reddit"].get("STANDINGS_NUM_TO_SHOW", 99),
            all_teams=all_teams,
            current_week=current_week,
            settings=self.settings["Old Reddit"],
        )
        if standings_text == "":
            self.log.warning("Standings text is blank, skipping sidebar update/insert.")
            return
        wiki_page = self.subreddit.wiki["config/sidebar"]
        full_sidebar_text = wiki_page.content_md
        regex = re.compile(
            self.settings["Old Reddit"]["STANDINGS_REGEX"]
            if self.settings["Old Reddit"].get("STANDINGS_REGEX", "") != ""
            else "\\[]\\(\\/redball\\/standings\\).*\\[]\\(\\/redball\\/standings\\)",
            flags=re.DOTALL,
        )
        if regex.search(full_sidebar_text):
            new_sidebar_text = re.sub(regex, standings_text, full_sidebar_text)
        else:
            self.log.info(
                "Regex didn't match anything in the sidebar, so appending to the end."
            )
            new_sidebar_text = f"{full_sidebar_text}\n\n{standings_text}"
        try:
            wiki_page.edit(content=new_sidebar_text, reason="Standings")
            self.log.debug("Finished updating old reddit.")
        except Exception as e:
            self.log.error(f"Error updating old reddit sidebar wiki: {e}")

    def update_reddit(self):
        if self.sport == "MLB":
            if self.settings.get("MLB", {}).get("TEAM", "") == "":
                self.log.critical("No team selected! Set MLB > TEAM in Bot Config.")
                self.bot.STOP = True
                return
            all_teams = statsapi.get(
                "teams", {"sportIds": 1, "hydrate": "league,division"}
            ).get("teams", [])
            my_team = next(
                (
                    x
                    for x in all_teams
                    if x["id"] == int(self.settings["MLB"]["TEAM"].split("|")[1])
                ),
                None,
            )
            if self.settings.get("Old Reddit", {}).get(
                "STANDINGS_ENABLED"
            ) or self.settings.get("New Reddit", {}).get("STANDINGS_ENABLED"):
                standings = statsapi.standings_data()
            else:
                standings = None
            team_subs = self.mlb_team_subs
            current_week = None
        elif self.sport == "NBA":
            if self.settings.get("NBA", {}).get("TEAM", "") == "":
                self.log.critical("No team selected! Set NBA > TEAM in Bot Config.")
                self.bot.STOP = True
                return
            nba = pynbaapi.nba.NBA(
                f"RedditSidebarUpdater/{__version__} (platform; redball/{redball.__version__})"
            )
            season = (
                datetime.today().strftime("%Y")
                if int(datetime.today().strftime("%m")) >= 8
                else str(int(datetime.today().strftime("%Y")) - 1)
            )
            all_teams = nba.all_teams(season)
            my_team = nba.team(int(self.settings["NBA"]["TEAM"].split("|")[1]))
            if self.settings.get("Old Reddit", {}).get(
                "STANDINGS_ENABLED"
            ) or self.settings.get("New Reddit", {}).get("STANDINGS_ENABLED"):
                standings = nba.standings(season=season)
            else:
                standings = None
            team_subs = self.nba_team_subs
            current_week = None
        elif self.sport == "NFL":
            if self.settings.get("NFL", {}).get("TEAM", "") == "":
                self.log.critical("No team selected! Set NFL > TEAM in Bot Config.")
                self.bot.STOP = True
                return
            nfl = mynflapi.APISession(self.get_nfl_token())
            current_week = nfl.weekByDate(datetime.now().strftime("%Y-%m-%d"))
            all_teams = nfl.teams(
                current_week.get("season", datetime.now().strftime("%Y"))
            ).get("teams", [])
            my_team = next(
                (
                    x
                    for x in all_teams
                    if x["abbreviation"] == self.settings["NFL"]["TEAM"].split("|")[1]
                ),
                None,
            )
            if self.settings.get("Old Reddit", {}).get(
                "STANDINGS_ENABLED"
            ) or self.settings.get("New Reddit", {}).get("STANDINGS_ENABLED"):
                standings = (
                    nfl.standings(
                        season=current_week["season"],
                        seasonType="REG",
                        week=current_week["week"]
                        if current_week["seasonType"] == "REG"
                        else 17
                        if current_week["seasonType"] == "POST"
                        else 1,
                    )
                    .get("weeks", [{}])[0]
                    .get("standings", [])
                )
            else:
                standings = None
            team_subs = self.nfl_team_subs
        elif self.sport == "NHL":
            if self.settings.get("NHL", {}).get("TEAM", "") == "":
                self.log.critical("No team selected! Set NHL > TEAM in Bot Config.")
                self.bot.STOP = True
                return
            nhl = pynhlapi.API()
            all_teams = nhl.teams()
            my_team = next(
                (
                    x
                    for x in all_teams
                    if x["id"] == int(self.settings["NHL"]["TEAM"].split("|")[1])
                ),
                None,
            )
            if self.settings.get("Old Reddit", {}).get(
                "STANDINGS_ENABLED"
            ) or self.settings.get("New Reddit", {}).get("STANDINGS_ENABLED"):
                standings = nhl.standings()
            else:
                standings = None
            team_subs = self.nhl_team_subs
            current_week = None

        self.log.debug(f"{self.sport=}")
        self.log.debug(f"{my_team=}")
        self.log.debug(f"{all_teams=}")
        self.log.debug(f"{standings=}")
        self.log.debug(f"{team_subs=}")
        self.log.debug(f"{current_week=}")

        if self.settings.get("Old Reddit", {}).get("STANDINGS_ENABLED"):
            self.log.debug("Updating Old Reddit...")
            self.update_old_reddit_standings(
                my_team,
                standings,
                team_subs,
                all_teams,
                current_week,
            )

        if self.settings.get("New Reddit", {}).get("STANDINGS_ENABLED"):
            self.log.debug("Updating New Reddit...")
            self.update_new_reddit_standings(
                my_team,
                standings,
                team_subs,
                all_teams,
                current_week,
            )

    mlb_team_subs = {
        142: "/r/minnesotatwins",
        145: "/r/WhiteSox",
        116: "/r/MotorCityKitties",
        118: "/r/KCRoyals",
        114: "/r/ClevelandGuardians",
        140: "/r/TexasRangers",
        117: "/r/Astros",
        133: "/r/OaklandAthletics",
        108: "/r/AngelsBaseball",
        136: "/r/Mariners",
        111: "/r/RedSox",
        147: "/r/NYYankees",
        141: "/r/TorontoBlueJays",
        139: "/r/TampaBayRays",
        110: "/r/Orioles",
        138: "/r/Cardinals",
        113: "/r/Reds",
        134: "/r/Buccos",
        112: "/r/CHICubs",
        158: "/r/Brewers",
        137: "/r/SFGiants",
        109: "/r/azdiamondbacks",
        115: "/r/ColoradoRockies",
        119: "/r/Dodgers",
        135: "/r/Padres",
        143: "/r/Phillies",
        121: "/r/NewYorkMets",
        146: "/r/MiamiMarlins",
        120: "/r/Nationals",
        144: "/r/Braves",
    }

    nba_team_subs = {
        1610612737: "/r/atlantahawks",
        1610612751: "/r/gonets",
        1610612738: "/r/bostonceltics",
        1610612766: "/r/charlottehornets",
        1610612741: "/r/chicagobulls",
        1610612739: "/r/clevelandcavs",
        1610612742: "/r/mavericks",
        1610612743: "/r/denvernuggets",
        1610612765: "/r/detroitpistons",
        1610612744: "/r/warriors",
        1610612745: "/r/rockets",
        1610612754: "/r/pacers",
        1610612746: "/r/laclippers",
        1610612747: "/r/lakers",
        1610612763: "/r/memphisgrizzlies",
        1610612748: "/r/heat",
        1610612749: "/r/mkebucks",
        1610612750: "/r/timberwolves",
        1610612740: "/r/nolapelicans",
        1610612752: "/r/nyknicks",
        1610612760: "/r/thunder",
        1610612753: "/r/orlandomagic",
        1610612755: "/r/sixers",
        1610612756: "/r/suns",
        1610612757: "/r/ripcity",
        1610612758: "/r/kings",
        1610612759: "/r/nbaspurs",
        1610612761: "/r/torontoraptors",
        1610612762: "/r/utahjazz",
        1610612764: "/r/washingtonwizards",
    }

    nfl_team_subs = {
        "ARI": "/r/AZCardinals",
        "ATL": "/r/falcons",
        "BAL": "/r/ravens",
        "BUF": "/r/buffalobills",
        "CAR": "/r/panthers",
        "CHI": "/r/CHIBears",
        "CIN": "/r/bengals",
        "CLE": "/r/Browns",
        "DAL": "/r/cowboys",
        "DEN": "/r/DenverBroncos",
        "DET": "/r/detroitlions",
        "GB": "/r/GreenBayPackers",
        "HOU": "/r/Texans",
        "IND": "/r/Colts",
        "JAX": "/r/Jaguars",
        "KC": "/r/KansasCityChiefs",
        "LA": "/r/LosAngelesRams",
        "LAC": "/r/Chargers",
        "LV": "/r/raiders",
        "MIA": "/r/miamidolphins",
        "MIN": "/r/minnesotavikings",
        "NE": "/r/Patriots",
        "NO": "/r/Saints",
        "NYG": "/r/NYGiants",
        "NYJ": "/r/nyjets",
        "PHI": "/r/eagles",
        "PIT": "/r/steelers",
        "SEA": "/r/Seahawks",
        "SF": "/r/49ers",
        "TB": "/r/buccaneers",
        "TEN": "/r/Tennesseetitans",
        "WAS": "/r/Commanders",
        0: "/r/NFL",
        "nfl": "/r/NFL",
        "NFL": "/r/NFL",
    }

    nhl_team_subs = {
        1: "/r/devils",
        2: "/r/newyorkislanders",
        3: "/r/rangers",
        4: "/r/flyers",
        5: "/r/penguins",
        6: "/r/bostonbruins",
        7: "/r/sabres",
        8: "/r/habs",
        9: "/r/ottawasenators",
        10: "/r/leafs",
        12: "/r/canes",
        13: "/r/floridapanthers",
        14: "/r/tampabaylightning",
        15: "/r/caps",
        16: "/r/hawks",
        17: "/r/detroitredwings",
        18: "/r/predators",
        19: "/r/stlouisblues",
        20: "/r/calgaryflames",
        21: "/r/coloradoavalanche",
        22: "/r/edmontonoilers",
        23: "/r/canucks",
        24: "/r/anaheimducks",
        25: "/r/dallasstars",
        26: "/r/losangeleskings",
        28: "/r/sanjosesharks",
        29: "/r/bluejackets",
        30: "/r/wildhockey",
        52: "/r/winnipegjets",
        53: "/r/coyotes",
        54: "/r/goldenknights",
        55: "/r/seattlekraken",
    }
