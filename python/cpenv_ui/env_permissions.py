# -*- coding: utf-8 -*-
from __future__ import print_function

# Standard library imports

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

# Local imports
from . import res

app = sgtk.platform.current_bundle()


class EnvPermissions(QtGui.QDialog):

    def __init__(self, environment, parent):
        super(EnvPermissions, self).__init__(parent)

        self.state = {
            'environment': environment,
        }

        self.save_button = QtGui.QPushButton('Save')
        self.cancel_button = QtGui.QPushButton('Cancel')

        # Layout widgets
        button_layout = QtGui.QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(QtGui.QLabel('Restrict to Users'))
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        # Connect widgets
        self.save_button.clicked.connect(self.on_save_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        self.setWindowTitle('Environment Permissions')
        self.setWindowIcon(QtGui.QIcon(res.get_path('icon_dark_256.png')))

        shotgun_fields = sgtk.platform.import_framework(
            "tk-framework-qtwidgets",
            "shotgun_fields",
        )
        self._fields_manager = shotgun_fields.ShotgunFieldManager(self)
        self._fields_manager.initialized.connect(self.on_initialized)
        self._fields_manager.initialize()

    def on_initialized(self):
        app.debug('ON_INITIALIZED')
        try:
            self.editor = self._fields_manager.create_widget(
                sg_entity_type=self.state['environment']['type'],
                field_name='sg_permissions_users',
                widget_type=self._fields_manager.EDITOR,
                entity=self.state['environment'],
                parent=self,
            )
            self.layout.insertWidget(1, self.editor)
        except Exception:
            app.logger.exception('Error occurred during Permission Dialog initialization.')

    def on_cancel_clicked(self):
        self.reject()

    def on_save_clicked(self):
        users = self.editor.get_value()

        try:
            app.io.set_environment_permissions(
                self.state['environment']['id'],
                users,
            )
            self.state['environment']['sg_permissions_users'] = users
        except Exception:
            app.logger.exception('Error occurred during save in Permission Dialog.')

        self.accept()
