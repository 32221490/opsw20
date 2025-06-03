from cmd2 import *
from player import *
from SaveSystem import *
from combat import *

class GameShell(Cmd):
    prompt = "(proj) "
    intro = """\n========= PROJ NAME =========\nENTER THE COLLAPSING SPACETIME with 'start <1~3>'\n"""

    def __init__(self):
        super().__init__()
        self.player = None
        self.slot = None

    def do_start(self, arg):
        """ENTER THE COLLAPSING SPACETIME : start < 1 | 2 | 3 >"""
        slot = arg.strip()
        if slot not in {"1", "2", "3"}:
            print("Invalid Slot Number! Choose 1, 2, 3")
            return
        save = SaveSystem(int(slot))
        data = save.load_player()
        if data:
            self.player = Player.from_dict(data)
            print(f"Slot {slot} LOADED SUCCESSFULLY!")
        else:
            name = input("Player Name : ")
            self.player = Player(name)
            save.save_player(self.player)
            print(f"NEW PLAYER '{name}' HAS BEEN CREATED SUCCESSFULLY")
        self.slot = slot

    def do_fight(self, arg):
        """ COMBAT STARTING """
        if not self.player:
            print("Start Game First with 'start <1~3>'")
            return
        difficulty = 1.0 + self.player.boss_count * 0.2
        combat = Combat(self.player, difficulty, self.player.boss_count)
        alive = combat.start_battle()

        if not alive:
            answer = input("Your Journey Ends Here. Do You Want to Get Back to First SPACETIME? (y/n) : ").lower()
            if answer == 'y':
                self.player = Player(name)
                self.player.boss_count = 0
                print("Your Journey Started Again from First SPACETIME")
            else:
                print("QUIT GAME.")
                return True

    def do_save(self, arg):
        """ SAVE CURRENT STATUS """
        if self.player:
            SaveSystem(int(self.slot)).save_player(self.player)
            print("SAVED SUCCESSFULLY")
        else:
            print("NO PLAYER DATA TO SAVE")

    def do_inventory(self, arg):
        if self.player:
            self.player.show_inventory()
        else:
            print("NO PLAYER DATA")

    def do_exit(self, arg):
        """ EXIT GAME """
        print("QUIT GAME")
        return True

    def do_slots(self, arg):
        """ CHECKING SAVE SLOTS """
        slots = list_save_slots()
        print("SAVE SLOTS : ")
        for slot in slots:
            print(f" - SLOT {slot}")

if __name__ == "__main__":
    GameShell().cmdloop()
