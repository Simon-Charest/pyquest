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

        if any(keys[code] for code in KEYS.get("quit", [])):
            running = False

        if any(keys[code] for code in KEYS.get("left", [])):
            character_rect.x -= SPEED

        if any(keys[code] for code in KEYS.get("right", [])):
            character_rect.x += SPEED

        if any(keys[code] for code in KEYS.get("up", [])):
            character_rect.y -= SPEED
            
        if any(keys[code] for code in KEYS.get("down", [])):
            character_rect.y += SPEED

        # Ensure character stays within the screen boundaries
        character_rect.x = max(0, min(map_image.get_width() - character_rect.width, character_rect.x))
        character_rect.y = max(0, min(map_image.get_height() - character_rect.height, character_rect.y))

        # Check if any arrow key is held down
        if any(keys[key] for key in [key for keys in KEYS.values() for key in keys]):
            # Check if it's time to change the character sprite
            current_time: int = get_ticks()

            if current_time - last_sprite_change >= sprite_change_interval:
                # Switch the sprite
                sprite_index = (sprite_index + 1) % len(character_images)
                last_sprite_change = current_time

        # Update camera position
        camera_x: int
        camera_y: int
        camera_x, camera_y = camera.update()

        # Render everything onto the screen
        screen.fill(WHITE)
        screen.blit(map_image, (-camera_x, -camera_y))  # Draw the map with camera offset
        screen.blit(character_images[sprite_index], (character_rect.x - camera_x, character_rect.y - camera_y))  # Draw the character with camera offset
        flip()

        # Add a slight delay to control frame rate
        delay(10)

    pygame_quit()
    sys_exit()
