# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from qt import QtCore, QtGui, QtWidgets
from qt.QtWidgets.QLineEdit import QLineEdit


class QSearchEdit(QLineEdit):
    """Basic edit input for search with a clear button"""

    focusOut = QtCore.Signal(QtGui.QFocusEvent)
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)

    def __init__(self, parent=None):
        super(QSearchEdit, self).__init__(parent)

        self.setPlaceholderText("Search...")

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_MacShowFocusRect, False)

        self._ui_clear = QtWidgets.QToolButton(self)
        self._ui_clear.setIconSize(QtCore.QSize(14, 14))
        self._ui_clear.setIcon(QtGui.QIcon(':/qt/close.png'))
        self._ui_clear.setCursor(QtCore.Qt.CursorShape.ArrowCursor)
        self._ui_clear.clicked.connect(self.clear)
        self._ui_clear.hide()

        self.textChanged.connect(self._update)

        frame_width = self.style().pixelMetric(QtWidgets.QStyle.PixelMetric.PM_DefaultFrameWidth)
        size_hint = self.minimumSizeHint()
        btn_size_hint = self._ui_clear.sizeHint()

        self.setMinimumSize(
            max(size_hint.width(), btn_size_hint.height() + frame_width * 2 + 2),
            max(size_hint.height(), btn_size_hint.height() + frame_width * 2 + 2))

        self._update()

    def resizeEvent(self, event):
        """Redraw some elements"""

        self._update()

    def keyPressEvent(self, event):
        """Implements keyPressed signal"""

        # super(QSearchEdit, self).keyPressEvent(event)

        self.keyPressed.emit(event)
        self._update()

    def focusOutEvent(self, event):
        """Focus is lost"""

        super(QSearchEdit, self).focusOutEvent(event)

        self.focusOut.emit(event)

    def _update(self):
        size = self.rect()
        btn_size = self._ui_clear.sizeHint()
        frame_width = self.style().pixelMetric(QtWidgets.QStyle.PixelMetric.PM_DefaultFrameWidth)

        self._ui_clear.setVisible(len(self.text()) > 0)
        self._ui_clear.move(size.width() - btn_size.width() - (frame_width * 2),
                            round((size.height() / 2) - (btn_size.height() / 2)))
