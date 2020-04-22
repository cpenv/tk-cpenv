# Standard library imports
import os

# Shotgun imports
from sgtk.platform import Application


class CpenvApp(Application):

    def init_app(self):
        self._ui = self.import_module('cpenv_ui')
        self._cpenv = self.import_module('cpenv')
        self.engine.register_command(
            'Set Modules',
            self.show_dialog
        )

    def show_dialog(self):
        '''Show the ModuleSelector dialog.'''
        self._ui.module_selector.show(self)

    def set_module_paths(self, module_paths):
        '''Set additional paths to use for looking up cpenv modules.'''

        new_module_paths = self._cpenv.get_module_paths()
        for module_path in module_paths[::-1]:
            if module_path not in new_module_paths:
                new_module_paths.insert(0, module_path)
        os.environ['CPENV_MODULE_PATHS'] = os.pathsep.join(new_module_paths)

    def get_modules(self):
        '''Wraps cpenv.get_modules'''

        return self._cpenv.get_modules()

    def get_active_modules(self):
        '''Wraps cpenv.get_modules'''

        return self._cpenv.get_active_modules()

    def get_project_modules(self, project_path):
        '''Return a list of modules this project has set.'''
        try:
            resolver = self._cpenv.resolve(project_path)
        except self._cpenv.ResolveError:
            self.logger.error(
                'Failed to resolve modules for %s',
                project_path
            )
            return []
        return resolver.resolved

    def set_project_modules(self, project_path, modules):
        '''Write modules to the projects root directory.'''

        module_path = os.path.join(project_path, '.cpenv')
        self.logger.debug('Writing modules to %s', module_path)
        with open(module_path, 'w') as f:
            f.write('\n'.join(modules))

    def resolve(self, *args, **kwargs):
        '''Wraps cpenv.resolve'''

        return self._cpenv.resolve(*args, **kwargs)

    def activate(self, *args, **kwargs):
        '''Wraps cpenv.activate'''

        return self._cpenv.activate(*args, **kwargs)

    def before_app_launch(self, app_path, app_args, version, engine_name,
                          software_entity=None, **kwargs):
        '''Call in your tk-multi-launchapp before_app_launch Hook to
        activate modules you have configured for your project.'''

        # Set module paths from shotgun setting
        module_paths = self.get_setting('module_paths') or []
        self.set_module_paths(module_paths)

        # If the enging_name is in the enabled_engines activate modules.
        enabled_engines = self.get_setting('enabled_engines') or []
        if engine_name in enabled_engines:
            modules = self.activate(self.tank.project_path)
            self.logger.debug('Activated: %s', str([m.name for m in modules]))
        else:
            self.logger.debug(
                'Skipping activation - %s not in enabled_engines(%s).',
                engine_name,
                enabled_engines
            )
