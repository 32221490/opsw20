from drop_table import *
from dice import *
from effect import *


class Mob():           # type : 'normal', 'elite', 'boss'
    def __init__(self, name, base_hp, base_atk, base_def, skill = None, skill_chance = 0.0, mob_type = "normal", loop = 1):
        scale = 1.0 + 0.1 * (loop - 1)
        self.name = name
        self.hp = int(base_hp * scale)
        self.atk = int(base_atk * scale)
        self.defense = int(base_def * scale)
        self.skill = skill
        self.skill_chance = skill_chance
        self.mob_type = mob_type

        self.status_effects = []
        self.stunned = False
        self.turn_action = 1

    def is_alive(self) -> bool:
        return self.hp > 0

    def reset_turn_state(self):
        self.stunned = False
        self.turn_action = 1

    def apply_statuses(self):
        to_remove = []
        for effect in self.status_effects:
            effect.on_turn(self)
            effect.duration -= 1
            if effect.duration <= 0:
                to_remove.append(effect)

        for e in to_remove:
            self.status_effects.remove(e)


    def is_stunned(self):
        return self.stunned

    def add_status(self, new_effect):
        self.status_effects.append(new_effect)
        if new_effect.__class__.__name__ == "StunEffect":
            new_effect.apply_immediate(self)

    def take_damage(self, damage):
        dmg_after_def = max(0, damage - self.defense)
        self.hp -= dmg_after_def
        if self.hp < 0:
            self.hp = 0

    def attack(self, target):
        roll = roll_d20()
        result = interpret_roll(roll)
        damage = 0

        if result == "Fumble!":
            damage = 0
        if result == "Failure":
            damage = 1
        if result == "Success":
            damage = self.atk
        if result == "Critical":
            damage = int(self.atk * 1.15)
        if result == "Super Critical!":
            damage = int(self.atk * 1.5)

        return roll, result, damage

    def use_skill(self, target):
        if self.skill == "Chronolock":
            duration = 1
            se = StunEffect(name="Chronolock Stun", duration=duration)
            target.add_status(se)
            print(f"{self.name} Used Chronolock! You lost your turn!")

        if self.skill == "Collapse Reforged":
            self.hp += 10
            self.atk = int(self.atk * 1.1)
            self.defense = int(self.defense * 1.1) 

    def __repr__(self):
        return f"<Mob name = {self.name}, hp = {self.hp}, atk = {self.atk}, def = {self.defense}, type = {self.mob_type}>"
