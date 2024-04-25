#!/usr/bin/env python3
import requests
import json
import sys
from pprint import pprint
import pandas as pd
from collections import defaultdict
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timezone

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

def get_schedule_results(year, team_id):
    games = requests.get(f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?limit=1000&dates={year}&seasontype=2")
    games_json = json.loads(games.text)
    results = []
    for daterange in games_json["leagues"][0]["calendar"]:
        if daterange["label"] == "Regular Season":
            start_date = datetime.fromisoformat(daterange["startDate"][:-1]).astimezone(timezone.utc)
            end_date = datetime.fromisoformat(daterange["endDate"][:-1]).astimezone(timezone.utc)
    for event in games_json["events"]:
        formatted_date = datetime.fromisoformat(event["competitions"][0]["date"][:-1]).astimezone(timezone.utc)
        if formatted_date <= end_date and formatted_date >= start_date:
            week_num = event["week"]["number"]
            if "name" in event["competitions"][0]["competitors"][0]["team"].keys() and "name" in event["competitions"][0]["competitors"][1]["team"].keys():
                team1 = event["competitions"][0]["competitors"][0]["team"]["name"]
                team2 = event["competitions"][0]["competitors"][1]["team"]["name"]
                if event["competitions"][0]["competitors"][0]["winner"]:
                    winner = team1
                    loser = team2
                else:
                    winner = team2
                    loser = team1
            results.append({"week": week_num, "winner": winner, "loser": loser})

    fields = ["week", "winner", "loser"]
    with open(f"{year}_season_results.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    return results

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
    results = get_schedule_results(2023, "")
    team_records = {}

    """
    for team in teams:
        team_name = team["team"]["name"]
        stat_dict["Team"].append(team_name)
        team_location = team["team"]["location"]
        stat_dict["Location"].append(team_location)
        team_id = team["team"]["id"]
        stat_dict = get_team_stats(2023, team_id, stat_dict)

        team_records[team_name] = 0

    for game in results:
        winner = game["winner"]
        team_records[winner] += 1

    stat_df = pd.DataFrame(stat_dict)
    field_goal_pct = calculate_field_goal_pct(stat_df)
    for key in field_goal_pct:
        stat_df[key] = field_goal_pct[key]

    # print(stat_df[["Location", "fumblesGeneral"]])
    pprint(team_records)
    """

if __name__ == "__main__":
    sys.exit(main(sys.argv))
