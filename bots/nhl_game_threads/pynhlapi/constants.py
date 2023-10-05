APP_NAME = "pynhlapi"
API_URL = "https://api-web.nhle.com"
TEAMS_ENDPOINT = API_URL + "/v1/schedule-calendar/{ymd}"
STANDINGS_ENDPOINT = API_URL + "/v1/standings/{ymd}"
SCOREBOARD_ENDPOINT = API_URL + "/v1/score/{ymd}"
SCHEDULE_ENDPOINT = API_URL + "/v1/schedule/{ymd}"
GAME_ENDPOINT = API_URL + "/v1/gamecenter/{game_pk}/landing"
SEASONS_ENDPOINT = "https://api.nhle.com/stats/rest/en/season?sort=%5B%7B%22property%22:%22id%22,%22direction%22:%22DESC%22%7D%5D"
GAME_BOXSCORE_ENDPOINT = API_URL + "/v1/gamecenter/{game_pk}/boxscore"
GAME_PLAYBYPLAY_ENDPOINT = API_URL + "/v1/gamecenter/{game_pk}/play-by-play"
