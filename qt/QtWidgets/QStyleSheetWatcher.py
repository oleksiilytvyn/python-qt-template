# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import re
import time
import logging
from typing import Dict
from PySide6 import QtCore
from PySide6 import QtWidgets

logger = logging.getLogger(__name__)


class QStyleSheetWatcher(QtCore.QObject):

    _local_file: str = ""
    _resource_file: str = ""
    _file_stylesheet: str = ""
    _resource_stylesheet: str = ""
    _variables: Dict[str, str] = {}

    updated = QtCore.Signal(str)

    def __init__(self, local_file: str, resources_file: str):

        super().__init__()

        logger.info("Attached stylesheet watcher")

        self._local_file = local_file
        self._resource_file = resources_file
        self._resource_stylesheet = self._read_file(resources_file)

        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.addPath(self._local_file)
        self.watcher.fileChanged.connect(self._changed)

    def stylesheet(self):
        return self._file_stylesheet if self._file_stylesheet else self._resource_stylesheet

    def set(self, key, value):
        pass

    def get(self, key):
        pass

    def _changed(self):

        logger.info("Updated %s" % time.strftime("%H:%M:%S"))

        self._file_stylesheet = self._read_file(self._local_file)
        self.updated.emit(self._file_stylesheet)

    def _read_file(self, path):
        """Get stylesheet from resource"""

        data = ""
        stream = QtCore.QFile(path)

        if stream.open(QtCore.QFile.OpenModeFlag.ReadOnly):
            data = str(stream.readAll())
            stream.close()

        return re.sub(r'(\\n)|(\\r)|(\\t)', '', data)[2:-1]

    def _parse(self, stylesheet, variables: Dict[str, str]):
        """Read stylesheet"""
        return stylesheet


class _ProxyStyle(QtWidgets.QProxyStyle):
    """Fix stylesheet issues with a custom style"""

    def styleHint(self, hint, option=None, widget=None, return_data=None):
        if QtWidgets.QStyle.StyleHint.SH_ComboBox_Popup == hint:
            return 0

        return QtWidgets.QProxyStyle.styleHint(self, hint, option, widget, return_data)


def apply_styles(app: QtWidgets.QApplication):
    """Add stylesheet watcher and apply style fixes for different OS's"""

    # fix for retina displays
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    # fix styles
    app.setStyle(_ProxyStyle())

    # use GTK style if available
    for style in QtWidgets.QStyleFactory.keys():
        if "gtk" in style.lower():
            app.setStyle(QtWidgets.QStyleFactory.create("gtk"))

    app.style_watcher = QStyleSheetWatcher("./resources/qt/theme.qss", ":/qt/theme.qss")
    app.style_watcher.updated.connect(lambda stylesheet: app.setStyleSheet(stylesheet))
    app.setStyleSheet(app.style_watcher.stylesheet())
