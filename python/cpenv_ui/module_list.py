# -*- coding: utf-8 -*-
from __future__ import print_function

# Standard library imports
from functools import partial

# Shotgun imports
from sgtk.platform.qt import QtCore, QtGui

# PySide1 compat
try:
    QtGui.QHeaderView.setSectionResizeMode
except AttributeError:
    QtGui.QHeaderView.setSectionResizeMode = QtGui.QHeaderView.setResizeMode


# Tree Columns
Name = 0
Version = 1


class ModuleList(QtGui.QTreeWidget):

    version_changed = QtCore.Signal([object])
    item_dropped = QtCore.Signal()

    def __init__(self, name, parent=None):
        super(ModuleList, self).__init__(parent=parent)

        self.setObjectName(name)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setMinimumWidth(200)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding,
        )

        # Setup header
        self.setHeaderLabels(['Name', 'Version'])
        header = self.header()
        header.setSectionResizeMode(header.ResizeToContents)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(Name, header.Stretch)

        # Selection behavior
        self.setSelectionMode(self.ExtendedSelection)
        self.setSelectionBehavior(self.SelectRows)

        # Drag and drop settings
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)

    def clear_selection(self):
        for item in self.iter_items():
            item.setSelected(False)

    def iter_items(self):
        for i in range(self.topLevelItemCount()):
            yield self.topLevelItem(i)

    def dropEvent(self, event):

        index = self.indexAt(event.pos())
        indicator = self.dropIndicatorPosition()

        if indicator in (self.OnItem, self.AboveItem):
            for item in reversed(event.source().selectedItems()):
                self.insert_spec_set(index.row(), item.spec_set)
        elif indicator is self.BelowItem:
            for item in reversed(event.source().selectedItems()):
                self.insert_spec_set(index.row() + 1, item.spec_set)
        else:
            for item in event.source().selectedItems():
                self.add_spec_set(item.spec_set)

        # We need to return prior to emitting item_dropped to ensure that
        # our list modifications have taken place. An alternative may be
        # to connect to item_dropped using QueuedConnection. Try it sometime!
        QtCore.QTimer.singleShot(200, self.item_dropped.emit)

        return event.accept()

    def on_version_changed(self, item, index):
        item.setText(Version, item.combo_box.currentText())
        item.spec_set.select(index)
        self.version_changed.emit(item.spec_set)

    def create_item(self, spec_set):
        item = QtGui.QTreeWidgetItem(parent=self)
        item.spec_set = spec_set
        item.setText(Name, spec_set.selection.name)
        item.setText(Version, spec_set.selection.version.string)
        item.setFlags(
            QtCore.Qt.ItemIsSelectable
            | QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsDragEnabled
        )

        # Add versions combobox
        item.combo_box = QtGui.QComboBox(parent=self)
        item.combo_box.setFocusPolicy(QtCore.Qt.NoFocus)
        for spec in item.spec_set.module_specs:
            item.combo_box.addItem(spec.version.string)
        item.combo_box.setCurrentIndex(spec_set.selection_index)
        item.combo_box.currentIndexChanged.connect(partial(
            self.on_version_changed,
            item
        ))

        return item

    def insert_spec_set(self, index, spec_set):
        item = self.create_item(spec_set)
        self.insertTopLevelItem(index, item)
        self.setItemWidget(item, Version, item.combo_box)
        return item

    def add_spec_set(self, spec_set):
        item = self.create_item(spec_set)
        self.addTopLevelItem(item)
        self.setItemWidget(item, Version, item.combo_box)
        return item
