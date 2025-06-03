from random import choice
from dice import *
from player import *
from mobs import *


# Add to Mob pool after creating new mobs
normal_mobs = [Junior_Time_Warden]
elite_mobs = [Senior_Time_Warden]
boss_mobs = [Devourer_of_Time]

class Combat:
    def __init__(self, player, difficulty_multiplier = 1.0, boss_count = 0):
        self.player = player
        self.difficulty_multiplier = difficulty_multiplier
        self.batle_count = 0
        self.elite_count = 0
        self.boss_count = boss_count

    def scale_mob_stats(self, mob):
        mob.hp = int(mob.hp * self.difficulty_multiplier)
        mob.attack = int(mob.attack * self.difficulty_multiplier)
        mob.defense = int(mob.defense * self.difficulty_multiplier)
        return mob

    def generate_enemies(self):
        if self.elite_count >= 4:
            print("\n========= Warning! Boss Approaching! =========")
            self.elite_count = 0
            self.boss_count += 1
            return [self.scale_mob_stats(mob()) for mob in boss_mobs]
        elif 5 >= self.batle_count >= 3:
            self.elite_count += 1
            self.batle_count = 0
            elites = random.sample(elite_mobs, k = random.randint(1, 2))
            return [self.scale_mob_stats(mob()) for mob in elite_mobs]
        else:
            self.batle_count += 1
            normals = random.sample(normal_mobs, k = random.randint (2, 4))
            return [self.scale_mob_stats(mob()) for mob in normals]

    def filter_drops_by_rarity(self, enemy, drops):
        result = []
        name = enemy.name.lower()

        for item in drops:
            rarity = item.rarity.lower()

            if "devourer" in name:
                if rarity == "legendary":
                    result.append(item)
            elif "senior" in name:
                if rarity in ("rare", "common"):
                    result.append(item)
                elif rarity == "legendary" and random.random() < 0.01:
                    result.append(item)
            else:
                if rarity == "common":
                    result.append(item)
                elif rarity == "rare" and random.random() < 0.05:
                    result.append(item)

        return result

    def start_battle(self):
        enemies = self.generate_enemies()
        print("========= Enemy Encountered! =========")

        while self.player.is_alive() and any(e.is_alive() for e in enemies):
            print(f"\nYour HP : {self.player.hp}")
            for i, enemy in enumerate(enemies):
                if enemy.is_alive():
                    print(f"[{i}] {enemy.name} - HP : {enemy.hp}")

            actions = 3
            while actions > 0:
                command = input(f"\nYou have {actions} actions remaining >> ").strip().lower()

                if command.startswith("attack"):
                    parts = command.split()
                    if len(parts) != 2 or not parts[1].isdigit():
                        print("HOW TO? : attack <index> (ex : attack 2)")
                        continue
                    idx = int(parts[1])
                    if 0 <= idx < len(enemies) and enemies[idx].is_alive():
                        self.player.attack(enemies[idx])
                        actions -= 1
                    else:
                        print("! There is no target like that!")

                elif command == "inventory":
                    self.player.show_inventory()

                elif command.startswith("use "):
                    item_name = command[4:]. strip()
                    used = self.player.use_item(item_name)
                    if used:
                        actions -= 1

                else:
                    print("! Unkown Command !")

                for enemy in enemies:
                    if not enemy.is_alive() and not hasattr(enemy, "_dead_announced"):
                        print(f"{enemy.name} ELIMINATED!")
                        enemy._dead_announced = True

            print("\n========= Enemies' Turn! =========")
            for enemy in enemies:
                if enemy.is_alive():
                    enemy.attack_target(self.player)
                    if not self.player.is_alive():
                        print("========= YOU DIED =========")
                        return
        
        if self.player.is_alive():
            print("\nYou Survived Another Day")
            print("\nThey Left Something...")
            for enemy in enemies:
                raw_drops = get_drops(enemy)
                filtered = self.filter_drops_by_rarity(enemy, raw_drops)
                for item in filtered:
                    print(f"{item.name} ({item.rarity})")
                    self.player.equip_item(item)

        else:
            print("\n========= YOU DIED =========\n")
            return self.player.is_alive()





from battle_history import save_battle_history
from datetime import datetime


if self.player.is_alive():
    print("\nYou Survived Another Day")
    print("\nThey Left Something...")
    for enemy in enemies:
        raw_drops = get_drops(enemy)
        filtered = self.filter_drops_by_rarity(enemy, raw_drops)
        for item in filtered:
            print(f"{item.name} ({item.rarity})")
            self.player.equip_item(item)

    battle_record = {
        "survived": True,
        "enemies_defeated": sum(1 for e in enemies if not e.is_alive()),
        "timestamp": datetime.now().isoformat()
    }
    save_battle_history(battle_record)

else:
    print("\n========= YOU DIED =========\n")
    battle_record = {
        "survived": False,
        "enemies_defeated": sum(1 for e in enemies if not e.is_alive()),
        "timestamp": datetime.now().isoformat()
    }
    save_battle_history(battle_record)




