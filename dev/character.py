from abc import abstractmethod, ABC
from effect import *

class Character(ABC):
    def __init__(self, name, hp):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.status_effects = []

    def apply_statuses(self):
        expired = []
        for s in self.status_effects:
            s.on_turn(self)
            s.duration -= 1
            if s.duration <= 0:
                expired.append(s)
        
        for s in expired:
            self.status_effects.remove(s)
            print(f"{self.name}'s {s.name} has worn off.")

    def add_status(self, status):
        self.status_effects.append(status)
        print(f"{self.name} is now affected by {status.name} for {status.duration} turns.")

    @abstractmethod
    def take_turn(self, opponents):
        pass

    @abstractmethod
    def reset_action(self):
        pass


    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amt):
        self.hp = max(0, self.hp-amt)
        return amt
    
    def heal(self, amt):
        self.hp = min(self.maxhp, self.hp+amt)
