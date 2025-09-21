# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from typing import Any

from PySide6 import QtWidgets


# noinspection PyPep8Naming
class QListWidgetItem(QtWidgets.QListWidgetItem):
    """List item"""

    def __init__(self, parent=None):
        super(QListWidgetItem, self).__init__(parent)

        self._data = None

    def setObject(self, data: Any) -> None:
        """Set associated data object

        Args:
            data (object): any object
        """

        self._data = data

    def object(self) -> Any | None:
        """Returns associated data object"""

        return self._data
