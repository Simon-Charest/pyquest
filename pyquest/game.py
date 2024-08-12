"""
Usage:
python pyquest [-c] -m
TODO: Fix collision detection with bridges.
"""

from pathlib import Path
from pygame import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_s, K_w, QUIT, Rect, Surface, init, quit as pygame_quit
from pygame.display import flip, set_caption, set_mode
from pygame.event import Event, get
from pygame.image import load
from pygame.key import ScancodeWrapper, get_pressed
from pygame.time import delay, get_ticks
from sys import exit as sys_exit

# Pyquest
from utils import write_map
from camera import Camera

WIDTH: int = 800
HEIGHT: int = 600
STEP: int = 1  # Default: 1
MILLISECONDS: int = 0  # Default: 5
KEYS: dict[str, list[int]] = {
    "quit": [K_ESCAPE],
    "left": [K_LEFT, K_a],
    "right": [K_RIGHT, K_d],
    "up": [K_UP, K_w],
    "down": [K_DOWN, K_s]
}
MARGIN: int = 2  # Default: 0
DATA: Path = Path(__file__).parent.joinpath("data")
STRING_MAP: Path = DATA.joinpath("map.txt")
IMAGE_MAP: Path = DATA.joinpath("map.png")
TILE: Path = DATA.joinpath("tile")
TILES: Path = TILE.joinpath("*.png")
OBSTACLES: list[Path] = list(map(TILE.joinpath, ["mountain.png", "wall.png", "water.png"]))
CHARACTER: list[Path] = list(map(DATA.joinpath, ["alef1.png", "alef2.png"]))

def run_game() -> None:
    # Initialize Pygame
    init()

    # Set up the display
    set_caption("Dragon Quest")
    screen: Surface = set_mode((WIDTH, HEIGHT))

    # Convert map from characters to bitmap
    string_map: str = open(STRING_MAP).read()
    write_map(string_map, TILES, IMAGE_MAP)

    # Load the map image
    surface_map: Surface = load(IMAGE_MAP).convert()

    obstacle_images: list[Surface] = load_surfaces(OBSTACLES)
    
    # Get the positions of the collidable tiles
    obstacles: list[Rect] = load_obstacles(surface_map, obstacle_images)

    # Load the character sprite
    character_images: list[Surface] = load_surfaces(CHARACTER)
    
    # Starting position of the character
    character_rect: Rect = character_images[0].get_rect()
    character_rect.center = (
        surface_map.get_width() // 2 - 16 * character_images[0].get_width() - character_images[0].get_width() // 2,
        surface_map.get_height() // 2 - 16 * character_images[0].get_height() - character_images[0].get_height() // 2
    )
    
    # Camera setup
    camera: Camera = Camera(character_rect, surface_map.get_width(), surface_map.get_height(), WIDTH, HEIGHT)

    # Character animation variables
    sprite_change_interval: int = 200  # milliseconds
    sprite_index: int = 0
    last_sprite_change: int = get_ticks()
    
    # Main game loop
    running: bool = True

    while running:
        # Event handling
        event: Event

        for event in get():
            if event.type == QUIT:
                running = False

        # Character movement controls
        keys: ScancodeWrapper = get_pressed()

        # Determine potential movement
        new_rect: Rect = character_rect.copy()

        if any(keys[code] for code in KEYS.get("quit", [])):
            break

        # Check for each movement direction separately
        if any(keys[code] for code in KEYS.get("left", [])):
            new_rect.x -= STEP

            if not is_colliding(new_rect, obstacles):
                character_rect.x -= STEP

            new_rect.x += STEP  # Reset to original position after checking

        if any(keys[code] for code in KEYS.get("right", [])):
            new_rect.x += STEP

            if not is_colliding(new_rect, obstacles):
                character_rect.x += STEP

            new_rect.x -= STEP  # Reset to original position after checking

        if any(keys[code] for code in KEYS.get("up", [])):
            new_rect.y -= STEP

            if not is_colliding(new_rect, obstacles):
                character_rect.y -= STEP

            new_rect.y += STEP  # Reset to original position after checking

        if any(keys[code] for code in KEYS.get("down", [])):
            new_rect.y += STEP

            if not is_colliding(new_rect, obstacles):
                character_rect.y += STEP

            new_rect.y -= STEP  # Reset to original position after checking

        # Ensure character stays within the map boundaries
        character_rect.x = max(0, min(surface_map.get_width() - character_rect.width, character_rect.x))
        character_rect.y = max(0, min(surface_map.get_height() - character_rect.height, character_rect.y))

        # Update camera position based on character's position
        camera_x: int
        camera_y: int
        camera_x, camera_y = camera.update(character_rect)

        # Check if any arrow key is held down
        if any(keys[key] for key in [key for keys in KEYS.values() for key in keys]):
            # Check if it's time to change the character sprite
            current_time: int = get_ticks()

            if current_time - last_sprite_change >= sprite_change_interval:
                # Switch the sprite
                sprite_index = (sprite_index + 1) % len(character_images)
                last_sprite_change = current_time

        # Render everything onto the screen
        screen.blit(surface_map, (-camera_x, -camera_y))  # Draw the map with camera offset
        screen.blit(character_images[sprite_index], (character_rect.x - camera_x, character_rect.y - camera_y))  # Draw the character with camera offset
        flip()

        # Add a slight delay to control frame rate
        delay(MILLISECONDS)

    pygame_quit()
    sys_exit()


def load_surfaces(images: list[Path]) -> list[Surface]:
    image: Path
    surfaces: list[Surface] = []
    
    for image in images:
        surfaces.append(load(image).convert_alpha())

    return surfaces


def load_obstacles(map_image: Surface, obstacle_images: list[Surface]) -> list[Rect]:
    obstacle_image: Surface
    obstacles: list[Rect] = []

    for obstacle_image in obstacle_images:
        # Get the size of the tile
        obstacle_width: int
        obstacle_height: int
        obstacle_width, obstacle_height = obstacle_image.get_size()

        # Loop through the map image to find positions of the collidable tiles
        x: int
        
        for x in range(0, map_image.get_width(), obstacle_width):
            y: int

            for y in range(0, map_image.get_height(), obstacle_height):
                # Create a sub-surface of the current tile in the map image
                sub_surface: Surface = map_image.subsurface((x, y, obstacle_width, obstacle_height))
                
                if sub_surface.get_at((0, 0)) == obstacle_image.get_at((0, 0)):  # Check if tile matches
                    obstacles.append(Rect(x, y, obstacle_width, obstacle_height))
    
    return obstacles


def is_colliding(obj: Rect, obstacles: list[Rect], margin: int = MARGIN) -> bool:
    obstacle: Rect

    # Shrink the object's rect by a small margin to create some space around it
    shrunk_object: Rect = obj.inflate(-margin, -margin)
    
    for obstacle in obstacles:
        if shrunk_object.colliderect(obstacle):
            return True
        
    return False
