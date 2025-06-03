from item import Weapon

weapon_registry = {}

def register_weapon(item):
    weapon_registry[item.name] = item
    return item

register_weapon(Weapon("Stun Baton", "Perfectly suited for subduing standard targets.", 15, rarity="common", effect={"type" : "electric", "value" : 3}))
register_weapon(Weapon("Longsword", "Old-fashioned, but still deadly.", 25, rarity="rare", effect={"type" : "bleed", "value" : 4}))
register_weapon(Weapon("Chainsaw", "Effective way to conversation.", 30, rarity="rare", effect={"type" : "bleed", "value" : 6}))
register_weapon(Weapon("Chiljido", "Forged for rites - from lands unknown", 45, rarity="legendary", effect={"type" : "critical", "value" : 1.7}))
