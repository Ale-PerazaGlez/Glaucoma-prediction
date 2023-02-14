from PySide6.QtWidgets import (QDialog, QWidget, QFormLayout, QPushButton,
                               QFileDialog, QLabel, QLineEdit, QVBoxLayout,
                               QDialogButtonBox, QMessageBox)
from json import dump, load
from os import path
from message import MessageBox


class SaveToFile(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setWindowTitle("Choose output file")
        self.layout = QVBoxLayout()
        self.setup()
        self.setLayout(self.layout)
        self.exec()

    def setup(self):
        form = QWidget(self)
        form_layout = QFormLayout()
        output_directory_label = QLabel('Select an output directory')
        self.directory_path = QLineEdit()
        self.directory_path.setReadOnly(True)
        form_layout.addRow(output_directory_label, self.directory_path)
        directory_browser = QPushButton('Directory Browser')
        directory_browser.setObjectName('BrowserButton')
        directory_browser.pressed.connect(lambda: self.directory_path.setText(
            QFileDialog.getExistingDirectory(None, "Choose output directory",
                                             "/home",
                                             QFileDialog.ShowDirsOnly
                                             | QFileDialog.DontResolveSymlinks) or self.directory_path.text()
        ))
        form_layout.addWidget(directory_browser)

        output_file_label = QLabel('Type the output file name')
        self.output_file_field = QLineEdit(self)

        form_layout.addRow(output_file_label, self.output_file_field)
        form.setLayout(form_layout)
        self.layout.addWidget(form)

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(buttonBox)

    def accept(self):
        self.output_file_path = path.join(self.directory_path.text(),
                                          self.output_file_field.text())
        message = MessageBox(self)

        if path.splitext(self.output_file_path)[1] != '.json':
            message.setup(QMessageBox.Ok,
                          "The given file format needs to be JSON",
                          QMessageBox.Critical)
            message.exec()
            return

        output_file = ''

        # Try opening to check if the directory is valid
        try:
            output_file = open(self.output_file_path, "r+")
        except (OSError, IOError):
            message.setup(QMessageBox.Ok,
                          "Could not access the given file",
                          QMessageBox.Critical)
            message.exec()
            return

        message.setup(QMessageBox.Ok,
                      "File set correctly",
                      QMessageBox.Information)
        message.exec()
        output_file.close()

        self.done(0)

    def save_clicks_content(self, clicks_data):
        output_file = ''
        try:
            output_file = open(self.output_file_path, "r+")
        except (OSError, IOError):
            print('The given output file could not be opened')
            return
        file_data = load(output_file)
        current_file_path = clicks_data[-1]

        indices = [index for (index, image) in enumerate(
            file_data) if image[-1] == current_file_path]

        if len(indices) == 0:
            file_data.append(clicks_data)
        elif len(indices) == 1:
            file_data[indices[0]] = clicks_data
        else:
            print('The given json file has more than one click data for the same path')
            return

        output_file.truncate(0)
        output_file.seek(0)
        dump(file_data, output_file, indent=4)
        output_file.close()
