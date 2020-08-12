# -*- coding: utf-8 -*-
from __future__ import print_function

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

app = sgtk.platform.current_bundle()


class MinimizedList(QtGui.QListWidget):

    def __init__(self, *args, **kwargs):
        super(MinimizedList, self).__init__(*args, **kwargs)
        self.setAlternatingRowColors(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSizePolicy(
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Maximum,
        )
        self.refresh_size()

    def refresh_size(self):
        min_height = 24
        max_height = 200
        items_height = self.sizeHintForRow(0) * (self.count() + 0.5)
        height = min(max_height, max(min_height, items_height))
        self.setMaximumHeight(height)
