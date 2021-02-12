# -*- coding: utf-8 -*-
from __future__ import print_function

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

# PySide1 compat
try:
    QtGui.QHeaderView.setSectionResizeMode
except AttributeError:
    QtGui.QHeaderView.setSectionResizeMode = QtGui.QHeaderView.setResizeMode

# Local imports
from . import res
from .env_tree import EnvTree
from .notice import Notice


app = sgtk.platform.current_bundle()


class EnvDisplay(QtGui.QDialog):

    def __init__(self, title, data, parent=None):
        super(EnvDisplay, self).__init__(parent=parent)
        self.data = data
        self.tree = EnvTree('environ', self.data)
        self.ok_button = QtGui.QPushButton('Ok')
        self.ok_button.setSizePolicy(
            QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Maximum,
        )
        self.ok_button.clicked.connect(self.accept)
        self.copy_button = QtGui.QPushButton(
            icon=QtGui.QIcon(res.get_path('copy.png')),
            text='Copy to Clipboard',
        )
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.setDirection(self.button_layout.RightToLeft)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.copy_button)
        self.button_layout.addStretch()

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.tree)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(res.get_path('icon_dark_256.png')))

    def copy_to_clipboard(self):
        string = app.cpenv.vendor.yaml.safe_dump(
            self.data,
            default_flow_style=False,
            sort_keys=False,
            indent=4,
            width=79,
        )
        qapp = QtGui.QApplication.instance()
        qapp.clipboard().setText(string)

        note = Notice(
            'Copied Environment to clipboard.',
            fg_color="#EEE",
            bg_color="#1694c9",
            parent=self,
        )
        note.show_top(self)
