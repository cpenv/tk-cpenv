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

    # TODO: This is a very useful class - should be moved into cpenv to be
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

        self.cpenv.set_reporter(_UIReporter(self, self.engine))

        # Setup ShotgunRepo
        self.io = CpenvIO(self)

        try:
            # Check if we should register this app by comparing
            # deny_ui_permissions to the user's permission group
            # deny_ui_permissions via info.yml only works for tk-shotgun
            filters = [['id', 'is', self.context.user['id']]]
            fields = ['permission_rule_set']
            user_data = self.shotgun.find_one('HumanUser', filters, fields)
            permission_group = user_data.get('permission_rule_set')['name']
            
            if permission_group in self.get_setting('deny_ui_permissions'):
                self.logger.warning("{}'s permission group ({}) does not have permission to access this app because of deny_ui_permissions. Not loading app!".format(self.context.user['name'], permission_group))
                return
        except Exception as e:
            self.logger.error(e)
            return

        try:
            # Check if we should register this app by comparing
            # deny_ui_platforms to the current platform
            # deny_ui_platforms via info.yml only works for tk-shotgun
            current_platform = None
            if sgtk.util.is_windows():
                current_platform = 'windows'
            if sgtk.util.is_macos():
                current_platform = 'mac'
            if sgtk.util.is_linux():
                current_platform = 'linux'

            if current_platform in self.get_setting('deny_ui_platforms'):
                self.logger.warning('This app is not allowed to load (deny_ui_platforms) from {}!'.format(current_platform))
                return
        except Exception as e:
            self.logger.error(e)   
            return     

        # Register Set Modules command to show the ModuleSelector dialog
        self.engine.register_command(
            self.get_setting('display_name'),
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

    def show_environment_selector(self, environments):
        '''Show the EnvSelector dialog.'''

        try:
            dialog, widget = self.engine._create_dialog_with_widget(
                title='tk-cpenv',
                bundle=self,
                widget_class=self.ui.env_selector.EnvSelector,
                environments=environments,
            )
            dialog.setMinimumWidth(300)
            dialog.resize(1, 1)
            dialog.exec_()
            return widget.state['choice']
        except:
            self.exception('Error!')

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

    def clear_active_modules(self):
        self.cpenv.api._active_modules[:] = []

    def activate(self, requirements):
        '''Wraps cpenv.activate'''

        self.debug('Activating modules...')
        try:

            # Clear existing modules first
            self.clear_active_modules()

            return self.cpenv.activate(requirements)

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

        self.debug('Module paths set to %s' % os.getenv('CPENV_MODULE_PATHS'))

    def before_app_launch(
        self,
        app_path,
        app_args,
        version,
        engine_name,
        software_entity,
        **kwargs
    ):
        '''Call in your tk-multi-launchapp before_app_launch Hook to
        activate modules you have configured for your project.

        See Also:
            example_config/hooks/before_app_launch.py
        '''

        try:
            self._before_app_launch(
                app_path,
                app_args,
                version,
                engine_name,
                software_entity,
                **kwargs
            )
        except Exception:
            self.exception('tk-cpenv before_app_launch failed.')
            self.show_error(
                label='tk-cpenv before_app_launch failed.',
                message=traceback.format_exc(),
            )

    def _before_app_launch(
        self,
        app_path,
        app_args,
        version,
        engine_name,
        software_entity,
        **kwargs
    ):
        '''Call in your tk-multi-launchapp before_app_launch Hook to
        activate modules you have configured for your project.

        See Also:
            example_config/hooks/before_app_launch.py
        '''

        # Set module paths from shotgun setting
        module_paths = self.get_setting('module_paths') or []
        self.set_module_paths(module_paths)

        # Get engine or software code
        software = None
        engine = engine_name
        if software_entity:
            software = software_entity.get('code')
            engine = software_entity.get('engine', engine_name)

        # Get Environment for engine
        environments = self.io.get_environments(
            software=software,
            engine=engine,
            user=self.context.user,
            software_versions=version,
        )
        if not environments:
            self.debug('Found no Environment for %s.' % engine)
            return

        self.debug('Found Environments: %s', environments)

        if len(environments) == 2:
            env = self.show_environment_selector(environments)
        else:
            env = environments[0]

        # Get Environment requirements
        requires_str = env['sg_requires']
        if not requires_str:
            self.debug('Environment %s has no requirements.' % env['code'])
            return

        # Parse Environment requirements
        requires = self.parse_requires(requires_str)
        modules = self.activate(requires)
        self.debug('Modules: %s' % [m.qual_name for m in modules])


class CpenvIO(object):
    '''Handles all IO operations for tk-cpenv.'''

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
                ['archived', 'is', False],
            ],
            fields=['name', 'id', 'type'],
        )
        if not entities:
            return []
        return list(sorted(entities, key=lambda e: e['name']))

    def get_environment(
        self,
        project=None,
        software=None,
        engine=None,
        name=None,
        user=None,
        requires=None,
        software_versions=None,
    ):
        '''Get an Environment for the specified engine and project.

        Arguments:
            project (dict): Project data (default: context.project)
            engine (str): toolkit engine name like tk-maya
            name (str): Name of the environment to lookup

        Returns:
            dict: Environment entity
        '''

        if (name, engine) == (None, None):
            raise ValueError('Missing required argument: name or engine')

        filters = [['project', 'is', project or self.app.context.project]]
        if user:
            filters.append({
                'filter_operator': 'any',
                'filters': [
                    ['sg_permissions_users', 'is', user],
                    ['sg_permissions_users', 'is', None],
                ]
            })
        if software or engine:
            sw_engine_filters = []
            if software:
                sw_engine_filters.append(['sg_engine', 'is', software])
            if engine:
                sw_engine_filters.append(['sg_engine', 'is', engine])
            sw_engine_filters = {
                'filter_operator': 'any',
                'filters': sw_engine_filters,
            }
            filters.append(sw_engine_filters)
        if name:
            filters.append(['code', 'is', name])
        if requires:
            filters.append(['sg_requires', 'contains', requires])
        if software_versions:
            filters.append(
                ['sg_software_versions', 'contains', software_versions]
            )

        return self.shotgun.find_one(
            self.environment_entity,
            filters=filters,
            fields=[
                'code',
                'id',
                'project',
                'sg_engine',
                'sg_permissions_users',
                'sg_requires',
                'sg_software_versions',
            ],
        )

    def get_environments(
        self,
        project=None,
        software=None,
        engine=None,
        name=None,
        user=None,
        requires=None,
        software_versions=None,
    ):
        '''Get a list Environment entities for a project.

        Arguments:
            project (dict): Project data (default: context.project)
            engine (str): toolkit engine name like tk-maya
            name (str): Name of the environment to lookup
            user (dict): User data
            requires (str): A module requirement to lookup

        Returns:
            list[dict]: Environment entities sorted by code(name).
        '''

        filters = [['project', 'is', project or self.app.context.project]]
        if user:
            filters.append({
                'filter_operator': 'any',
                'filters': [
                    ['sg_permissions_users', 'is', user],
                    ['sg_permissions_users', 'is', None],
                ]
            })
        if software or engine:
            sw_engine_filters = []
            if software:
                sw_engine_filters.append(['sg_engine', 'is', software])
            if engine:
                sw_engine_filters.append(['sg_engine', 'is', engine])
            sw_engine_filters = {
                'filter_operator': 'any',
                'filters': sw_engine_filters,
            }
            filters.append(sw_engine_filters)
        if name:
            filters.append(['code', 'is', name])
        if requires:
            filters.append(['sg_requires', 'contains', requires])
        if software_versions:
            filters.append({
                'filter_operator': 'any',
                'filters': [
                    ['sg_software_versions', 'contains', software_versions],
                    ['sg_software_versions', 'is', None],
                ]
            })

        entities = self.shotgun.find(
            self.environment_entity,
            filters=filters,
            fields=[
                'code',
                'id',
                'project',
                'sg_engine',
                'sg_permissions_users',
                'sg_requires',
                'sg_software_versions',
            ],
        )
        if not entities:
            return []

        return list(sorted(entities, key=lambda e: e['code']))

    def set_environment_permissions(self, id, users):
        '''Set the permissions for an environment with the specified id.

        Arguments:
            id (int): Id of Environment to update.
            users (list): List of User Entities to add to sg_permissions_users.
        '''

        self.shotgun.update(
            entity_type=self.environment_entity,
            entity_id=id,
            data={'sg_permissions_users': users}
        )

    def update_environment(
        self,
        code,
        engine,
        requires,
        software_versions,
        project,
        id=None,
    ):
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
            'sg_software_versions': software_versions,
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

    def duplicate_environment(self, code, entity):
        '''Duplicate an environment with a new code.'''

        data = dict(entity)
        data.pop('type', None)
        data.pop('id', None)
        data['code'] = code

        new_entity = self.shotgun.create(
            self.environment_entity,
            data=data,
            return_fields=[
                'code',
                'id',
                'project',
                'sg_engine',
                'sg_permissions_users',
                'sg_requires',
                'sg_software_versions',
            ],
        )
        return new_entity

    def delete_environment(self, id):
        '''Delete an Environment by id.'''

        self.shotgun.delete(
            self.environment_entity,
            id,
        )

    def get_engines(self):
        '''Get a list of engine names and codes from configured Software entities.

        Prior to 0.5.10, this method only returned engine names. However, some Software
        entities do not have toolkit engines, so we now return software codes as well.
        '''

        entities = self.shotgun.find(
            'Software',
            filters=[['sg_status_list', 'is', 'act']],
            fields=['engine', 'code'],
        )
        if not entities:
            return []

        entities = sorted(entities, key=lambda e: e.get('code', e.get('engine', '')))
        results = []
        for entity in entities:
            if entity.get('code') and entity.get('code') not in results:
                results.append(entity['code'])
            if entity.get('engine') and entity.get('engine') not in results:
                results.append(entity['engine'])
        return list(results)

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
