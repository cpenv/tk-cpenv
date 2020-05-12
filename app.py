# Standard library imports
import os

# Shotgun imports
import sgtk


class ModuleSpecSet(object):
    '''A set of ModuleSpecs.

    Maintains a selection of one of the ModuleSpecs in the set. Used to manage
    multiple versions of a Module.
    '''

    def __init__(self, module_specs):
        self.module_specs = module_specs
        self.selection = module_specs[0]
        self.selection_index = 0

    def __contains__(self, spec):
        for item in self.module_specs:
            if item.name == spec.name and item.version == spec.version:
                return True
        return False

    def select_by_version(self, version):
        for i, spec in enumerate(self.module_specs):
            if spec.version.string == version:
                self.select(i)
                return i
        raise IndexError('Could not find spec matching %s' % version)

    def index(self, spec):
        return self.module_specs.index(spec)

    def add(self, spec):
        if spec.name != self.selection.name:
            return
        for item in self.module_specs:
            if item.version == spec.version:
                return
        self.module_specs.append(spec)

    def select(self, index):
        self.selection = self.module_specs[index]
        self.selection_index = index


class CpenvApplication(sgtk.platform.Application):

    ModuleSpecSet = ModuleSpecSet

    def info(self, message, *args):
        self.logger.info('tk-cpenv: %s' % (message % args))

    def debug(self, message, *args):
        self.logger.debug('tk-cpenv: %s' % (message % args))

    def error(self, message, *args):
        self.logger.error('tk-cpenv: %s' % (message % args))

    def exception(self, message, *args):
        self.logger.exception('tk-cpenv: %s' % (message % args))

    def init_app(self):
        self._ui = self.import_module('cpenv_ui')
        self._cpenv = self.import_module('cpenv')
        self._repo = self._cpenv.ShotgunRepo(
            name='tk-cpenv',
            api=self.sgtk.shotgun,
        )
        self._cpenv.add_repo(self._repo)
        self.engine.register_command(
            'Set Modules',
            self.show_module_selector,
        )

    def show_module_selector(self):
        '''Show the ModuleSelector dialog.'''

        self._ui.module_selector.show(self)

    def set_module_paths(self, module_paths):
        '''Set additional paths to use for looking up cpenv modules.'''

        new_module_paths = self._cpenv.get_module_paths()
        for module_path in module_paths[::-1]:
            if module_path not in new_module_paths:
                new_module_paths.insert(0, module_path)
        os.environ['CPENV_MODULE_PATHS'] = os.pathsep.join(new_module_paths)

        self.debug('set module paths to %s' % os.getenv('CPENV_MODULE_PATHS'))

    def get_modules(self):
        '''Wraps cpenv.get_modules'''

        return self._cpenv.get_modules()

    def get_module_spec_sets(self):
        '''Get a list of ModuleSpecSets.'''

        sets = {}
        for module_spec in self._repo.list():
            spec_set = sets.setdefault(
                module_spec.name,
                ModuleSpecSet([module_spec])
            )
            spec_set.add(module_spec)
        return list(sets.values())

    def get_active_modules(self):
        '''Wraps cpenv.get_modules'''

        return self._cpenv.get_active_modules()

    def get_project_modules(self, project_path):
        '''Return a list of modules this project has set.'''
        try:
            resolved = self._cpenv.resolve([project_path])
            return resolved
        except self._cpenv.ResolveError as e:
            self.error('Failed to resolve modules from %s' % project_path)
            self.exception(e.message)
            return []

    def set_project_modules(self, project_path, modules):
        '''Write modules to the projects root directory.'''

        module_path = os.path.join(project_path, '.cpenv')
        self.debug('Writing modules to %s' % module_path)
        with open(module_path, 'w') as f:
            f.write('\n'.join(modules))

    def resolve(self, *args, **kwargs):
        '''Wraps cpenv.resolve'''

        self.debug('Resolving %s' % args)
        return self._cpenv.resolve(*args, **kwargs)

    def activate(self, *args, **kwargs):
        '''Wraps cpenv.activate'''

        self.debug('Activating %s' % args)
        return self._cpenv.activate(*args, **kwargs)

    def before_app_launch(self, app_path, app_args, version, engine_name,
                          software_entity=None, **kwargs):
        '''Call in your tk-multi-launchapp before_app_launch Hook to
        activate modules you have configured for your project.'''

        self.debug('Running before_app_launch')

        # Set module paths from shotgun setting
        module_paths = self.get_setting('module_paths') or []
        self.set_module_paths(module_paths)

        # If the engine is in the enabled_engines activate modules.
        enabled_engines = self.get_setting('enabled_engines') or []
        software_entity = software_entity or {}
        if software_entity.get('engine', engine_name) in enabled_engines:
            modules = self.activate([self.tank.project_path])
            self.debug('Activated: %s' % [m.qual_name for m in modules])
        else:
            self.debug(
                'Skipping activation - %s not in enabled_engines(%s).' %
                (engine_name, enabled_engines)
            )
