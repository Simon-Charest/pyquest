"""
PyQuery is a Dragon Quest 1 (Famicom) / Dragon Warrior 1 (NES) clone.
"""

from game import const, data, logic, ui
import json
import random


def main():
    # ui.run()
    # init_game()
    levels = load_json('data/levels.json')
    spells = load_json('data/spells.json')
    weapons = load_json('data/weapons.json')
    armors = load_json('data/armors.json')
    shields = load_json('data/shields.json')
    monsters = load_json('data/monsters.json')
    commands = load_json('data/commands.json')
    hero = load_json('data/hero.json')

    monster = random.choice(monsters)

    print(hero)
    print(monster)


def load_json(file):
    stream = open(file)
    json_data = json.load(stream)
    stream.close()

    return json_data


def init_game():
    hero = logic.init_hero()

    # Display hero stats
    print(hero)

    # Get stats for specific level
    print(logic.get_level(data.LEVELS, 0))

    # Get specific spell
    print(logic.get_element(data.SPELLS, "Heal"))

    # Get specific equipment
    print(logic.get_element(data.WEAPONS, "Club"))
    print(logic.get_element(data.ARMORS, "Leather Armor"))
    print(logic.get_element(data.SHIELDS, "Leather Shield"))

    # Get random enemy
    print(logic.get_random_element(data.ENEMIES))

    # Display list of commands
    print(logic.get_commands())


if __name__ == '__main__':
    main()
