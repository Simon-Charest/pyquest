"""
Usage:
python pyquest -m
"""

import random
import json
from pathlib import Path
from pygame import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_a, K_d, K_f, K_r, K_s, K_w, QUIT, KEYDOWN, Rect, Surface, init, quit as pygame_quit
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
MILLISECONDS: int = 5  # Default: 5
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

# Encounter system constants
ENCOUNTER_CHANCE: float = 0.02  # 2% chance per step
ENCOUNTER_STEPS: int = 10  # Steps between encounter checks


def run_game() -> None:
    # Initialize Pygame
    init()

    # Set up the display
    set_caption("Dragon Quest")
    screen: Surface = set_mode((WIDTH, HEIGHT))

    # Load game data
    enemies_file = DATA.joinpath("enemies.json")
    with open(enemies_file, 'r') as f:
        enemies = json.load(f)
    
    hero_file = DATA.joinpath("hero.json")
    with open(hero_file, 'r') as f:
        hero = json.load(f)

    # Convert map from characters to bitmap
    string_map: str = open(STRING_MAP).read()
    write_map(string_map, TILES, IMAGE_MAP)

    # Load the map image
    surface_map: Surface = load(IMAGE_MAP).convert()

    obstacle_images: list[Surface] = load_surfaces(OBSTACLES)
    
    # Get the positions of the collidable tiles (pass string_map to skip bridges)
    obstacles: list[Rect] = load_obstacles(surface_map, obstacle_images, string_map)

    # Load the character sprite
    character_images: list[Surface] = load_surfaces(CHARACTER)
    
    # Starting position of the character (castle position)
    character_rect: Rect = character_images[0].get_rect()
    castle_x = surface_map.get_width() // 2 - 16 * character_images[0].get_width() - character_images[0].get_width() // 2
    castle_y = surface_map.get_height() // 2 - 16 * character_images[0].get_height() - character_images[0].get_height() // 2
    character_rect.center = (castle_x, castle_y)
    
    # Camera setup
    camera: Camera = Camera(character_rect, surface_map.get_width(), surface_map.get_height(), WIDTH, HEIGHT)

    # Character animation variables
    sprite_change_interval: int = 200  # milliseconds
    sprite_index: int = 0
    last_sprite_change: int = get_ticks()
    
    # Encounter system variables
    encounter_timer: int = 0
    game_state: str = "exploring"  # "exploring" or "fighting"
    current_enemy = None
    
    # Main game loop
    running: bool = True

    while running:
        # Event handling
        for event in get():
            if event.type == QUIT:
                running = False
            elif game_state == "fighting" and event.type == KEYDOWN:
                if event.key == K_f:  # Fight command
                    # Implement fight logic here
                    if current_enemy:
                        # Simple damage calculation
                        hero_attack = hero['level']['str'] // 2 + (hero['weapon']['atk'] if hero['weapon'] else 0)
                        damage = random.randint(0, hero_attack)
                        damage = max(0, damage - current_enemy['def'])
                        
                        if damage > 0:
                            current_enemy['hp'] -= damage
                            print(f"You deal {damage} damage to {current_enemy['name']}!")
                            
                            if current_enemy['hp'] <= 0:
                                # Enemy defeated
                                hero['xp'] += current_enemy['xp']
                                hero['gp'] += current_enemy['gp']
                                print(f"You defeated {current_enemy['name']}! Gained {current_enemy['xp']} XP and {current_enemy['gp']} gold.")
                                
                                # Check for level up
                                if hero['xp'] >= hero['level']['xp_next']:
                                    print("Level up!")
                                    # Load levels data for level up logic
                                    levels_file = DATA.joinpath("levels.json")
                                    with open(levels_file, 'r') as f:
                                        levels = json.load(f)
                                    # Find next level
                                    next_level = None
                                    for level in levels:
                                        if level['xp_next'] > hero['level']['xp_next']:
                                            next_level = level
                                            break
                                    if next_level:
                                        hero['level'] = next_level
                                        print(f"Reached level {hero['level']['lv']}!")
                                
                                # Save hero data
                                with open(hero_file, 'w') as f:
                                    json.dump(hero, f, indent=2)
                                
                                game_state = "exploring"
                                current_enemy = None
                        else:
                            print("Your attack missed!")
                        
                        # Enemy counterattack if still alive
                        if current_enemy and current_enemy['hp'] > 0:
                            enemy_damage = random.randint(0, current_enemy['atk'])
                            hero_defense = hero['level']['agi'] // 2
                            if hero['armor']:
                                hero_defense += hero['armor']['def']
                            if hero['shield']:
                                hero_defense += hero['shield']['def']
                            enemy_damage = max(0, enemy_damage - hero_defense)
                            
                            if enemy_damage > 0:
                                hero['hp'] -= enemy_damage
                                print(f"{current_enemy['name']} deals {enemy_damage} damage to you!")
                                
                                if hero['hp'] <= 0:
                                    print("You have been defeated!")
                                    # Death penalty: lose half gold, reset HP to max
                                    hero['gp'] = hero['gp'] // 2
                                    hero['hp'] = hero['level']['hp_max']
                                    print(f"You lost half your gold! Remaining gold: {hero['gp']}")
                                    print(f"HP restored to maximum: {hero['hp']}")
                                    print("You have been returned to Tantegel Castle!")
                                    # Teleport back to castle
                                    character_rect.center = (castle_x, castle_y)
                                    game_state = "exploring"
                                    current_enemy = None
                                    # Save hero data on death
                                    with open(hero_file, 'w') as f:
                                        json.dump(hero, f, indent=2)
                                else:
                                    # Save hero data after taking damage
                                    with open(hero_file, 'w') as f:
                                        json.dump(hero, f, indent=2)
                            else:
                                print(f"{current_enemy['name']}'s attack missed!")
                    
                elif event.key == K_r:  # Run command
                    if random.random() < 0.5:  # 50% chance to escape
                        print("You successfully escaped!")
                        game_state = "exploring"
                        current_enemy = None
                        # Save hero data
                        with open(hero_file, 'w') as f:
                            json.dump(hero, f, indent=2)
                    else:
                        print("You failed to escape!")
                        # Enemy gets a free attack
                        if current_enemy:
                            enemy_damage = random.randint(0, current_enemy['atk'])
                            hero_defense = hero['level']['agi'] // 2
                            if hero['armor']:
                                hero_defense += hero['armor']['def']
                            if hero['shield']:
                                hero_defense += hero['shield']['def']
                            enemy_damage = max(0, enemy_damage - hero_defense)
                            
                            if enemy_damage > 0:
                                hero['hp'] -= enemy_damage
                                print(f"{current_enemy['name']} deals {enemy_damage} damage during your escape attempt!")
                                
                                if hero['hp'] <= 0:
                                    print("You have been defeated!")
                                    # Death penalty: lose half gold, reset HP to max
                                    hero['gp'] = hero['gp'] // 2
                                    hero['hp'] = hero['level']['hp_max']
                                    print(f"You lost half your gold! Remaining gold: {hero['gp']}")
                                    print(f"HP restored to maximum: {hero['hp']}")
                                    print("You have been returned to Tantegel Castle!")
                                    # Teleport back to castle
                                    character_rect.center = (castle_x, castle_y)
                                    game_state = "exploring"
                                    current_enemy = None
                                    # Save hero data on death
                                    with open(hero_file, 'w') as f:
                                        json.dump(hero, f, indent=2)
                                else:
                                    # Save hero data after taking damage
                                    with open(hero_file, 'w') as f:
                                        json.dump(hero, f, indent=2)
                            else:
                                print(f"{current_enemy['name']}'s attack missed!")
                # Other keys during combat are ignored

        # Character movement controls (only when exploring)
        if game_state == "exploring":
            keys: ScancodeWrapper = get_pressed()

            # Determine potential movement
            new_rect: Rect = character_rect.copy()
            moved: bool = False

            if any(keys[code] for code in KEYS.get("quit", [])):
                break

            # Check for each movement direction separately
            if any(keys[code] for code in KEYS.get("left", [])):
                new_rect.x -= STEP

                if not is_colliding(new_rect, obstacles):
                    character_rect.x -= STEP
                    moved = True

                new_rect.x += STEP  # Reset to original position after checking

            if any(keys[code] for code in KEYS.get("right", [])):
                new_rect.x += STEP

                if not is_colliding(new_rect, obstacles):
                    character_rect.x += STEP
                    moved = True

                new_rect.x -= STEP  # Reset to original position after checking

            if any(keys[code] for code in KEYS.get("up", [])):
                new_rect.y -= STEP

                if not is_colliding(new_rect, obstacles):
                    character_rect.y -= STEP
                    moved = True

                new_rect.y += STEP  # Reset to original position after checking

            if any(keys[code] for code in KEYS.get("down", [])):
                new_rect.y += STEP

                if not is_colliding(new_rect, obstacles):
                    character_rect.y += STEP
                    moved = True

                new_rect.y -= STEP  # Reset to original position after checking

            # Ensure character stays within the map boundaries
            character_rect.x = max(0, min(surface_map.get_width() - character_rect.width, character_rect.x))
            character_rect.y = max(0, min(surface_map.get_height() - character_rect.height, character_rect.y))

            # Check for random encounters
            if moved:
                encounter_timer += 1
                if encounter_timer >= ENCOUNTER_STEPS:
                    encounter_timer = 0
                    if random.random() < ENCOUNTER_CHANCE:
                        # Trigger encounter
                        current_enemy = random.choice(enemies)
                        game_state = "fighting"
                        print(f"A {current_enemy['name']} draws near!")

        # Update camera position based on character's position
        camera_x: int
        camera_y: int
        camera_x, camera_y = camera.update(character_rect)

        # Check if any arrow key is held down for sprite animation (only when exploring)
        if game_state == "exploring":
            keys_for_animation = get_pressed()
            if any(keys_for_animation[key] for key in [key for keys_list in KEYS.values() for key in keys_list]):
                # Check if it's time to change the character sprite
                current_time: int = get_ticks()

                if current_time - last_sprite_change >= sprite_change_interval:
                    # Switch the sprite
                    sprite_index = (sprite_index + 1) % len(character_images)
                    last_sprite_change = current_time

        # Render everything onto the screen
        screen.blit(surface_map, (-camera_x, -camera_y))  # Draw the map with camera offset
        screen.blit(character_images[sprite_index], (character_rect.x - camera_x, character_rect.y - camera_y))  # Draw the character with camera offset
        
        # Render combat UI if in fighting state
        if game_state == "fighting" and current_enemy:
            # Simple text overlay for combat
            from pygame.font import Font, init as font_init
            font_init()
            font = Font(None, 36)
            
            # Combat background
            from pygame.draw import rect
            from pygame import Color as PygameColor
            rect(screen, (0, 0, 0), (50, 50, WIDTH-100, HEIGHT-100))
            rect(screen, (255, 255, 255), (50, 50, WIDTH-100, HEIGHT-100), 2)
            
            # Enemy name
            enemy_text = font.render(f"{current_enemy['name']} appears!", True, (255, 255, 255))
            screen.blit(enemy_text, (100, 100))
            
            # Combat options
            fight_text = font.render("F: Fight", True, (255, 255, 255))
            screen.blit(fight_text, (100, 150))
            
            run_text = font.render("R: Run", True, (255, 255, 255))
            screen.blit(run_text, (100, 200))
            
            # Hero and enemy stats
            hero_stats = font.render(f"Hero HP: {hero['hp']}", True, (255, 255, 255))
            screen.blit(hero_stats, (100, 300))
            
            enemy_stats = font.render(f"Enemy HP: {current_enemy['hp']}", True, (255, 255, 255))
            screen.blit(enemy_stats, (100, 350))
            
            # Instructions
            instructions = font.render("Press F to fight or R to run", True, (200, 200, 200))
            screen.blit(instructions, (100, 450))
        
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


def load_obstacles(map_image: Surface, obstacle_images: list[Surface], string_map: str = "") -> list[Rect]:
    obstacle_image: Surface
    obstacles: list[Rect] = []
    
    # Parse bridge positions from the map string
    bridge_positions: set[tuple[int, int]] = set()
    if string_map:
        rows: list[str] = string_map.strip().split("\n")
        for row_idx, row in enumerate(rows):
            for col_idx, char in enumerate(row):
                if char == "B":  # Bridge tile
                    bridge_positions.add((col_idx, row_idx))

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
                # Convert pixel position to tile grid position
                tile_x: int = x // obstacle_width
                tile_y: int = y // obstacle_height
                
                # Skip if this is a bridge position
                if (tile_x, tile_y) in bridge_positions:
                    continue
                
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
