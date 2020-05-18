# -*- coding: utf-8 -*-
from __future__ import print_function

# Standard library imports
from functools import partial

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

# Local imports
from .module_list import ModuleList
from .module_info import ModuleInfo


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

        self._app = sgtk.platform.current_bundle()
        self._app.info("Launching cpenv module selector...")

        # Set initial state
        self.state = {
            'available': {},  # Full list of available modules
            'selected': {},  # List of modules to activate on app launch
        }

        # Create widgets
        self.header_label = QtGui.QLabel(self.header_message)
        self.header_label.setWordWrap(True)

        self.available_label = QtGui.QLabel('<b>Available Modules</b>')
        self.available_list = ModuleList('available', parent=self)

        self.selected_label = QtGui.QLabel('Selected')
        self.selected_list = ModuleList('selected', parent=self)

        self.module_info = ModuleInfo(parent=self)

        self.message_label = QtGui.QLabel('Unsaved changes....')
        self.message_label.hide()
        self.save_button = QtGui.QPushButton('Save Changes')
        self.save_button.setStyleSheet(self.button_style)
        self.save_button.setEnabled(False)

        # Layout widgets
        self.header = QtGui.QHBoxLayout()
        self.header.addWidget(self.header_label)

        self.footer = QtGui.QHBoxLayout()
        self.footer.setAlignment(QtCore.Qt.AlignRight)
        self.footer.addStretch(1)
        self.footer.addWidget(self.message_label)
        self.footer.addWidget(self.save_button)

        self.layout = QtGui.QGridLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        self.layout.setRowStretch(2, 1)
        self.layout.setColumnStretch(2, 1)
        self.layout.addLayout(self.header, 0, 0, 1, 2)
        self.layout.addWidget(self.available_label, 1, 0)
        self.layout.addWidget(self.available_list, 2, 0)
        self.layout.addWidget(self.selected_label, 1, 1)
        self.layout.addWidget(self.selected_list, 2, 1)
        self.layout.addWidget(self.module_info, 2, 2)
        self.layout.addLayout(self.footer, 3, 0, 1, 3)
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

        # Update initial state from app context
        self.set_state_from_context(self._app.context)

    def set_state_from_context(self, context):
        self.state['available'].clear()
        self.state['selected'].clear()

        self._app.info('Setting state from context: %s', str(context))
        project_name = context.project['name']
        self.header_label.setText(self.header_message % project_name)
        self.selected_label.setText(
            '<b>%s</b>' % (project_name + ' Modules')
        )

        self._app.info('Collecting available cpenv modules')
        for spec_set in self._app.get_module_spec_sets():
            name = spec_set.selection.name
            self.state['available'][name] = spec_set

        self._app.info('Collecting modules for %s', project_name)
        project_modules = self._app.get_project_modules(
            self._app.tank.project_path
        )
        for spec in project_modules:
            spec_set = self.state['available'].get(
                spec.name,
                self._app.ModuleSpecSet([spec])
            )
            spec_set.select_by_version(spec.version.string)
            self.state['selected'][spec.name] = spec_set
            self.selected_list.add_spec_set(spec_set)

        for spec_set in self.state['available'].values():
            if spec_set.selection.name in self.state['selected']:
                continue
            self.available_list.add_spec_set(spec_set)

    def set_unsaved(self, message='Unsaved changes...'):
        self.message_label.setText(message)
        self.message_label.show()
        self.save_button.setEnabled(True)

    def set_saved(self, message='Changes saved.'):
        self.message_label.setText(message)
        self.message_label.show()
        self.save_button.setEnabled(False)
        QtCore.QTimer.singleShot(2000, self.message_label.hide)

    def on_selection_changed(self, widget):

        # Deselect items in the opposite list
        if widget == self.selected_list:
            self._app.info('Selected List changed.')
            self.available_list.blockSignals(True)
            self.available_list.clear_selection()
            self.available_list.blockSignals(False)
        else:
            self._app.info('Available List changed.')
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

    def on_version_changed(self, spec_set):
        if self.module_info._spec:
            if spec_set.selection.name == self.module_info._spec.name:
                self.module_info.set_module_spec(spec_set.selection)

        self._app.info(spec_set.selection.name)
        self._app.info(', '.join(self.state['selected']))
        if spec_set.selection.name in self.state['selected']:
            self.set_unsaved()

    def on_item_dropped(self):
        old_keys = set(self.state['selected'].keys())
        new_keys = set()
        self.state['selected'].clear()

        # Update selected state
        for item in self.selected_list.iter_items():
            module_name = item.text(0)
            new_keys.add(module_name)
            self.state['selected'][module_name] = item.spec_set

        if new_keys != old_keys:
            self.set_unsaved()

    def on_save_clicked(self):
        # Get a list of requirements
        requirements = []
        for spec_set in self.state['selected'].values():
            requirements.append(spec_set.selection.qual_name)

        try:
            self._app.info('Saving modules:\n' + '\n'.join(requirements))
            self._app.set_project_modules(
                self._app.tank.project_path,
                sorted(requirements),
            )
            self.set_saved()
        except Exception:
            self._app.execption('Failed to save project modules...')
            self.set_saved('Failed to save project modules...')
