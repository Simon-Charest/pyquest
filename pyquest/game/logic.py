import random


def get(list_, key, value):
    return [item for item in list_ if value in item.get(key)]


def get_enemy(enemies, hero_str):
    weak_enemies = get_greater_or_equal(enemies, 'atk', hero_str)
    enemy = random.choice(weak_enemies)

    return enemy


def get_greater_or_equal(list_, key, value):
    return [item for item in list_ if value >= item.get(key)]


def get_lesser(list_, key, value):
    return [item for item in list_ if value < item.get(key)]


def get_lesser_or_equal(list_, key, value):
    return [item for item in list_ if value <= item.get(key)]
