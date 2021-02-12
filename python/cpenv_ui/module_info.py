# -*- coding: utf-8 -*-
from __future__ import print_function

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

# Local imports
from . import res
from .env_tree import EnvTree
from .minimized_list import MinimizedList
from .notice import Notice

app = sgtk.platform.current_bundle()


class FormLabel(QtGui.QLabel):
    '''Right aligned label'''

    def __init__(self, *args, **kwargs):
        super(FormLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)


class ModuleInfo(QtGui.QWidget):

    def __init__(self, parent=None):
        super(ModuleInfo, self).__init__(parent=parent)
        self._spec = None
        self._default_icon = QtGui.QPixmap(res.get_path('module_256.png'))

        self.icon = QtGui.QLabel()
        self.icon.setFixedSize(48, 48)
        self.icon.setScaledContents(True)
        self.icon.setPixmap(self._default_icon)

        self.name = QtGui.QLabel('Module Info')
        self.name.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.description = QtGui.QLabel('')
        self.description.setMinimumHeight(24)
        self.description.setWordWrap(True)
        self.author = QtGui.QLabel('Author')
        self.author.setWordWrap(True)
        self.email = QtGui.QLabel('Email')
        self.email.setWordWrap(True)
        self.version = QtGui.QLabel('Version')
        self.size = QtGui.QLabel('Size')
        self.requires = MinimizedList(parent=self)
        self.requires.setSelectionMode(self.requires.NoSelection)
        self.requires.setFocusPolicy(QtCore.Qt.NoFocus)
        self.requires_copy = QtGui.QToolButton(
            icon=QtGui.QIcon(res.get_path('copy.png'))
        )
        self.requires_copy.setIconSize(QtCore.QSize(10, 10))
        self.requires_copy.setToolTip('Copy requires to clipboard.')
        self.requires_copy.clicked.connect(
            lambda: self.copy_to_clipboard('requires')
        )
        self.environment = EnvTree('module_environment', {}, parent=self)
        self.environment.setSizePolicy(
            QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Expanding,
        )
        self.environment.setFocusPolicy(QtCore.Qt.NoFocus)
        self.environment.setSelectionMode(self.environment.NoSelection)
        self.environment_copy = QtGui.QToolButton(
            icon=QtGui.QIcon(res.get_path('copy.png'))
        )
        self.environment_copy.setIconSize(QtCore.QSize(10, 10))
        self.environment_copy.setToolTip('Copy environment to clipboard.')
        self.environment_copy.clicked.connect(
            lambda: self.copy_to_clipboard('environment')
        )
        header_layout = QtGui.QHBoxLayout()
        header_layout.addWidget(self.icon)
        header_layout.addWidget(self.name)

        info_grid = QtGui.QGridLayout()
        info_grid.setColumnStretch(1, 1)
        info_grid.setRowStretch(7, 1)
        for i in range(7):
            info_grid.setRowMinimumHeight(i, 10)
        info_grid.addWidget(FormLabel('version:'), 0, 0)
        info_grid.addWidget(self.version, 0, 1)
        info_grid.addWidget(FormLabel('author:'), 1, 0)
        info_grid.addWidget(self.author, 1, 1)
        info_grid.addWidget(FormLabel('email:'), 2, 0)
        info_grid.addWidget(self.email, 2, 1)
        info_grid.addWidget(FormLabel('size:'), 3, 0)
        info_grid.addWidget(self.size, 3, 1)
        info_grid.addWidget(FormLabel('requires:'), 4, 0)
        info_grid.addWidget(
            self.requires_copy, 4, 1, alignment=QtCore.Qt.AlignRight
        )
        info_grid.addWidget(self.requires, 5, 0, 1, 2)
        info_grid.addWidget(FormLabel('environment:'), 6, 0)
        info_grid.addWidget(
            self.environment_copy, 6, 1, alignment=QtCore.Qt.AlignRight
        )
        info_grid.addWidget(self.environment, 7, 0, 1, 2)
        info_widget = QtGui.QWidget(parent=self)
        info_widget.setLayout(info_grid)
        self.info = QtGui.QScrollArea(parent=self)
        self.info.setFocusPolicy(QtCore.Qt.NoFocus)
        self.info.setWidgetResizable(True)
        self.info.setWidget(info_widget)
        self.info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.description)
        self.layout.addWidget(self.info)
        self.setLayout(self.layout)
        self.setMinimumWidth(300)
        self.clear_module_spec()

    def clear_module_spec(self):
        self.name.setText('Module Info')
        font = self.name.font()
        font.setPixelSize(24)
        self.name.setFont(font)
        self.description.setText('Select a module to view info.')
        self.icon.setPixmap(self._default_icon)

        # Hide info
        self.info.hide()
        self._spec = None

    def set_module_spec(self, spec):
        # Show info
        self.info.show()
        self._spec = spec

        # Update widget styles
        font = self.name.font()
        font.setPixelSize(24)
        self.name.setFont(font)

        # Set basic metadata
        self._data = spec.repo.get_data(spec)
        self.name.setText(self._data['name'])
        self.version.setText(self._data['version'])
        self.description.setText(self._data['description'])
        self.author.setText(self._data['author'])
        self.email.setText(self._data['email'])

        self.size.setText(self.format_size(self.get_size(spec)))

        # Format requires
        self.requires.clear()
        for require in self._data['requires']:
            self.requires.addItem(str(require))
        self.requires.refresh_size()

        # Format environment
        self.environment.set_data(self._data['environment'])

        # Set icon
        try:
            self.icon.setPixmap(self.get_thumbnail(spec))
        except Exception:
            self.icon.setPixmap(self._default_icon)
            app.exception('Error loading icon from %s', spec)

    def copy_to_clipboard(self, *keys):
        '''Copy module data keys to clipboard as nicely formatted yaml.'''

        data = {key: self._data[key] for key in keys}
        string = app.cpenv.vendor.yaml.safe_dump(
            data,
            default_flow_style=False,
            sort_keys=False,
            indent=4,
            width=79,
        )
        qapp = QtGui.QApplication.instance()
        qapp.clipboard().setText(string)

        if keys == ('environment',):
            message = 'Copied Environment to clipboard.'
        elif keys == ('requires',):
            message = 'Copied Requires to clipboard.'
        else:
            message = 'Copied to clipboard.'

        note = Notice(
            message,
            fg_color="#EEE",
            bg_color="#1694c9",
            parent=self.parent()
        )
        note.show_top(self.parent())

    def get_thumbnail(self, spec):
        '''Download thumbnail and return QPixmap for spec.'''

        icon = spec.repo.get_thumbnail(spec)
        if icon:
            return QtGui.QPixmap(spec.repo.get_thumbnail(spec))
        else:
            return self._default_icon

    def get_size(self, spec):
        '''Query Shotgun for archive size.'''

        return spec.repo.get_size(spec)

    def format_size(self, number_of_bytes):
        '''Human readable size.'''

        value = number_of_bytes
        for unit in ['b', 'kb', 'mb', 'gb']:
            if value < 1024.0:
                return "{:.0f} {}".format(value, unit)
            value /= 1024.0
        return "{:.0f} {}".format(value, unit)


class ContentAwareTextEdit(QtGui.QTextEdit):
    '''QTextEdit widget that expands to it's content.'''

    def __init__(self, *args, **kwargs):
        super(ContentAwareTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.resize_to_content)
        self.setFixedHeight(24)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

    def setText(self, text):
        super(ContentAwareTextEdit, self).setText(text)
        self.resize_to_content()

    def resize_to_content(self):
        height = min(self.document().size().height() + 4, 400)
        self.setFixedHeight(height)
