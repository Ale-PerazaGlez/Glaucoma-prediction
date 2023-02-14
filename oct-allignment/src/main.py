from PySide6.QtWidgets import QApplication, QMainWindow
from menu_bar import MenuBar

app = QApplication([])
window = QMainWindow()
window.show()
window.setWindowTitle("OCT-Allignment")
window.setGeometry(120, 100, 100, 100)
window.setMenuBar(MenuBar(window))

app.exec()
