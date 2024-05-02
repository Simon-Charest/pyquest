from numpy import array, ndarray
from pathlib import Path


__author__: str = "Simon Charest"
__copyright__: str = "© 2019-2024 SLCIT Inc. All rights reserved."
__credits__: str = [
    {"Programmer": "Koichi Nakamura"},
    {"Director": "Koichi Nakamura"},
    {"Designer": "Yuji Horii"},
    {"Writer": "Yuji Horii"},
    {"Artist": "Akira Toriyama"},
    {"Composer": "Koichi Sugiyama"},
    {"Producer": "Yukinobu Chida"},
    {"Developer": "Chunsoft"},
    {
        "Publisher":
        [
            {"JP": "Enix"},
            {"NA": "Nintendo"}
        ]
    }
]
__email__: str = "simoncharest@gmail.com"
__license__: str = "MIT"
__maintainer__: str = "Simon Charest"
__project__: str = "Pyquest"
__status__: str = "Developement"
__version__: str = "1.0.0"


# Colors
class Color:
    BLACK: ndarray = array((0, 0, 0))
    BLUE: ndarray = array((235, 195, 117))
    RED: ndarray = array((58, 46, 234))
    LIGHT_GRAY: ndarray = array((173, 173, 173))
    GRAY: ndarray = array((117, 117, 117))
    LIGHT_GREEN: ndarray = array((141, 253, 159))
    GREEN: ndarray = array((131, 181, 121))
    DARK_GREEN: ndarray = array((115, 130, 100))
    LIGHT_BROWN: ndarray = array((120, 162, 204))
    BROWN: ndarray = array((76, 115, 196))
    DARK_BROWN: ndarray = array((116, 130, 150))
    ORANGE: ndarray = array((31, 156, 219))
    PURPLE: ndarray = array((96, 64, 88))
    WHITE: ndarray = array((246, 248, 254))
    YELLOW: ndarray = array((128, 234, 255))


# Paths
SRC_PATH: Path = Path(__file__).parent
ROOT_PATH: Path = SRC_PATH.parent
DATA_PATH: Path = SRC_PATH.joinpath("data")

TILE_SIZE: int = 64
