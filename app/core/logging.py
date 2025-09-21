# -*- coding: UTF-8 -*-
"""Configure application logging

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import logging
import app

def configure_logging():
    """Configure logging"""
    log_format = '%(asctime)s [%(levelname)s] %(name)s - %(message)s'

    if app.DEBUG:
        logging.basicConfig(
            level=logging.DEBUG,
            format=log_format,
            handlers=[
                logging.FileHandler("debug.log", encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(
            level=logging.ERROR,
            format=log_format,
            handlers=[
                logging.StreamHandler()
            ]
        )
