# -*- coding: utf-8 -*-
from __future__ import print_function

# Standard library imports
from collections import OrderedDict
from functools import partial
from string import Template
import sys
import traceback

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

# Local imports
from .dialogs import ErrorDialog
from .env_importer import EnvImporter
from .env_display import EnvDisplay
from .env_permissions import EnvPermissions
from .module_list import ModuleList
from .module_info import ModuleInfo
from .notice import Notice
from . import res

app = sgtk.platform.current_bundle()


def show(app_instance):
    '''Show the CpenvModuleSelect for the given app_instance.'''

    return app_instance.engine.show_dialog(
        "Set cpenv modules...",
        app_instance,
        ModuleSelector,
    )


class ModuleSelector(QtGui.QWidget):
    '''A Dialog that allows the user to select modules to activate from a
    list of available modules.
    '''

    button_style = '''
    QPushButton:disabled {
        border-color: #333;
        background-color: #555;
        color: #777;
    }
    '''
    header_message = (
        'Drag modules from <b>Available Modules</b> to '
        '<b>%s Modules</b> to activate them for this job. '
        'When software is launched, these modules will be activated and '
        'available within the software.'
    )

    def __init__(self, *args, **kwargs):
        super(ModuleSelector, self).__init__(*args, **kwargs)

        app.info("Launching cpenv module selector...")

        # Set initial state
        self.state = {
            'environment': None,  # Current environment
            'environments': [],  # Project environments
            'engines': [],  # Name of available engines
            'available': {},  # Full list of available modules
            'selected': OrderedDict(),  # List of modules to activate on launch
            'unsaved_changes': False,
        }

        # Create widgets
        self.header_label = QtGui.QLabel(self.header_message)
        self.header_label.setWordWrap(True)

        self.env_list = QtGui.QComboBox()
        self.env_list.setFixedHeight(24)
        self.env_label = QtGui.QLabel('Environment')
        self.env_label.setToolTip(
            'An environment consists of module requirements and applies to '
            'a single toolkit engine. The required modules will be activated '
            'when the toolkit engines application is launched.')
        self.env_label.setSizePolicy(
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding,
        )
        self.env_import = QtGui.QToolButton(
            icon=QtGui.QIcon(res.get_path('import.png'))
        )
        self.env_import.setToolTip('Import environments from another project.')
        self.env_add = QtGui.QToolButton(
            icon=QtGui.QIcon(res.get_path('add.png'))
        )
        self.env_add.setToolTip('Add a new environment to this project.')
        self.env_remove = QtGui.QToolButton(
            icon=QtGui.QIcon(res.get_path('remove.png'))
        )
        self.env_remove.setToolTip('Delete current environment.')
        self.env_preview = QtGui.QToolButton(
            icon=QtGui.QIcon(res.get_path('preview.png'))
        )
        self.env_preview.setToolTip('Preview combined environment variables.')
        self.env_lock = QtGui.QToolButton(
            icon=QtGui.QIcon(res.get_path('lock_open.png'))
        )
        self.env_lock.setToolTip('Restrict to users.')
        self.env_header = QtGui.QHBoxLayout()
        self.env_header.addWidget(self.env_label)
        self.env_header.addWidget(self.env_import)
        self.env_header.addWidget(self.env_add)
        self.env_header.addWidget(self.env_remove)
        self.env_header.addWidget(self.env_preview)
        self.env_header.addWidget(self.env_lock)

        self.engine_label = QtGui.QLabel('Engine')
        self.engine_label.setToolTip(
            'The toolkit engine this environment applies to.'
        )
        self.engine_list = QtGui.QComboBox()
        self.engine_label.setToolTip(
            'Select a toolkit engine this environment applies to.'
        )
        self.engine_list.setFixedHeight(24)

        self.available_label = QtGui.QLabel('Available Modules')
        self.available_label.setToolTip('List of available modules.')
        self.available_list = ModuleList('available', parent=self)

        self.selected_label = QtGui.QLabel('Requires')
        self.selected_label.setToolTip(
            'The modules this environment requires.\n'
            'These will be activated when launching the associated engine.'
        )
        self.selected_list = ModuleList('selected', parent=self)
        self.selected_list.setSortingEnabled(False)

        self.module_info = ModuleInfo(parent=self)

        self.message_label = QtGui.QLabel('Unsaved changes....')
        self.message_label.hide()
        self.save_button = QtGui.QPushButton('Save Changes')
        self.save_button.setStyleSheet(self.button_style)
        self.save_button.setEnabled(False)

        self.footer = QtGui.QHBoxLayout()
        self.footer.setAlignment(QtCore.Qt.AlignRight)
        self.footer.addStretch(1)
        self.footer.addWidget(self.message_label)
        self.footer.addWidget(self.save_button)

        self.layout = QtGui.QGridLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setVerticalSpacing(4)
        self.layout.setHorizontalSpacing(12)
        self.layout.setRowStretch(5, 1)
        self.layout.setColumnStretch(2, 1)
        self.layout.addWidget(self.available_label, 0, 1)
        self.layout.addWidget(self.available_list, 1, 1, 5, 1)
        self.layout.addLayout(self.env_header, 0, 0)
        self.layout.addWidget(self.env_list, 1, 0)
        self.layout.addWidget(self.engine_label, 2, 0)
        self.layout.addWidget(self.engine_list, 3, 0)
        self.layout.addWidget(self.selected_label, 4, 0)
        self.layout.addWidget(self.selected_list, 5, 0)
        self.layout.addWidget(self.module_info, 1, 2, 5, 1)
        self.layout.addLayout(self.footer, 6, 0)
        self.setLayout(self.layout)

        # Connect widgets
        self.available_list.itemSelectionChanged.connect(partial(
            self.on_selection_changed,
            self.available_list
        ))
        self.available_list.item_dropped.connect(self.on_item_dropped)
        self.available_list.version_changed.connect(self.on_version_changed)
        self.selected_list.itemSelectionChanged.connect(partial(
            self.on_selection_changed,
            self.selected_list
        ))
        self.selected_list.item_dropped.connect(self.on_item_dropped)
        self.selected_list.version_changed.connect(self.on_version_changed)
        self.save_button.clicked.connect(self.on_save_clicked)
        self.engine_list.activated.connect(self.on_engine_changed)
        self.env_import.clicked.connect(self.on_env_import_clicked)
        self.env_add.clicked.connect(self.on_env_add_clicked)
        self.env_remove.clicked.connect(self.on_env_remove_clicked)
        self.env_preview.clicked.connect(self.on_env_preview_clicked)
        self.env_lock.clicked.connect(self.on_env_lock_clicked)
        self.env_list.activated.connect(self.on_env_changed)

        # Update initial state from app context
        self.set_state_from_context(app.context)
        self.resize(QtCore.QSize(900, 640))

    def clear_state(self):
        self.state['available'].clear()
        self.state['engines'][:] = []
        self.state['environment'] = None
        self.state['environments'][:] = []
        self.state['selected'].clear()
        self.state['unsaved_changes'] = False

    def set_state_from_context(self, context):
        self.clear_state()

        app.info('Setting state from context: %s', str(context))

        app.info('Collecting environments')
        self.state['environments'] = app.io.get_environments()
        if self.state['environments']:
            self.state['environment'] = self.state['environments'][0]

        app.info('Collecting engines')
        self.state['engines'] = app.io.get_engines()

        app.info('Collecting available cpenv modules')
        for spec_set in app.io.get_module_spec_sets():
            name = spec_set.selection.name
            self.state['available'][name] = spec_set

        app.info('Updating state from environment requires')
        self.update_state()

        app.info('Updating Widgets')
        self.update_widgets()

    def update_state(self):
        if self.state['environment']:
            # Update selected state
            self.state['selected'].clear()

            if not self.state['environment']['sg_requires']:
                return

            requires_text = self.state['environment']['sg_requires']
            requires = app.parse_requires(requires_text)
            module_specs = app.resolve(requires)
            for spec in module_specs:
                spec_set = self.state['available'].get(
                    spec.name,
                    app.ModuleSpecSet([spec])
                )
                spec_set.select_by_version(spec.version.string)
                self.state['selected'][spec.name] = spec_set

    def update_widgets(self):
        '''Update all widgets based on current state.'''

        self.module_info.clear_module_spec()
        self._update_available_list()
        self._update_env_list()
        self._update_env_lock()
        self._update_engine_list()
        self._update_selected_list()
        self.set_saved(message='')

    def _update_env_lock(self):
        is_locked = bool(self.state['environment'].get('sg_permissions_users'))
        icon = [
            QtGui.QIcon(res.get_path('lock_open.png')),
            QtGui.QIcon(res.get_path('lock.png')),
        ][is_locked]
        self.env_lock.setIcon(icon)

    def _update_available_list(self):
        self.available_list.clear()
        for spec_set in self.state['available'].values():
            if spec_set.selection.name in self.state['selected']:
                continue
            self.available_list.add_spec_set(spec_set)

    def _update_env_list(self):
        self.env_list.clear()

        if not self.state['environments']:
            self.env_list.setEnabled(False)
            self.env_list.addItem('No Environments')
        else:
            self.env_list.setEnabled(True)

            for env in self.state['environments']:
                self.env_list.addItem(env['code'])

            if self.state['environment']:
                idx = self.env_list.findText(self.state['environment']['code'])
                if idx != -1:
                    self.env_list.setCurrentIndex(idx)

    def _update_engine_list(self):
        self.engine_list.clear()
        if not self.state['environment']:
            self.engine_list.setEnabled(False)
        else:
            self.engine_list.setEnabled(True)
            if self.state['engines']:
                self.engine_list.addItems(self.state['engines'])
            engine = self.state['environment']['sg_engine']
            idx = self.engine_list.findText(engine)
            if idx != -1:
                self.engine_list.setCurrentIndex(idx)
            else:
                self.engine_list.addItem('Select an Engine')
                self.engine_list.setCurrentIndex(self.engine_list.count() - 1)

    def _update_selected_list(self):
        self.selected_list.clear()
        if not self.state['environment']:
            self.selected_list.setEnabled(False)
        else:
            self.selected_list.setEnabled(True)
            for spec_set in self.state['selected'].values():
                self.selected_list.add_spec_set(spec_set)

    def set_unsaved(self, message='Unsaved changes...'):
        self.message_label.setText(message)
        self.message_label.show()
        self.state['unsaved_changes'] = True
        self.save_button.setEnabled(True)

    def set_saved(self, message='Changes saved.', notify=False):
        self.message_label.hide()
        self.save_button.setEnabled(False)
        self.state['unsaved_changes'] = False

        if notify:
            note = Notice(
                'Changes saved.',
                fg_color="#EEE",
                bg_color="#1694c9",
                parent=self
            )
            note.show_top(self)

    def on_selected_order_changed(self):
        # Reflect user reordering in state
        self.state['selected'].clear()
        for item in self.selected_list.iter_items():
            self.state['selected'][item.text(0)] = item.spec_set

        self.set_unsaved()

    def on_selection_changed(self, widget):
        # Deselect items in the opposite list
        if widget == self.selected_list:
            self.available_list.blockSignals(True)
            self.available_list.clear_selection()
            self.available_list.blockSignals(False)
        else:
            self.selected_list.blockSignals(True)
            self.selected_list.clear_selection()
            self.selected_list.blockSignals(False)

        # Update ModuleInfo panel
        items = widget.selectedItems()
        if items:
            if len(items) == 1:
                spec = items[0].spec_set.selection
                self.module_info.set_module_spec(spec)
        else:
            self.module_info.clear_module_spec()

    def on_env_lock_clicked(self):
        '''Bring up the environment permissions dialog.'''

        try:
            dialog = EnvPermissions(self.state['environment'], self)
            save = dialog.exec_()
            if save:
                self._update_env_lock()
        except Exception:
            error_message = ErrorDialog(
                label='Failed to open Permissions Dialog.',
                message=traceback.format_exc(),
                parent=self,
            )
            error_message.exec_()

    def on_env_preview_clicked(self):
        '''In order to preview an environment we need to take the same steps
        cpenv takes when combining module environments during activation, but,
        we must do so without having the module localized.

        TODO: Because of how complex it is to build the environment preview,
              this aspect of cpenv may need to be refactored.
        '''
        env = self.state['environment']
        home_path = app.cpenv.get_home_modules_path()
        platform = app.cpenv.compat.platform
        pyver = sys.version[:3]
        yaml = app.cpenv.vendor.yaml
        mappings = app.cpenv.mappings

        module_envs = []
        for spec_set in self.state['selected'].values():
            spec = spec_set.selection
            config_vars = {
                'MODULE': '/'.join([home_path, spec.qual_name]),
                'PLATFORM': platform,
                'PYVER': pyver,
            }
            # 1. read environment from Module entity
            module_env = spec.repo.get_data(spec)['environment']
            # 2. Dump to string
            module_env = yaml.safe_dump(module_env)
            # 3. Substitute config variables
            module_env = Template(module_env).safe_substitute(config_vars)
            # 4. Load as dict
            module_env = yaml.safe_load(module_env)
            module_envs.append(module_env)

        # Combine all module environments
        preview_dict = mappings.join_dicts(*module_envs)
        preview_env = mappings.dict_to_env(preview_dict)
        preview_env = mappings.expand_envvars(preview_env)

        try:
            dialog = EnvDisplay(
                title='Previewing Environment:  %s' % env['code'],
                data=preview_env,
                parent=self,
            )
            dialog.show()
        except Exception:
            error_message = ErrorDialog(
                label='Failed to preview environment.',
                message=traceback.format_exc(),
                parent=self,
            )
            error_message.exec_()

    def on_env_remove_clicked(self):

        env = self.state['environment']

        response = QtGui.QMessageBox.question(
            self,
            'Delete Environment',
            'Are you sure you want to delete %s?' % env['code'],
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
        )
        if response == QtGui.QMessageBox.No:
            return

        try:
            app.io.delete_environment(env['id'])
        except Exception:
            error_message = ErrorDialog(
                label='Failed to delete environment.',
                message=traceback.format_exc(),
                parent=self,
            )
            error_message.exec_()
            return

        self.state['environments'].remove(env)
        if self.state['environments']:
            self.state['environment'] = self.state['environments'][0]
        else:
            self.state['environment'] = None

        self.update_state()
        self.update_widgets()

    def on_env_add_clicked(self):
        env_names = [e['code'] for e in self.state['environments']]
        while True:
            name, ok = QtGui.QInputDialog.getText(
                self,
                'Add environment',
                'Environment Name:',
            )
            if ok and name in env_names:
                error_message = ErrorDialog(
                    label='Environment already exists:',
                    message='Please choose another name.',
                    parent=self,
                )
                error_message.exec_()
            elif ok:
                # Exit retry loop
                break
            else:
                # Canceled
                return

        new_env = app.io.update_environment(
            code=name,
            engine='',
            requires='',
            project=app.context.project,
        )
        self.state['environments'].append(new_env)
        self.state['environment'] = new_env

        # Update state and ui
        self.update_state()
        self.update_widgets()

    def on_env_import_clicked(self):
        app.info('Import clicked.')
        importer = EnvImporter(self)
        accepted = importer.exec_()
        if accepted:
            # Refresh the entire UI
            self.set_state_from_context(app.context)

    def on_env_changed(self, index):
        env = self.state['environment']
        if self.state['unsaved_changes']:
            response = QtGui.QMessageBox.question(
                self,
                'Unsaved Changes...',
                'Discard unsaved changes to %s?' % env['code'],
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            )
            if response == QtGui.QMessageBox.No:
                idx = self.env_list.findText(env['code'])
                if idx != -1:
                    self.env_list.setCurrentIndex(idx)
                return

        self.state['environment'] = self.state['environments'][index]
        self.update_state()
        self.update_widgets()

    def on_engine_changed(self, index):
        if self.state['environment']:
            engine = self.engine_list.itemText(index)
            if engine != self.state['environment']['sg_engine']:
                self.set_unsaved()

    def on_version_changed(self, spec_set):
        if self.module_info._spec:
            if spec_set.selection.name == self.module_info._spec.name:
                self.module_info.set_module_spec(spec_set.selection)

        app.info(spec_set.selection.name)
        app.info(', '.join(self.state['selected']))
        if spec_set.selection.name in self.state['selected']:
            self.set_unsaved()

    def on_item_dropped(self):

        old_keys = list(self.state['selected'].keys())
        new_keys = []

        self.state['selected'].clear()

        # Update selected state
        for item in self.selected_list.iter_items():
            module_name = item.text(0)
            new_keys.append(module_name)
            self.state['selected'][module_name] = item.spec_set

        if new_keys != old_keys:
            self.set_unsaved()

    def on_save_clicked(self):
        # Get a list of requirements
        requires = []
        for spec_set in self.state['selected'].values():
            requires.append(spec_set.selection.qual_name)

        env = self.state['environment']

        try:
            app.info(
                ('Saving %s:\n' % env['code'])
                + '\n'.join(requires)
            )
            upd_env = app.io.update_environment(
                code=env['code'],
                engine=self.engine_list.currentText(),
                requires=' '.join(requires),
                project=env.get('project', app.context.project),
                id=env.get('id', None)
            )
            # Update env in state
            env.update(upd_env)
            self.set_saved(notify=True)
        except Exception:
            message = 'Failed to save Environment changes.'
            error_message = ErrorDialog(
                label=message,
                message=traceback.format_exc(),
                parent=self,
            )
            error_message.exec_()
            app.execption(message)
