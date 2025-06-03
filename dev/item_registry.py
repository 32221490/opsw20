from item_weapon import *
from item_passive import *
from item_active import *

item_registry = {}
item_registry.update(weapon_registry)
item_registry.update(passive_registry)
item_registry.update(active_registry)

weapons = list(weapon_registry.values())
passives = list(passive_registry.values())
actives = list(active_registry.values())
