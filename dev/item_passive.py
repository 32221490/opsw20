from item import Passive

passive_registry = {}

def register_passive(item):
    passive_registry[item.name] = item
    return item

register_passive(Passive("Rabbit's Foot", "Brings you a bit of luck", 0, rarity="common", effect={"type" : "luck", "value" : 5}))
register_passive(Passive("Anti-Blade Vest", "Stops blades... more or less", 10, rarity="common", effect={"type" : "reduce", "value" : 10}))
register_passive(Passive("Monkey's Paw", "Brings you luck. Probably", 3, rarity="rare", effect={"type" : "dice", "value" : 3}))
register_passive(Passive("Ballistic Helmet", "Must-Have in any combat zone", 20, rarity="rare", effect={"type" : "reduce", "value" : 15}))
register_passive(Passive("Four-leaf Clover", "There's no such word as Failure!", 15, rarity="legendary", effect={"type" : "luck", "value" : 20}))
register_passive(Passive("Gothic Plate Armour", "German Classic", 25, rarity="legendary", effect={"type" : "reduce", "value" : 20}))
