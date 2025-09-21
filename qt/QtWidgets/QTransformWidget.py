# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import math

from PySide6 import QtCore, QtGui, QtWidgets
from app.core import DEFAULT_FONT, DEFAULT_FONT_SIZE

def quad_points(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float) -> list[QtCore.QPointF]:
    """Convert 4 pairs of x, y coordinates to 4 QPointF"""
    return [QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2), QtCore.QPointF(x3, y3), QtCore.QPointF(x4, y4)]

# TODO: Add ability to set transformed image or video source

# noinspection PyPep8Naming
class QTransformWidget(QtWidgets.QWidget):
    updated = QtCore.Signal()

    def __init__(self, parent=None):

        super(QTransformWidget, self).__init__(parent)

        self.updated.connect(self.updatedEvent)
        self.setMouseTracking(True)
        self.setContextMenuPolicy(QtGui.Qt.ContextMenuPolicy.CustomContextMenu)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        self.menu = QtWidgets.QMenu("Coverage", self)

        whole_action = QtGui.QAction('Whole area', self.menu)
        whole_action.triggered.connect(self.wholeTransformation)

        left_action = QtGui.QAction('Left side', self.menu)
        left_action.triggered.connect(self.leftTransformation)

        right_action = QtGui.QAction('Right side', self.menu)
        right_action.triggered.connect(self.rightTransformation)

        center_action = QtGui.QAction('Center', self.menu)
        center_action.triggered.connect(self.centerTransformation)

        self.menu.addAction(left_action)
        self.menu.addAction(right_action)
        self.menu.addAction(whole_action)
        self.menu.addSeparator()
        self.menu.addAction(center_action)

        self.customContextMenuRequested.connect(self.contextMenu)

        screen = QtGui.QGuiApplication.screens()[0]
        self.screen = QtCore.QRect(0, 0, screen.availableSize().width(), screen.availableSize().height())
        self.points = quad_points(0, 0, 0, 0, 0, 0, 0, 0)
        self.wholeTransformation()

        self.mouseX = 0
        self.mouseY = 0
        self.mouseHold = False
        self.mouseHoldX = 0
        self.mouseHoldY = 0

        self.x = 0
        self.y = 0
        self.scale = 1
        self.pointIndex = -1

        self.font = QtGui.QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        self.text = ""

    def contextMenu(self, event):

        self.menu.exec_(self.mapToGlobal(event))

    def paintEvent(self, event):

        # TODO: Use theme colors
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.TextAntialiasing)

        painter.fillRect(event.rect(), QtGui.QColor("#626364"))

        rect = event.rect()
        scale = min(rect.width() / self.screen.width(), rect.height() / self.screen.height()) * 0.9

        w = self.screen.width() * scale
        h = self.screen.height() * scale

        x = (rect.width() - w) / 2
        y = (rect.height() - h) / 2

        self.x = x
        self.y = y
        self.scale = scale

        painter.fillRect(QtCore.QRectF(x, y, w, h), QtGui.QColor("#000000"))

        painter.setPen(QtGui.QColor("#d6d6d6"))
        painter.setBrush(QtGui.QColor("#111111"))

        points = []

        for point in self.points:
            points.append(self.mapToWidget(point))

        painter.drawPolygon(QtGui.QPolygonF(points))

        painter.setPen(QtGui.QColor("#8a9fbb"))
        painter.setBrush(QtGui.QColor("#8a9fbb"))

        for point in points:
            painter.drawEllipse(point, 4, 4)

        painter.setPen(QtGui.QColor("#e6e6e6"))
        painter.setFont(self.font)
        painter.drawText(event.rect(), QtGui.Qt.AlignmentFlag.AlignCenter | QtGui.Qt.TextFlag.TextWordWrap, self.text)

        painter.end()

    def mousePressEvent(self, event):
        self.mouseHold = True
        index = 0

        for point in self.points:
            point = self.mapToWidget(point)

            if math.sqrt(pow(point.x() - event.x(), 2) + pow(point.y() - event.y(), 2)) <= 5:
                self.pointIndex = index
                self.mouseHoldX = event.x() - point.x()
                self.mouseHoldY = event.y() - point.y()

            index = index + 1

    def mouseReleaseEvent(self, event):
        self.mouseHold = False
        self.pointIndex = -1

    def mouseMoveEvent(self, event):
        self.mouseX = event.x()
        self.mouseY = event.y()

        if self.pointIndex >= 0:
            point = self.mapToScreen(QtCore.QPointF(event.x() - self.x, event.y() - self.y))

            self.text = "(%d, %d)" % (point.x(), point.y())
            self.points[self.pointIndex] = point

            self.updated.emit()
        else:
            self.text = ""

        self.update()

    def mapToWidget(self, point):

        return QtCore.QPointF(self.x + self.scale * point.x(), self.y + self.scale * point.y())

    def mapToScreen(self, point):

        return QtCore.QPointF(point.x() * (1 / self.scale), point.y() * (1 / self.scale))

    def centerTransformation(self):

        w = self.screen.width()
        h = self.screen.height()
        min_x = w
        min_y = h
        max_x = 0
        max_y = 0

        for point in self.points:
            if point.x() < min_x:
                min_x = point.x()

            if point.y() < min_y:
                min_y = point.y()

            if point.x() > max_x:
                max_x = point.x()

            if point.y() > max_y:
                max_y = point.y()

        x = w / 2 - (max_x - min_x) / 2
        y = h / 2 - (max_y - min_y) / 2

        index = 0

        for point in self.points:
            point.setX(point.x() - min_x + x)
            point.setY(point.y() - min_y + y)

            self.points[index] = point
            index = index + 1

        self.updated.emit()
        self.update()

    def wholeTransformation(self):
        """
        Fill the whole screen
        """

        w = self.screen.width()
        h = self.screen.height()
        self.points = quad_points(0, 0, w, 0, w, h, 0, h)
        self.updated.emit()
        self.update()

    def leftTransformation(self):
        """
        Fill the left side of the screen
        """

        w = self.screen.width()
        h = self.screen.height()
        self.points = quad_points(0, 0, w / 2, 0, w / 2, h, 0, h)
        self.updated.emit()
        self.update()

    def rightTransformation(self):
        """
        Fill the right side
        """

        w = self.screen.width()
        h = self.screen.height()
        self.points = quad_points(w / 2, 0, w, 0, w, h, w / 2, h)
        self.updated.emit()
        self.update()

    def setScreen(self, screen):

        self.screen = screen
        self.wholeTransformation()

    def getTransform(self):
        t = QtGui.QTransform()
        p = []
        q = [
            QtCore.QPointF(0, 0),
            QtCore.QPointF(self.screen.width(), 0),
            QtCore.QPointF(self.screen.width(), self.screen.height()),
            QtCore.QPointF(0, self.screen.height())]

        for o in self.points:
            a = QtCore.QPointF(o.x(), o.y())
            p.append(a)

        QtGui.QTransform.quadToQuad(QtGui.QPolygonF(q), QtGui.QPolygonF(p), t)

        return t

    def updatedEvent(self):
        pass
