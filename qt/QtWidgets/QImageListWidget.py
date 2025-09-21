# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtCore, QtGui, QtWidgets


class QImageListWidget(QtWidgets.QListWidget):
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)
    fileDropped = QtCore.Signal(QtCore.QUrl)

    def __init__(self, parent=None):
        super(QImageListWidget, self).__init__(parent)

        size = QtCore.QSize(128, 128)

        self.setSpacing(0)
        self.setIconSize(size)
        self.setSortingEnabled(True)
        self.setUniformItemSizes(False)
        self.setContentsMargins(0, 0, 0, 0)
        self.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.setAttribute(QtGui.Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(QtGui.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def keyPressEvent(self, event):
        self.keyPressed.emit(event)

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            QtWidgets.QListWidget.dragEnterEvent(self, event)

    def dragMoveEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            QtWidgets.QListWidget.dragMoveEvent(self, event)

    def dropEvent(self, event):

        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()

            if urls:
                for url in urls:
                    self.fileDropped.emit(url)

            event.acceptProposedAction()

        QtWidgets.QListWidget.dropEvent(self, event)
