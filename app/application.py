# -*- coding: UTF-8 -*-
"""Application main window

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import logging
import datetime
import requests
import packaging.version

import app
logger = logging.getLogger('application')

from app.core.util import *
# UI
from app.ui.main_window import MainWindow
from app.ui.update_dialog import UpdateDialog
from qt import QtWidgets, QtNetwork, QtCore, QtGui
from qt.QtWidgets.QStyleSheetWatcher import apply_styles


class Application(QtWidgets.QApplication):
    """Application Instance"""

    _instance = None
    _quitting = False
    # Triggered when mapping mode changed
    mapping = QtCore.Signal(bool)

    def __init__(self, argv):
        super(Application, self).__init__(argv)

        logger.info(f"Starting {app.APPLICATION_NAME} {app.__version__}")

        Application._instance = self

        self._actions = {}

        # Set up a socket to check if another instance started
        self._socket = QtNetwork.QLocalSocket()
        self._socket.connectToServer(app.GUID, QtCore.QIODevice.OpenModeFlag.ReadOnly)
        self._socket_connected = self._socket.waitForConnected()

        self._server = QtNetwork.QLocalServer()
        self._server.listen(app.GUID)

        self._sys_exception_handler = sys.excepthook

        # set exception handler
        sys.excepthook = self.unhandled_exception

        self.setQuitOnLastWindowClosed(False)
        self.setWindowIcon(QtGui.Icon("256")) # TODO: Use default icon
        self.lastWindowClosed.connect(self._closed)
        self.setApplicationVersion(app.__version__)
        self.setApplicationName(app.APPLICATION_NAME)
        self.setOrganizationName(app.ORGANISATION_NAME)
        self.setOrganizationDomain(app.ORGANISATION_DOMAIN)

        # prevent from running more than one instance
        if not self.more_than_one_instance_allowed and self.is_already_running():
            self.another_instance_started()
            self.quit()

            return

        Application.check_updates(False)
        apply_styles(self)

        # Launch application
        self.main_window = MainWindow(self)

    def _closed(self):
        """Called when all windows closed"""

        self.quit()

    def quit(self):
        """Quit the application and close all connections"""

        if self._quitting:
            logger.info("Quit already requested")
            return

        self._quitting = True

        logger.info(f"Quitting {app.APPLICATION_NAME}")

        self._server.close()
        self.processEvents()

        QtWidgets.QApplication.quit()
        logging.shutdown()

    def unhandled_exception(self, exception_type, value, traceback_object):
        """Re-implement this method to catch exceptions"""

        logger.error("Unhandled exception", exc_info=(exception_type, value, traceback_object))
        self._sys_exception_handler(exception_type, value, traceback_object)

    def is_already_running(self):
        """Check for another instance of this application

        Returns: bool
        """

        return self._socket_connected

    @property
    def more_than_one_instance_allowed(self):
        """Do not allow multiple instances"""

        return False

    def another_instance_started(self):
        """Show a warning dialog when a user tries to
        launch multiple instances of Application
        """

        message = QtWidgets.QMessageDialog(title=f"{app.APPLICATION_NAME} already launched",
                                           text=f"Close previously opened {app.APPLICATION_NAME} and try again",
                                           icon=QtWidgets.QMessageDialog.Critical)
        message.exec_()

    @staticmethod
    def check_updates(force: bool = False) -> None:
        """Check for the new version"""

        settings = QtCore.QSettings()
        last_check = settings.value("last_version_check", "")
        today = datetime.date.today().isoformat()

        if force or last_check != today:
            settings.setValue("last_version_check", today)
        else:
            # Don't check within a day
            return

        try:
            logger.info("Checking for updates. Current version: %s", app.__version__)

            # TODO: Check for application platform (windows, macos, linux)
            response = requests.get(f"{app.APPLICATION_WEB}/api/version", timeout=1)
            latest_version = response.json()['latest']

            if packaging.version.parse(latest_version) > packaging.version.parse(app.__version__):
                logger.info("Latest version: %s", latest_version)

                message = UpdateDialog(None, latest_version)
                message.exec_()

        except requests.RequestException as e:
            logger.error(f"Failed to check for updates: {str(e)}")

        except (KeyError, ValueError, packaging.version.InvalidVersion) as e:
            logger.error(f"Invalid version data: {str(e)}")

    @classmethod
    def instance(cls) -> 'Application':
        """Get instance of Application

        Returns: instance of Application
        """

        return cls._instance
