# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtGui
from PySide6 import QtWidgets


def q_move_center(widget: QtWidgets.QWidget) -> None:
    """Center a widget to screen center"""

    qr = widget.frameGeometry()
    cp = QtGui.QGuiApplication.primaryScreen().geometry().center()
    qr.moveCenter(cp)

    widget.move(qr.topLeft())
