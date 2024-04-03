#!/usr/bin/env python3
import requests
import json
import sys
from pprint import pprint
import pandas as pd
from collections import defaultdict

def get_teams():
    teams = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams")
    teams_json = json.loads(teams.text)
    teams_json = teams_json["sports"][0]["leagues"][0]["teams"]

    return teams_json

def get_team_stats(year, team_id, stat_dict):
    stats_response = requests.get(f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/types/2/teams/{team_id}/statistics")
    stats = json.loads(stats_response.text)
    for category in stats["splits"]["categories"]:
        category_name = category["displayName"]
        for stat in category["stats"]:
            stat_name = stat["name"] + category_name
            stat_value = stat["value"]
            stat_dict[stat_name].append(stat_value)

    return stat_dict

def rank_teams_by_feature(stat_df, feature):
   return stat_df.sort_values(by=[feature])

def main(argv):
    teams = get_teams()
    stat_dict = defaultdict(list)
    for team in teams:
        team_name = team["team"]["name"]
        stat_dict["Team"].append(team_name)
        team_location = team["team"]["location"]
        stat_dict["Location"].append(team_location)
        team_id = team["team"]["id"]
        stat_dict = get_team_stats(2023, team_id, stat_dict)

    stat_df = pd.DataFrame(stat_dict)


if __name__ == "__main__":
    sys.exit(main(sys.argv))

