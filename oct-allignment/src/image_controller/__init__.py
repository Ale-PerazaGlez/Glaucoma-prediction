from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtCore import Signal


class ImageController(QLabel):
    three_clicks = Signal(list)

    def __init__(self, parent: QWidget, image_path: str):
        super().__init__(parent)
        self.image_path = image_path
        self.click_list = []
        pixmap = QPixmap(image_path)
        self.setPixmap(pixmap)
        self.setFixedSize(pixmap.width(), pixmap.height())

    def mousePressEvent(self, ev: QMouseEvent):
        self.click_list.append({'x': ev.x(), 'y': ev.y()})
        if(len(self.click_list) == 3):
            self.three_clicks.emit(self.click_list)
            self.click_list = []
