from cv2 import imread, imwrite
from cv2.typing import MatLike
from glob import glob
from numpy import uint8, zeros

# Pyquest
try: from constant import *
except: pass
try: from pyquest.constant import *
except: pass


def read_map(filename: Path) -> str:
    map: MatLike = imread(str(filename))
    tiles: dict[str, MatLike] = read_tiles(DATA_PATH.joinpath("*.png"))
    y: int
    x: int
    tile: ndarray
    string: str = ""

    for y in range(0, map.shape[0], TILE_SIZE):
        for x in range(0, map.shape[1], TILE_SIZE):
            tile = map[y : y + TILE_SIZE, x : x + TILE_SIZE]

            if are_equal(tile, tiles["castle"]):
                string += "C"

            elif are_equal(tile, tiles["cave"]):
                string += "c"

            elif are_equal(tile, tiles["town"]):
                string += "T"

            elif are_equal(tile, tiles["stairs"]):
                string += "s"

            elif are_equal(tile, tiles["bridge"]):
                string += "B"

            elif are_equal(tile, tiles["wall"]):
                string += "W"
            
            elif are_equal(tile, tiles["water"]):
                string += "w"
            
            elif are_equal(tile, tiles["plain"]):
                string += "P"

            elif are_equal(tile, tiles["forest"]):
                string += "F"

            elif are_equal(tile, tiles["hill"]):
                string += "H"

            elif are_equal(tile, tiles["mountain"]):
                string += "M"

            elif are_equal(tile, tiles["desert"]):
                string += "D"

            elif are_equal(tile, tiles["swamp"]):
                string += "S"

            else:
                string += "_"

        string += "\n"

    return string


def get_image(color: tuple[int, int, int], width: int = 1, height: int = 1) -> ndarray:
    image: ndarray = zeros((1, 1, 3), uint8)
    y: int
    x: int

    for y in range(0, height):
        for x in range(0, width):
            image[x, y] = color

    return image


def read_zelda_map(filename: Path, tile_size: int = 1, threshold: float = 0.0001) -> str:
    map: MatLike = imread(str(filename))
    y: int
    x: int
    tile: ndarray
    string: str = ""
    cave: ndarray = get_image((0, 0, 0))
    ground1: ndarray = get_image((189, 239, 247))
    ground2: ndarray = get_image((123, 123, 123))
    ladder: ndarray = get_image((247, 82, 90))
    forest1: ndarray = get_image((41, 189, 90))
    forest2: ndarray = get_image((82, 82, 173))
    mountain1: ndarray = get_image((0, 74, 239))
    mountain2: ndarray = get_image((0, 152, 0))
    mountain3: ndarray = get_image((181, 181, 181))
    water: ndarray = get_image((255, 0, 24))

    for y in range(0, map.shape[0], tile_size):
        if y % 40 == 0:
            continue

        for x in range(0, map.shape[1], tile_size):
            if x % 60 == 0:
                continue

            tile = map[y : y + tile_size, x : x + tile_size]

            if are_equal(tile, cave, threshold):
                string += "C"

            elif are_equal(tile, ground1, threshold):
                string += " "
                
            elif are_equal(tile, ground2, threshold):
                string += " "

            elif are_equal(tile, ladder, threshold):
                string += " "

            elif are_equal(tile, forest1, threshold):
                string += "F"

            elif are_equal(tile, forest2, threshold):
                string += "F"
            
            elif are_equal(tile, mountain1, threshold):
                string += "M"

            elif are_equal(tile, mountain2, threshold):
                string += "M"

            elif are_equal(tile, mountain3, threshold):
                string += "M"

            elif are_equal(tile, water, threshold):
                string += "W"

            else:
                string += "_"

        string += "\n"

    return string


def read_tiles(pathname: Path) -> dict[str, MatLike]:
    paths: list[str] = glob(str(pathname))
    path: str
    tiles: dict[str, MatLike] = {}

    for path in paths:
        tiles[Path(path).stem] = imread(path)

    return tiles


def write_map(map_string: str, filename: Path):
    rows: list[str] = map_string.split("\n")[:-1]
    width: int = TILE_SIZE * len(rows[0])
    height: int = TILE_SIZE * len(rows)
    channels: int = 3
    map_image: ndarray = zeros((height, width, channels))
    tiles: dict[str, MatLike] = read_tiles(DATA_PATH.joinpath("*.png"))

    for y, row in enumerate(rows):
        for x, tile_char in enumerate(row):
            if tile_char == "C":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["castle"]

            elif tile_char == "c":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["cave"]

            elif tile_char == "T":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["town"]

            elif tile_char == "s":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["stairs"]
                                                                                                            
            elif tile_char == "B":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["bridge"]
            
            elif tile_char == "W":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["wall"]

            elif tile_char == "w":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["water"]

            elif tile_char == "P":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["plain"]

            elif tile_char == "F":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["forest"]

            elif tile_char == "H":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["hill"]

            elif tile_char == "M":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["mountain"]
            
            elif tile_char == "D":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["desert"]

            elif tile_char == "S":
                map_image[y * TILE_SIZE : (y + 1) * TILE_SIZE, x * TILE_SIZE : (x + 1) * TILE_SIZE] = tiles["swamp"]

    imwrite(str(filename.parent.joinpath("out.png")), map_image)


def replace_image(original_path: Path, old_path: Path, new_path: Path) -> None:
    original_image: MatLike = imread(str(original_path))
    old_image: MatLike = imread(str(old_path))
    new_image: MatLike = imread(str(new_path))
    y: int
    x: int

    for y in range(0, original_image.shape[1], TILE_SIZE):
        for x in range(0, original_image.shape[0], TILE_SIZE):
            if are_equal(original_image[y : y + TILE_SIZE, x : x + TILE_SIZE], old_image):
                original_image[y : y + TILE_SIZE, x : x + TILE_SIZE] = new_image

    imwrite(str(original_path), original_image)


def are_equal(image1: MatLike, image2: MatLike, threshold: float = 0.0001) -> bool:
    if image1.shape != image2.shape:
        return False
        
    # The images are considered equal if the mean squared error (MSE) is very close to 0
    return ((image1 - image2) ** 2).mean() < threshold
