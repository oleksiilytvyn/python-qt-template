# -*- coding: UTF-8 -*-
"""Run application as python package

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import os
import sys

from app.core.util import application_location
from app.application import Application

if __name__ == "__main__":
    os.chdir(application_location())
    from app.core.logging import configure_logging

    configure_logging()
    app_instance = Application(sys.argv)
    app_instance.exec_()
    sys.exit(0)
