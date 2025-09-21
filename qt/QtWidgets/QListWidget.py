# -*- coding: UTF-8 -*-
"""Custom list widget

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtWidgets, QtCore


class QListWidget(QtWidgets.QListWidget):
    """Simple list widget"""

    def __init__(self, parent=None):
        super(QListWidget, self).__init__(parent)

        self.setAlternatingRowColors(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)

        self._scrollbar_original = self.verticalScrollBar()
        self._scrollbar = QtWidgets.QScrollBar(QtCore.Qt.Orientation.Vertical, self)
        self._scrollbar.valueChanged.connect(self._scrollbar_original.setValue)
        self._scrollbar_original.valueChanged.connect(self._scrollbar.setValue)

        self._update_scrollbar()

    def _update_scrollbar(self):
        """Update a custom scrollbar"""

        original = self._scrollbar_original

        if original.value() == original.maximum() and original.value() == 0:
            self._scrollbar.hide()
        else:
            self._scrollbar.show()

        self._scrollbar.setPageStep(original.pageStep())
        self._scrollbar.setRange(original.minimum(), original.maximum())
        self._scrollbar.resize(8, self.rect().height())
        self._scrollbar.move(self.rect().width() - 8, 0)

    def paintEvent(self, event):
        """Redraw a widget"""

        QtWidgets.QListWidget.paintEvent(self, event)

        self._update_scrollbar()
