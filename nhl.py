# Schedule:  https://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.teams,schedule.scoringplays,schedule.game.seriesSummary,seriesSummary.series,schedule.linescore
#            https://statsapi.web.nhl.com/api/v1/schedule?date=2022-11-23
# Standings: https://statsapi.web.nhl.com/api/v1/standings
# Boxscore:  https://statsapi.web.nhl.com/api/v1/game/2021021092/boxscore

import requests
NHL_API_URL = "https://statsapi.web.nhl.com/api/v1"

def get_schedule_today():

    # fetch game list
    response = requests.get(NHL_API_URL + "/schedule?expand=schedule.teams", params={"Content-Type": "application/json"})
    data = response.json()
    # loop through dates
    txt = ""
    for date in data["dates"]:
        #print("--- Date:", date["date"])
        txt += "\n--- Date: " + date["date"] + " ---\n"
        # and now through games
        for game in date["games"]:
            #print(game["teams"]["away"]["team"]["abbreviation"], "@", game["teams"]["home"]["team"]["abbreviation"], "-", f"{game['teams']['away']['score']}:{game['teams']['home']['score']}", "/", f"({game['status']['detailedState']})")
            txt += game["teams"]["away"]["team"]["abbreviation"] + " @ " + game["teams"]["home"]["team"]["abbreviation"] + " - " + str(game['teams']['away']['score']) + ":" + str(game['teams']['home']['score']) + " / (" + game['status']['detailedState'] + ")\n"
    return txt


#print(get_schedule_today())

