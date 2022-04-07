class DebuffTracker:
    """
    returns: total time each unit is affected by each player debuff
    example
                   arka        puppy
    oax            30s         10s
    havocrel1      10s         30s
    frog1          1s          3s

    => others=sum(havocrel and frog) = 11 et 33s
    and then statistics wrt total fight time can be made
    to be confirmed: a same target can't have two "crushers" for different players active at the same time
    """
    def __init__(self, debuff_code):
        self.a = debuff_code

    def analyse(self, events):
        print(events)
        # logique en plusieurs passes (pour chaque joueur)
        # puis en une seule passe (dicos)
        big_dic = {}
        for event in events:
            # TODO if abiilityGameId != debuff_code. check that graphql query works correctly?
            source, target = event["sourceID"], event["targetID"]
            type = event["type"]
            time = event["timestamp"]
            if source not in big_dic:
                big_dic[source] = {}
            up_per_source = big_dic[source]
            if target not in up_per_source:
                up_per_source[target] = [0, None]
            tracker = up_per_source[target]
            if type == "applydebuff":
                tracker[1] = time
            elif type == "removedebuff":
                if tracker[1]:
                    tracker[0] += (time - tracker[1])
                tracker[1] = None

        print(big_dic)


if __name__ == "__main__":
    from events import events
    t = DebuffTracker("crusher code? we might not need it")
    t.analyse(events)