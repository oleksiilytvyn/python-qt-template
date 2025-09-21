# -*- coding: UTF-8 -*-
"""Bootstrap and run the application

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import os, sys
from app.core.util import *

__version__ = '1.0.0'
APPLICATION_NAME = "Application"
APPLICATION_AUTHOR = "Oleksii Lytvyn"
APPLICATION_WEB = "https://github.com/oleksiilytvyn"
APPLICATION_EMAIL = ""
VERSION_ENDPOINT = f"https://oleksiilytvyn.github.io/python-qt-template/api/version"
COPYRIGHT = f"2025 {APPLICATION_AUTHOR}"
LICENSE = "MIT"
DESCRIPTION = "Application description"
DESCRIPTION_LONG = ""
KEYWORDS = "qt template pyqt pyside"
ORGANISATION_NAME = "template" # Qt uses this
ORGANISATION_DOMAIN = "template.com" # Qt uses this
GUID = "{2142899e-665c-422c-9dac-cf0cad64214b}" # TODO: Check GUID format
DEBUG = os.getenv("DEBUG", "0") == "1"


def main():
    """Run application from the location of installation"""

    from app.application import Application
    from app.core.logging import configure_logging
    configure_logging()

    os.chdir(application_location())

    app_instance = Application(sys.argv)
    app_instance.exec_()
    sys.exit(0)


if __name__ == "__main__":
    main()
