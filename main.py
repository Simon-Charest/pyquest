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
    hero = get(characters, 'title', 'Hero')
    hero[0]['level'] = get_less_or_equal(levels, 'xp', hero[0]['xp'])[0]
    hero[0]['weapon'] = get(weapons, 'name', 'Club')[0]
    hero[0]['armor'] = get(armors, 'name', 'Leather Armor')[0]
    hero[0]['shield'] = get(shields, 'name', 'Leather Shield')[0]
    mode = 'walkabout'

    # Display
    # print(hero)
    # print(weapon)
    # print(armor)
    # print(shield)
    # print(spell)

    walkabout_commands = get(commands, 'mode', 'walkabout')
    fighting_commands = get(commands, 'mode', 'fighting')

    while True:
        if mode == 'fighting':
            print_commands(fighting_commands)

        else:
            print_commands(walkabout_commands)

        print('Command?')

        command = input().lower()
        enemy = enemies[0]

        if mode == 'walkabout':
            if command == 'f':
                mode = 'fighting'
                enemy = random.choice(enemies)
                print(f"A {enemy['name']} draws near!")

            elif command == 's':
                print('Spell')

            elif command == 'i':
                print('Item')

            elif command == 'b':
                print('Buy')

            elif command == 'e':
                print('Sell')

            elif command == 't':
                print('Rest')

        else:
            if command == 'f':
                while enemy['hp'] > 0 and hero[0]['level']['hp'] - hero[0]['hp'] > 0:
                    enemy['hp'] -= random.randint(0, hero[0]['weapon']['atk'] + hero[0]['level']['str'])
                    hero[0]['hp'] += random.randint(0, enemy['atk'])

                    break

            elif command == 's':
                print('Spell')

            elif command == 'i':
                print('Item')

            elif command == 'r':
                mode = 'walkabout'


def get(list_, key, value):
    return [item for item in list_ if value in item.get(key)]


def get_less_or_equal(list_, key, value):
    return [item for item in list_ if value <= item.get(key)]


def load_json(file):
    stream = open(file)
    json_data = json.load(stream)
    stream.close()

    return json_data


def print_commands(commands):
    string = ''

    for command in commands:
        if string:
            string += ' | '

        string += f"{command['key']}: {command['name']}"

    print(string)


if __name__ == '__main__':
    main()
