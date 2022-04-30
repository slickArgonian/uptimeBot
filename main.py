from DebuffTracker import DebuffTracker
from GraphQLClient import GraphQLClient
from Queries import Report
from tabulate import tabulate

with open("./credentials", "r") as f:
    ls = f.readlines()
    client_id = ls[0].strip()
    client_secret = ls[1].strip()


def get_fight_name(fight):
    boss = fight["name"]
    diff = fight["difficulty"]
    kill = fight["kill"]
    percentage = fight["fightPercentage"]
    diff_string = boss
    if diff == 120:
        diff_string += " Normal"
    else:
        diff_string += " Vet"
        if diff == 122:
            diff_string += " HM"
        else:
            plus = abs(122-diff)
            diff_string += f"+{plus}"
    if kill:
        diff_string += " Kill"
    else:
        diff_string += f" ({percentage}%)"
    return diff_string
# future argument
report_code = "NHtJPYjwfZn1Wqp2"
# isolate the boss fights, cleared or not
# find start and end time (=fight time)

# query boss fights for report
report = Report(report_code, GraphQLClient("https://www.esologs.com/api/v2/client", client_id, client_secret))
fights = report.get_boss_fights()

true_table = []
for fight in fights:
    fightTime = fight["endTime"] - fight["startTime"]
    kill = "Kill" if fight["kill"] else "Wipe"
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
    true_table.append([get_fight_name(fight), round(100*sum([v for _, v in format_table["@arkaell"].items()]), 1)])
print(true_table)
headers = ["Encounter", "Crusher"]
print(tabulate(true_table, headers=headers))
