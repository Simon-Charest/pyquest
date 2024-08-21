"""
Usage:
python pyquest/test.py
TODO: Fix collision detection with bridges.
"""

from datetime import datetime
from numpy import ndarray, transpose
from pathlib import Path
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QAction, QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QMainWindow, QMenu, QMenuBar, QMessageBox, QPushButton, QStatusBar, QToolBar, QVBoxLayout, QWidget
from pygame import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, NOFRAME, SRCALPHA, K_a, K_d, K_s, K_w, QUIT, Rect, Surface, init, quit as pygame_quit
from pygame.display import flip, iconify, quit, set_caption, set_mode
from pygame.event import Event, get
from pygame.image import load
from pygame.key import ScancodeWrapper, get_pressed
from pygame.surfarray import array3d
from pygame.time import delay, get_ticks
from sys import argv, exit as sys_exit
from typing import Self
from win32api import GetSystemMetrics
from win32con import SM_CXSCREEN, SM_CYSCREEN

# Pyquest
from utils import write_map
from camera import Camera

WINDOW_TITLE: str = "Pyquest"
AUTHOR: str = "SLCIT Inc."
FORMAT: str = "%Y-%m-%d %H:%M:%S"
WIDTH: int = 800
HEIGHT: int = 600
SURFACE_WIDTH: int = 640
SURFACE_HEIGHT: int = 480
DEPTH: int = 32
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


class PygameWidget(QWidget):
    width: int
    height: int
    depth: int
    msec: int
    pixmap: QPixmap
    pygame_surface: Surface
    timer: QTimer
    
    def __init__(self: Self, parent: QWidget = None):
        super().__init__(parent)
        self.width = 640
        self.height = 480
        self.depth = 32
        self.msec = 16  # Update at ~60 FPS
        self.init_pygame()
        self.pixmap = QPixmap(self.size())

    def init_pygame(self: Self):
        # Initialize Pygame
        init()

        # Initialize the display module
        self.display_surface = set_mode((1, 1), NOFRAME)  # Minimal display mode

        # Hide the window (for Windows)
        if GetSystemMetrics(SM_CXSCREEN) > 0 and GetSystemMetrics(SM_CYSCREEN) > 0:
            iconify()  # Minimize the window
            #quit()  # Close the window (but keep Pygame initialized)

        # Create a Pygame Surface
        self.pygame_surface = Surface((self.width, self.height), SRCALPHA, self.depth)

        # Convert map from characters to bitmap
        string_map: str = open(STRING_MAP).read()
        write_map(string_map, TILES, IMAGE_MAP)

        # Load the map image
        map_image: Surface = load(IMAGE_MAP).convert_alpha()
        
        # Copy the loaded map image to our surface
        self.pygame_surface.blit(map_image, (0, 0))

        """TODO: Dev this"""

        # Set a timer to update the Pygame content
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pygame)
        self.timer.start(self.msec)

    def update_pygame(self: Self):
        # Fill the Pygame surface with a color
        #self.pygame_surface.fill((255, 0, 0))  # Example: Red background

        # Draw a circle
        #circle(self.pygame_surface, (0, 255, 0), (320, 240), 50)

        # Convert the Pygame surface to a QImage and display it
        data: bytes = self.pygame_surface.get_view("1")
        image: QImage = QImage(data, self.width, self.height, QImage.Format.Format_RGB32)
        self.set_pixmap(QPixmap.fromImage(image))
    
    def set_pixmap(self: Self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.update()

    def paintEvent(self: Self, event: Event):
        painter: QPainter = QPainter(self)
    
        if self.pixmap:
            painter.drawPixmap(self.rect(), self.pixmap)

    def load_surfaces(self: Self, images: list[Path]) -> list[Surface]:
        image: Path
        surfaces: list[Surface] = []
        
        for image in images:
            surfaces.append(load(image).convert_alpha())

        return surfaces

    def load_obstacles(self: Self, map_image: Surface, obstacle_images: list[Surface]) -> list[Rect]:
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

    def is_colliding(self: Self, obj: Rect, obstacles: list[Rect], margin: int = MARGIN) -> bool:
        obstacle: Rect

        # Shrink the object's rect by a small margin to create some space around it
        shrunk_object: Rect = obj.inflate(-margin, -margin)
        
        for obstacle in obstacles:
            if shrunk_object.colliderect(obstacle):
                return True
            
        return False


class MainWindow(QMainWindow):
    pygame_widget: PygameWidget
    
    def __init__(self: Self):
        super().__init__()

        # Create central widget
        self.pygame_widget = PygameWidget(self)
        self.setCentralWidget(self.pygame_widget)
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(0, 0, WIDTH, HEIGHT)

        # Create layouts
        main_layout: QVBoxLayout = QVBoxLayout()
        
        # Set central widget layout
        self.pygame_widget.setLayout(main_layout)
        
        # Add widgets to layouts
        self.setMenuBar(self.create_menu_bar())
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.create_tool_bar())        
        self.setStatusBar(self.create_status_bar())

    def create_menu_bar(self: Self) -> QMenuBar:
        # Create a menu bar
        menu_bar = QMenuBar()
        
        # Create menus
        file: QMenu = menu_bar.addMenu("File")
        help: QMenu = menu_bar.addMenu("Help")
        
        # Create actions
        exit: QAction = QAction("Exit", self)
        about: QAction = QAction("About", self)

        # Add actions to menu
        file.addAction(exit)
        help.addAction(about)

        # Connect events to functions
        exit.triggered.connect(QApplication.quit)
        about.triggered.connect(self.show_about)

        return menu_bar

    def create_tool_bar(self: Self) -> QToolBar:
        # Create layouts
        tool_bar_widget: QWidget = QWidget()
        tool_bar_layout: QHBoxLayout = QHBoxLayout(tool_bar_widget)

        # Create widgets
        tool_bar: QToolBar = QToolBar("Toolbar", self)
        tool_bar.addWidget(tool_bar_widget)

        load: QPushButton = QPushButton()
        load.setText("Load")

        save: QPushButton = QPushButton()
        save.setText("Save")

        # Add widgets to layouts
        tool_bar_layout.addStretch()  # Push buttons to the right
        #tool_bar_layout.addWidget(self.create_separator())
        tool_bar_layout.addWidget(load)
        tool_bar_layout.addWidget(save)

        # Connect events to functions
        load.clicked.connect(lambda: self.load())
        save.clicked.connect(lambda: self.save())

        return tool_bar

    def create_separator(self: Self) -> QFrame:
        """Create a line separator using QFrame."""
        
        line: QFrame = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        
        return line

    def create_status_bar(self: Self) -> QStatusBar:
        status_bar: QStatusBar = QStatusBar()
        self.message = QLabel()
        status_bar.addWidget(self.message)

        # Launch events
        self.message.setText(self.timestamp("Ready."))
        
        return status_bar
        
    def show_about(self: Self):
        QMessageBox.about(self, f"About {WINDOW_TITLE}", f"© {AUTHOR}. All rights reserved.")

    def load(self: Self) -> None:
        pass

    def save(self: Self) -> None:
        pass

    def timestamp(self: Self, string: str, format: str = FORMAT) -> str:
        return f"[{datetime.now().strftime(format)}] {string}"


def main() -> None:
    application: QApplication = QApplication(argv)
    main_window: MainWindow = MainWindow()
    main_window.show()
    sys_exit(application.exec())


if __name__ == "__main__":
    main()
