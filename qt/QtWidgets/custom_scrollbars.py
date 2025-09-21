import PySide6.QtGui as QtGui
import PySide6.QtCore as QtCore
import PySide6.QtWidgets as QtWidgets


class QCustomScrollBarMixin(QtWidgets.QAbstractScrollArea):
    """Mixin for adding custom scrollbars to widgets"""

    __vertical_new: QtWidgets.QScrollBar = None
    __horizontal_new: QtWidgets.QScrollBar = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setVerticalScrollBarPolicy(QtGui.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtGui.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.__vertical = self.verticalScrollBar()
        self.__horizontal = self.horizontalScrollBar()

        self.__vertical_new = QtWidgets.QScrollBar(QtCore.Qt.Orientation.Vertical, self)
        self.__vertical_new.valueChanged.connect(self.__vertical.setValue)

        self.__horizontal_new = QtWidgets.QScrollBar(QtCore.Qt.Orientation.Horizontal, self)
        self.__horizontal_new.valueChanged.connect(self.__horizontal.setValue)

        self.__vertical.valueChanged.connect(self.__vertical_new.setValue)
        self.__horizontal.valueChanged.connect(self.__horizontal_new.setValue)

        self.__update()

    def __update(self):
        """Update a custom scrollbars"""

        rect = self.rect()
        original = self.__vertical
        value = original.value()
        offset = 8

        if value == original.maximum() and value == 0:
            self.__vertical_new.hide()
        else:
            self.__vertical_new.show()

        self.__vertical_new.setPageStep(original.pageStep())
        self.__vertical_new.setRange(original.minimum(), original.maximum())
        self.__vertical_new.resize(offset, rect.height())
        self.__vertical_new.move(rect.width() - offset, 0)

    def setCustomScrollbars(self, vertical: bool = False, horizontal: bool = False):
        """Set custom scrollbars"""

        if vertical:
            self.setVerticalScrollBarPolicy(QtGui.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            self.setVerticalScrollBarPolicy(QtGui.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        if horizontal:
            self.setHorizontalScrollBarPolicy(QtGui.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            self.setHorizontalScrollBarPolicy(QtGui.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
