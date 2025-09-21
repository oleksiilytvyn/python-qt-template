# -*- coding: UTF-8 -*-
"""Bootstrap and run the application

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from qt import QtCore
from qt import QtGui


class QSvgIcon(QtGui.QIcon):
    """
    Use SVG icons as QIcon
    """

    def __init__(self, path: str, size: QtCore.QSize = None, color: QtGui.QColor = None):
        super().__init__()
