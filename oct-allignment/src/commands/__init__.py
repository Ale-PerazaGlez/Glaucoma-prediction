from PySide6.QtWidgets import QWidgetAction, QWidget, QMainWindow

class Command(QWidgetAction):
    def __init__(self, parent: QWidget, command_name: str):
        super().__init__(parent)
        self.setText(command_name)
        self.triggered.connect(lambda: self.run(parent))
    
    def run(self, main_window: QMainWindow):
        print("Error. Trying to execute a base command")
      
    