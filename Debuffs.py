from DebuffTracker import DebuffTracker, StaggerTracker


class Gear:
    def __init__(self, gear_name):
        # we go by name instead of setId to not deal with mix of perf/non-perf. todo use set id and gather them
        self.gear_name = gear_name
        self.gear_count = 0

    def update(self, gear):
        if "name" not in gear:
            return
        if self.gear_name in gear["name"]:
            self.gear_count += 1

    def equipped(self):
        return self.gear_count >= 3


class Enchant:
    def __init__(self, enchant_id):
        self.enchant_id = enchant_id
        self.present = False

    def update(self, gear):
        if gear["enchantType"] == self.enchant_id:
            self.present = True

    def equipped(self):
        return self.present


class Trait:
    def __init__(self, trait_id):
        self.trait_id = trait_id
        self.present = False

    def update(self, gear):
        if gear["trait"] == self.trait_id:
            self.present = True

    def equipped(self):
        return self.present


class Skill:
    def __init__(self, skill_id):
        self.skill_id = skill_id
        self.present = False

    def update(self, skill):
        if skill["guid"] == self.skill_id:
            self.present = True

    def equipped(self):
        return self.present


def get_debuffs(report, player):
    tanks = report.get_players_info()["tanks"]
    skills = None
    gear = None
    for t in tanks:
        if player == t["id"]:
            skills = t["combatantInfo"]["talents"]
            gear = t["combatantInfo"]["gear"]
    gear_map = {Gear("Alkosh"): DebuffTracker("Alkosh", 76667),
                Gear("Crimson Oath"): DebuffTracker("Crimson", 159288),
                Gear("Turning Tide"): DebuffTracker("Maj Vuln", 99),
                Gear("Catalyst"): DebuffTracker("Flame W", 142610),
                Gear("Catalyst"): DebuffTracker("Shock W", 142653),
                Gear("Catalyst"): DebuffTracker("Frost W", 142652),
                Gear("Martial Knowledge"): DebuffTracker("MK", 127070),
                Enchant(28): DebuffTracker("Crusher", 17906),
                #  TODO: more conditions for brittle: pulsar or destructive reach
                Trait(23): DebuffTracker("mBrittle", 146697)  # 23: Charged
                }
    for g in gear:
        for gb in gear_map:
            gb.update(g)
    debuffs = [d for g, d in gear_map.items() if g.equipped()]
    skill_map = {Skill(31816): StaggerTracker(),
                 Skill(46331): DebuffTracker("Crystal Weapon", 143808)
                 # todo minor vuln (totem, flies, ambush)
                 }

    for s in skills:
        for sb in skill_map:
            sb.update(s)
    debuffs += [d for s, d in skill_map.items() if s.equipped()]
    return debuffs
