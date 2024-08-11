from pygame import Rect
from typing import Self


class Camera:
    character: Rect
    map_width: int
    map_height: int
    screen_width: int
    screen_height: int
    camera_rect: Rect

    def __init__(self: Self, character: Rect, map_width: int, map_height: int, screen_width: int, screen_height: int) -> None:
        self.character = character
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_rect = Rect(0, 0, screen_width, screen_height)

    def update(self: Self, character: Rect) -> tuple[int, int]:
        # Center the camera on the target object
        self.camera_rect.center = character.center

        # Clamp the camera rect to the bounds of the map
        self.camera_rect.x = max(0, min(self.map_width - self.screen_width, self.camera_rect.x))
        self.camera_rect.y = max(0, min(self.map_height - self.screen_height, self.camera_rect.y))

        # Return the camera's x and y offset
        return self.camera_rect.x, self.camera_rect.y
