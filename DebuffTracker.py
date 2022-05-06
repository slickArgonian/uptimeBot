class DebuffTracker:
    def __init__(self, debuff_name, debuff_code):
        self.debuff_name = debuff_name
        self.debuff_code = debuff_code

    def debuff_active(self, event):
        return event["type"] == "applydebuff"

    def uptime_percent(self, events, fight, sourceId):
        # able to track debuffs that can affect multiple targets
        fightTime = fight["endTime"] - fight["startTime"]
        player_targets = set()
        player_time = [0, None]
        total_targets = set()
        total_time = [0, None]
        for event in events:
            source = event["sourceID"]
            target = event["targetID"]
            type = event["type"]
            time = event["timestamp"]

            if self.debuff_active(event):
                total_targets.add(target)
                if len(total_targets) == 1:
                    total_time[1] = time
                if source == sourceId:
                    player_targets.add(target)
                    if len(player_targets) == 1:
                        player_time[1] = time
            elif type == "removedebuff":
                try:
                    total_targets.remove(target)
                    if source == sourceId:
                        player_targets.remove(target)
                except KeyError:  # Strange thing happening with multiple adds (example: coagulants in flagravn)
                    print("target wasn't present in list")

                if len(total_targets) == 0 and total_time[1]:
                    total_time[0] += (time - total_time[1])
                    total_time[1] = None
                if source == sourceId:
                    if len(player_targets) == 0 and player_time[1]:
                        player_time[0] += (time - player_time[1])
                        player_time[1] = None
        if player_time[0] == total_time[0]:
            second_term = None
        else:
            second_term = round(100 * total_time[0] / fightTime, 1)
        res = round(100 * player_time[0] / fightTime, 1)
        if res == 0 and second_term == 0:
            return "N/A"
        elif res == 0 and second_term > 0:
            return f"N/A ({second_term})"
        elif not second_term:
            return res
        else:
            return f"{res} ({second_term})"


class StaggerTracker(DebuffTracker):

    def __init__(self):
        super().__init__("Stagger (3)", 134336)

    def debuff_active(self, event):
        return event["type"] == "applydebuffstack" and event["stack"] == 3
