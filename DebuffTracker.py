class DebuffTracker:
    def __init__(self, debuff_name, debuff_code):
        self.debuff_name = debuff_name
        self.debuff_code = debuff_code

    def debuff_active(self, event):
        return event["type"] == "applydebuff"

    def uptime_percent(self, events, fight, sourceId):
        # able to track debuffs that can affect multiple targets
        fightTime = fight["endTime"] - fight["startTime"]
        targets = set()
        total_time = [0, None]
        for event in events:
            source = event["sourceID"]
            target = event["targetID"]
            if source != sourceId:
                continue
            type = event["type"]
            time = event["timestamp"]

            if self.debuff_active(event):
                targets.add(target)
                if len(targets) == 1:
                    total_time[1] = time
            elif type == "removedebuff":
                try:
                    targets.remove(target)
                except KeyError:  # Strange thing happening with multiple adds (example: coagulants in flagravn)
                    print("target wasn't present in list")
                if len(targets) == 0 and total_time[1]:
                    total_time[0] += (time - total_time[1])
                    total_time[1] = None
        return round(100 * total_time[0] / fightTime, 1)


class StaggerTracker(DebuffTracker):

    def debuff_active(self, event):
        return event["type"] == "applydebuffstack" and event["stack"] == 3
