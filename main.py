"""
PyQuery is a Dragon Quest 1 (Famicom) / Dragon Warrior 1 (NES) clone.
"""

from game import const, logic, ui
import json
import random
from msvcrt import getch, getche


def main():
    # Hero
    characters = load_json('data/characters.json')
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
    hero = get(characters, 'title', 'Hero')
    weapon = get(weapons, 'name', 'Club')
    armor = get(armors, 'name', 'Leather Armor')
    shield = get(shields, 'name', 'Leather Shield')
    spell = get(spells, 'name', 'Heal')

    # Display
    print(hero)
    print(weapon)
    print(armor)
    print(shield)
    print(spell)
    print(enemy)

    input_command(commands)


def get(list_, key, value):
    return next(item for item in list_ if item.get(key) == value)


def input_command(commands):
    for command in commands:
        print(f"{command['key']}: {command['name']}")

    while True:
        print('Command?')

        command = input()

        if command in ['F', 'f']:
            print('Fight')

        if command in ['S', 's']:
            print('Spell')

        if command in ['I', 'i']:
            print('Item')

        if command in ['R', 'r']:
            print('Run')

        if command in ['Q', 'q']:
            break


def load_json(file):
    stream = open(file)
    json_data = json.load(stream)
    stream.close()

    return json_data


if __name__ == '__main__':
    main()
