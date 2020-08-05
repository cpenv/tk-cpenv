# -*- coding: utf-8 -*-
from __future__ import print_function

# Standard library imports
import os

# Shotgun imports
from sgtk.platform.qt import QtCore, QtGui

# PySide1 compat
try:
    QtGui.QHeaderView.setSectionResizeMode
except AttributeError:
    QtGui.QHeaderView.setSectionResizeMode = QtGui.QHeaderView.setResizeMode

# Tree Columns
Key = 0
Value = 1


class EnvTree(QtGui.QTreeWidget):

    def __init__(self, name, data, parent=None):
        super(EnvTree, self).__init__(parent=parent)

        self.setObjectName(name)
        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setMinimumWidth(200)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding,
        )

        # Setup header
        self.setHeaderLabels(['Key', 'Value'])
        header = self.header()
        header.setSectionResizeMode(header.ResizeToContents)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(Value, header.Stretch)

        self.set_data(data)

    def set_data(self, data):
        self.clear()
        self._data = {}
        for k, v in sorted(data.items()):
            self.set(k, v)

    def set(self, key, value):
        self._data[key] = value
        if os.pathsep in value:
            parent = QtGui.QTreeWidgetItem(parent=self)
            parent.setText(Key, key)
            self.addTopLevelItem(parent)

            for value in value.split(os.pathsep):
                child = QtGui.QTreeWidgetItem()
                child.setText(Value, value)
                parent.addChild(child)

            parent.setExpanded(True)
        elif isinstance(value, (list, tuple)):
            parent = QtGui.QTreeWidgetItem(parent=self)
            parent.setText(Key, key)
            self.addTopLevelItem(parent)

            for v in value:
                child = QtGui.QTreeWidgetItem()
                child.setText(Value, v)
                parent.addChild(child)

            parent.setExpanded(True)
        else:
            item = QtGui.QTreeWidgetItem(parent=self)
            item.setText(Key, key)
            item.setText(Value, value)
            self.addTopLevelItem(item)
