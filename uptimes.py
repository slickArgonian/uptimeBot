from DebuffTracker import DebuffTracker, StaggerTracker
from GraphQLClient import GraphQLClient
from Queries import Report
from tabulate import tabulate

from utils import get_fight_name

with open("./credentials", "r") as f:
    ls = f.readlines()
    client_id = ls[0].strip()
    client_secret = ls[1].strip()

from pathos.multiprocessing import ProcessingPool as Pool


def process_fight(debuffs, report, userId, trackers):
    def process_inside(fight):
        fight_name = get_fight_name(fight)
        # prefix fight id number to sort back after
        fight_stats = [fight["id"], fight_name]
        print("Computing for fight", fight_name)
        for tracker in trackers:
            events = report.get_buff_events(fight, tracker.debuff_code)
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
    # TODO: for crusher, also compute total uptime
    headers = ["Encounter", "Crusher", "Stagger (3)"]
    debuffs = {"stagger": 134336}  # , "alkosh": 76667, "crystal weapon": 143808}
    trackers = [
        DebuffTracker("Crusher", 17906),
        # DebuffTracker("Alkosh", 76667),
        # DebuffTracker("Crystal Weapon", 143808),
        StaggerTracker("Stagger", 134336)
    ]

    if parallel:
        pool = Pool(len(fights))  # Create a multiprocessing Pool
        total_successes = pool.map(process_fight(debuffs, report, userId, trackers), fights)
        # sort back in case we lost order
        sorting = sorted(total_successes, key=lambda x: x[0])
        true_table = [x[1:] for x in sorting]
    else:
        for fight in fights:
            true_table.append(process_fight(debuffs, report, userId, trackers)(fight)[1:])

    return tabulate(true_table, headers=headers)
