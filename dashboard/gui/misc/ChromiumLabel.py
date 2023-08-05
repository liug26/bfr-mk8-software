from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
import os


class ChromiumLabel(QLabel):
    toggle_visibility = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, ev):
        self.toggle_visibility.emit(False)
        os.system('chromium-browser')
        self.toggle_visibility.emit(True)
