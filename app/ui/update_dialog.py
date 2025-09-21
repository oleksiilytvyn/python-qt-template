# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import app
from qt import QtCore, QtGui, QtWidgets


class UpdateDialog(QtWidgets.QDialog):
    """Update Dialog"""

    def __init__(self, parent=None, version: str = "0.0.1"):
        """A basic about dialog"""

        super(UpdateDialog, self).__init__(parent)

        self._window_title = "Update Available"
        self._title = "Update Available"
        self._description = f"A new version of {app.APPLICATION_NAME} ({version}) is available."

        self.url_report = app.APPLICATION_WEB
        self.url_help = app.APPLICATION_WEB

        self.__ui__()

    def __ui__(self):

        pixmap = QtGui.QPixmap(":/icons/256.png")
        pixmap.setDevicePixelRatio(2)

        self._ui_icon = QtWidgets.QLabel(self)
        self._ui_icon.setPixmap(pixmap)
        self._ui_icon.setAlignment(QtGui.Qt.AlignmentFlag.AlignCenter)
        self._ui_icon.setGeometry(20, 20, 128, 128)

        self._ui_title = QtWidgets.QLabel(self._title, self)
        self._ui_title.setGeometry(160, 34, 311, 26)
        self._ui_title.setObjectName("AboutDialogTitle")

        self._ui_description = QtWidgets.QPlainTextEdit(self._description, self)
        self._ui_description.setHorizontalScrollBarPolicy(QtGui.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._ui_description.setVerticalScrollBarPolicy(QtGui.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._ui_description.setReadOnly(True)
        self._ui_description.setGeometry(156, 74, 311, 88)
        self._ui_description.setObjectName("AboutDialogDescription")

        self._ui_btn_help = QtWidgets.QPushButton("Help")
        self._ui_btn_help.clicked.connect(self.help)

        self._ui_btn_report = QtWidgets.QPushButton("Download")
        self._ui_btn_report.clicked.connect(self.download)

        self.ui_btn_close = QtWidgets.QPushButton("Close")
        self.ui_btn_close.setDefault(True)
        self.ui_btn_close.clicked.connect(self.close)

        self._ui_buttons_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.LeftToRight)
        self._ui_buttons_layout.addWidget(self._ui_btn_help)
        self._ui_buttons_layout.addStretch()
        self._ui_buttons_layout.addWidget(self._ui_btn_report)
        self._ui_buttons_layout.addWidget(self.ui_btn_close)

        self._ui_buttons = QtWidgets.QWidget(self)
        self._ui_buttons.setLayout(self._ui_buttons_layout)
        self._ui_buttons.setGeometry(8, 172, 484 - 16, 50)

        self.setWindowTitle(self._window_title)
        self.setWindowIcon(QtGui.Icon.getAppIcon())
        self.setWindowFlags(QtGui.Qt.WindowType.WindowCloseButtonHint)
        self.setGeometry(100, 100, 484, 224)
        self.setFixedSize(484, 224)
        self.moveCenter()

    def help(self):
        """Open a web page"""
        url = QtCore.QUrl(self.url_help)
        QtGui.QDesktopServices.openUrl(url)

    def download(self):
        """Open a web page"""
        url = QtCore.QUrl(self.url_report)
        QtGui.QDesktopServices.openUrl(url)
