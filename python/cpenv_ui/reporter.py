# -*- coding: utf-8 -*-

# Local imports
from .dialogs import ProgressDialog


class UIReporter(object):
    '''A reporter for cpenv that displays reports in a ProgresDialog.'''

    def __init__(self):
        self._dialog = None

    @property
    def dialog(self):
        '''Get the ProgressDialog'''

        if self._dialog is None:
            self._dialog = ProgressDialog()
        return self._dialog

    def start_resolve(self, requirements):
        '''Called when a Resolver.resolve is called with some requirements.'''

        max_size = len(requirements)
        self.dialog.show()
        self.dialog.set_label('Resolving requirements')
        self.dialog.set_progress(max_size=max_size)

    def find_requirement(self, requirement):
        '''Called just before attempting to resolve a requirement.'''

        value, max_value = self.dialog.value(), self.dialog.max_value()
        self.dialog.set_frame('{} of {} - {}...'.format(
            value,
            max_value,
            requirement,
        ))

    def resolve_requirement(self, requirement, module_spec):
        '''Called when a a requirement is resolved.'''

        self.dialog.set_progress(chunk_size=1)

    def end_resolve(self, resolved, unresolved):
        '''Called when Resolver.resolve is done.'''

        if unresolved:
            self.dialog.error(
                label='Failed to resolve',
                message='\n  '.join(unresolved),
            )
        else:
            self.dialog.set_label('Done!')
            self.dialog.hide()

    def start_localize(self, module_specs):
        '''Called when Localizer.localize is called with a list of specs.'''

        max_size = len(module_specs)
        self._count = 1
        self._total = max_size
        self.dialog.show()
        self.dialog.set_label('Localizing modules')
        self.dialog.set_progress(max_size=max_size)

    def localize_module(self, module_spec, module):
        '''Called when a module is localized.'''

        self.dialog.set_frame('{} of {} - {}...'.format(
            self._count,
            self._total,
            module_spec.qual_name,
        ))
        self._count += 1

    def end_localize(self, localized):
        '''Called when Localizer.localize is done.'''

        self.dialog.set_label('Localized %s modules!' % len(localized))
        self.dialog.hide()

    def start_progress(self, label, max_size, data):
        '''Called when a download is started.'''
        self.dialog.set_progress(max_size=max_size)

    def update_progress(self, label, chunk_size, data):
        '''Called each time a chunk is downloaded.'''
        self.dialog.set_progress(chunk_size=chunk_size)

    def end_progress(self, label, data):
        '''Called when a download is finished.'''
