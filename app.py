# Standard library imports
import os
import traceback

# Shotgun imports
import sgtk


class ModuleSpecSet(object):
    '''A set of ModuleSpecs.

    Maintains a selection of one of the ModuleSpecs in the set. Used to manage
    multiple versions of a single Module.
    '''

    # TODO: This is a very useful class - should be moved into the cpenv to be
    #       used in a standalone cpenv qt application.

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

    def init_app(self):
        self.ui = self.import_module('cpenv_ui')
        self.cpenv = self.import_module('cpenv')

        # Setup UIReporter
        class _UIReporter(self.ui.UIReporter, self.cpenv.Reporter):
            '''Mix UIReporter with Reporter base class and inject deps.'''
            app = self
            engine = self.engine

        self.cpenv.set_reporter(_UIReporter)

        # Setup ShotgunRepo
        self.io = CpenvIO(self)

        # Register Set Modules command to show the ModuleSelector dialog
        self.engine.register_command(
            'Set Modules',
            self.show_module_selector,
        )

    def show_error(self, label, message):
        return self.engine.show_modal(
            title='tk-cpenv Error',
            bundle=self,
            widget_class=self.ui.dialogs.ErrorDialog,
            label=label,
            message=message,
        )

    def show_module_selector(self):
        '''Show the ModuleSelector dialog.'''

        self.ui.module_selector.show(self)

    def info(self, message, *args):
        '''Log info prefixed with tk-cpenv:'''

        self.logger.info('tk-cpenv: %s' % (message % args))

    def debug(self, message, *args):
        '''Log debug prefixed with tk-cpenv:'''

        self.logger.debug('tk-cpenv: %s' % (message % args))

    def error(self, message, *args):
        '''Log error prefixed with tk-cpenv:'''

        self.logger.error('tk-cpenv: %s' % (message % args))

    def exception(self, message, *args):
        '''Log exception prefixed with tk-cpenv:'''

        self.logger.exception('tk-cpenv: %s' % (message % args))

    def parse_requires(self, requires):
        '''Wraps cpenv.parse_redirect'''

        self.debug('Parsing %s' % requires)
        try:
            return self.cpenv.parse_redirect(requires)
        except Exception:
            self.exception('Failed to parse cpenv modules.')
            raise

    def resolve(self, *args, **kwargs):
        '''Wraps cpenv.resolve'''

        self.debug('Resolving %s' % args)
        try:
            return self.cpenv.resolve(*args, **kwargs)
        except Exception:
            self.exception('Failed to resolve cpenv modules.')
            raise

    def activate(self, *args, **kwargs):
        '''Wraps cpenv.activate'''

        self.debug('Activating modules...')
        try:
            return self.cpenv.activate(*args, **kwargs)
        except Exception:
            self.exception('Failed to activate cpenv modules.')
            raise

    def set_module_paths(self, module_paths):
        '''Set additional paths to use for looking up cpenv modules.'''

        new_module_paths = self.cpenv.get_module_paths()
        for module_path in module_paths[::-1]:
            if module_path not in new_module_paths:
                new_module_paths.insert(0, module_path)
        os.environ['CPENV_MODULE_PATHS'] = os.pathsep.join(new_module_paths)

        self.debug('set module paths to %s' % os.getenv('CPENV_MODULE_PATHS'))

    def before_app_launch(
        self,
        app_path,
        app_args,
        version,
        engine_name,
        software_entity=None,
        **kwargs
    ):
        '''Call in your tk-multi-launchapp before_app_launch Hook to
        activate modules you have configured for your project.

        See Also:
            example_config/hooks/before_app_launch.py
        '''

        self.debug('Running before_app_launch')

        # Set module paths from shotgun setting
        module_paths = self.get_setting('module_paths') or []
        self.set_module_paths(module_paths)

        # If the engine is in the enabled_engines activate modules.
        engine = software_entity.get('engine', engine_name)
        env = self.io.get_environment(engine=engine)
        if not env:
            self.debug('Found no environment for %s.' % engine)
            return

        requires = env['sg_requires']
        if not requires:
            self.debug('Environment %s has no requirements.' % env['code'])
            return

        self.debug('Activating environment "%s"' % env['code'])
        modules = self.activate(self.cpenv.parse_redirect(requires))
        self.debug('Modules: %s' % [m.qual_name for m in modules])


