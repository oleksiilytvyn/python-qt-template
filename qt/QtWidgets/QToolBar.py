# -*- coding: UTF-8 -*-
"""Replacement for default OS message dialog

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtWidgets, QtCore, QtGui
from qt.QtWidgets.QSpacer import QSpacer


# noinspection PyPep8Naming
class QToolBar(QtWidgets.QToolBar):
    def __init__(self, parent=None):
        super(QToolBar, self).__init__(parent)

        self.setIconSize(QtCore.QSize(16, 16))

    def addStretch(self, size=0):
        """Add space stretch"""

        spacer = QSpacer()

        if size > 0:
            spacer.setMinimumWidth(size)

        self.addWidget(spacer)
