# -*- coding: UTF-8 -*-
"""Replacement for default OS message dialog

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtGui, QtCore, QtWidgets

from app.core.util import OS_LINUX, OS_MAC
import qt.colors as qt_colors


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming
class QPopup(QtWidgets.QDialog):
    """Dialog without title bar and frame, but with rounded corners and pointing triangle"""

    def __init__(self, parent=None):
        super(QPopup, self).__init__(parent)

        self.__close_on_focus_lost = True
        self.__background_color = QtGui.QColor(qt_colors.CONTAINER)
        # Shadow padding
        self.__padding = 12
        # Caret size
        self.__caret_size = 5
        # Caret position relative to a center of dialog
        self.__caret_position = 0
        # Corner roundness
        self.__roundness = 5

        self.setWindowFlags(QtCore.Qt.WindowType.Widget | QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.autoFillBackground = True

        self.installEventFilter(self)

        if not OS_MAC:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setBlurRadius(12)
            effect.setColor(QtGui.QColor(0, 0, 0, 126))
            effect.setOffset(0)

            self.setGraphicsEffect(effect)

        self.setContentsMargins(self.__padding, self.__padding, self.__padding, self.__padding + self.__caret_size)

    def paintEvent(self, event):
        """Draw a dialog"""

        width = self.width()
        height = self.height()
        caret_offset = self.__caret_position

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Clear previous drawing
        painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Source)
        painter.fillRect(self.rect(), QtCore.Qt.GlobalColor.transparent)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceOver)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QColor(255, 0, 0, 127))

        points = [QtCore.QPointF(width / 2 + caret_offset, height - self.__padding),
                  QtCore.QPointF(width / 2 - self.__caret_size + caret_offset,
                                 height - self.__caret_size - self.__padding),
                  QtCore.QPointF(width / 2 + self.__caret_size + caret_offset,
                                 height - self.__caret_size - self.__padding)]
        triangle = QtGui.QPolygonF(points)

        rounded_rect = QtGui.QPainterPath()
        rounded_rect.addRoundedRect(self.__padding, self.__padding,
                                    width - self.__padding * 2,
                                    height - self.__caret_size - self.__padding * 2,
                                    self.__roundness, self.__roundness)
        rounded_rect.addPolygon(triangle)

        painter.setOpacity(1)
        painter.fillPath(rounded_rect, QtGui.QBrush(self.__background_color))

        painter.restore()
        painter.end()

    def eventFilter(self, target, event):
        """Close a dialog when focus is lost"""

        flag = self.__close_on_focus_lost
        type_ = event.type()

        if flag and type_ == QtCore.QEvent.Type.WindowDeactivate:
            self.hide()
            return True

        # Workaround for linux
        if flag and type_ == QtCore.QEvent.Type.Leave and OS_LINUX:
            self.hide()
            return True

        return super().eventFilter(target, event)

    def sizeHint(self):
        """Default minimum size"""

        return QtCore.QSize(300, 300)

    def closeOnFocusLost(self, value):
        """Close a dialog when it looses focus

        Args:
            value (bool): close this dialog when it looses focus or not
        """

        self.__close_on_focus_lost = value

    def showAt(self, point):
        """Show dialog tip at a given point

        Args:
            point (QPoint): point to show at
        """

        self.show()
        self.raise_()

        screen = QtWidgets.QApplication.primaryScreen().geometry()
        location = QtCore.QPoint(point.x() - self.width() / 2, point.y() - self.height() + 12)

        # calculate point location inside current screen
        if location.x() <= screen.x():
            location.setX(screen.x())
            self.__caret_position = -self.width() / 2 + self.__padding + self.__caret_size * 2
        elif location.x() + self.width() >= screen.x() + screen.width():
            location.setX(screen.x() + screen.width() - self.width())
            self.__caret_position = self.width() / 2 - self.__padding - self.__caret_size * 2
        else:
            self.__caret_position = 0

        self.move(location.x(), location.y())

    def setBackgroundColor(self, color):
        """Set a color of a whole dialog

        Args:
            color (QColor): background color of widget
        """

        self.__background_color = color
