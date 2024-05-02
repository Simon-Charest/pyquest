from argparse import ArgumentParser, Namespace
from collections import Counter
from cv2 import imread
from cv2.typing import MatLike
from numpy import array, array_equal

# Pygquest
from constant import *
from game import command, file, logic, cli


def main() -> None:
    argument_parser: ArgumentParser = ArgumentParser("Pyquest: A Dragon Quest (Famicom) / Warrior (NES) clone.")
    argument_parser.add_argument("--map", "-m", action="store_true", help="process map")
    arguments: Namespace = argument_parser.parse_args()

    if arguments.map:
        image: MatLike = imread(str(DATA_PATH.joinpath("map.png")))
        x: int
        y: int
        b: int
        g: int
        r: int
        string: str = ""

        for x in range(0, image.shape[0], TILE_SIZE):
            for y in range(0, image.shape[1], TILE_SIZE):
                # Plain
                if array_equal(image[x + 17, y + 17], array((141, 253, 159))):
                    string += "P"

                # Desert
                elif array_equal(image[x + 17, y + 17], array((128, 234, 255))):
                    string += "D"

                # Forest
                elif array_equal(image[x + 17, y + 17], array((115, 130, 100))):
                    string += "F"

                # Hill
                elif array_equal(image[x + 17, y + 17], array((120, 162, 204))):
                    string += "H"

                # Mountain
                elif array_equal(image[x + 17, y + 17], array((117, 117, 117))):
                    string += "M"
                
                # Water
                elif array_equal(image[x + 17, y + 17], array((235, 195, 117))):
                    string += "W"

                # Swamp
                elif array_equal(image[x + 17, y + 17], array((96, 64, 88))):
                    string += "S"

                # Cave
                elif array_equal(image[x + 17, y + 17], array((96, 64, 88))):
                    string += "C"

                # Castle
                elif array_equal(image[x + 17, y + 17], array((117, 117, 121))):
                    string += "A"
                
                # Town
                elif array_equal(image[x + 17, y + 17], array((58, 46, 234))):
                    string += "T"

                # Wall
                elif array_equal(image[x + 17, y + 17], array((173, 173, 173))):
                    string += "L"

                # Undefined
                else:
                    print(image[x + 17, y + 17])
                    string += "_"

            string += "\n"

        open(DATA_PATH.joinpath("map.txt"), "w").write(string)

        character: str
        
        for character in ["P", "D", "F", "H", "M", "W", "S", "C", "A", "T", "L", "_"]:
            print(f"{character}: {Counter(string).get(character, 0)}")

        exit()

    # Hero
    hero_file: Path = DATA_PATH.joinpath("hero.json")
    commands: list = file.load_json(DATA_PATH.joinpath("commands.json"))
    levels: list = file.load_json(DATA_PATH.joinpath("levels.json"))
    characters: list = file.load_json(DATA_PATH.joinpath("characters.json"))
    hero: dict = file.load_json(hero_file)
    spells: list = file.load_json(DATA_PATH.joinpath("spells.json"))

    # Items
    armors = file.load_json(DATA_PATH.joinpath("armors.json"))
    shields = file.load_json(DATA_PATH.joinpath("shields.json"))
    weapons = file.load_json(DATA_PATH.joinpath("weapons.json"))
    items = file.load_json(DATA_PATH.joinpath("items.json"))

    # Map
    enemies: list = file.load_json(DATA_PATH.joinpath("enemies.json"))
    locations: list = file.load_json(DATA_PATH.joinpath("locations.json"))
    terrains: list = file.load_json(DATA_PATH.joinpath("terrains.json"))

    # Gameplay
    mode: str = "walkabout"

    fighting_commands = logic.get(commands, "mode", "fighting")
    walkabout_commands = logic.get(commands, "mode", "walkabout")
    enemy = enemies[0]

    while True:
        if mode == "fighting":
            cli.print_commands(fighting_commands)

        else:
            cli.print_commands(walkabout_commands)

        print("Command?")
        string = input().lower()

        if string == "t":
            command.print_status(hero)

        elif mode == "walkabout":
            if string == "f":
                enemy, mode = command.approach(enemies, hero)

            elif string == "s":
                print("Spell")

            elif string == "i":
                print("Item")

            elif string == "b":
                print("Buy")

            elif string == "e":
                print("Sell")

            elif string == "l":
                command.sleep(hero)

            elif string == "a":
                command.save(hero, hero_file)

            elif string == "r":
                command.rest()

        else:
            if string == "f":
                mode = command.fight(hero, enemy, levels)

            elif string == "s":
                print("Spell")

            elif string == "i":
                print("Item")

            elif string == "r":
                mode = command.run(hero)


if __name__ == "__main__":
    main()
