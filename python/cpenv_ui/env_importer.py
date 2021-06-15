# -*- coding: utf-8 -*-
from __future__ import print_function

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

# Local imports
from . import res

app = sgtk.platform.current_bundle()


class EnvImporter(QtGui.QDialog):

    def __init__(self, parent):
        super(EnvImporter, self).__init__(parent)

        self.state = {
            'projects': None,
            'project': None,
            'environments': None,
            'environment': None,
        }

        # Can't get this search widget to work right...
        # search = sgtk.platform.import_framework(
        #     "tk-framework-qtwidgets",
        #     "shotgun_search_widget",
        # )
        # self.project_search = search.GlobalSearchWidget(self)
        # self.project_search.set_searchable_entity_types({'Project': []})
        # self.project_search.set_placeholder_text('Search for Project')
        # self.project_search.entity_activated.connect(self.on_entity_activated)

        # Create widgets
        self.project_search = QtGui.QComboBox()
        self.env_list = QtGui.QComboBox()
        self.engine = QtGui.QLineEdit()
        self.engine.setReadOnly(True)
        self.engine.setFocusPolicy(QtCore.Qt.NoFocus)
        self.req_list = QtGui.QListWidget()
        self.import_button = QtGui.QPushButton('Import')
        self.cancel_button = QtGui.QPushButton('Cancel')

        # Layout widgets
        button_layout = QtGui.QHBoxLayout()
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.cancel_button)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(QtGui.QLabel('Project'))
        layout.addWidget(self.project_search)
        layout.addWidget(QtGui.QLabel('Environment'))
        layout.addWidget(self.env_list)
        layout.addWidget(QtGui.QLabel('Engine'))
        layout.addWidget(self.engine)
        layout.addWidget(QtGui.QLabel('Requires'))
        layout.addWidget(self.req_list)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Connect widgets
        self.project_search.activated.connect(self.on_project_changed)
        self.env_list.activated.connect(self.on_env_changed)
        self.import_button.clicked.connect(self.on_import_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        self.setWindowTitle('Import Environments')
        self.setWindowIcon(QtGui.QIcon(res.get_path('icon_dark_256.png')))

        self.update_projects()

    def update_projects(self):
        entities = app.io.get_projects()
        if not entities:
            self.state['projects'] = None
        else:
            self.state['projects'] = list(
                sorted(entities, key=lambda e: e['name'])
            )
            if self.state['projects']:
                self.state['project'] = self.state['projects'][0]
            for project in self.state['projects']:
                app.info(str(project))
                self.project_search.addItem(project['name'])

        self.update_state()
        self.update_widgets()

    def update_state(self):
        # Clear env state if no project
        if not self.state['project']:
            self.state['environments'] = None
            self.state['environment'] = None
            return

        # Get environments for current project
        environments = app.io.get_environments(self.state['project'])
        self.state['environments'] = environments
        if self.state['environments']:
            self.state['environment'] = self.state['environments'][0]
        else:
            self.state['environment'] = None

    def update_widgets(self):
        '''Update all widgets'''

        # Update env_list
        self.env_list.clear()

        if self.state['environments']:
            self.env_list.setEnabled(True)
            for env in self.state['environments']:
                self.env_list.addItem(env['code'])
            if self.state['environment']:
                idx = self.env_list.findText(self.state['environment']['code'])
                if idx > -1:
                    self.env_list.setCurrentIndex(idx)
        else:
            self.env_list.setEnabled(False)
            if self.state['project']:
                self.env_list.addItem('No Environments.')

        # Update engine and req_list
        self.req_list.clear()

        if self.state['environment']:
            self.engine.setText(self.state['environment'].get(
                'sg_engine',
                'No engine set.'
            ))

            self.req_list.setEnabled(True)
            requires = self.state['environment']['sg_requires']
            if requires:
                requires = app.parse_requires(requires)
                self.req_list.addItems(requires)
        else:
            self.req_list.setEnabled(False)

    def on_project_changed(self, index):
        self.state['project'] = self.state['projects'][index]
        self.update_state()
        self.update_widgets()

    def on_env_changed(self, index):
        self.state['environment'] = self.state['environments'][index]
        self.update_widgets()

    def on_cancel_clicked(self):
        self.reject()

    def on_import_clicked(self):

        # Validate state
        if not self.state['project']:
            msg = QtGui.QMessageBox()
            msg.setText('You must select a project to import from.')
            msg.exec_()
            return

        if not self.state['environments']:
            msg = QtGui.QMessageBox()
            msg.setText('The project you have chosen has no Environments.')
            msg.exec_()
            return

        # Confirm import
        project = app.context.project['name']
        response = QtGui.QMessageBox.question(
            self,
            'Import Environments',
            (
                'Importing will replace all Environments in %s.\n'
                'Are you sure you want to continue?'
            ) % project,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
        )
        if response == QtGui.QMessageBox.No:
            return

        app.info('Importing environments to %s...' % project)
        for env in app.io.get_environments():
            app.info('Deleting %s - %s' % (env['id'], env['code']))
            app.io.delete_environment(env['id'])

        for env in self.state['environments']:
            app.info('Importing %s' % env['code'])
            app.io.update_environment(
                code=env['code'],
                engine=env['sg_engine'],
                requires=env['sg_requires'],
                software_versions=env['sg_software_versions'],
                project=app.context.project,
            )

        self.accept()
