# -*- coding: UTF-8 -*-
"""Replacement for default OS message dialog

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
from PySide6 import QtWidgets

class QSpacer(QtWidgets.QWidget):
    """Widget that simply allocates space and spread widgets"""

    def __init__(self, policy_horizontal=QtWidgets.QSizePolicy.Policy.Expanding,
                 policy_vertical=QtWidgets.QSizePolicy.Policy.Expanding):
        """Create a spacer component that allocates space and stretches all other components in the layout

        Args:
            policy_horizontal (QSizePolicy.Policy): horizontal space allocation rule
            policy_vertical (QSizePolicy.Policy): vertical space allocation rule
        """
        super(QSpacer, self).__init__()

        self.setSizePolicy(policy_horizontal, policy_vertical)
