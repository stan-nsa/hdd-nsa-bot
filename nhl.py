# Schedule:  https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.teams,schedule.scoringplays,schedule.game.seriesSummary,seriesSummary.series,schedule.linescore
#            https://statsapi.web.nhl.com/api/v1/schedule?date=2022-11-25
# Standings: https://statsapi.web.nhl.com/api/v1/standings
# Boxscore:  https://statsapi.web.nhl.com/api/v1/game/2021021092/boxscore

import requests
from datetime import datetime, timezone
import pytz
from emoji import emojize #Overview of all emoji: https://carpedm20.github.io/emoji/

NHL_API_URL = "https://statsapi.web.nhl.com/api/v1"

# TimeZone
tzEST = pytz.timezone("US/Eastern")
tzMSK = pytz.timezone("Europe/Moscow")
tzVLAT = pytz.timezone("Asia/Vladivostok")

def get_schedule_today():
    # fetch game list
    schedule_str = "/schedule?expand=schedule.teams,schedule.linescore"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-25"
    #schedule_str = "/schedule?expand=schedule.teams,schedule.linescore&date=2022-11-23"
    response = requests.get(NHL_API_URL + schedule_str, params={"Content-Type": "application/json"})
    data = response.json()
    # loop through dates
    txt = ""
    for date in data['dates']:
        txt += "\n--- Date: " + date['date'] + " ---\n"
        # and now through games
        for game in date['games']:
            if int(game['status']['statusCode']) < 3 :
                txt += f"{game['teams']['away']['team']['abbreviation']} @ {game['teams']['home']['team']['abbreviation']} - {get_game_time_tz(game['gameDate'])}\n"
            elif int(game['status']['statusCode']) in {8, 9} :
                txt += f"{game['teams']['away']['team']['abbreviation']} @ {game['teams']['home']['team']['abbreviation']} - {game['status']['detailedState']}\n"
            else:
                period = "" if (int(game['status']['statusCode'])==7)and(game['linescore']['currentPeriod']==3) else "/" + game['linescore']['currentPeriodOrdinal']
                txt += f"{get_game_teams_score(game['teams'], game['status'])} / ({game['status']['detailedState']}{period})\n"
    return txt


def get_game_time_tz(dt_str):

    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    dtEST = dt.astimezone(tzEST)
    dtMSK = dt.astimezone(tzMSK)
    dtVLAT = dt.astimezone(tzVLAT)

    ft = "%H:%M %Z"
    str = f"{dtEST.strftime(ft)} / {dtMSK.strftime(ft)} / {dtVLAT.strftime(ft).replace('+10', 'KHV')}"

    return str


def get_game_teams_score(game_teams, game_status):

    away_team = game_teams['away']['team']['abbreviation']
    #away_team_score = game_teams['away']['score']
    away_team_score = emojize(f":keycap_{game_teams['away']['score']}:")

    home_team = game_teams['home']['team']['abbreviation']
    #home_team_score = game_teams['home']['score']
    home_team_score = emojize(f":keycap_{game_teams['home']['score']}:")

    if int(game_status['statusCode']) == 7 : # Final
        if away_team_score > home_team_score :
            away_team = f"<b>{away_team}</b>"
        else:
            home_team = f"<b>{home_team}</b>"

    game_teams_score = f"{away_team} {str(away_team_score)}:{str(home_team_score)} {home_team}"

    return game_teams_score


#print(get_schedule_today())
