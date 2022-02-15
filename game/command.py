from game import file, logic
import random


def approach(enemies, hero):
    enemy = logic.get_enemy(enemies, hero['level']['str'])
    print(f"A {enemy['name']} draws near!")

    return enemy, 'fighting'


def fight(hero, enemy, levels):
    print(f"{hero['name']} attacks!")
    hero_atk = int(hero['level']['str'] / 2) + int(hero['weapon']['atk'])
    enemy_dmg = random.randint(0, hero_atk)

    if random.randint(1, 64) == 64:
        print(f'Excellent move!')

    else:
        enemy_dmg -= enemy['def']

    if enemy_dmg <= 0:
        print('The attack failed and there was no loss of Hit Points!')

    else:
        print(f"The {enemy['name']}'s Hit Points have been reduced by {enemy_dmg}.")
        enemy['hp'] -= enemy_dmg

    if enemy['hp'] <= 0:
        print(f"Thou hast done well in defeating the {enemy['name']}.")
        print(f"Thy Experience increases by {enemy['xp']}.")
        print(f"Thy GOLD increases by {enemy['gp']}.")
        hero['xp'] += enemy['xp']
        hero['gp'] += enemy['gp']

        if hero['xp'] >= hero['level']['xp_next']:
            print('Courage and wit have served thee well. Thou hast been promoted to the next level.')
            print(f"Thy Power increases by {1}.")
            print(f"They Response Speed increases by {2}.")
            print(f"They Maximum Hit Points increase by {3}.")
            hero['level'] = logic.get_lesser(levels, 'xp_next', hero['xp'])[0]

        return 'walkabout'

    else:
        hero_def = int(hero['level']['agi'] / 2)

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


def print_status(hero):
    print(f"{hero['name']} | LV: {hero['level']['lv']} | HP: {hero['hp']} | MP: {hero['mp']} | G: {hero['gp']}"
          f" | E: {hero['xp']}")
    print(f"Before reaching thy next level of experience thou must gain {hero['level']['xp_next'] - hero['xp']}"
          f" points.")


def rest():
    print('Rest then for awhile.')
    exit()


def run(hero):
    print(f"{hero['name']} started to run away.")

    return 'walkabout'


def save(hero, hero_file):
    file.dump_json(hero_file, hero)
    print('Thy deeds have been recorded on the Imperial Scrolls of Honor.')


def sleep(hero):
    print('Good night.')
    hero['gp'] = int(0.75 * hero['gp'])
    hero['hp'] = hero['level']['hp_max']
    hero['mp'] = hero['level']['mp_max']
    print('Good morning. Thou seems to have spent a good night. I shall see thee again.')
