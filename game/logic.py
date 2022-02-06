import random


def get_element(list_, name):
    """ Get specific element """
    for element in list_:
        if list_[element]['name'] == name:
            return list_[element]

    return None


def get_level(levels, exp):
    """ Get level stats, by experience points """
    for level in sorted(levels.keys(), reverse=True):
        if exp >= levels[level]["exp_req"]:
            return levels[level]


def get_power(power, item_power=0):
    return power + item_power


def get_random_element(list_):
    """ Get random element """
    return random.choice(list_)


def init_hero(exp=0):
    return {
        "name": "Solo",
        "lv": get_level(data.LEVELS, exp)["lv"],
        "hp": get_level(data.LEVELS, exp)["hp_max"],
        "mp": get_level(data.LEVELS, exp)["mp_max"],
        "str": get_level(data.LEVELS, exp)["str"],
        "agi": get_level(data.LEVELS, exp)["agi"],
        "atk": get_power(get_level(data.LEVELS, exp)["str"]),
        "def": get_power(get_level(data.LEVELS, exp)["agi"]),
        "gp": 120,
        "exp": get_level(data.LEVELS, exp)["exp_req"],
        "weapon": None,
        "armor": None,
        "shield": None,
        "spells": get_level(data.LEVELS, exp)["spells"]
    }


def load(file, mode='rt'):
    """ Read file and return content, line by line, as a list """
    with open(file, mode) as handle:
        lines = handle.read().splitlines()

    return lines


def save(file, content, mode='wt'):
    """ Write file, line by line """
    with open(file, mode) as handle:
        for line in content:
            handle.write(line + '\n')

    return True
