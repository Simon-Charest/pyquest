"""
PyQuery is a Dragon Quest 1 (Famicom) / Dragon Warrior 1 (NES) clone.
"""

from game import const, data, logic, ui
import json
import random


def main():
    # ui.run()
    # init_game()

    # Hero
    hero = load_json('data/hero.json')
    commands = load_json('data/commands.json')
    levels = load_json('data/levels.json')
    save = load_json('data/save.json')
    spells = load_json('data/spells.json')

    # Items
    armors = load_json('data/armors.json')
    shields = load_json('data/shields.json')
    weapons = load_json('data/weapons.json')
    items = load_json('data/items.json')

    # Map
    enemies = load_json('data/enemies.json')
    locations = load_json('data/locations.json')
    terrains = load_json('data/terrains.json')

    # Gameplay
    enemy = random.choice(enemies)

    # Display
    print(hero)
    print(enemy)


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
