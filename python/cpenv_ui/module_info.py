# -*- coding: utf-8 -*-
from __future__ import print_function

# Standard library imports
import os

# Shotgun imports
import sgtk
from sgtk.platform.qt import QtCore, QtGui

# Local imports
from . import res


class ModuleInfo(QtGui.QWidget):

    def __init__(self, parent=None):
        super(ModuleInfo, self).__init__(parent=parent)
        self._app = sgtk.platform.current_bundle()
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
        self.requires = ContentAwareTextEdit('')
        self.requires.setTextInteractionFlags(
            QtCore.Qt.TextBrowserInteraction
        )
        self.requires.setFocusPolicy(QtCore.Qt.NoFocus)
        self.environment = ContentAwareTextEdit('')
        self.environment.setTextInteractionFlags(
            QtCore.Qt.TextBrowserInteraction
        )
        self.environment.setFocusPolicy(QtCore.Qt.NoFocus)

        header_layout = QtGui.QHBoxLayout()
        header_layout.addWidget(self.icon)
        header_layout.addWidget(self.name)

        info_form = QtGui.QFormLayout()
        info_form.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        info_form.addRow('version:', self.version)
        info_form.addRow('author:', self.author)
        info_form.addRow('email:', self.email)
        info_form.addRow('size:', self.size)
        info_form.addRow('requires:', QtGui.QLabel(''))
        info_form.addRow(self.requires)
        info_form.addRow(QtGui.QLabel('environment:'))
        info_form.addRow(self.environment)
        info_widget = QtGui.QWidget(parent=self)
        info_widget.setLayout(info_form)
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

        mono = QtGui.QFont('Monospace')
        mono.setStyleHint(QtGui.QFont.TypeWriter)
        self.requires.setFont(mono)
        self.environment.setFont(mono)

        # Set basic metadata
        data = spec.repo.get_data(spec)
        self.name.setText(data['name'])
        self.version.setText(data['version'])
        self.description.setText(data['description'])
        self.author.setText(data['author'])
        self.email.setText(data['email'])

        # TODO: include size in ShotgunRepo.get_data so we only do 1 query.
        self.size.setText(self.format_size(self.get_size(spec)))

        # Format requires
        requires = '\n'.join(data['requires'] or [])
        self.requires.setText(requires)

        # Format environment
        if data['environment']:
            environment = self._app._cpenv.vendor.yaml.safe_dump(
                data['environment'],
                default_flow_style=False,
                sort_keys=False,
                indent=4,
                width=79,
            )
        else:
            environment = ''
        self.environment.setText(environment)

        # Set icon
        try:
            self.icon.setPixmap(self.get_thumbnail(spec))
        except Exception:
            self._app.exception('X')

    def get_thumbnail(self, spec):
        '''Download thumbnail and return QPixmap for spec.'''

        cpenv = self._app._cpenv

        # We need to construct a url since the shotgun api only
        # returns a url for a low res thumbnail.
        base_url = spec.repo.base_url
        thumbnail = '/thumbnail/full/' + '/'.join(spec.path.split('/')[-2:])
        thumbnail_url = base_url + thumbnail

        # Ensure icons cache dir exists
        icons_root = cpenv.get_cache_path('icons')
        if not os.path.isdir(icons_root):
            os.makedirs(icons_root)

        # Download and cache thumbnail locally
        icon_path = cpenv.get_cache_path('icons', spec.qual_name + '_icon.png')
        if not os.path.isfile(icon_path):
            try:
                data = spec.repo.shotgun.download_attachment(
                    {'url': thumbnail_url}
                )
                with open(icon_path, 'wb') as f:
                    f.write(data)
            except Exception:
                return self._default_icon

        return QtGui.QPixmap(icon_path)

    def get_size(self, spec):
        '''Query Shotgun for archive size.'''

        return int(spec.repo.shotgun.find_one(
            spec.repo.module_entity,
            filters=[
                ['code', 'is', spec.name],
                ['sg_version', 'is', spec.version.string]
            ],
            fields=['sg_archive_size'],
        )['sg_archive_size'] or 0)

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
