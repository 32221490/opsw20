from effect import *
from dice import roll_d20, interpret_roll
import copy

class Item:
    def __init__(self, name, description, rarity = "common", effect: Effect = None, status: StatusEffect = None):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.effect = effect
        self.status = status

class Weapon(Item):
    def __init__(self, name, description, damage, rarity = "common", effect: Effect = None, status: StatusEffect = None):
        super().__init__(name, description, rarity, effect, status)
        self.damage = damage

class Passive(Item):
    def __init__(self, name, description, rarity = "common", roll_effect: Effect= None, defense_effect: Effect = None, status: StatusEffect = None):
        super().__init__(name, description, rarity, effect = None, status = status)
        self.roll_effect = roll_effect
        self.defense_effect = defense_effect

    def apply_defense_bonus(self, roll, category: str):
        if self.defense_effect and category not in ("Fumble!", "Failure"):        # will be detailed
            return self.defense_effect.apply(roll, category)
        return 0

class Active(Item):     # if target is True -> target of item is Enemy, if False than target is player
    def __init__(self, name, description, rarity = "common", effect: Effect = None, target: list = None, uses = 1, status: StatusEffect = None):
        super().__init__(name, description, rarity, effect, status)
        self.uses = uses
        self.max_uses = uses
        self.target = target if target is not None else []

    def use(self, user, target):
        roll = roll_d20()
        result = interpret_roll(roll)
        value = 0

        if result not in ("Fumble!", "Failure"):
            if self.effect:
                value = self.effect.apply(roll, result)
            if self.status:
                dur = self.status.duration + (1 if result == "Super Critical!" else 0)
                new_status = copy.deepcopy(self.status)
                new_status.duration = dur
                if "enemy" in self.target:
                    target.add_status(new_status)
                else:
                    user.add_status(new_status)

        if isinstance(self.effect, AttackBuffEffect):
            user.weapon.base_damage += value
            print(f"Attack buff! {user.name}'s base damage is now {user.weapon.base_damage} for this turn.")
        elif not self.target:
            user.hp += value
            print(f"{user.name} healed for {value} HP. (HP now {user.hp})")
        else:
            target.take_damage(value)
            print(f"Dealt {value} damage to {target.name}.")

        self.uses -= 1
        return roll, result, value
