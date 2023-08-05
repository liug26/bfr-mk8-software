from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRectF
import globalfonts as gf


WIDTH = 240


class LambdaDisplay(QWidget):
    def __init__(self, parent=None):
        super(LambdaDisplay, self).__init__(parent)

        label = QLabel(self)
        label.setText("Lambda")
        label.setStyleSheet(gf.FONT_CSS + gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.scaled_css_size(45))
        label.setGeometry(0, 50, WIDTH, 40)
        label.setAlignment(Qt.AlignCenter)

        self.lambd = QLabel(self)
        self.lambd.setText("N")
        self.lambd.setStyleSheet(gf.FONT_CSS + gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.scaled_css_size(100))
        self.lambd.setGeometry(0, 55, WIDTH, 200)
        self.lambd.setAlignment(Qt.AlignCenter)

        self.obsolete = False

    def paintEvent(self, e):
        # paint the border
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(182, 182, 182, 255), 5, Qt.SolidLine))
        painter.drawRoundedRect(QRectF(0, 0, self.width(), self.height()), 40, 40)

    def set_obsolete(self, obsolete):
        if obsolete and not self.obsolete:
            self.lambd.setStyleSheet(gf.FONT_CSS + gf.OBSOLETE_COLOR_CSS + gf.TRANSPARENT_CSS + gf.scaled_css_size(250))
        elif not obsolete and self.obsolete:
            self.lambd.setStyleSheet(gf.FONT_CSS + gf.WHITE_CSS + gf.TRANSPARENT_CSS + gf.scaled_css_size(250))
        self.obsolete = obsolete

    def update_value(self, value):
        value = round(value, 2)
        self.lambd.setText(str(value))
