# -*- coding: utf-8 -*-
from __future__ import print_function, division

# Shotgun imports
from sgtk.platform.qt import QtCore, QtGui

# Local imports
from . import res


class ProgressDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)

        # Window options
        self.setWindowTitle('tk-cpenv')
        self.setWindowIcon(QtGui.QIcon(res.get_path('module_dark_256.png')))
        self.setWindowFlags(
            self.windowFlags()
            | QtCore.Qt.WindowStaysOnTopHint
        )
        self.hide_timer = None

        # Layout widgets
        self.label = QtGui.QLabel('Starting...')
        self.progress = QtGui.QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(True)
        self.progress.setAlignment(QtCore.Qt.AlignCenter)
        self.progress.setFormat('starting')
        self.frame = QtGui.QLabel()
        self.button = QtGui.QPushButton('Cancel')
        self.button.setSizePolicy(
            QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Maximum,
        )
        self.button.clicked.connect(self.cancel)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.button)
        self.layout.setAlignment(self.button, QtCore.Qt.AlignRight)
        self.setLayout(self.layout)

    def pump(self):
        app = QtGui.QApplication.instance()
        app.processEvents()

    def value(self):
        return self.progress.value()

    def max_value(self):
        return self.progress.maximum()

    def show(self):
        super(ProgressDialog, self).show()
        if self.hide_timer:
            self.hide_timer.stop()
            self.hide_timer = None

    def hide(self):
        self.hide_timer = QtCore.QTimer()
        self.hide_timer.timeout.connect(super(ProgressDialog, self).hide)
        self.hide_timer.setSingleShot(2000)
        self.hide_timer.start()

    def set_label(self, text):
        self.label.setText(text)
        self.pump()

    def set_frame(self, text):
        self.frame.setText(text)
        self.pump()

    def set_progress(self, chunk_size=None, max_size=None):
        if max_size:
            self.progress.setRange(0, max_size)
            self.progress.setValue(0)
            self.progress.setFormat('0%')
        if chunk_size:
            value = self.progress.value() + chunk_size
            percent = (value / self.progress.maximum()) * 100
            self.progress.setValue(value)
            self.progress.setFormat('{:0.0f}%'.format(percent))
        self.pump()

    def error(self, label, message):
        self.label.setText('Error.')
        QtCore.QTimer.singleShot(1000, self.reject)
        error_message = ErrorDialog(label, message, self.parent())
        error_message.exec_()

    def cancel(self):
        self.label.setText('Cancelling...')
        self.reject()
        raise RuntimeError(self.label.text() + ' cancelled.')

    def accept(self):
        super(ProgressDialog, self).accept()
        self.close()

    def reject(self):
        super(ProgressDialog, self).reject()
        self.close()

    @property
    def hide_tk_title_bar(self):
        return True


class ErrorDialog(QtGui.QDialog):

    def __init__(self, label, message, parent=None):
        super(ErrorDialog, self).__init__(parent)

        self.setWindowTitle('tk-cpenv Error')
        self.setWindowIcon(QtGui.QIcon(res.get_path('module_dark_256.png')))
        self.setWindowFlags(
            self.windowFlags()
            | QtCore.Qt.WindowStaysOnTopHint
        )

        self.label = QtGui.QLabel(label)
        self.text = QtGui.QPlainTextEdit(message)
        self.text.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)

        self.button = QtGui.QPushButton('Dismiss')
        self.button.setSizePolicy(
            QtGui.QSizePolicy.Maximum,
            QtGui.QSizePolicy.Maximum,
        )
        self.button.clicked.connect(self.accept)

        self.layout = QtGui.QVBoxLayout()
        self.layout.setStretch(1, 1)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.setAlignment(self.button, QtCore.Qt.AlignRight)
        self.setLayout(self.layout)

    def accept(self):
        super(ErrorDialog, self).accept()
        self.close()

    def reject(self):
        super(ErrorDialog, self).reject()
        self.close()

    @property
    def hide_tk_title_bar(self):
        return True
