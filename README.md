# tk-cpenv
Integrates [cpenv](https://github.com/cpenv/cpenv) with Shotgun Toolkit.

<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/set_modules_dialog.png" width="80%"/>

cpenv is used to manage plugins, project dependencies and environment
variables through the use of modules. Modules are simple folders containing a
dependency like Arnold for Maya and a module.yml file that includes
environment variables. Modules can be as complex or as simple as you would
like.

The simplest module is a folder containing a module.yml that sets some
environment variables.

A complex module may include all platform varieties of a particular plugin.
The module.yml file can set environment variables that use the $PLATFORM
variable to choose which plugin to provision at runtime.

# Features
- Store modules directly in your shotgun site
- Localize modules when launching applications
- Build Environments (a list of modules) to be activated per job and toolkit engine.
- Drag and drop modules to build environments.
- Import Environments from other jobs, making it easy to setup new jobs.

# Configuring tk-cpenv
The example_config folder includes modifications you need to make to your
Shotgun Toolkit config in order to get cpenv working. The module_entity and
environment_entity keys will be specific to your shotgun site.

## tk-cpenv settings
- **home_path**: Where to store modules locally. Defaults to a local path available across all users on your machine. You may choose to use a network location here, so that all users in a network share modules.
- **module_paths**: List of additional paths used to lookup modules. Can be useful when developing modules.
- **module_entity**: Name of the CustomNonProjectEntity named "Module".
- **environment_entity**: Name of the CustomEntity named "Environment".

## Enable Module and Environment custom entities
1. Browse to site-preferences
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/1_site_prefs.png" width="256"/>
2. Expand the entities section.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/2_entities.png" width="640"/>
3. Enable the first available CustomNonProjectEntity with the following settings.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/3_module_entity.png" width="640"/>
4. Enable the first available CustomEntity with the following settings.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/3_environment_entity.png" width="640"/>

## Add fields to your new entities
1. Add the following fields to the Module Entity.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/4_module_fields.png" width="640"/>
2. Add the following fields to the Environment Entity.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/4_environment_fields.png" width="640"/>

## Modify your shotgun toolkit config
1. Open env/includes/settings/tk-cpenv.yml.
2. Set the value of the `module_entity` to match the `CustomNonProjectEntity` you enabled. This would be `CustomNonProjectEntity01` according to the image above.
3. Set the value of the `environment_entity` to match the `CustomEntity` you enabled. This would be `CustomEntity03` according to the image above.

# Developing and publishing modules
The best practice is to use the cpenv cli tool to create, test, and publish
modules to your shotgun site.

[Visit the cpenv repository for more info.](https://github.com/cpenv/cpenv)
