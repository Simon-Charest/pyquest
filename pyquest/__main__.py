from constant import *
from game import command, file, logic, cli


def main() -> None:
    # Hero
    hero_file: Path = SRC_PATH.joinpath("data/hero.json")
    commands: list = file.load_json(SRC_PATH.joinpath("data/commands.json"))
    levels: list = file.load_json(SRC_PATH.joinpath("data/levels.json"))
    characters: list = file.load_json(SRC_PATH.joinpath("data/characters.json"))
    hero: dict = file.load_json(hero_file)
    spells: list = file.load_json(SRC_PATH.joinpath("data/spells.json"))

    # Items
    armors = file.load_json(SRC_PATH.joinpath("data/armors.json"))
    shields = file.load_json(SRC_PATH.joinpath("data/shields.json"))
    weapons = file.load_json(SRC_PATH.joinpath("data/weapons.json"))
    items = file.load_json(SRC_PATH.joinpath("data/items.json"))

    # Map
    enemies: list = file.load_json(SRC_PATH.joinpath("data/enemies.json"))
    locations: list = file.load_json(SRC_PATH.joinpath("data/locations.json"))
    terrains: list = file.load_json(SRC_PATH.joinpath("data/terrains.json"))

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
