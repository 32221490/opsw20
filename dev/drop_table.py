import random
from item_registry import *
from item import Weapon, Passive, Active

weapons = [item for item in item_registry.values() if isinstance(item, Weapon)]
passives = [item for item in item_registry.values() if isinstance(item, Passive)]
actives = [item for item in item_registry.values() if isinstance(item, Active)]

def get_table(mob_type):
    tables = {
        'normal': [
            (item, 0.95 if item.rarity == 'common' else 0.05)
            for item in weapons + passives + actives
            if item.rarity == 'common' or (item.rarity == 'rare' and random.random() < 0.05)
        ],
        'elite': [
            (item, 0.75 if item.rarity == 'rare' else (0.14 if item.rarity == 'common' else 0.01))
            for item in weapons + passives + actives
        ],
        'boss': [
            (item, 1.0 if item.rarity == 'legendary' else 0.05)
            for item in weapons + passives + actives
        ]
    }
    return tables[mob_type]

def roll_drops(mob_type, max_drops=1):
    pool = get_table(mob_type)
    random.shuffle(pool)
    drops = []
    for item, chance in pool:
        if random.random() <= chance:
            drops.append(item)
            if len(drops) >= max_drops:
                break
    return drops
