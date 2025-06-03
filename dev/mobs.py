import random
from mob import *
from drop_table import drop_table

def get_drops(mob, max_drops = 1):
    rarity = mob.drops
    pool = drop_table.get(rarity, [])
    random.shuffle(pool)

    drops = []
    for entry in pool:
        if random.random() <= entry["chance"]:
            drops.append(entry["item"])
            if len(drops) >= max_drops:
                break
    return drops

def Junior_Time_Warden():
    return Mob("Junior Time Warden", 50, 10, 5, "common")

def Senior_Time_Warden():
    return EliteMob("Senior_Time_Warden", 65, 15, 10, "rare", "Chronolock")

def Devourer_of_Time():
    return EliteMob("Devourer_of_Time", 120, 20, 15, "legendary", "Collapse Reforged")
