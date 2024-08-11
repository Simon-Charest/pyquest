"""
Usage:
python pyquest --map
"""

from pygame import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_s, K_w, QUIT, Rect, Surface, init, quit as pygame_quit
from pygame.display import flip, set_caption, set_mode
from pygame.event import Event, get
from pygame.image import load
from pygame.key import ScancodeWrapper, get_pressed
from pygame.time import delay, get_ticks
from sys import exit as sys_exit

# Pyquest
from camera import Camera
from constant import *

WIDTH: int = 800
HEIGHT: int = 600
SPEED: int = 3
WHITE: tuple[int, int, int] = (255, 255, 255)
KEYS: dict[str, list[int]] = {
    "quit": [K_ESCAPE],
    "left": [K_LEFT, K_a],
    "right": [K_RIGHT, K_d],
    "up": [K_UP, K_w],
    "down": [K_DOWN, K_s]
}


def run_game() -> None:
    # Initialize Pygame
    init()

    # Set up the display
    set_caption("Dragon Quest")
    screen: Surface = set_mode((WIDTH, HEIGHT))

    # Load the map image
    map_image: Surface = load(DATA_PATH.joinpath("map.png")).convert()

    # Load the collidable tile images
    collidable_tiles: list[Surface] = [
        load(DATA_PATH.joinpath("mountain.png")).convert_alpha(),
        load(DATA_PATH.joinpath("water.png")).convert_alpha()
    ]

    # Get the positions of the collidable tiles
    collidable_positions: list = load_collidable_positions(map_image, collidable_tiles)

    # Load the character sprite
    character_images: list[Surface] = [
        load(DATA_PATH.joinpath("alef1.png")).convert_alpha(),
        load(DATA_PATH.joinpath("alef2.png")).convert_alpha()
    ]
    
    # Starting position of the character
    character_rect: Rect = character_images[0].get_rect()
    character_rect.center = (
        map_image.get_width() // 2 - 16 * character_images[0].get_width() - character_images[0].get_width() // 2,
        map_image.get_height() // 2 - 16 * character_images[0].get_height() - character_images[0].get_height() // 2
    )
    
    # Camera setup
    camera: Camera = Camera(character_rect, map_image.get_width(), map_image.get_height(), WIDTH, HEIGHT)

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
            running = False

        if any(keys[code] for code in KEYS.get("left", [])):
            new_rect.x -= SPEED

        if any(keys[code] for code in KEYS.get("right", [])):
            new_rect.x += SPEED

        if any(keys[code] for code in KEYS.get("up", [])):
            new_rect.y -= SPEED
            
        if any(keys[code] for code in KEYS.get("down", [])):
            new_rect.y += SPEED

        # Check for collisions and update character position if no collision
        if not check_collision(new_rect, collidable_positions):
            character_rect = new_rect

        # Ensure character stays within the map boundaries
        character_rect.x = max(0, min(map_image.get_width() - character_rect.width, character_rect.x))
        character_rect.y = max(0, min(map_image.get_height() - character_rect.height, character_rect.y))

        # Update camera position based on character's position
        camera_x: int
        camera_y: int
        camera_x, camera_y = camera.update()

        # Check if any arrow key is held down
        if any(keys[key] for key in [key for keys in KEYS.values() for key in keys]):
            # Check if it's time to change the character sprite
            current_time: int = get_ticks()

            if current_time - last_sprite_change >= sprite_change_interval:
                # Switch the sprite
                sprite_index = (sprite_index + 1) % len(character_images)
                last_sprite_change = current_time

        # Render everything onto the screen
        screen.fill(WHITE)
        screen.blit(map_image, (-camera_x, -camera_y))  # Draw the map with camera offset
        screen.blit(character_images[sprite_index], (character_rect.x - camera_x, character_rect.y - camera_y))  # Draw the character with camera offset
        flip()

        # Add a slight delay to control frame rate
        delay(10)

    pygame_quit()
    sys_exit()


def load_collidable_positions(map_image: Surface, collidable_tiles: list[Surface]) -> list[Rect]:
    collidable_positions: list[Surface] = []
    tile: Surface

    for tile in collidable_tiles:
        # Get the size of the tile
        tile_width: int
        tile_height: int
        tile_width, tile_height = tile.get_size()

        # Loop through the map image to find positions of the collidable tiles
        x: int
        
        for x in range(0, map_image.get_width(), tile_width):
            y: int

            for y in range(0, map_image.get_height(), tile_height):
                # Create a sub-surface of the current tile in the map image
                sub_surface: Surface = map_image.subsurface((x, y, tile_width, tile_height))
                
                if sub_surface.get_at((0, 0)) == tile.get_at((0, 0)):  # Check if tile matches
                    collidable_positions.append(Rect(x, y, tile_width, tile_height))
    
    return collidable_positions


def check_collision(rect: Rect, collidable_positions: list[Rect]) -> bool:
    pos: Rect

    for pos in collidable_positions:
        if rect.colliderect(pos):
            return True
        
    return False
