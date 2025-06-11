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

    def is_stunned(self):
        return self.stunned

    def apply_statuses(self):
        return super().apply_statuses()

    def reset_action(self):
        self.turn_action = 3

    def defend(self, damaged):
        ascii_dice_roll_animation()
        roll = roll_d20()
        result = interpret_roll(roll)
        print(style_map.get(result, Fore.CYAN) + f"Defense Roll: {roll} ({result})")

        if self.passive and self.passive.defense_effect:
            reduction = self.passive.defense_effect.apply(damaged, result)
            damaged = max(0, damaged - reduction)

        if result == "Fumble!":
            print(Fore.RED + f"Defense Roll - Fumbled! | You take full damage!")

        self.hp = max(0, self.hp - damaged)
        return damaged

    def take_turn(self, opponents: list[Mob]):
        print(Fore.MAGENTA + Style.BRIGHT + "\n--== YOUR TURN ==--\n")
        self.display_battle_status(opponents)

        print(Fore.YELLOW + "Available Commands:")
        print(Fore.YELLOW + "- attack <enemy index>")
        print(Fore.YELLOW + "- use <item index> [<enemy index>]")
        print(Fore.YELLOW + "- equip <item index>     (for passive items)")
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
                print(Fore.RED + Style.BRIGHT + "*SLASH!* \U0001F4A5")
                self.log.append(f"{self.name} attacked {target.name}: {roll}({result}) -> {damage}")
                self.turn_action -= 1
            except (ValueError, IndexError):
                print("Usage: attack <valid_enemy_index>")

        elif action == "inventory":
            print(Fore.CYAN + f"Weapon: {self.weapon.name} (Damage: {self.weapon.damage})")
            print(f"\"{self.weapon.description}\"\n")

            if self.passive:
                val = getattr(self.passive.defense_effect, 'bonus', '') if self.passive.defense_effect else ''
                print(Fore.CYAN + f"Passive: {self.passive.name} / {val}")
                print(f"\"{self.passive.description}\"")
            else:
                print(Fore.CYAN + "Passive: None")

            print(Fore.CYAN + "Active Items:")
            for slot in range(1, self.active_slots + 1):
                if slot <= len(self.active_items):
                    item = self.active_items[slot - 1]
                    val = (
                        getattr(item.effect, 'bonus', '')
                        or getattr(item.effect, 'damage_per_turn', '')
                        or getattr(item.effect, 'heal_per_turn', '')
                    )
                    uses = item.uses if hasattr(item, 'uses') else '?'
                    max_uses = getattr(item, 'max_uses', uses)
                    print(f"slot {slot}: {item.name}({uses}/{max_uses}) / {val} / \"{item.description}\"")
                else:
                    print(f"slot {slot}: None")

        elif action == "use" and len(cmd) in (2,3):
            try:
                slot = int(cmd[1]) - 1
                item = self.active_items[slot]
                target = self if len(cmd) == 2 else opponents[int(cmd[2]) - 1]

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

        elif action == "equip" and len(cmd) == 2:
            try:
                idx = int(cmd[1]) - 1
                item = self.active_items[idx]
                if isinstance(item, Passive):
                    old = self.passive
                    self.passive = item
                    if old:
                        self.active_items[idx] = old
                    else:
                        self.active_items.pop(idx)
                    print(f"Equipped passive: {item.name}")
                else:
                    print("That item is not a Passive.")
            except (ValueError, IndexError):
                print("Usage: equip <active_item_number>")

        elif action == "quit":
            print(Fore.MAGENTA + "Exiting game.")
            exit(0)

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
