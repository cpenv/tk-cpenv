# -*- coding: utf-8 -*-
from __future__ import print_function

# Shotgun imports
from sgtk.platform.qt import QtCore, QtGui

# PySide1 compat
try:
    QtGui.QHeaderView.setSectionResizeMode
except AttributeError:
    QtGui.QHeaderView.setSectionResizeMode = QtGui.QHeaderView.setResizeMode

# Local imports
from .env_tree import EnvTree


class EnvDisplay(QtGui.QDialog):

    def __init__(self, title, data, parent=None):
        super(EnvDisplay, self).__init__(parent=parent)

        self.setWindowTitle(title)

        self.tree = EnvTree('environ', data)
        self.button = QtGui.QPushButton('Ok')
        self.button.setSizePolicy(
            QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Maximum,
        )
        self.button.clicked.connect(self.accept)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.button)
        self.layout.setAlignment(self.button, QtCore.Qt.AlignRight)
        self.setLayout(self.layout)
