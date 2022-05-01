from GraphQLClient import GraphQLClient


class Report:

    def __init__(self, code, client: GraphQLClient):
        self.encounter_code = code
        self.client = client
        self.players = self.init_players()
        self.bosses = self.init_bosses()

    def init_players(self):
        query = self.for_report("""masterData{
                                    actors(type:"player"){
                                    displayName
                                    id
        }
        }""")
        res = self.client.get(query)
        actors = res["data"]["reportData"]["report"]["masterData"]["actors"]
        dic = {}
        for a in actors:
            dic[a["id"]] = a["displayName"]
        return dic

    def player_exists(self, player):
        player = "@" + player if "@" not in player else player
        return player in self.players.values()

    def init_bosses(self):
        # TODO this looks a lot like the init_players. find a way to find actors(type = "player" or type = " npc" and subtype = "boss")
        query = self.for_report("""masterData{
                                actors(type:"npc",subType:"Boss"){
                                    id
                                    type 
                                    name
                                    subType
                                }}
                                """)
        res = self.client.get(query)
        bosses = res["data"]["reportData"]["report"]["masterData"]["actors"]
        dic = {}
        for a in bosses:
            dic[a["id"]] = a["name"]
        return dic

    def get_boss_fights(self):
        query = self.for_report("""
                fights(killType: Encounters){
                    id
                    startTime
                    endTime
                    name
                    kill
                    difficulty
                    fightPercentage
            }
       """)
        res = self.client.get(query)
        return res["data"]["reportData"]["report"]["fights"]

    def get_buff_events(self, fight, ability):
        start, e, i = fight["startTime"], fight["endTime"], fight["id"]
        while start is not None:
            events = f"(dataType:Debuffs,startTime:{start},endTime:{e},fightIDs:{i},hostilityType:Enemies,abilityID:{ability})"
            query = self.for_report("events" + events + "{data nextPageTimestamp}")
            res = self.client.get(query)
            start = res["data"]["reportData"]["report"]["events"]["nextPageTimestamp"]
            for event in res["data"]["reportData"]["report"]["events"]["data"]:
                yield event

    def for_report(self, query):
        return """query{
                reportData{
                    report(code: \"""" + self.encounter_code + """\"){
                        """ + query + "}}}"
