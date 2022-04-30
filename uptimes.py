from DebuffTracker import DebuffTracker
from GraphQLClient import GraphQLClient
from Queries import Report
from tabulate import tabulate

from utils import get_fight_name

with open("./credentials", "r") as f:
    ls = f.readlines()
    client_id = ls[0].strip()
    client_secret = ls[1].strip()


def uptimes(report_code, user):
    try:
        report = Report(report_code, GraphQLClient("https://www.esologs.com/api/v2/client", client_id, client_secret))
    except:
        # TODO in graphqlclient, throw the error message to pinpoint problem (existence, permission?)
        return f"Error ! The report {report_code} could not be reached, make sure the report exists and has Public or Unlisted visibility."

    if "user with @ or without not" in "report":  # TODO write true code
        return "user not in report"
    fights = report.get_boss_fights()

    true_table = []
    for fight in fights:
        fightTime = fight["endTime"] - fight["startTime"]
        ability_code = 17906
        events = report.get_buff_events(fight, ability_code)
        tracker = DebuffTracker("crushzrher")  # TODO smarten it
        table = tracker.analyse(events)
        format_table = {}

        for player, uptimes in table.items():
            new_up = {"others": 0}
            for boss, boss_up in uptimes.items():
                if boss in report.bosses:
                    new_up[report.bosses[boss]] = boss_up[0] / fightTime
                else:
                    new_up["others"] += boss_up[0] / fightTime
            format_table[report.players[player]] = new_up
        true_table.append(
            [get_fight_name(fight), round(100 * sum([v for _, v in format_table["@arkaell"].items()]), 1)])
    headers = ["Encounter", "Crusher"]
    return tabulate(true_table, headers=headers)


