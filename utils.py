
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
