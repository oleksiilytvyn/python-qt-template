# -*- coding: UTF-8 -*-
"""Replacement for default OS message dialog

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtWidgets


# noinspection PyPep8Naming
class QTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    """Representation of a node as QTreeWidgetItem"""

    def __init__(self, data=None):
        super(QTreeWidgetItem, self).__init__()

        self._data = data

    def object(self):
        """Returns associated object"""

        return self._data

    def setObject(self, data):
        """Set associated object"""

        self._data = data
