import enum
from typing import get_type_hints as get_annotations
from effect import *
from dice import *
from item import *
from character import Character
from mob import Mob
from colorama import Fore, Style, Back, init
import time
import os
import random

init(autoreset=True)

style_map = {
    "Fumble!": Fore.WHITE + Back.RED + Style.BRIGHT,
    "Failure": Fore.BLACK + Back.YELLOW,
    "Success": Fore.GREEN + Style.BRIGHT,
    "Critical": Fore.BLUE + Style.BRIGHT,
    "Super Critical!": Fore.MAGENTA + Back.WHITE + Style.BRIGHT,
}

dice_frames = [
    r"""
     _______
    |       |
    |   o   |
    |_______|
    """,
    r"""
     _______
    | o     |
    |       |
    |_____o_|
    """,
    r"""
     _______
    | o     |
    |   o   |
    |_o_____|
    """,
    r"""
     _______
    | o   o |
    |       |
    |_o___o_|
    """,
    r"""
     _______
    | o   o |
    |   o   |
    |_o___o_|
    """,
    r"""
     _______
    | o   o |
    | o   o |
    |_o___o_|
    """
]

def ascii_dice_roll_animation(frames=10, delay=0.08):
    for _ in range(frames):
        face = random.choice(dice_frames)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + face)
        time.sleep(delay)
    print()

