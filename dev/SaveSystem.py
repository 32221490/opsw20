import os
from os.path import exists
from tinydb import TinyDB, Query
from item import Weapon, Passive, Active

class SaveSystem:
    def __init__(self, slot_number):
        if slot_number not in [1, 2, 3]:
            raise ValueError("You Can Only Choose Save File 1, 2, 3.")

        SAVE_DIR = os.path.expanduser("../save_files/")
        os.makedirs(SAVE_DIR, exist_ok=True)
        file_path = os.path.join(SAVE_DIR, f"save_slot_{slot_number}.json")
        self.db = TinyDB(file_path)
        self.slot_number = slot_number

    def save_player(self, player):
        self.db.truncate()

        data = {
            'name': player.name,
            'hp': player.hp,
            'base_attack': player.base_attack,
            'base_defense': player.base_defense,
            'weapon': self.serialize_item(player.weapon_slot),
            'passive': self.serialize_item(player.passive_slot),
            'active': self.serialize_item(player.active_slot)
        }

        self.db.insert(data)
        print(f"Saved Successfully in [Save File {self.slot_number}]")

    def load_player(self):
        data = self.db.all()
        if not data:
            print(f"No Save Data in [Save File {self.slot_number}]")
            return None

        info = data[0]
        from player import Player
        player = Player(info['name'])
        player.hp = info['hp']
        player.base_attack = info['base_attack']
        player.base_defense = info['base_defense']

        player.weapon_slot = self.deserialize_item(info['weapon'])
        player.passive_slot = self.deserialize_item(info['passive'])
        player.active_slot = self.deserialize_item(info['active'])

        print(f"Loaded [Save File {self.slot_number}] Successfully")
        return player

    def clear_slot(self):
        self.db.truncate()
        print(f"Removed [Save File {self.slot_number}] Successfully")

    def serialize_item(self, item):
        if item is None:
            return None

        return {
            'class': item.__class__.__name__,
            'name': item.name,
            'description': item.description,
            'rarity': item.rarity,
            'effect': item.effect,
            'damage': getattr(item, 'damage', None),
            'max_uses': getattr(item,'max_uses', None),
            'remaining_uses': getattr(item, 'remaining_uses', None)
        }

    def deserialize_item(self, data):
        if data is None:
            return None

        cls_name = data['class']
        name = data['name']
        desc = data['description']
        rarity = data['rarity']
        effect = data['effect']

        if cls_name == 'Weapon':
            return Weapon(name, desc, data['damage'], effect, rarity)
        elif cls_name == 'Passive':
            return Passive(name, desc, data.get('deffend', 0), rarity, effect)
        elif cls_name == 'Active':
            item = Active(name, desc, effect, data['max_uses'], rarity)
            item.remaining = data['remaining_uses']
            return item
        else:
            print(f"Unknown Item Class: {cls_name}")
            return None
