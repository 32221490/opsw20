from types import NoneType
from dice import roll_d20, interpret_roll
from item import Weapon, Passive, Active

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.base_attack = 10
        self.base_defense = 0

        self.weapon_slot = None
        self.passive_slot = None
        self.active_slot = [None, None, None]

    def is_alive(self):
        return self.hp > 0

    def equip_item(self, item):
        if isinstance(item, Weapon):
            print(f"\n{item.name} EQUIPPED (REPLACING CURRENT WEAPON)")
            self.weapon_slot = item
        elif isinstance(item, Passive):
            print(f"\n{item.name} EQUIPPED (REPLACING CURRENT PASSIVE)")
            self.passive_slot = item
        elif isinstance(item, Active):
            for i in range(len(self.active_slot)):
                if self.active_slot[i] is None:
                    self.active_slot[i] = item
                    print(f"\n{item.name} EQUIPPED in ACTIVE SLOT {i+1}")
                    return
            # EXCEPTION WHEN ACTIVE SLOT IS FULL
            print("ACTIVE SLOT IS FULL!")
            self.show_inventory()
            try:
                choice = int(input("\nCHOOSE ACTIVE SLOT TO REPLACE : ")) -1
                if 0 <= choice < 3:
                    print(f"\nREPLACED {self.active_slot[choice].name} -> {item.name}")
                    self.active_slot[choice] = item
            except:
                print("YOU ONLY HAVE SLOT 1, 2, 3")

    def show_inventory(self):
        print(f"\n========= {self.name}'s Inventory =========\n")
        print(f" Weapon : {self.weapon_slot.name if self.weapon_slot else 'NONE'}\n")
        print(f" Passive : {self.passive_slot.name if self.passive_slot else 'NONE'}\n")
        print(" Active Slots : ")
        for i, item in enumerate(self.active_slot):
            if item:
                print(f"  [{i+1}] {item.name} ({item.remaining_uses}/{item.max_uses})")
            else:
                print(f"  [{i+1}] - NONE")

    def get_total_attack(self):
        bonus = self.weapon_slot.damage if self.weapon_slot else 0
        return self.base_attack + bonus

    def get_total_defense(self):
        bonus = 0
        if self.passive_slot and self.passive_slot.effect:
            if self.passive_slot.effect.get("type") == "defense_boost":
                bonus += self.passive_slot.effect.get("value", 0)

        return bonus

    def attack(self, target):
        roll = roll_d20()
        result = interpret_roll(roll)
        total_attack = self.get_total_attack()
        print(f"{self.name} Rolled the Dice : {roll} ({result})")

        if result == "Fumble!":
            print("You Missed Attack!")
            return

        if result == "Failure":
            damage = 1
        elif result == "Success":
            damage = total_attack
        elif result == "Critical":
            damage = (total_attack * 1.2)
        elif result == "Super Critical!":
            damage = (total_attack * 1.5)

        target.take_damage(damage)
        print(f"You Damaged {damage} to {target.name}!")

        if self.weapon_slot and self.weapon_slot.effect:
            self.apply_effect(self.weapon_slot.effect, target)

    def use_item(self, name):
        for i, item in enumerate(self.active_slot):
            if item and item.name.lower() == name.lower():
                used = item.use(self)
                if used and item.remaining_uses <= 0:
                    self.active_slot[i] = None
                return True
        print(f"{name} Does NOT Exist or Cannot Use")
        return False

    def take_damage(self, amount):
        damage = max(0, amount - self.get_total_defense())
        self.hp -= damage
        print(f"{self.name} Damaged {damage}. Remain HP: {self.hp}")

    def heal(self, amount):
        self.hp += amount
        print(f"{self.name} Healed {amount}. Remain HP: {self.hp}")

    def apply_effect(self, effect, target = None):
        # On Develop
        if not effect:
            return

    def to_dict(self):
        return {
            'name': self.name,
            'hp': self.hp,
            'boss_count': getattr(self, 'boss_count', 0),
            'weapon': self.weapon_slot.to_dict() if self.weapon_slot else None,
            'passive': self.passive_slot.to_dict() if self.passive_slot else None,
            'actives': [item.to_dict if item else None for item in self.active_slot]
        }
    
    @classmethod
    def from_dict(cls, data):
        player = cls(data['name'])
        player.hp = data.get('hp', 100)
        player.boss_count = data.get('boss_count', 0)

        if data['weapon']:
            player.weapon_slot = Weapon(**data['weapon'])

        if data['passive']:
            player.passive_slot = Passive(**data['passive'])

        player.active_slot = []
        for item_data in data['active_items']:
            if item_data:
                item = Active(**item_data)
                player.active_slot.append(item)
            else:
                player.active_slot.append(None)

        return player
