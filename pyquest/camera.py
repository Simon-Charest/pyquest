class Camera:
    def __init__(self, character, map_width, map_height, screen_width, screen_height):
        self.character = character
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        # Calculate the position to keep the character centered
        camera_x = self.character.x - self.screen_width / 2
        camera_y = self.character.y - self.screen_height / 2

        # Ensure the camera doesn't go out of bounds
        camera_x = max(0, min(camera_x, self.map_width - self.screen_width))
        camera_y = max(0, min(camera_y, self.map_height - self.screen_height))

        return (camera_x, camera_y)
