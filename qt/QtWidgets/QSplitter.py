# -*- coding: UTF-8 -*-
"""Replacement for default OS message dialog

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtWidgets

class QSplitter(QtWidgets.QSplitter):
    """Splitter component"""

    def __init__(self, *args):
        super(QSplitter, self).__init__(*args)

        self.setHandleWidth(1)
