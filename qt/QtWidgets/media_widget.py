# -*- coding: UTF-8 -*-
"""

:copyright: (c) 2025 by Oleksii Lytvyn (https://github.com/oleksiilytvyn).
:license: MIT, see LICENSE for more details.
"""
import os

from PySide6 import QtCore, QtGui, QtWidgets

from qt.QtWidgets.QImageListWidget import QImageListWidget


# noinspection PyPep8Naming
class MediaWidget(QtWidgets.QWidget):
    itemSelected = QtCore.Signal(object)
    switchMode = QtCore.Signal()
    blackoutImage = QtCore.Signal(object)
    textImage = QtCore.Signal(object)

    def __init__(self, parent=None):

        super(MediaWidget, self).__init__(parent)

        size = 128
        add_action = QtGui.QAction(QtGui.QIcon(':/icons/add.png'), 'Add', self)
        add_action.triggered.connect(self.addFilesAction)

        toggle_action = QtGui.QAction(QtGui.QIcon(':/icons/library.png'), 'Library', self)
        toggle_action.triggered.connect(self.toggleAction)

        self.files_list = []
        self._ui_layout = QtWidgets.QVBoxLayout()
        self._ui_layout.setObjectName("media_dialog")
        self._ui_layout.setSpacing(0)
        self._ui_layout.setContentsMargins(0, 0, 0, 0)

        self._ui_expander = QtWidgets.QWidget()
        self._ui_expander.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self._ui_toolbar = QtWidgets.QToolBar()
        self._ui_toolbar.setObjectName("media_toolbar")
        self._ui_toolbar.setIconSize(QtCore.QSize(16, 16))
        self._ui_toolbar.addAction(add_action)
        self._ui_toolbar.addWidget(self._ui_expander)
        self._ui_toolbar.addAction(toggle_action)

        self.ui_list = QImageListWidget()
        self.ui_list.setObjectName("media_list")
        self.ui_list.keyPressed.connect(self.itemKeypress)
        self.ui_list.fileDropped.connect(self.fileDropped)
        self.ui_list.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.ui_list.setSpacing(0)
        self.ui_list.setWrapping(True)
        self.ui_list.setAcceptDrops(True)
        self.ui_list.setDragEnabled(False)
        self.ui_list.setUniformItemSizes(True)
        self.ui_list.setDropIndicatorShown(True)
        self.ui_list.setBatchSize(size)
        self.ui_list.setIconSize(QtCore.QSize(size, size))
        self.ui_list.setGridSize(QtCore.QSize(size, size))
        self.ui_list.setMovement(QtWidgets.QListView.Movement.Snap)
        self.ui_list.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.ui_list.setLayoutMode(QtWidgets.QListView.LayoutMode.Batched)
        self.ui_list.setResizeMode(QtWidgets.QListView.ResizeMode.Adjust)
        self.ui_list.setAttribute(QtGui.Qt.WidgetAttribute.WA_MacShowFocusRect, False)

        self._ui_layout.addWidget(self.ui_list)
        self._ui_layout.addWidget(self._ui_toolbar)

        self.setLayout(self._ui_layout)
        self.setContextMenuPolicy(QtGui.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

    def contextMenu(self, pos):

        item = self.ui_list.itemAt(pos)
        menu = QtWidgets.QMenu("Context Menu", self)

        clear_action = QtGui.QAction('Clear list', menu)
        clear_action.triggered.connect(self.clear)

        add_action = QtGui.QAction('Add', menu)
        add_action.triggered.connect(self.addFilesAction)

        def setBlackoutImageAction():
            self.blackoutImage.emit(item.data(QtGui.Qt.ItemDataRole.UserRole))

        background_action = QtGui.QAction('Set as blackout image', menu)
        background_action.triggered.connect(setBlackoutImageAction)

        def setTextImageAction():
            self.textImage.emit(item.data(QtGui.Qt.ItemDataRole.UserRole))

        text_action = QtGui.QAction('Set as default text image', menu)
        text_action.triggered.connect(setTextImageAction)

        def removeItemAction():
            self.ui_list.takeItem(self.ui_list.row(item))

        remove_action = QtGui.QAction('Remove', menu)
        remove_action.triggered.connect(removeItemAction)

        def removeBlackoutImageAction():
            self.blackoutImage.emit(None)

        remove_blackout_action = QtGui.QAction('Remove blackout image', menu)
        remove_blackout_action.triggered.connect(removeBlackoutImageAction)

        def removeTextImageAction():
            self.textImage.emit(None)

        remove_text_action = QtGui.QAction('Remove text image', menu)
        remove_text_action.triggered.connect(removeTextImageAction)

        if not item:
            background_action.setEnabled(False)
            text_action.setEnabled(False)
            remove_action.setEnabled(False)

        menu.addAction(background_action)
        menu.addAction(text_action)
        menu.addAction(remove_action)
        menu.addSeparator()
        menu.addAction(remove_text_action)
        menu.addAction(remove_blackout_action)
        menu.addSeparator()
        menu.addAction(add_action)
        menu.addAction(clear_action)

        ret = menu.exec_(self.mapToGlobal(pos))

        return ret

    def addFilesAction(self):

        location = QtCore.QStandardPaths.locate(QtCore.QStandardPaths.StandardLocation.PicturesLocation, "",
                                                QtCore.QStandardPaths.LocateOption.LocateDirectory)

        dialog = QtWidgets.QFileDialog()
        dialog.setDirectory(location)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpeg *.jpg *.gif)")

        if dialog.exec():
            for path in dialog.selectedFiles():
                self.addListItem(path)

    def fileDropped(self, url):

        path, ext = os.path.splitext(url.toLocalFile())

        if ext in [".png", ".jpeg", ".jpg", ".gif"]:
            self.addListItem(url.toLocalFile())

    def clear(self):

        self.files_list = []
        self.ui_list.clear()

    def toggleAction(self):

        self.switchMode.emit()

    def blackoutAction(self):

        self.itemSelected.emit(None)

    def addListItem(self, path):

        if path not in self.files_list:

            item_pixmap = QtGui.QPixmap(path)
            item_icon = QtGui.QIcon(item_pixmap)
            size = item_pixmap.size()

            # if size is 0x0 don't load image it can broke view
            if size.width() == 0 and size.width() == 0:
                return False

            item = QtWidgets.QListWidgetItem()
            item.setIcon(item_icon)
            item.setData(QtGui.Qt.ItemDataRole.UserRole, path)
            item.setFlags(
                QtGui.Qt.ItemFlag.ItemIsEnabled | QtGui.Qt.ItemFlag.ItemIsSelectable | QtGui.Qt.ItemFlag.ItemIsDragEnabled)

            self.files_list.append(path)
            self.ui_list.addItem(item)

    def itemDoubleClicked(self, item):

        self.itemSelected.emit(item.data(QtGui.Qt.ItemDataRole.UserRole))

    def itemKeypress(self, event):

        if event.key() == QtGui.Qt.Key.Key_Return:
            item = self.ui_list.currentItem()
            self.itemSelected.emit(item.data(QtGui.Qt.ItemDataRole.UserRole))
        else:
            QtWidgets.QListWidget.keyPressEvent(self.ui_list, event)
