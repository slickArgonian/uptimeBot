def get_debuffs(report, fights, player):
    # skills
    tanks = report.get_players_info()["tanks"]
    skills = None
    for t in tanks:
        print(t)
        if player == t["id"]:
            skills = t["combatantInfo"]["talents"]

    # gear, per fight
    fight_ids = [f["id"] for f in fights]
    gear = report.get_player_gear(fight_ids, player)
    assert(len(gear) == len(fights))
