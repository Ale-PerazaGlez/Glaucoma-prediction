from .. import Command
from os import path, walk, sep
from PySide6.QtWidgets import QWidget, QMainWindow, QFileDialog
from PySide6.QtCore import QDir
from PySide6.QtGui import QPixmap
from image_controller import ImageController
from save_to_file import SaveToFile


class OpenFiles(Command):
    def __init__(self, parent: QWidget, command_name: str):
        super().__init__(parent, command_name)
        self.parent = parent
        self.image_path_queue = []
        self.current_clicks_data = []

    def run(self, main_window: QMainWindow):
        self.main_window = main_window
        image_formats = [".png", ".PNG", ".jpg", ".jpeg", ".bmp", ".tif"]
        dir = QFileDialog.getExistingDirectory(None, "Open Directory",
                                               "/home",
                                               QFileDialog.ShowDirsOnly
                                               | QFileDialog.DontResolveSymlinks)
        self.image_path_queue = []
        self.current_clicks_data = []
        dir = QDir.toNativeSeparators(dir)
        file_list = [path.join(sep, dp, f) for dp, _, fn in walk(
            path.expanduser(dir)) for f in fn]
        image_files = filter(lambda file: path.splitext(file)[
                             1] in image_formats, file_list)
        self.image_path_queue = list(
            map(lambda image: path.join(dir, image), image_files))

        self.save_to_file = SaveToFile(self.main_window)
        self.main_window.takeCentralWidget()
        
        self.nextImage([])

    def nextImage(self, click_list):
        if (click_list):
            click_list.append(self.image_path_queue[0])
            self.save_to_file.save_clicks_content(click_list)
            self.image_path_queue.pop(0)
        if self.image_path_queue:
            current_image_path = self.image_path_queue[0]
            self.createImage(current_image_path)

    def createImage(self, pixmap: QPixmap):
        label = ImageController(self.parent, pixmap)
        label.three_clicks.connect(self.nextImage)
        self.main_window.setCentralWidget(label)
