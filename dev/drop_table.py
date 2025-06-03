from item_registry import *

default_chance = {
    "common" : 0.5,
    "rare" : 0.3,
    "legendary" : 0.2
}

drop_table = {
    "common" : [],
    "rare" : [],
    "legendary" : []
}

for item in weapons + passives + actives:
    rarity = item.rarity.lower()
    if rarity in drop_table:
        drop_table[rarity].append({"item" : item, "chance" : default_chance[rarity]});
