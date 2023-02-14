from PySide6.QtWidgets import QMenuBar, QWidget, QMenu
from commands.file_commands import OpenFiles

class MenuBar(QMenuBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        file_menu = QMenu("&File", self)
        self.addMenu(file_menu)
        file_menu.addAction(OpenFiles(parent, "Open Files"))
        