import pathlib
import copy
from tinydb import TinyDB
from item_registry import item_registry
from player import Player

class SaveSystem:
    SAVE_DIR = pathlib.Path(__file__).parent / "save_files"
    VALID_SLOTS = {1, 2, 3}

    def __init__(self, slot_number):
        if slot_number not in self.VALID_SLOTS:
            raise ValueError(f"INVALID SLOT : {slot_number}. Choose one of {self.VALID_SLOTS}.")
        self.slot = slot_number

        self.SAVE_DIR.mkdir(parents=True, exist_ok=True)
        self.filepath = self.SAVE_DIR / f"slot_{slot_number}.json"
        self.db = TinyDB(self.filepath)

    @classmethod
    def list_slots(cls):
        return [n for n in cls.VALID_SLOTS if (cls.SAVE_DIR / f"slot_{n}.json").exists()]

    def delete_slot(self):
        self.db.close()
        if self.filepath.exists():
            self.filepath.unlink()

    def save_player(self, player, player_log):
        self.db.truncate()
        record = {
            "name": player.name,
            "hp": player.hp,
            "weapon": player.weapon.name,
            "passive": player.passive.name if player.passive else None,
            "active_items": [
                {"name": item.name, **({"uses": item.uses} if hasattr(item, "uses") else {})}
                for item in player.active_items
            ],
            "time_played": player_log.get("time_played", 0),
            "battle_logs": player_log.get("battle_logs", []),
            "items_acquired": player_log.get("items_acquired", 0)
        }
        self.db.insert(record)

    def load_player(self):
        all_records = self.db.all()
        if not all_records:
            return None

        rec = all_records[0]
        weapon_proto = item_registry[rec["weapon"]]
        weapon = copy.deepcopy(weapon_proto)
        passive = None
        if rec.get("passive"):
            passive_proto = item_registry[rec["passive"]]
            passive = copy.deepcopy(passive_proto)

        player = Player(
            name=rec["name"],
            hp=rec["hp"],
            weapon=weapon,
            passive=passive
        )

        player.active_items = []
        for entry in rec.get("active_items", []):
            proto = item_registry[entry["name"]]
            item_copy = copy.deepcopy(proto)
            item_copy.uses = entry["uses"]
            player.active_items.append(item_copy)

        player_log = {
            "time_played": rec.get("time_played", 0),
            "battle_logs": rec.get("battle_logs", []),
            "items_acquired": rec.get("items_acquired", 0)
        }

        return player, player_log
