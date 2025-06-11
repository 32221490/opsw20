from abc import abstractmethod, ABC

class Effect(ABC):
    @abstractmethod
    def apply(self, value, category):
        pass

class AttackBuffEffect(Effect):
    def __init__(self, name, bonus):
        self.name = name
        self.bonus = bonus

    def apply(self, value, category):
        if category == "Fumble!":
            return 0
        if category == "Failure":
            return 1
        if category == "Success":
            return self.bonus
        if category == "Critical":
            return int(self.bonus * 1.1)
        if category == "Super Critical!":
            return int(self.bonus * 1.3)


class DefenseBuffEffect(Effect):
    def __init__(self, name, bonus):
        self.name = name
        self.bonus = bonus

    def apply(self, value, category):
        if category == "Fumble!":
            return 0
        if category == "Failure":
            return 1
        if category == "Success":
            return self.bonus
        if category == "Critical":
            return int(self.bonus * 1.1)
        if category == "Super Critical!":
            return int(self.bonus * 1.3)

class StatusEffect(ABC):
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    @abstractmethod
    def on_turn(self, target):
        pass

    def apply_immediate(self, target):
        pass

class BleedEffect(StatusEffect):
    def __init__(self, name, damage_per_turn, duration):
        super().__init__(name, duration)
        self.damage_per_turn = damage_per_turn

    def on_turn(self, target):
        print(f"{target.name} suffers {self.damage_per_turn} bleed damage.")
        target.take_damage(self.damage_per_turn)

class FireEffect(StatusEffect):
    def __init__(self, name, damage_per_turn, duration):
        super().__init__(name, duration)
        self.damage_per_turn = damage_per_turn

    def on_turn(self, target):
        print(f"{target.name} suffers {self.damage_per_turn} fire damage.")
        target.take_damage(self.damage_per_turn)

class RegenEffect(StatusEffect):
    def __init__(self, name, heal_per_turn, duration):
        super().__init__(name, duration)
        self.heal_per_turn = heal_per_turn

    def on_turn(self, target):
        print(f"{target.name} regenerates {self.heal_per_turn} HP.")
        target.hp += self.heal_per_turn

    def apply(self, value, category):
        return self.heal_per_turn

class StunEffect(StatusEffect):
    def __init__(self, name, duration):
        super().__init__(name, duration)

    def on_turn(self, target):
        pass

    def apply_immediate(self, target):
        target.is_stunned = True
