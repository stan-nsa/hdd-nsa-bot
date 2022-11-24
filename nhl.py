# Schedule:  https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.teams,schedule.scoringplays,schedule.game.seriesSummary,seriesSummary.series,schedule.linescore
#            https://statsapi.web.nhl.com/api/v1/schedule?date=2022-11-23
# Standings: https://statsapi.web.nhl.com/api/v1/standings
# Boxscore:  https://statsapi.web.nhl.com/api/v1/game/2021021092/boxscore

import requests
from datetime import datetime, timezone
import pytz

NHL_API_URL = "https://statsapi.web.nhl.com/api/v1"

# TimeZone
tzEST = pytz.timezone("US/Eastern")
tzMSK = pytz.timezone("Europe/Moscow")
tzVLAT = pytz.timezone("Asia/Vladivostok")


def get_schedule_today():
    # fetch game list
    schedule_str = "/schedule?expand=schedule.teams"
    #schedule_str = "/schedule?expand=schedule.teams&date=2022-11-25"
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
                txt += f"{game['teams']['away']['team']['abbreviation']} {str(game['teams']['away']['score'])}:{str(game['teams']['home']['score'])} {game['teams']['home']['team']['abbreviation']} / ({game['status']['detailedState']})\n"
    return txt


def get_game_time_tz(dt_str):

    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    dtEST = dt.astimezone(tzEST)
    dtMSK = dt.astimezone(tzMSK)
    dtVLAT = dt.astimezone(tzVLAT)

    ft = "%H:%M %Z"
    #str = dtEST.strftime(ft) + " / " + dtMSK.strftime(ft) + " / " + dtVLAT.strftime(ft).replace('+10', 'KHV')
    str = f"{dtEST.strftime(ft)} / {dtMSK.strftime(ft)} / {dtVLAT.strftime(ft).replace('+10', 'KHV')}"

    return str

#print(get_schedule_today())
