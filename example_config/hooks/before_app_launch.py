# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Before App Launch Hook

This hook is executed prior to application launch and is useful if you need
to set environment variables or run scripts as part of the app initialization.
"""

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class BeforeAppLaunch(HookBaseClass):
    """
    Hook to set up the system prior to app launch.

    The execute function of the hook will be called prior to starting the
    required application

    # tk-cpenv
    Customized to support activating cpenv modules before launching. CPENV
    is used to provide plugins, modules, and tools at runtime within DCCs like
    maya, nuke, and houdini.

    :param app_path: (str) The path of the application executable
    :param app_args: (str) Any arguments the application may require
    :param version: (str) version of the application being run if set in
        the "versions" settings of the Launcher instance, otherwise None
    :param engine_name (str) The name of the engine associated with the
        software about to be launched.
    :param software_entity: (dict) If set, this is the Software entity
        that is associated with this launch command.
    """

    def execute(self, app_path, app_args, version, engine_name,
                software_entity=None, **kwargs):

        # Add the following lines of code to your before_app_launch hook
        # if you already have one.

        # Here we get the tk-cpenv app from the current engine.
        self.logger.info('Loading tk-cpenv...')
        tk_cpenv = self.parent.engine.apps.get('tk-cpenv')

        # Now we call the before_app_launch method of the tk-cpenv app
        self.logger.info('Running tk-cpenv before_app_launch...')
        try:
            tk_cpenv.before_app_launch(
                app_path,
                app_args,
                version,
                engine_name,
                software_entity,
                **kwargs
            )
        except Exception:
            self.logger.exception('Failed to activate cpenv modules.')
