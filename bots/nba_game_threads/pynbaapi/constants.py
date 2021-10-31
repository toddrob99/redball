APP_NAME = "pynbaapi"

API_URL = "https://stats.nba.com/stats"
# Flat response endpoints
API_COMMONTEAMROSTER_ENDPOINT = "/commonteamroster?LeagueID={league_id}&Season={season}&TeamID={team_id}"
API_COMMONALLPLAYERS_ENDPOINT = "/commonallplayers?IsOnlyCurrentSeason={current_season_only}&LeagueID={league_id}&Season={season}"
API_LEAGUESTANDINGSV3_ENDPOINT = "/leaguestandingsv3?LeagueID={league_id}&Season={season}&SeasonType={season_type}"
API_SCOREBOARDV2_ENDPOINT = "/scoreboardv2?DayOffset={day_offset}&GameDate={game_date}&LeagueID={league_id}"
API_TEAMDETAILS_ENDPOINT = "/teamdetails?TeamID={team_id}"
API_TEAMINFOCOMMON_ENDPOINT = "/teaminfocommon?LeagueID={league_id}&Season={season}&SeasonType={season_type}&TeamID={team_id}"

# Nested response endpoints
API_BOXSCORESUMMARYV3_ENDPOINT = "/boxscoresummaryv3?GameID={game_id}"
API_BOXSCORETRADITIONALV3_ENDPOINT = "/boxscoretraditionalv3?GameID={game_id}&StartPeriod={start_period}&EndPeriod={end_period}&StartRange={start_range}&EndRange={end_range}&RangeType={range_type}"
API_PLAYBYPLAYV3_ENDPOINT = "/playbyplayv3?GameID={game_id}&StartPeriod={start_period}&EndPeriod={end_period}"
API_SCHEDULELEAGUEV2_ENDPOINT = "/scheduleleaguev2?LeagueID={league_id}&Season={season}"  # &TeamID={team_id}
API_SCOREBOARDV3_ENDPOINT = "/scoreboardv3?DayOffset={day_offset}&GameDate={game_date}&LeagueID={league_id}"
