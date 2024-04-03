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

def calculate_field_goal_pct(stat_df):
    field_goal_pct = defaultdict(list)
    for i, row in stat_df.iterrows():
        if row["fieldGoalAttempts1_19Kicking"] != 0.0:
            pct1_19 = row["fieldGoalsMade1_19Kicking"] / row["fieldGoalAttempts1_19Kicking"]
        else:
            pct1_19 = 0.0
        field_goal_pct["fieldGoalsMadePct1_19Kicking"].append(pct1_19)

        if row["fieldGoalAttempts20_29Kicking"] != 0.0:
            pct20_29 = row["fieldGoalsMade20_29Kicking"] / row["fieldGoalAttempts20_29Kicking"]
        else:
            pct20_29 = 0.0
        field_goal_pct["fieldGoalsMadePct20_29Kicking"].append(pct20_29)

        if row["fieldGoalAttempts30_39Kicking"] != 0.0:
            pct30_39 = row["fieldGoalsMade30_39Kicking"] / row["fieldGoalAttempts30_39Kicking"]
        else:
            pct30_39 = 0.0
        field_goal_pct["fieldGoalsMadePct30_39Kicking"].append(pct30_39)

        if row["fieldGoalAttempts40_49Kicking"] != 0.0:
            pct40_49 = row["fieldGoalsMade40_49Kicking"] / row["fieldGoalAttempts40_49Kicking"]
        else:
            pct40_49 = 0.0
        field_goal_pct["fieldGoalsMadePct40_49Kicking"].append(pct40_49)

        if row["fieldGoalAttempts50_59Kicking"] != 0.0:
            pct50_59 = row["fieldGoalsMade50_59Kicking"] / row["fieldGoalAttempts50_59Kicking"]
        else:
            pct50_59 = 0.0
        field_goal_pct["fieldGoalsMadePct50_59Kicking"].append(pct50_59)

        if row["fieldGoalAttempts60_99Kicking"] != 0.0:
            pct60_99 = row["fieldGoalsMade60_99Kicking"] / row["fieldGoalAttempts60_99Kicking"]
        else:
            pct60_99 = 0.0
        field_goal_pct["fieldGoalsMadePct60_99Kicking"].append(pct60_99)

    return field_goal_pct

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
    field_goal_pct = calculate_field_goal_pct(stat_df)
    for key in field_goal_pct:
        stat_df[key] = field_goal_pct[key]


if __name__ == "__main__":
    sys.exit(main(sys.argv))

