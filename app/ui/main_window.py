# -*- coding: UTF-8 -*-
"""Application main window

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""

# generic imports

import app
# noinspection PyUnresolvedReferences
from app import resources
from qt import QtCore, QtGui, QtWidgets
from app.core.util import *
from app.ui.about_dialog import AboutDialog
from qt.utils import q_move_center


class MainWindow(QtWidgets.QMainWindow):
    """Main window"""

    def __init__(self, _app):
        super(MainWindow, self).__init__(None)

        self.app = _app
        self.__ui__()

    def closeEvent(self, event):
        """Close dialogs on close event"""

        self.dialog_about.close()
        self.app.quit()

        super(MainWindow, self).closeEvent(event)

    def __ui__(self):

        self.dialog_about = AboutDialog()

        # menubar
        self._ui_menubar = QtWidgets.QMenuBar(self)

        # Help
        self._ui_about_action = QtGui.QAction('About %s' % (app.APPLICATION_NAME,), self)
        self._ui_about_action.triggered.connect(self.about_action)

        # help menu
        self.ui_menu_help = self._ui_menubar.addMenu('&Help')
        self.ui_menu_help.addAction(self._ui_about_action)

        if not OS_MAC:
            self.setMenuBar(self._ui_menubar)

        self.setWindowIcon(QtGui.Icon.getAppIcon())
        self.setGeometry(300, 300, 800, 480)
        self.setMinimumSize(320, 240)
        self.setWindowTitle(app.APPLICATION_NAME)
        q_move_center(self)
        self.show()

    def about_action(self):
        """Show about dialog"""

        self.dialog_about.show()
