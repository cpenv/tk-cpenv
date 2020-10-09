# -*- coding: utf-8 -*-
from __future__ import print_function

# Standard library imports
import os

try:
    basestring
except NameError:
    basestring = (str, bytes)

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

# PySide1 compat
try:
    QtGui.QHeaderView.setSectionResizeMode
except AttributeError:
    QtGui.QHeaderView.setSectionResizeMode = QtGui.QHeaderView.setResizeMode


app = sgtk.platform.current_bundle()


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

    def set(self, key, value, parent_item=None):
        if os.pathsep in value:
            value = value.split(os.pathsep)

        if isinstance(value, basestring):
            if parent_item:
                child = QtGui.QTreeWidgetItem()
                child.setText(Value, value)
                if key != parent_item.text(Key):
                    child.setText(Key, key)
                parent_item.addChild(child)
            else:
                item = QtGui.QTreeWidgetItem(parent=self)
                item.setText(Key, key)
                item.setText(Value, value)
                self.addTopLevelItem(item)
        elif isinstance(value, (list, tuple)):
            if not parent_item:
                parent_item = QtGui.QTreeWidgetItem(parent=self)
                parent_item.setText(Key, key)
                self.addTopLevelItem(parent_item)

            for v in value:
                self.set(key, v, parent_item)
        elif isinstance(value, dict):
            if not parent_item:
                parent_item = QtGui.QTreeWidgetItem(parent=self)
                parent_item.setText(Key, key)
                self.addTopLevelItem(parent_item)

            for k, v in sorted(value.items()):
                self.set(k, v, parent_item)
        else:
            app.info('Failed to display {}: {} in tree.'.format(k, v))

        if parent_item:
            parent_item.setExpanded(True)
