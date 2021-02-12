# -*- coding: utf-8 -*-
from __future__ import print_function, division

# Standard library imports
import textwrap
import string

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui


app = sgtk.platform.current_bundle()


class Notice(QtGui.QWidget):

    style = string.Template(textwrap.dedent('''
        QWidget {
            background: $bg_color;
        }
        QLabel {
            color: $fg_color;
        }
    '''))

    def __init__(self, message, fg_color, bg_color, parent):
        super(Notice, self).__init__(parent=parent)

        self.label = QtGui.QLabel(
            message,
            alignment=QtCore.Qt.AlignCenter,
        )
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        style = self.style.substitute(fg_color=fg_color, bg_color=bg_color)
        self.setStyleSheet(style)

        self.setWindowFlags(
            QtCore.Qt.Tool
            | QtCore.Qt.FramelessWindowHint
        )
        self.setMinimumSize(1, 1)
        self.setMaximumHeight(30)

    def show_top(self, widget, duration=2000):
        '''Show the notice at the top center of the specified widget'''

        ref_rect = widget.rect()
        ref_pos = QtCore.QPoint(int(ref_rect.width() * 0.5), ref_rect.top())
        ref_pos = widget.mapToGlobal(ref_pos)

        rect = self.rect()
        rect.setWidth(ref_rect.width())
        self.setGeometry(rect)

        pos = QtCore.QPoint(int(rect.width() * 0.5), rect.top())

        delta = ref_pos - pos
        self.move(delta)

        # Set start and end values for animation
        start_value = self.geometry()
        start_value.setHeight(0)
        end_value = self.geometry()

        self.show()

        anim = QtCore.QPropertyAnimation(
            self,
            QtCore.QByteArray('geometry'.encode()),
            parent=self,
        )
        anim.setDuration(150)
        anim.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        anim.setStartValue(start_value)
        anim.setEndValue(end_value)
        anim.start()
        QtCore.QTimer.singleShot(duration, self._hide_top)

    def _hide_top(self):
        start_value = self.geometry()
        end_value = self.geometry()
        end_value.setHeight(0)

        anim = QtCore.QPropertyAnimation(
            self,
            QtCore.QByteArray('geometry'.encode()),
            parent=self,
        )
        anim.setDuration(150)
        anim.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        anim.setStartValue(start_value)
        anim.setEndValue(end_value)
        anim.finished.connect(self.close)
        anim.start()
