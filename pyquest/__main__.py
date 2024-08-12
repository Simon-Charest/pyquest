from argparse import ArgumentParser, Namespace
from pathlib import Path

# Pygquest
from constant import *
from utils import *
from cli import *
from command import *
from file import *
from game import run_game
from logic import *


def main() -> None:
    argument_parser: ArgumentParser = ArgumentParser("Pyquest: A Dragon Quest (Famicom) / Warrior (NES) clone.")
    argument_parser.add_argument("--map_c2b", "-b", action="store_true", help="convert map from characters to bitmap")
    argument_parser.add_argument("--map_b2c", "-c", action="store_true", help="convert map from bitmap to characters")
    argument_parser.add_argument("--map", "-m", action="store_true", help="load map")
    argument_parser.add_argument("--zelda", "-z", action="store_true", help="load The Legend of Zelda map")
    argument_parser.add_argument("--game", "-g", action="store_true", help="start game")
    arguments: Namespace = argument_parser.parse_args()

    if arguments.map_c2b:
        map_string: str = open(DATA_PATH.joinpath("map.txt")).read()
        write_map(map_string, DATA_PATH.joinpath("out.png"), DATA_PATH.joinpath("tile/*.png"))

    if arguments.map_b2c:
        map_string: str = read_map(DATA_PATH.joinpath("map.png"), DATA_PATH.joinpath("tile/*.png"))
        open(DATA_PATH.joinpath("map.txt"), "w").write(map_string)

    if arguments.map:
        run_game()

    if arguments.zelda:
        map: str = read_zelda_map(DATA_PATH.joinpath("zelda1.png"))
        open(DATA_PATH.joinpath("zelda1.txt"), "w").write(map)

    if arguments.game:
        # Hero
        hero_file: Path = DATA_PATH.joinpath("hero.json")
        commands: list = load_json(DATA_PATH.joinpath("commands.json"))
        levels: list = load_json(DATA_PATH.joinpath("levels.json"))
        characters: list = load_json(DATA_PATH.joinpath("characters.json"))
        hero: dict = load_json(hero_file)
        spells: list = load_json(DATA_PATH.joinpath("spells.json"))

        # Items
        armors = load_json(DATA_PATH.joinpath("armors.json"))
        shields = load_json(DATA_PATH.joinpath("shields.json"))
        weapons = load_json(DATA_PATH.joinpath("weapons.json"))
        items = load_json(DATA_PATH.joinpath("items.json"))

        # Map
        enemies: list = load_json(DATA_PATH.joinpath("enemies.json"))
        locations: list = load_json(DATA_PATH.joinpath("locations.json"))
        terrains: list = load_json(DATA_PATH.joinpath("terrains.json"))

        # Gameplay
        mode: str = "walkabout"

        fighting_commands = get(commands, "mode", "fighting")
        walkabout_commands = get(commands, "mode", "walkabout")
        enemy = enemies[0]

        while True:
            if mode == "fighting":
                print_commands(fighting_commands)

            else:
                print_commands(walkabout_commands)

            print("Command?")
            string = input().lower()

            if string == "t":
                print_status(hero)

            elif mode == "walkabout":
                if string == "f":
                    enemy, mode = approach(enemies, hero)

                elif string == "s":
                    print("Spell")

                elif string == "i":
                    print("Item")

                elif string == "b":
                    print("Buy")

                elif string == "e":
                    print("Sell")

                elif string == "l":
                    sleep(hero)

                elif string == "a":
                    save(hero, hero_file)

                elif string == "r":
                    rest()

            else:
                if string == "f":
                    mode = fight(hero, enemy, levels)

                elif string == "s":
                    print("Spell")

                elif string == "i":
                    print("Item")

                elif string == "r":
                    mode = run(hero)


if __name__ == "__main__":
    main()
