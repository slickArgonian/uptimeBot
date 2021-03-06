from Debuffs import get_debuffs
from GraphQLClient import GraphQLClient
from Queries import Report
from tabulate import tabulate
import os

from pathos.multiprocessing import ProcessingPool as Pool
from utils import get_fight_name

if "CLIENT_ID" in os.environ:
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
else:
    with open("./credentials", "r") as f:
        ls = f.readlines()
        client_id = ls[0].strip()
        client_secret = ls[1].strip()


def process_fight(trackers, report, userId):
    def process_inside(fight):
        fight_name = get_fight_name(fight)
        # prefix fight id number to sort back after
        fight_stats = [fight["id"], fight_name]
        print("Computing for fight", fight_name)
        for tracker in trackers:
            events = report.get_debuff_events(fight, tracker.debuff_code)
            fight_stats.append(tracker.uptime_percent(events, fight, userId))
        return fight_stats

    return process_inside


def uptimes(report_code, user, parallel=True):
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

    trackers = get_debuffs(report, userId)
    headers = ["Encounter"] + [d.debuff_name for d in trackers]

    if parallel:
        pool = Pool(len(fights))  # Create a multiprocessing Pool
        total_successes = pool.map(process_fight(trackers, report, userId), fights)
        # sort back in case we lost order
        sorting = sorted(total_successes, key=lambda x: x[0])
        true_table = [x[1:] for x in sorting]
    else:
        for fight in fights:
            true_table.append(process_fight(trackers, report, userId)(fight)[1:])

    return tabulate(true_table, headers=headers)
