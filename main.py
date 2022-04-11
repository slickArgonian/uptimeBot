import requests
import os

from DebuffTracker import DebuffTracker
from GraphQLClient import GraphQLClient
from Queries import Report

if os.path.exists("./access_token"):
    with open("./access_token", "r") as f:
        access_token = f.readlines()[0].strip()
else:
    with open("./credentials", "r") as f, open("./access_token", "w") as f1:
        ls = f.readlines()
        client_id = ls[0].strip()
        client_secret = ls[1].strip()
        access_token = requests.post("https://www.esologs.com/oauth/token", auth=(client_id, client_secret),
                                     json={"grant_type": "client_credentials"}).json()["access_token"]
        print(access_token, file=f1)

# future argument
report_code = "NHtJPYjwfZn1Wqp2"
# isolate the boss fights, cleared or not
# find start and end time (=fight time)

# query boss fights for report
report = Report(report_code, GraphQLClient("https://www.esologs.com/api/v2/client", access_token))
fights = report.get_boss_fights()
for fight in fights:
    fightTime = fight["endTime"] - fight["startTime"]
    ability_code = 17906
    events = report.get_buff_events(fight, ability_code)
    tracker = DebuffTracker("crushzrher")
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

    print(format_table)