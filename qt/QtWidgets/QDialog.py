# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtWidgets, QtCore, QtGui
from qt.QtGui.icon import Icon
from app import OS_MAC


# noinspection PyPep8Naming,PyPep8Naming
class QDialog(QtWidgets.QDialog):
    """Abstract dialog window"""

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)

        # Set a default window icon, used on Windows and some Linux distributions
        if not OS_MAC:
            self.setWindowIcon(Icon.getAppIcon())

        self.setObjectName(type(self).__name__)

    def moveCenter(self):
        """Move a window to the center of the current screen"""

        geometry = self.frameGeometry()
        screen = QtWidgets.QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        geometry.moveCenter(center_point)

        self.move(geometry.topLeft())

    def showWindow(self):
        """Raise a dialog in any way"""

        self.show()
        self.raise_()
        self.setWindowState(
            self.windowState() & ~QtCore.Qt.WindowState.WindowMinimized | QtCore.Qt.WindowState.WindowActive)
        self.activateWindow()
