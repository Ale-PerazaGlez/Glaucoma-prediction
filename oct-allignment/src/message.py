from PySide6.QtWidgets import QMessageBox, QWidget

class MessageBox(QMessageBox):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def setup(self, button: QMessageBox.StandardButton,
              text: str, info: QMessageBox.Critical):
        self.setStandardButtons(button)
        self.setText(text)
        self.setIcon(info)
