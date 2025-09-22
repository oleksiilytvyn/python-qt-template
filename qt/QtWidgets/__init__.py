# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""

from PySide6 import QtWidgets, QtCore
# noinspection PyUnresolvedReferences
from PySide6.QtWidgets import *

# Override built-in widgets
from qt.QtWidgets.QDialog import QDialog  # type: ignore
from qt.QtWidgets.QHBoxLayout import QHBoxLayout
from qt.QtWidgets.QImageListWidget import QImageListWidget
from qt.QtWidgets.QLineEdit import QLineEdit
from qt.QtWidgets.QListWidget import QListWidget  # type: ignore
from qt.QtWidgets.QListWidgetItem import QListWidgetItem  # type: ignore
from qt.QtWidgets.QMessageDialog import QMessageDialog
# Dialogs
from qt.QtWidgets.QPopup import QPopup
from qt.QtWidgets.QProgressDialog import QProgressDialog  # type: ignore
from qt.QtWidgets.QSearchEdit import QSearchEdit
# Widgets
from qt.QtWidgets.QSpacer import QSpacer
from qt.QtWidgets.QSplitter import QSplitter  # type: ignore
from qt.QtWidgets.QTableWidget import QTableWidget  # type: ignore
from qt.QtWidgets.QTextEdit import QTextEdit  # type: ignore
from qt.QtWidgets.QToolBar import QToolBar  # type: ignore
from qt.QtWidgets.QTransformWidget import QTransformWidget
from qt.QtWidgets.QTreeWidget import QTreeWidget  # type: ignore
from qt.QtWidgets.QTreeWidgetItem import QTreeWidgetItem  # type: ignore
from qt.QtWidgets.QVBoxLayout import QVBoxLayout

# New widgets
from qt.QtWidgets.QStyleSheetWatcher import QStyleSheetWatcher

QtDocumentsLocation = QtCore.QStandardPaths.locate(QtCore.QStandardPaths.StandardLocation.DocumentsLocation, "",
                                                   QtCore.QStandardPaths.LocateOption.LocateDirectory)


def get_save_file_name(parent: QWidget = None, title: str = "Save", location: str = QtDocumentsLocation,
                       ext: str = "") -> str:
    """Open a save file dialog"""

    path, _ = QtWidgets.QFileDialog.getSaveFileName(parent, title, location, ext)

    return path


def get_open_file_name(parent: QWidget = None, title: str = "Save", location: str = QtDocumentsLocation, ext: str = ""):
    """Open file dialog and return path to a selected file"""

    path, _ = QtWidgets.QFileDialog.getOpenFileName(parent, title, location, ext)

    return path
