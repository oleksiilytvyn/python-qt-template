# -*- coding: UTF-8 -*-
"""Bootstrap and run the application

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from qt import QtGui

class QFontIcon(QtGui.QIcon):
    """
    Use font icons as QIcon
    """

    def __init__(self, font):
        super().__init__()
