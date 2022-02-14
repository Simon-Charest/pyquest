#!/usr/bin/python
# coding=utf-8

__author__ = 'Simon Charest'
__copyright__ = '© 2019-2022 SLCIT Inc. All rights reserved.'
__credits__ = [
    {"Programmer": "Koichi Nakamura"},
    {"Director": "Koichi Nakamura"},
    {"Designer": "Yuji Horii"},
    {"Writer": "Yuji Horii"},
    {"Artist": "Akira Toriyama"},
    {"Composer": "Koichi Sugiyama"},
    {"Producer": "Yukinobu Chida"},
    {"Developer": "Chunsoft"},
    {
        "Publisher":
        [
            {"JP": "Enix"},
            {"NA": "Nintendo"}
        ]
    }
]
__email__ = 'simoncharest@gmail.com'
__license__ = 'MIT'
__maintainer__ = 'Simon Charest'
__project__ = 'PyQuest'
__status__ = 'Developement'
__version__ = '1.0.0'

# PyQuery is a Dragon Quest 1 (Famicom) / Dragon Warrior 1 (NES) clone.

from game import logic
import json
import random


def main():
    # Hero
    hero_file = 'data/hero.json'
    characters = logic.load_json('data/characters.json')
    commands = logic.load_json('data/commands.json')
    levels = logic.load_json('data/levels.json')
    hero = logic.load_json('data/hero.json')
    spells = logic.load_json('data/spells.json')

    # Items
    armors = logic.load_json('data/armors.json')
    shields = logic.load_json('data/shields.json')
    weapons = logic.load_json('data/weapons.json')
    items = logic.load_json('data/items.json')

    # Map
    enemies = logic.load_json('data/enemies.json')
    locations = logic.load_json('data/locations.json')
    terrains = logic.load_json('data/terrains.json')

    # Gameplay
    hero = logic.load_json(hero_file)
    # hero[0]['level'] = get_lesser_or_equal(levels, 'xp', hero[0]['xp'])[0]
    # hero[0]['weapon'] = get(weapons, 'name', 'Club')[0]
    # hero[0]['armor'] = get(armors, 'name', 'Leather Armor')[0]
    # hero[0]['shield'] = get(shields, 'name', 'Leather Shield')[0]
    mode = 'walkabout'

    # Display
    # print(hero)
    # print(weapon)
    # print(armor)
    # print(shield)
    # print(spell)

    walkabout_commands = logic.get(commands, 'mode', 'walkabout')
    fighting_commands = logic.get(commands, 'mode', 'fighting')
    enemy = enemies[0]

    while True:
        if mode == 'fighting':
            logic.print_commands(fighting_commands)

        else:
            logic.print_commands(walkabout_commands)

        print('Command?')

        command = input().lower()

        if mode == 'walkabout':
            if command == 'f':
                mode = 'fighting'
                enemy = logic.get_enemy(enemies, hero['lv']['str'])

            elif command == 't':
                logic.print_status(hero)

            elif command == 's':
                print('Spell')

            elif command == 'i':
                print('Item')

            elif command == 'b':
                print('Buy')

            elif command == 'e':
                print('Sell')

            elif command == 'r':
                hero['gp'] = int(0.75 * hero['gp'])
                hero['hp'] = hero['lv']['hp_max']
                hero['mp'] = hero['lv']['mp_max']
                logic.dump_json(hero_file, hero)

        else:
            if command == 'f':
                mode = logic.fight(hero, enemy)

            elif command == 's':
                print('Spell')

            elif command == 'i':
                print('Item')

            elif command == 'r':
                mode = 'walkabout'


if __name__ == '__main__':
    main()
