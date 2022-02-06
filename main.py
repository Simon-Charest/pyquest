"""
PyQuery is a Dragon Quest 1 (Famicom) / Dragon Warrior 1 (NES) clone.
"""

from game import const, logic, ui
import json
import random


def main():
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


def get(list_, key, value):
    return [item for item in list_ if item.get(key) == value]


def load_json(file):
    stream = open(file)
    json_data = json.load(stream)
    stream.close()

    return json_data


if __name__ == '__main__':
    main()
