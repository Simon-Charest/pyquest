from collections import Counter
from pytest import fixture

# Pyquest
from pyquest.utils import *
from pyquest.constant import *


class TestReadMap:
    # Arrange
    @fixture(scope="session")
    def tiles(self) -> list[str]:
        # Act
        return ["w", "F", "P", "M", "H", "D", "S", "\n", "W", "B", "T", "c", "s", "C"]

    @fixture(scope="session")
    def map(self) -> str:
        # Act
        return read_map(str(DATA_PATH.joinpath("map.png")))
    
    @fixture(scope="session")
    def characters(self, map: str) -> Counter[str]:
        # Act
        return Counter(map)

    # Assert
    def test_column_count(self, map: str) -> None:
        assert len(map[:map.find("\n")]) == 128

    def test_row_count(self, characters: Counter[str]) -> None:
        assert characters["\n"] == 128

    def test_unique_count(self, characters: Counter[str], tiles: list[str]) -> None:
        assert len(characters) == len(tiles)

    def test_tiles(self, characters: Counter[str], tiles: list[str]) -> None:
        assert set(characters) == set(tiles)

    def test_unidentified_not_found(self, characters: Counter[str]) -> None:
        assert "_" not in characters

    def test_water_count(self, characters: Counter[str]) -> None:
        assert characters["w"] == 5854

    def test_forest_count(self, characters: Counter[str]) -> None:
        assert characters["F"] == 4216

    def test_plain_count(self, characters: Counter[str]) -> None:
        assert characters["P"] == 2278

    def test_mountain_count(self, characters: Counter[str]) -> None:
        assert characters["M"] == 1644

    def test_hill_count(self, characters: Counter[str]) -> None:
        assert characters["H"] == 1334

    def test_desert_count(self, characters: Counter[str]) -> None:
        assert characters["D"] == 671

    def test_swamp_count(self, characters: Counter[str]) -> None:
        assert characters["S"] == 348

    def test_wall_count(self, characters: Counter[str]) -> None:
        assert characters["W"] == 15

    def test_bridge_count(self, characters: Counter[str]) -> None:
        assert characters["B"] == 10

    def test_town_count(self, characters: Counter[str]) -> None:
        assert characters["T"] == 6

    def test_cave_count(self, characters: Counter[str]) -> None:
        assert characters["c"] == 4

    def test_stairs_count(self, characters: Counter[str]) -> None:
        assert characters["s"] == 2

    def test_castle_count(self, characters: Counter[str]) -> None:
        assert characters["C"] == 2    