class CpenvIO(object):
    '''Handles all IO operations for CpenvApplication.'''

    def __init__(self, app):
        self.app = app
        self.cpenv = app.cpenv
        self.shotgun = app.shotgun
        self.module_entity = app.get_setting('module_entity')
        self.environment_entity = app.get_setting('environment_entity')
        self.repo = app.cpenv.ShotgunRepo(
            name='tk-cpenv',
            api=app.shotgun,
            module_entity=self.app.get_setting('module_entity'),
        )
        app.cpenv.add_repo(self.repo)

    def get_projects(self):
        '''Get a list of all active projects sorted by name.'''

        entities = self.shotgun.find(
            'Project',
            filters=[
                ['is_demo', 'is', False],
                ['is_template', 'is', False],
                ['archived', 'is', False],
            ],
            fields=['name', 'id', 'type'],
        )
        if not entities:
            return []
        return list(sorted(entities, key=lambda e: e['name']))

    def get_environment(self, name=None, engine=None, project=None):
        '''Get an Environment for the specified engine and project.

        Arguments:
            engine (str): toolkit engine name like tk-maya
            project (dict): Project data (default: context.project)
            name (str): Name of the environment to lookup

        Returns:
            dict: Environment entity
        '''

        if (name, engine) == (None, None):
            raise ValueError('Missing required argument: name or engine')

        # Build filters
        filters = [['project', 'is', project or self.app.context.project]]
        if name:
            filters.append(['code', 'is', name])
        if engine:
            filters.append(['sg_engine', 'is', engine])

        return self.shotgun.find_one(
            self.environment_entity,
            filters=filters,
            fields=['code', 'sg_engine', 'id', 'sg_requires', 'project'],
        )

    def get_environments(self, project=None):
        '''Get a list Environment entities for a project.

        Arguments:
            project (dict): Project data (default: context.project)

        Returns:
            list[dict]: Environment entities sorted by code(name).
        '''

        entities = self.shotgun.find(
            self.environment_entity,
            filters=[['project', 'is', project or self.app.context.project]],
            fields=['code', 'sg_engine', 'id', 'sg_requires', 'project'],
        )
        if not entities:
            return []

        return list(sorted(entities, key=lambda e: e['code']))

    def update_environment(self, code, engine, requires, project, id=None):
        '''Create or update an environment.

        Arguments:
            code (str): Name of the Environment to create
            engine (str): Toolkit engine that the env applies to
            requires (str): Space separated list of module requirements
            project (dict): Project data including id key
            id (int): Id of Environment to update. Will attempt to find an id
                if none is provided using code and project. If an id is not
                found a new Environment will be created.

        Returns:
            dict: Environment data
        '''

        entity_type = self.environment_entity
        data = {
            'code': code,
            'sg_engine': engine,
            'sg_requires': requires,
            'project': project,
        }

        if not id:
            entity = self.shotgun.find_one(
                entity_type,
                filters=[
                    ['code', 'is', code],
                    ['project', 'is', project or self.app.context.project],
                ],
            )
            if entity:
                id = entity['id']

        if id:
            entity = self.shotgun.update(
                entity_type,
                entity_id=id,
                data=data,
            )
        else:
            entity = self.shotgun.create(
                entity_type,
                data=data,
            )
        return entity

    def delete_environment(self, id):
        '''Delete an Environment by id.'''

        self.shotgun.delete(
            self.environment_entity,
            id,
        )

    def get_engines(self):
        '''Get a list of engine names from configured Software entities.'''

        entities = self.shotgun.find('Software', [], ['engine'])
        if not entities:
            return []

        return list(
            sorted(set([e['engine'] for e in entities if e['engine']]))
        )

    def get_module_spec_sets(self):
        '''Get a list of all the Modules stored in Shotgun.

        Returns:
            list[ModuleSpecSet]: each ModuleSpecSet contains all versions
                of a particular Module.
        '''

        sets = {}
        for module_spec in self.repo.list():
            spec_set = sets.setdefault(
                module_spec.name,
                ModuleSpecSet([module_spec])
            )
            spec_set.add(module_spec)

        return list(sets.values())
