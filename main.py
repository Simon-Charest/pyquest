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
    hero[0]['level'] = get_lesser_or_equal(levels, 'xp', hero[0]['xp'])[0]
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
    enemy = enemies[0]

    while True:
        if mode == 'fighting':
            print_commands(fighting_commands)

        else:
            print_commands(walkabout_commands)

        print('Command?')

        command = input().lower()

        if mode == 'walkabout':
            if command == 'f':
                mode = 'fighting'
                enemy = get_enemy(enemies, hero[0]['level']['str'])

            elif command == 't':
                print_status(hero)

            elif command == 's':
                print('Spell')

            elif command == 'i':
                print('Item')

            elif command == 'b':
                print('Buy')

            elif command == 'e':
                print('Sell')

            elif command == 'r':
                print('Rest')

        else:
            if command == 'f':
                mode = fight(hero, enemy)

            elif command == 's':
                print('Spell')

            elif command == 'i':
                print('Item')

            elif command == 'r':
                mode = 'walkabout'


def get_enemy(enemies, hero_str):
    weak_enemies = get_greater_or_equal(enemies, 'atk', hero_str)
    enemy = random.choice(weak_enemies)
    print(f"A {enemy['name']} draws near!")

    return enemy


def fight(hero, enemy):
    hero_atk = int(hero[0]['level']['str'] / 2) + hero[0]['weapon']['atk']
    enemy_hp = random.randint(0, hero_atk) - enemy['def']
    print(f"{hero[0]['name']} attacks!")

    if enemy_hp <= 0:
        print('The attack failed and there was no loss of Hit Points!')

    else:
        enemy['hp'] -= enemy_hp
        print(f"The {enemy['name']}'s Hit Points have been reduced by {enemy_hp}.")

    if enemy['hp'] <= 0:
        hero[0]['xp'] += enemy['xp']
        hero[0]['gp'] += enemy['gp']
        print(f"Thou hast done well in defeating the {enemy['name']}.")
        print(f"Thy Experience increases by {enemy['xp']}.")
        print(f"Thy GOLD increases by {enemy['gp']}.")

        return 'walkabout'

    else:
        hero_def = int(hero[0]['level']['agi'] / 2) + hero[0]['armor']['def'] + hero[0]['shield']['def']
        hero_hp = random.randint(0, enemy['atk']) - hero_def
        print(f"The {enemy['name']} attacks!")
        # print(f"{enemy['name']} chants the spell of {spell}.")
        # print(f"{enemy['name']} is breathing fire.")
        # print('The spell will not work.')

        if hero_hp <= 0:
            print('A miss! No damage hath been scored!')

        else:
            hero[0]['hp'] += hero_hp
            print(f"Thy Hits decreased by {hero_hp}.")

        if hero[0]['hp'] >= hero[0]['level']['hp']:
            print('Thou art dead.')
            exit()

    return 'fighting'


def get(list_, key, value):
    return [item for item in list_ if value in item.get(key)]


def get_greater_or_equal(list_, key, value):
    return [item for item in list_ if value >= item.get(key)]


def get_lesser_or_equal(list_, key, value):
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


def print_status(hero):
    print(f"{hero[0]['name']} | LV: {hero[0]['level']['lv']} | HP: {hero[0]['hp']} | MP: {hero[0]['mp']}"
          f" | G: {hero[0]['gp']} | E: {hero[0]['xp']}")


if __name__ == '__main__':
    main()
