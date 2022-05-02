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

    userId = report.player_id(user)
    if not userId:
        return f"Error ! The user {user} does not appear in the report."
    fights = report.get_boss_fights()

    true_table = []
    # TODO: for crusher, also compute total uptime
    headers = ["Encounter", "Crusher", "Alkosh", "Crystal weapon"]
    debuffs = {"crusher": 17906, "alkosh": 76667, "crystal weapon": 143808}
    for fight in fights:
        fight_name = get_fight_name(fight)
        fight_stats = [fight_name]
        print("Computing for fight", fight_name)
        for debuffname, debuffcode in debuffs.items():
            events = report.get_buff_events(fight, debuffcode)
            tracker = DebuffTracker(debuffname)
            fight_stats.append(tracker.uptime_percent(events, fight, userId))
        true_table.append(fight_stats)

    return tabulate(true_table, headers=headers)