class Player(Character):
    def __init__(self, name, hp, weapon: Weapon, passive: Passive, active_slots = 3):
        super().__init__(name, hp)
        self.weapon = weapon
        self.passive = passive
        self.active_items: list[Active] = []
        self.active_slots = active_slots
        self.turn_action = 3
        self.log: list[str] = []
        self.stunned = False
        self.status_effects = []

    def is_stunned(self):
        return self.stunned

    def apply_statuses(self):
        return super().apply_statuses()

    def reset_action(self):
        self.turn_action = 3

    def defend(self, damaged):
        buff = 0
        if isinstance(self.passive.effect, DefenseReductionEffect):
            buff = self.passive.effect.apply(0, "")
        damaged = max(0, damaged - buff)
        ascii_dice_roll_animation()
        roll = roll_d20()
        result = interpret_roll(roll)
        print(style_map.get(result, Fore.CYAN) + f"Defense Roll: {roll} ({result})")

        if result not in ("Fumble!", "Failure") and self.passive.DefenseReductionEffect:
            damaged = self.passive.DefenseReductionEffect.apply(damaged, result)
        elif result == "Fumble!":
            print(Fore.RED + f"Defense Roll - Fumbled! | You take full damage!")
        self.hp = max(0, self.hp - damaged)
        
        return damaged

    def take_turn(self, opponents: list[Mob]):
        print(Fore.MAGENTA + Style.BRIGHT + "\n--== YOUR TURN ==--\n")
        self.display_battle_status(opponents)

        print(Fore.YELLOW + "Available Commands:")
        print(Fore.YELLOW + "- attack <enemy index>")
        print(Fore.YELLOW + "- use <item index> <enemy index>")
        print(Fore.YELLOW + "- inventory, save, quit\n")

        cmd = input(f"{self.name} (HP:{self.hp}, Actions:{self.turn_action}) >> ").strip().split()
        if not cmd:
            return

        action = cmd[0].lower()

        if action == "attack" and len(cmd) == 2:
            try:
                idx = int(cmd[1]) - 1
                target = opponents[idx]
                if not target.is_alive():
                    print(Fore.RED + "YOU ALREADY KILLED THAT GUY.")
                    return

                damage = self.weapon.damage
                ascii_dice_roll_animation()
                roll = roll_d20()
                result = interpret_roll(roll)
                style = style_map.get(result, Fore.CYAN)
                print(style + f"You Rolled {roll} ({result})")

                if result == "Fumble!":
                    damage = 0
                elif result == "Failure":
                    damage = 1
                elif result == "Success":
                    damage = self.weapon.damage
                elif result == "Critical":
                    damage = int(self.weapon.damage * 1.15)
                elif result == "Super Critical!":
                    damage = int(self.weapon.damage * 1.5)

                target.take_damage(damage)
                print(Fore.YELLOW + f"Dealt {damage} to {target.name}!")
                print(Fore.RED + f"{target.name}'s HP: {target.hp}")
                print(Fore.RED + Style.BRIGHT + "*SLASH!* 💥")
                self.log.append(f"{self.name} attacked {target.name}: {roll}({result}) -> {damage}")
                self.turn_action -= 1
            except (ValueError, IndexError):
                print("Usage: attack <valid_enemy_index>")

        elif action == "inventory":
            print(Fore.CYAN + f"Weapon: {self.weapon.name} (Damage: {self.weapon.damage})")
            print(f"\"{self.weapon.description}\"\n")

            if self.passive:
                val = getattr(self.passive.roll_effect, 'bonus', '')
                print(Fore.CYAN + f"Passive: {self.passive.name if self.passive else 'None'} / {val}")
                print(f"\"{self.passive.description}\"")
            else:
                print(Fore.CYAN + "Passive: None")

            print(Fore.CYAN + "Active Items:")
            active_list = [it for it in self.active_items if isinstance(it, Active)]
            for slot in range(1, self.active_slots + 1):
                if slot <= len(active_list):
                    item = active_list[slot - 1]
                    val = (
                        getattr(item.effect, 'bonus', '')
                        or getattr(item.effect, 'damage_per_turn', '')
                        or getattr(item.effect, 'heal_per_turn', '')
                    )
                    if hasattr(item, 'uses'):
                        uses = item.uses
                        max_uses = getattr(item, 'max_uses', uses)
                        print(f"slot {slot}: {item.name}({uses}/{max_uses}) / {val} / \"{item.description}\"")
                    else:
                        print(f"slot {slot}: {item.name} / {val} / \"{item.description}\"")
                else:
                    print(f"slot {slot}: None")

        elif action == "use" and len(cmd) in (2,3):
            try:
                slot = int(cmd[1]) - 1
                item = self.active_items[slot]
                if len(cmd) == 3:
                    tidx = int (cmd[2]) - 1
                    target = opponents[tidx]
                else:
                    target = self

                ascii_dice_roll_animation()
                roll, result, value = item.use(self, target)
                style = style_map.get(result, Fore.CYAN)
                print(style + f"Used {item.name} on {'self' if target is self else target.name}: {roll} ({result}) → {value}")
                self.log.append(f"{self.name} used {item.name} on {'self' if target is self else target.name}: {roll}({result}) → {value}")

                if item.uses <= 0:
                    self.active_items.pop(slot)
                self.turn_action -= 1
            except (ValueError, IndexError):
                print("Usage: use <valid_item_index> [<enemy_index>]")

        elif action == "save":
            self.save_system.save_player(self, self.player_log)
            print(Fore.GREEN + "Game saved.")

        elif cmd[0].lower() == "equip" and len(cmd) == 2:
            try:
                idx = int(cmd[1]) - 1
                item = self.active_items[idx]
                if isinstance(item, Passive):
                    old = self.passive
                    self.passive = item
                    self.active_items[idx] = old if old else None
                    if self.active_items[idx] is None:
                        self.active_items.pop(idx)
                    print(f"Equipped passive: {item.name}")
                else:
                    print("That item is not a Passive.")
            except (ValueError, IndexError):
                print("Usage: equip <active_item_number>")
            return

        elif action == "quit":
            print(Fore.MAGENTA + "Exiting game.")
            exit(0)

    def attack(self, target: Mob):
        ascii_dice_roll_animation()
        roll = roll_d20()
        result = interpret_roll(roll)
        style = style_map.get(result, Fore.CYAN)
        print(style + f"{self.name} Rolled the Dice : {roll} ({result})")

        buff = 0
        if isinstance(self.weapon.effect, DamageBonusEffect):
            buff = self.weapon.effect.apply(0, "")
        damage = self.weapon.damage + buff  

        if result == "Fumble!":
            print(Fore.RED + "You Missed Attack!")
            damage = 0
        elif result == "Failure":
            damage = 5
        elif result == "Critical":
            damage *= 1.2
        elif result == "Super Critical!":
            damage *= 1.5

        target.take_damage(damage)
        print(Fore.YELLOW + f"You Damaged {damage} to {target.name}!")

    def use_active(self, slot_idx, target: Character):
        if slot_idx < 0 or slot_idx >= len(self.active_items):
            raise IndexError("Invalid active slot")
        item = self.active_items[slot_idx]
        ascii_dice_roll_animation()
        roll = roll_d20()
        result = interpret_roll(roll)
        style = style_map.get(result, Fore.CYAN)
        print(style + f"Rolled: {roll} ({result})")
        val = 0
        if result not in ("Fumble!", "Failure") and item.effect:
            val = item.effect.apply(roll, result)
        if item.status:
            if result in ("Success", "Critical", "Super Critical!"):
                dur = item.status.duration + (1 if result == "Super Critical!" else 0)
                target.add_status(type(item.status)(**{k:v for k, v in item.status.__dict__.items() if k!='duration'}, duration = dur))
                print(Fore.RED + Style.BRIGHT + f"{target.name} is now affected by {item.status.__class__.__name__}!")
            elif result == "Fumble!":
                self.add_status(type(item.status)(**{k:v for k, v in item.status.__dict__.items() if k!='duration'}, duration = item.status.duration))
                print(Fore.RED + Style.BRIGHT + f"You fumbled and applied {item.status.__class__.__name__} to yourself!")
        item.uses -= 1
        if not item.targets:
            self.heal(val)
        else:
            target.take_damage(val)

        if item.uses <= 0:
            self.active_items.pop(slot_idx)
        self.turn_action -= 1
        return roll, result, val

    def display_battle_status(self, opponents: list[Mob]):
        names   = [Fore.GREEN + "YOU"] + [Fore.RED + m.name for m in opponents]
        hps     = [Fore.GREEN + f"HP:{self.hp}"] + [Fore.RED + f"HP:{m.hp}" for m in opponents]

        def plain(s): return s.replace(Fore.GREEN, '').replace(Fore.RED, '').replace(Style.BRIGHT, '')
        widths = [max(len(plain(n)), len(plain(h))) + 4 for n, h in zip(names, hps)]
        total_width = sum(widths)

        title = " Current Situation "
        print(Fore.MAGENTA + "=" * total_width)
        print(Fore.MAGENTA + title.center(total_width, "="))
        print(Fore.MAGENTA + "=" * total_width)

        for i, name in enumerate(names):
            print(name.center(widths[i]), end='')
        print()

        for i, hp in enumerate(hps):
            print(hp.center(widths[i]), end='')
        print(Style.RESET_ALL)

        print(Fore.MAGENTA + "=" * total_width + Style.RESET_ALL)
