import random

def roll_d20():
    result = random.randint(1, 20)
    print(f"Rolled a {result}")
    return result

def interpret_roll(roll):
    if roll == 1:
        return "Fumble!"
    elif 2 <= roll <= 7:
        return "Failure"
    elif 8 <= roll <= 14:
        return "Success"
    elif 15 <= roll <= 19:
        return "Critical"
    elif roll == 20:
        return "Super Critical!"
