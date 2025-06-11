from item import *
from effect import *

item_registry = {
    "Basic Sword": Weapon(
        name="Basic Sword",
        description="A simple iron sword.",
        damage=10,
        rarity="common",
        effect=AttackBuffEffect(name="Sharpness", bonus=2),
        status=None
    ),

    "Stun Baton": Weapon(
        name="Stun Baton",
        description="Perfectly suited for subduing standard targets.",
        damage=15,
        rarity="common",
        effect=AttackBuffEffect(name="Stunned", bonus=5),
        status=None
    ),
    
    "Longsword": Weapon(
        name="Longsword",
        description="Old-fashioned, but still deadly.",
        damage=25,
        rarity="rare",
        effect=BleedEffect(name="Bleed", damage_per_turn=3, duration=3),
        status=None
    ),

    "Chainsaw": Weapon(
        name="Chainsaw",
        description="Effective way to conversation.",
        damage=30,
        rarity="rare",
        effect=BleedEffect(name="Teared", damage_per_turn=5, duration=2),
        status=None
    ),
    
    "Chiljido": Weapon(
        name="Chiljido",
        description="Forged for rites - from lands unknown",
        damage=45,
        rarity="legendary",
        effect=AttackBuffEffect(name="Buff", bonus = 10),
        status=None
    ),

    "Anti-Blade Vest": Passive(
        name="Anti-Blade Vest",
        description="Stops blades... more or less",
        rarity="common",
        roll_effect=None,
        defense_effect=DefenseBuffEffect(name="Anti-Blade", bonus = 10),
        status=None
    ),

    "Ballistic Helmet": Passive(
        name="Ballistic Helmet",
        description="Must-Have in any combat zone",
        rarity="rare",
        roll_effect=None,
        defense_effect=DefenseBuffEffect(name="Helmet", bonus=20),
        status=None
    ),

    "Gothic Plate Armour": Passive(
        name="Gothic Plate Armour",
        description="German Classic",
        rarity="legendary",
        roll_effect=None,
        defense_effect=DefenseBuffEffect(name="Armour", bonus= 25),
        status=None
    ),

    "Bourbon": Active(
        name="Bourbon",
        description="A Kentucky Classic. Brings you courage in every sip",
        rarity="common",
        effect=AttackBuffEffect(name="courage", bonus=3),
        target=[],
        uses=3,
        status=None
    ),

    "Healing Potion": Active(
        name="Healing Potion",
        description="Even its creator doesn't know how it works.",
        rarity="common",
        effect=RegenEffect(name="Heal", heal_per_turn=5, duration=3),
        target=[],
        uses=3,
        status=None
    ),

    "Molotov Cocktail": Active(
        name="Molotov Cocktail",
        description="Hot Stuff. Handle with care",
        rarity="rare",
        effect=None,
        target=["enemy"],
        uses=1,
        status=FireEffect(name="Burn", damage_per_turn=3, duration=4)
    ),

    "Greater Healing Potion": Active(
        name="Greater Healing Portion",
        description="The first was an accident",
        rarity="rare",
        effect=RegenEffect(name="Heal", heal_per_turn=8, duration=3),
        target=[],
        uses=2,
        status=None
    ),

    "Stimulant": Active(
        name="Stimultant", 
        description="You feel stronger. Avoid Overuse!",
        rarity="rare",
        effect=AttackBuffEffect(name="stronger", bonus=10),
        target=[],
        uses=1,
        status=None
    ),

    "Elixir": Active(
        name="Elixirt",
        description="It's magic",
        rarity="legendary",
        effect=RegenEffect(name="Heal", heal_per_turn=100, duration=1),
        target=[],
        uses=1,
        status=None
    )
}
