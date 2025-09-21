# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtWidgets


class QHBoxLayout(QtWidgets.QHBoxLayout):
    """Horizontal layout"""

    def __init__(self, parent=None):
        super(QHBoxLayout, self).__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
