#!/usr/bin/env python3
import requests
import json
from pprint import pprint
import pandas as pd
from collections import defaultdict

teams = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams")
teams_json = json.loads(teams.text)
teams_json = teams_json["sports"][0]["leagues"][0]["teams"]
stat_dict = defaultdict(list)
for team in teams_json:
    team_name = team["team"]["name"]
    stat_dict["Team"].append(team_name)
    team_location = team["team"]["location"]
    stat_dict["Location"].append(team_location)
    team_id = team["team"]["id"]

    stats_response = requests.get(f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2023/types/2/teams/{team_id}/statistics")
    stats = json.loads(stats_response.text)
    for category in stats["splits"]["categories"]:
        category_name = category["displayName"]
        for stat in category["stats"]:
            stat_name = stat["name"] + category_name
            stat_value = stat["value"]
            stat_dict[stat_name].append(stat_value)

stat_df = pd.DataFrame(stat_dict)
