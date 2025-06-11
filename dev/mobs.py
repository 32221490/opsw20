import random
from drop_table import *
from mob import Mob

def get_drops(mob: Mob, max_drops = 1):
    return roll_drops(mob.mob_type, max_drops)

        
### NORMAL TYPE ###

def Junior_Time_Warden(loop = 1) -> Mob:       # basic example of normal mob
    return Mob(
        name="Junior Time Warden",
        base_hp=50,
        base_atk=10,
        base_def=0,
        mob_type="normal",
        loop=loop
    )

### ELITE TYPE ###

def Senior_Time_Warden(loop = 1) -> Mob:       # basic example of elite mob
    return Mob(
        name="Senior Time Warden",
        base_hp=65,
        base_atk=15,
        base_def=5,
        skill="Chronolock",
        skill_chance=0.25,
        mob_type="elite",
        loop=loop
    )

### BOSS TYPE ###

def Devourer_of_Time(loop = 1) -> Mob:         # basic example of boss mob
    return Mob(
        name="Devourer of Time",
        base_hp=120,
        base_atk=20,
        base_def=10,
        skill="Collapse Reforged",
        skill_chance=0.3,
        mob_type="boss",
        loop=loop
    )


def get_stage_enemies(loop, stage_number, battle_index):
    enemies = []

    if stage_number == 1:
        if battle_index == 0:
            enemies.append(Junior_Time_Warden(loop))
        else:
            count = random.randint(1, 3)
            for _ in range(count):
                enemies.append(Junior_Time_Warden(loop))

    elif stage_number == 2:
        elite_count = random.randint(1, 2)
        normal_count = random.randint(1, 3)
        for _ in range(elite_count):
            enemies.append(Senior_Time_Warden(loop))
        for _ in range(normal_count):
            enemies.append(Junior_Time_Warden(loop))

    elif stage_number == 3:
        enemies.append(Devourer_of_Time(loop))

    else:
        raise ValueError(f"Invalid stage number: {stage_number!r}")

    return enemies
"""
class Skill:
    def __init__(self, name, description, base_power):
        self.name = name
        self.description = description
        self.base_power = base_power

    def apply(self, roll, result):
        if result == "Super Critical!":
            return int(self.base_power * 2)
        elif result == "Critical":
            return int(self.base_power * 1.5)
        elif result == "Success":
            return self.base_power
        elif result == "Partial":
            return int(self.base_power * 0.5)
        return 0

def Junior_Time_Warden():
    skills = [
        Skill("Temporal Flick", "A quick jab that confuses time perception.", 5),
        Skill("Minor Rewind", "Restores minor HP if hit is successful.", 0),  
        Skill("Stutter Step", "Reduces opponent's initiative.", 4),
        Skill("Time Zap", "Sends a temporal shockwave.", 6),
    ]
    return Mob("Junior_Time_Warden", hp=50, attack=10, skills=skills, skill_chance=0.3, mob_type="normal")


def Senior_Time_Warden():
    skills = [
        Skill("Chronolock", "Locks target in a moment of time.", 10),
        Skill("Phase Distort", "Deals damage and slows target.", 12),
        Skill("Temporal Slash", "Cuts through timelines.", 14),
        Skill("Rewind Burst", "Damages all nearby enemies.", 11),
    ]
    return Mob("Senior_Time_Warden", hp=65, attack=15, skills=skills, skill_chance=0.4, mob_type="elite")


def Devourer_of_Time():
    skills = [
        Skill("Collapse Reforged", "Rewrites current time state with damage.", 18),
        Skill("Chrono Eruption", "Explodes stored time energy.", 20),
        Skill("Void Pulse", "A wave of nothingness saps the will.", 22),
        Skill("Timeless Bite", "A physical slash imbued with temporal energy.", 24),
    ]
    return Mob("Devourer_of_Time", hp=120, attack=20, skills=skills, skill_chance=0.5, mob_type="boss")
"""
