from glob import glob
from cv2 import imread, imwrite
from cv2.typing import MatLike

# Pyquest
try: from constant import *
except: pass
try: from pyquest.constant import *
except: pass


def read_map(filename: str) -> str:
    map: MatLike = imread(filename)
    paths: list[str] = glob(str(DATA_PATH.joinpath("*.png")))
    path: str
    tiles: dict[str, MatLike] = {}

    for path in paths:
        tiles[Path(path).stem] = imread(path)

    y: int
    x: int
    tile: ndarray
    string: str = ""

    for y in range(0, map.shape[1], TILE_SIZE):
        for x in range(0, map.shape[0], TILE_SIZE):
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
