class Mob:
    def __init__(self, name, hp, attack, defense, drops):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.drops = drops

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        damage = max(0, amount - self.defense)
        self.hp -= damage
        print(f"{self.name} has taken {damage} damage. Remaining HP : {self.hp}")

    def attack_target(self, target):
        print(f"{self.name} is attacking {target.name}!")
        target.take_damage(self.attack)

class EliteMob(Mob):
    def __init__(self, name, hp, attack, defense, drops, skill):
        super().__init__(name, hp, attack, defense, drops)
        self.skill = skill

    def use_skill(self, target):
        print(f"{self.name} is using '{self.skill}'!")
        # Method Override
