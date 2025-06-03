from item import Active

active_registry = {}

def register_active(item):
    active_registry[item.name] = item
    return item

register_active(Active("Bourbon", "A Kentucky Classic. Brings you courage in every sip", 3, rarity="common", effect={"type" : "attack_bonus", "value" : 3}))
register_active(Active("Healing Potion", "Even its creator doesn't know how it works.", 3, rarity="common", effect={"type" : "heal", "value" : 15}))
register_active(Active("Molotov Cocktail", "Hot stuff. Handle with care.", 2, rarity="common", effect={"type" : "fire", "value" : 2}))
register_active(Active("Greater Healing Potion", "The first was an accident.", 3, rarity="rare", effect={"type" : "heal", "value" : 25}))
register_active(Active("Stimultant", "You feel stronger. Avoid Overuse!", 1, rarity='rare', effect={"type" : "attack_bonus", "value" : 15}))
register_active(Active("Holy Grenade", "Count to Three. Not two. Not Four", 1, rarity="rare", effect={"type" : "attack", "value" : 40}))
register_active(Active("Elixir", "It's magic", 1, rarity="legendary", effect={"type" : "heal", "value" : 100}))
