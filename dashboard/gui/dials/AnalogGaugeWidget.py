#!/usr/bin/env python

###
# Author: Stefan Holstein
# inspired by: https://github.com/Werkov/PyQt4/blob/master/examples/widgets/analogclock.py
# Thanks to https://stackoverflow.com/

# Updated by
########################################################################
# SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinndesign.com
# GitHub : https://github.com/KhamisiKibet
########################################################################


from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPolygon, QPolygonF, QColor, QPen, QFont, QPainter, QFontMetrics, QConicalGradient, QRadialGradient, QFontDatabase
from PyQt5.QtCore import Qt, QPoint, QPointF, QRect, QSize, QObject
import math


class AnalogGaugeWidget(QWidget):
    def __init__(self, parent=None, value_float=False, scale_float=False):
        super(AnalogGaugeWidget, self).__init__(parent)
        # can the value text be a float
        self.value_float = value_float
        # can the scale numbers be floats
        self.scale_float = scale_float
        # if not value has been initialized
        self.null_value = True
        # controls how big the hold around the center is
        # 16 to completely hide the hole, 6 to have a transparent cocentric circle at the center
        self.center_hole_size = 16
        # the larger this number is, the smaller the center knob is
        self.center_size = 8
        # helpful variables to customize gauge widget
        self.NeedleColor = QColor(0, 0, 0, 255)
        self.ScaleValueColor = QColor(0, 0, 0, 255)
        self.DisplayValueColor = QColor(0, 0, 0, 255)
        self.scalaCount = 10
        self.scale_fontsize = 0
        self.value_fontsize = 0
        self.scale_angle_start_value = 135
        self.scale_angle_size = 270
        # import Ubuntu font
        id = QFontDatabase.addApplicationFont(':/res/ubuntu')
        families = QFontDatabase.applicationFontFamilies(id)
        self.scale_fontname = families[0]
        self.value_fontname = families[0]
        # not very helpful variables
        self.value_needle = QObject
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9
        self.scala_subdiv_count = 5
        self.pen = QPen(QColor(0, 0, 0))
        self.scale_polygon_colors = []
        self.text_radius_factor = 0.5
        self.needle_scale_factor = 0.8
        # adapt to different sizes
        self.rescale_method()
        # QPainter(self) = QPainter(self)
        self.generate_polygons()

    # pass in 3 colors: 1st is right outer circle color, 2nd left outer circle color, 3rd inner circle center color
    def setCustomGaugeTheme(self, **colors):
        self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                       [.5, QColor(
                                           str(colors['color2']))],
                                       [.75, QColor(str(colors['color3']))]])

        self.needle_center_bg = [
                                [0, QColor(str(colors['color3']))],
                                [0.322581, QColor(
                                    str(colors['color1']))],
                                [0.571429, QColor(
                                    str(colors['color2']))],
                                [1, QColor(str(colors['color3']))]
        ]

        self.outer_circle_bg = [
            [0.0645161, QColor(str(colors['color3']))],
            [0.36, QColor(
                str(colors['color1']))],
            [1, QColor(str(colors['color2']))]
        ]

    # rescale widget depending on given size
    def rescale_method(self):
        # print("rescale")
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()

        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, int(- self.widget_diameter / 2 * self.needle_scale_factor)),
            QPoint(0, int(- self.widget_diameter /
                   2 * self.needle_scale_factor - 6)),
            QPoint(2, int(- self.widget_diameter / 2 * self.needle_scale_factor))
        ])])
        self.generate_polygons()

    def generate_polygons(self):
        self.outer_circle_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width())),
            (self.widget_diameter / self.center_hole_size),
            self.scale_angle_start_value / 10, 360, False)
        self.filled_polygon_polygon = self.create_polygon_pie(
            ((self.widget_diameter / 2) - (self.pen.width() / 2)) *
            self.gauge_color_outer_radius_factor,
            (((self.widget_diameter / 2) - (self.pen.width() / 2))
             * self.gauge_color_inner_radius_factor),
            self.scale_angle_start_value, self.scale_angle_size)
        self.big_needle_center_point_polygon = self.create_polygon_pie(
            ((self.widget_diameter / self.center_size) - (self.pen.width() / 2)),
            0,
            self.scale_angle_start_value, 360, False)

    # not sure what it does, helper method
    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)

    # called by main update loop, update changes to gui
    def updateValue(self, value, mouse_controlled=False):
        self.null_value = False
        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
        self.update()

    # not sure what it does, helper method
    def set_scale_polygon_colors(self, color_array):
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array is None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph=True):
        polygon_pie = QPolygonF()
        # start = self.scale_angle_start_value
        # start = 0
        # lenght = self.scale_angle_size
        # lenght = 180
        # inner_raduis = self.width()/4
        # print(start)
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # add the points of polygon
        for i in range(lenght + 1):
            t = w * i + start
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        # add the points of polygon
        for i in range(lenght + 1):
            # print("2 " + str(i))
            t = w * (lenght - i) + start
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(
                self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            gauge_rect = QRect(QPoint(0, 0), QSize(
                int(self.widget_diameter / 2 - 1), int(self.widget_diameter - 1)))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value - 1)

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            # grad.setColorAt(.00, Qt.red)
            # grad.setColorAt(.1, Qt.yellow)
            # grad.setColorAt(.15, Qt.green)
            # grad.setColorAt(1, Qt.transparent)
            # self.brush = QBrush(QColor(255, 0, 255, 255))
            # grad.setStyle(Qt.Dense6Pattern)
            # painter_filled_polygon.setBrush(self.brush)
            painter_filled_polygon.setBrush(grad)

            painter_filled_polygon.drawPolygon(self.filled_polygon_polygon)
            # return painter_filled_polygon

    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int((self.widget_diameter / 2) -
                                (self.widget_diameter / 20))
        # print(stepszize)
        for i in range(self.scalaCount + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scale_fontname, int(self.scale_fontsize), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        # jason: allows float scales
        scale_per_div = (float(self.maxValue) - self.minValue) / self.scalaCount

        angle_distance = (float(self.scale_angle_size) /
                          float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            # text = str(int((self.maxValue - self.minValue) / self.scalaCount * i))
            if self.scale_float:
                text = str(float(self.minValue + scale_per_div * i))
            else:
                text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname,
                            int(self.scale_fontsize), QFont.Bold))
            angle = angle_distance * i + \
                float(self.scale_angle_start_value)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)

            painter.drawText(int(x - w / 2), int(y - h / 2), int(w),
                             int(h), Qt.AlignCenter, text)
        # painter.restore()

    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value)
        steps_size = (float(self.scale_angle_size) /
                      float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter // 2
        scale_line_lenght = int(
            (self.widget_diameter / 2) - (self.widget_diameter / 40))
        for i in range((self.scalaCount * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0,
                                scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        # painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        # xShadow = 3.0
        # yShadow = 3.0
        font = QFont(self.value_fontname, int(self.value_fontsize), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        # angle_distance = (float(self.scale_angle_size) / float(self.scalaCount))
        # for i in range(self.scalaCount + 1):
        if self.value_float:
            text = str(round(float(self.value), 1))
        else:
            text = str(int(self.value))
        if self.null_value:
            text = "N"
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname,
                        int(self.value_fontsize), QFont.Bold))

        # Mitte zwischen Skalenstart und Skalenende:
        # Skalenende = Skalenanfang - 360 + Skalenlaenge
        # Skalenmitte = (Skalenende - Skalenanfang) / 2 + Skalenanfang
        angle_end = float(self.scale_angle_start_value +
                          self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / \
            2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        # print(w, h, x, y, text)

        # jason: added '-' in front of x & y to move value text above the center instead of below
        painter.drawText(int(- x - w / 2), int(- y - h / 2), int(w),
                         int(h), Qt.AlignCenter, text)

    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        # painter.setPen(Qt.NoPen)

        # painter.setBrush(self.CenterPointColor)
        # diameter = diameter # self.widget_diameter/6
        # painter.drawEllipse(int(-diameter / 2), int(-diameter / 2), int(diameter), int(diameter))

        grad = QConicalGradient(QPointF(0, 0), 0)

        # todo definition scale color as array here
        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        # grad.setColorAt(.00, Qt.red)
        # grad.setColorAt(.1, Qt.yellow)
        # grad.setColorAt(.15, Qt.green)
        # grad.setColorAt(1, Qt.transparent)
        painter.setBrush(grad)
        # self.brush = QBrush(QColor(255, 0, 255, 255))
        # painter_filled_polygon.setBrush(self.brush)

        painter.drawPolygon(self.big_needle_center_point_polygon)
        # return painter_filled_polygon

    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])

        painter.setBrush(radialGradient)

        painter.drawPolygon(self.outer_circle_polygon)

    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    def resizeEvent(self, event):
        self.rescale_method()

    # paint event, called every main update loop, runs rather slow
    # rpm dial: 5-6ms, speed & lambda dial: 3ms
    def paintEvent(self, event):
        # inside of the pie - removing this adds about 15fps on my laptop, when it's unplugged - randall
        self.draw_outer_circle()

        # colored pie area - removing this adds about 10fps on my laptop, when it's unplugged - randall
        self.draw_filled_polygon()

        # draw scale marker lines
        self.create_fine_scaled_marker()
        self.draw_big_scaled_marker()

        # draw scale marker value text
        self.create_scale_marker_values_text()

        # Display Value
        self.create_values_text()

        # draw needle 1
        self.draw_needle()

        # Draw Center Point - removing this adds about 5fps on my laptop, when it's unplugged - randall
        self.draw_big_needle_center_point(diameter=(self.widget_diameter / 6))

        pass
