Goal: a discord bot that checks uptimes on eso logs, for example aggregating crusher on several bosses

### TODOs

smart identification of uptimes to check (ie check abilities and gear slotted and compute uptimes for those abilities)

extend to dd stuff

compute all uptimes from one query of dataType:Debuffs and hostilityType:Enemies. in one go from events list
we can't get all events because pagination will make computation too long. as we can't filter on several abilities, we will need one query per debuff

hosting

interactive? if not enough arguments, discord bot asks for report code, gets the answer, then asks for players, answer, buffs...

parallelization wrt debuffs or fights according to how many there are

buffs varying on fight: N/A on table