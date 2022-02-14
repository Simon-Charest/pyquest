import json
import random


def dump_json(file, json_data):
    stream = open(file, 'w')
    json.dump(json_data, stream, indent=2)
    stream.close()


def fight(hero, enemy):
    hero_atk = int(hero['lv']['str'] / 2) + int(hero['weapon']['atk'])
    enemy_dmg = random.randint(0, hero_atk) - enemy['def']
    print(f"{hero['name']} attacks!")

    if enemy_dmg <= 0:
        print('The attack failed and there was no loss of Hit Points!')

    else:
        enemy['hp'] -= enemy_dmg
        print(f"The {enemy['name']}'s Hit Points have been reduced by {enemy_dmg}.")

    if enemy['hp'] <= 0:
        hero['xp'] += enemy['xp']
        hero['gp'] += enemy['gp']
        print(f"Thou hast done well in defeating the {enemy['name']}.")
        print(f"Thy Experience increases by {enemy['xp']}.")
        print(f"Thy GOLD increases by {enemy['gp']}.")

        return 'walkabout'

    else:
        hero_def = int(hero['lv']['agi'] / 2)

        if hero['armor']:
            hero_def += hero['armor']['def']

        if hero['shield']:
            hero_def += hero['shield']['def']

        hero_dmg = random.randint(0, enemy['atk']) - hero_def
        print(f"The {enemy['name']} attacks!")
        # print(f"{enemy['name']} chants the spell of {spell}.")
        # print(f"{enemy['name']} is breathing fire.")
        # print('The spell will not work.')

        if hero_dmg <= 0:
            print('A miss! No damage hath been scored!')

        else:
            hero['hp'] -= hero_dmg
            print(f"Thy Hits decreased by {hero_dmg}.")

        if hero['hp'] <= 0:
            print('Thou art dead.')
            exit()

    return 'fighting'


def get(list_, key, value):
    return [item for item in list_ if value in item.get(key)]


def get_enemy(enemies, hero_str):
    weak_enemies = get_greater_or_equal(enemies, 'atk', hero_str)
    enemy = random.choice(weak_enemies)
    print(f"A {enemy['name']} draws near!")

    return enemy


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
    print(f"{hero['name']} | LV: {hero['lv']['lv']} | HP: {hero['hp']} | MP: {hero['mp']}"
          f" | G: {hero['gp']} | E: {hero['xp']}")
