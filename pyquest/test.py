"""
Usage:
python pyquest/test.py
"""

from datetime import datetime
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QStatusBar, QToolBar, QVBoxLayout, QWidget
from pygame import Surface, init
from pygame.draw import circle
from pygame.event import Event
from sys import argv, exit as sys_exit
from typing import Self

TITLE: str = "Pyquest"
WIDTH: int = 800
HEIGHT: int = 600
FORMAT: str = "%Y-%m-%d %H:%M:%S"


class PygameWidget(QWidget):
    pygame_screen: Surface
    timer: QTimer
    pixmap: QPixmap

    def __init__(self: Self, parent: QWidget=None):
        super().__init__(parent)
        self.init_pygame()
        self.pixmap = QPixmap(self.size())

    def init_pygame(self: Self):
        # Initialize Pygame
        init()
        self.pygame_screen = Surface((640, 480)).convert(32)

        # Set a timer to update the Pygame content
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pygame)
        self.timer.start(16)  # Update at ~60 FPS

    def update_pygame(self: Self):
        # Fill the Pygame surface with a color
        self.pygame_screen.fill((255, 0, 0))  # Example: Red background

        # Draw a circle
        circle(self.pygame_screen, (0, 255, 0), (320, 240), 50)

        # Convert the Pygame surface to a QImage and display it
        data: bytes = self.pygame_screen.get_view("1")
        image: QImage = QImage(data, 640, 480, QImage.Format.Format_RGB32)
        self.set_pixmap(QPixmap.fromImage(image))

    def set_pixmap(self: Self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.update()

    def paintEvent(self: Self, event: Event):
        painter: QPainter = QPainter(self)
    
        if self.pixmap:
            painter.drawPixmap(self.rect(), self.pixmap)


class MainWindow(QMainWindow):
    pygame_widget: PygameWidget
    
    def __init__(self: Self):
        super().__init__()

        # Create central widget
        self.pygame_widget = PygameWidget(self)
        self.setCentralWidget(self.pygame_widget)
        self.setWindowTitle(TITLE)
        self.resize(WIDTH, HEIGHT)

        # Create layouts
        toolbar_widget: QWidget = QWidget()
        toolbar_layout: QHBoxLayout = QHBoxLayout(toolbar_widget)
        main_layout: QVBoxLayout = QVBoxLayout()
        
        # Set central widget layout
        self.pygame_widget.setLayout(main_layout)

        # Create widgets
        toolbar: QToolBar = QToolBar("Toolbar", self)
        toolbar.addWidget(toolbar_widget)

        status_bar: QStatusBar = QStatusBar()
        self.message = QLabel()
        status_bar.addWidget(self.message)
        self.setStatusBar(status_bar)
        
        # Add widgets to layouts
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        toolbar_layout.addStretch()

        # Launch events
        self.message.setText(timestamp("Ready."))


def timestamp(string: str, format: str = FORMAT) -> str:
    return f"[{datetime.now().strftime(format)}] {string}"


if __name__ == "__main__":
    application: QApplication = QApplication(argv)
    main_window: MainWindow = MainWindow()
    main_window.show()
    sys_exit(application.exec())
