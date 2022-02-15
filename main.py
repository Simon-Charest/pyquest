#!/usr/bin/python
# coding: utf-8

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

from game import command, file, logic, ui


def main():
    # Hero
    hero_file = 'data/hero.json'
    commands = file.load_json('data/commands.json')
    levels = file.load_json('data/levels.json')
    # characters = file.load_json('data/characters.json')
    # hero = file.load_json('data/hero.json')
    # spells = file.load_json('data/spells.json')

    # Items
    # armors = file.load_json('data/armors.json')
    # shields = file.load_json('data/shields.json')
    # weapons = file.load_json('data/weapons.json')
    # items = file.load_json('data/items.json')

    # Map
    enemies = file.load_json('data/enemies.json')
    # locations = file.load_json('data/locations.json')
    # terrains = file.load_json('data/terrains.json')

    # Gameplay
    hero = file.load_json(hero_file)
    mode = 'walkabout'

    walkabout_commands = logic.get(commands, 'mode', 'walkabout')
    fighting_commands = logic.get(commands, 'mode', 'fighting')
    enemy = enemies[0]

    while True:
        if mode == 'fighting':
            ui.print_commands(fighting_commands)

        else:
            ui.print_commands(walkabout_commands)

        print('Command?')

        string = input().lower()

        if string == 't':
            command.print_status(hero)

        elif mode == 'walkabout':
            if string == 'f':
                enemy, mode = command.approach(enemies, hero)

            elif string == 's':
                print('Spell')

            elif string == 'i':
                print('Item')

            elif string == 'b':
                print('Buy')

            elif string == 'e':
                print('Sell')

            elif string == 'l':
                command.sleep(hero)

            elif string == 'a':
                command.save(hero, hero_file)

            elif string == 'r':
                command.rest()

        else:
            if string == 'f':
                mode = command.fight(hero, enemy, levels)

            elif string == 's':
                print('Spell')

            elif string == 'i':
                print('Item')

            elif string == 'r':
                mode = command.run(hero)


if __name__ == '__main__':
    main()
