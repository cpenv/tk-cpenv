# Standard library imports
import os

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui


_log = sgtk.platform.get_logger(__name__)


def show(app_instance):
    '''Show the CpenvModuleSelect for the given app_instance.'''

    app_instance.engine.show_dialog(
        "Set cpenv modules...",
        app_instance,
        ModuleSelector,
    )


class DraggableList(QtGui.QListWidget):
    '''Simple list widget that supports moving items from this list to
    another DraggableList. Emits item_dropped after an item is dropped.'''

    item_dropped = QtCore.Signal()

    def __init__(self, parent=None):
        super(DraggableList, self).__init__(parent=parent)
        self.setSortingEnabled(True)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QtGui.QListWidget.ExtendedSelection)

    def dropEvent(self, event):
        QtCore.QTimer.singleShot(200, self.item_dropped.emit)
        return super(DraggableList, self).dropEvent(event)


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

        _log.info("Launching cpenv module selector...")
        self._app = sgtk.platform.current_bundle()

        # Create widgets
        self.header_label = QtGui.QLabel(self.header_message)
        self.header_label.setWordWrap(True)

        self.available_label = QtGui.QLabel('<b>Available Modules</b>')
        self.available_list = DraggableList(parent=self)

        self.selected_label = QtGui.QLabel('Selected')
        self.selected_list = DraggableList(parent=self)

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
        self.layout.addLayout(self.header, 0, 0, 1, 2)
        self.layout.addWidget(self.available_label, 1, 0)
        self.layout.addWidget(self.available_list, 2, 0)
        self.layout.addWidget(self.selected_label, 1, 1)
        self.layout.addWidget(self.selected_list, 2, 1)
        self.layout.addLayout(self.footer, 3, 0, 1, 2)
        self.setLayout(self.layout)

        # Connect widgets
        self.available_list.item_dropped.connect(self.on_item_dropped)
        self.selected_list.item_dropped.connect(self.on_item_dropped)
        self.save_button.clicked.connect(self.on_save_clicked)

        # Set initial state
        self.state = {
            'available': {},
            'selected': {},
        }
        self.set_state_from_context(self._app.context)

    def set_state_from_context(self, context):
        self.state['available'].clear()
        self.state['selected'].clear()

        _log.info('Setting state from context: %s', str(context))
        project_name = context.project['name']
        self.header_label.setText(self.header_message % project_name)
        self.selected_label.setText(
            '<b>%s</b>' % (project_name + ' Modules')
        )

        _log.info('Collecting active modules for %s', project_name)
        project_modules = self._app.get_project_modules(
            self._app.tank.project_path
        )
        for module in project_modules:
            self.state['selected'][module.name] = module
            self.selected_list.addItem(module.name)

        _log.info(
            'Collecting available cpenv modules from %s',
            os.getenv('CPENV_MODULES'),
        )
        available_modules = self._app.get_modules()
        for module in available_modules:
            self.state['available'][module.name] = module
            if module.name not in self.state['selected']:
                self.available_list.addItem(module.name)

    def on_item_dropped(self):

        old_keys = set(self.state['selected'].keys())
        new_keys = set()
        self.state['selected'].clear()

        # Update selected state
        for i in range(self.selected_list.count()):
            item = self.selected_list.item(i)
            module_name = item.text()
            new_keys.add(module_name)
            module = self.state['available'][module_name]
            self.state['selected'][module_name] = module

        if new_keys != old_keys:
            self.message_label.setText('Unsaved changes...')
            self.message_label.show()
            self.save_button.setEnabled(True)

    def on_save_clicked(self):
        try:
            self._app.set_project_modules(
                self._app.tank.project_path,
                sorted(self.state['selected'].keys()),
            )
            self.message_label.setText('Changes saved.')
        except Exception:
            _log.execption('Failed to save project modules...')
            self.message_label.setText('Failed to save project modules...')

        self.save_button.setEnabled(False)
        self.message_label.show()
        QtCore.QTimer.singleShot(2000, self.message_label.hide)
