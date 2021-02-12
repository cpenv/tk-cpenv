# -*- coding: utf-8 -*-
from __future__ import print_function

# Standard library imports
import textwrap

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

# Local imports
from . import res

app = sgtk.platform.current_bundle()


class EnvSelector(QtGui.QDialog):

    style = textwrap.dedent('''
        #SelectButton {
            padding: 12px 24px 12px 24px;
            font-size: 16px;
        }
    ''')

    def __init__(self, environments, parent=None):
        super(EnvSelector, self).__init__(parent)

        self.state = {
            'environments': environments,
            'choice': environments[0],
        }

        self.msg = QtGui.QLabel('Select an Environment')
        self.msg.setAlignment(QtCore.Qt.AlignCenter)

        buttons = []
        for environment in environments:
            button = QtGui.QPushButton(environment['code'])
            button.setToolTip(
                'Modules:\n'
                + '\n'.join(environment['sg_requires'].split())
            )
            button.setObjectName('SelectButton')
            button.clicked.connect(self.choose(environment))
            buttons.append(button)

        # Layout widgets
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.msg)
        for button in buttons:
            self.layout.addWidget(button)
        self.setLayout(self.layout)

        self.setWindowTitle('tk-cpenv')
        self.setWindowIcon(QtGui.QIcon(res.get_path('icon_dark_256.png')))
        self.setStyleSheet(self.style)

    def choose(self, environment):
        def on_choose(*args):
            self.state['choice'] = environment
            self.accept()
        return on_choose

    def reject(self):
        super(EnvSelector, self).reject()
        self.close()

    def accept(self):
        super(EnvSelector, self).accept()
        self.close()

    @property
    def hide_tk_title_bar(self):
        return True
