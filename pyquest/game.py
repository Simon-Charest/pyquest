from pygame import K_DOWN, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_s, K_w, QUIT, Rect, Surface, init, quit as pygame_quit
from pygame.display import flip, set_caption, set_mode
from pygame.event import get
from pygame.image import load
from pygame.key import ScancodeWrapper, get_pressed
from pygame.event import Event
from pygame.time import delay, get_ticks
from sys import exit as sys_exit

# Pyquest
from constant import *
from camera import Camera

def run_game() -> None:
    # Initialize Pygame
    init()

    # Set up the display
    WIDTH: int = 800
    HEIGHT: int = 600
    screen: Surface = set_mode((WIDTH, HEIGHT))
    set_caption("Dragon Quest")

    # Load the map image
    map_image: Surface = load(DATA_PATH.joinpath("map.png")).convert()

    # Load the character sprite
    character_images: list[Surface] = [
        load(DATA_PATH.joinpath("alef1.png")).convert_alpha(),
        load(DATA_PATH.joinpath("alef2.png")).convert_alpha()
    ]
    character_rect: Rect = character_images[0].get_rect()
    character_rect.center = (WIDTH // 2, HEIGHT // 2)  # Starting position of the character

    # Define some colors
    WHITE: tuple[int, int, int] = (255, 255, 255)

    # Main game loop
    running: bool = True

    # Camera setup
    camera: Camera = Camera(character_rect, map_image.get_width(), map_image.get_height(), WIDTH, HEIGHT)

    # Character animation variables
    sprite_index: int = 0
    last_sprite_change: int = get_ticks()
    sprite_change_interval: int = 200  # milliseconds
    event: Event
    keys: ScancodeWrapper
    current_time: int
    camera_x: int
    camera_y: int

    while running:
        # Event handling
        for event in get():
            if event.type == QUIT:
                running = False

        # Character movement controls
        keys = get_pressed()

        if keys[K_LEFT] or keys[K_a]:
            character_rect.x -= 5

        if keys[K_RIGHT] or keys[K_d]:
            character_rect.x += 5

        if keys[K_UP] or keys[K_w]:
            character_rect.y -= 5
            
        if keys[K_DOWN] or keys[K_s]:
            character_rect.y += 5

        # Ensure character stays within the screen boundaries
        character_rect.x = max(0, min(WIDTH - character_rect.width, character_rect.x))
        character_rect.y = max(0, min(HEIGHT - character_rect.height, character_rect.y))

        # Check if any arrow key is held down
        if any(keys[key] for key in [K_LEFT, K_RIGHT, K_UP, K_DOWN]):
            # Check if it's time to change the character sprite
            current_time = get_ticks()
            if current_time - last_sprite_change >= sprite_change_interval:
                # Switch the sprite
                sprite_index = (sprite_index + 1) % len(character_images)
                last_sprite_change = current_time

        # Update camera position
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
