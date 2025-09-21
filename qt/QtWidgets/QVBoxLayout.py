# -*- coding: UTF-8 -*-
"""Replacement for default OS message dialog

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtWidgets


class QVBoxLayout(QtWidgets.QVBoxLayout):
    """Vertical layout"""

    def __init__(self, parent=None):
        super(QVBoxLayout, self).__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
