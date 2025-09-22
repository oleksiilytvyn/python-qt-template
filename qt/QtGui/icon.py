# -*- coding: UTF-8 -*-
"""Bootstrap and run the application

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import PySide6
from PySide6 import QtCore, QtGui


_icons = {
    "icon": ':/icon/icon.png'
}
_icons_cache: dict[str, QtGui.QIcon] = {}


# noinspection PyPep8Naming,PyPep8Naming
class Icon(QtGui.QIcon):
    """Pixmap/vector icon"""

    _app_icon = None

    @staticmethod
    def getAppIcon() -> PySide6.QtGui.QIcon:
        if Icon._app_icon is None:
            icon = PySide6.QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(':/icon/icon.png'))

            Icon._app_icon = icon

        return Icon._app_icon

    def __init__(self, path=None):
        super(Icon, self).__init__(path)

    def __new__(cls, *args, **kwargs):
        """Create QIcon by name"""
        name = args[0]

        if name in _icons_cache:
            return _icons_cache[name]

        if name in _icons:
            icon = QtGui.QIcon(_icons[name])
        else:
            icon = Icon(*args, **kwargs)

        _icons_cache[name] = icon

        return icon

    def coloredPixmap(self, width, height, color, original_color=QtGui.QColor('black')):
        """Create a pixmap from the original icon, changing `original_color` color to the given color

        Args:
            width (int): width of pixmap
            height (int): height of pixmap
            color (QColor): color of icon
            original_color (QColor): new color
        Returns:
            QPixmap of icon
        """

        pixmap = self.pixmap(width, height)
        mask = pixmap.createMaskFromColor(original_color, QtCore.Qt.MaskMode.MaskOutColor)
        pixmap.fill(color)
        pixmap.setMask(mask)

        return pixmap

    def addColoredPixmap(self, width=128, height=128, color=QtGui.QColor("#000"),
                         mode=QtGui.QIcon.Mode.Normal,
                         state=QtGui.QIcon.State.On):
        """Add a pixmap with a given color

        Args:
            width (int): width of added pixmap
            height (int): height of added pixmap
            color (QColor): color of icon
            mode: QIcon mode
            state: QIcon state
        """

        self.addPixmap(self.coloredPixmap(width, height, color), mode, state)

    @staticmethod
    def colored(path, color, original_color=QtGui.QColor('black')):
        """Colorize icon and return new instance

        Args:
            path (str): image location
            color (QColor): new color
            original_color (QColor): original color that will be used as a mask to fill with a new color
        """

        icon = Icon(path)
        size = icon.availableSizes()[0] if len(icon.availableSizes()) > 0 else QtCore.QSize(16, 16)

        return Icon(icon.coloredPixmap(size.width(), size.height(), color, original_color))
