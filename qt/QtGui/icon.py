# -*- coding: UTF-8 -*-
"""Bootstrap and run the application

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import PySide6
from PySide6 import QtCore, QtGui


_icons = {
    "32": ':/icons/32.png',
    "64": ':/icons/64.png',
    "128": ':/icons/128.png',
    "256": ':/icons/256.png',
    "512": ':/icons/512.png',
    "edit": ':/icons/edit.png',
    "songs": ':/icons/songs.png',
    "font": ':/icons/font.png',
    "shadow": ':/icons/shadow.png',
    "align": ':/icons/align.png',
    "case": ':/icons/case.png',
    "color": ':/icons/color.png',
    "background": ':/icons/background.png',
    "zone-select": ':/icons/zone-select.png',
    "selection-select": ':/icons/selection-select.png',
    "testcard": ':/icons/testcard.png',
    "text-padding-box": ':/icons/text-padding-box.png',
    "add": ':/icons/add.png',
    "media": ':/icons/media.png',
    "stop": ':/icons/stop.png',
    "play": ':/icons/play.png',
    "save": ':/icons/save.png',
    "live": ':/icons/live.png',
    "remove-white": ':/icons/remove-white.png',
    "library": ':/icons/library.png',
    "search-clear": ':/rc/search-clear.png'
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
            icon.addPixmap(QtGui.QPixmap(':/icons/32.png'))
            icon.addPixmap(QtGui.QPixmap(':/icons/64.png'))
            icon.addPixmap(QtGui.QPixmap(':/icons/128.png'))
            icon.addPixmap(QtGui.QPixmap(':/icons/256.png'))
            icon.addPixmap(QtGui.QPixmap(':/icons/512.png'))

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
