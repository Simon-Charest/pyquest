from pygame import Rect
from typing import Self


class Camera:
    character: Rect
    map_width: int
    map_height: int
    screen_width: int
    screen_height: int

    def __init__(self: Self, character: Rect, map_width: int, map_height: int, screen_width: int, screen_height: int) -> None:
        self.character = character
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self: Self) -> tuple[int, int]:
        # Calculate the position to keep the character centered
        camera_x: int = self.character.x - self.screen_width / 2
        camera_y: int = self.character.y - self.screen_height / 2

        # Ensure the camera doesn't go out of bounds
        camera_x = max(0, min(camera_x, self.map_width - self.screen_width))
        camera_y = max(0, min(camera_y, self.map_height - self.screen_height))

        return (camera_x, camera_y)
