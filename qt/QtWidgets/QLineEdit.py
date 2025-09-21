# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtGui, QtWidgets, QtCore

import qt.colors as qt_colors


class QLineEdit(QtWidgets.QLineEdit):
    """Line edit widget"""

    def __init__(self, *args, **kwargs):
        super(QLineEdit, self).__init__(*args, **kwargs)

        # fix: placeholder text color doesn't match the theme color
        if hasattr(QtGui.QPalette, 'PlaceholderText'):
            palette = self.palette()
            palette.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor(qt_colors.BASE_TEXT_ALT))

            self.setPalette(palette)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_MacShowFocusRect, False)
