# tk-cpenv
Integrates cpenv with Shotgun Toolkit.

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

# Configuring tk-cpenv
The example_config folder includes all modifications you need to make to your
Shotgun Toolkit config in order to get cpenv working. 

## tk-cpenv settings
- **enabled_engines**: List of engines that tk-cpenv will activate modules for.
- **home_path**: Where to store modules locally. Defaults to a local path available across all users on your machine. You may choose to use a network location here, so that all users in a network share modules.
- **module_paths**: List of additional paths used to lookup modules. Can be useful when developing modules.
- **module_entity**: Name of the CustomNonProjectEntity named "Module".

You will need to customize the value of the module_entity config key when you enable a CustomNonProjectEntity in the next section.

## Enable a CustomNonProjectEntity named Module
1. Browse to site-preferences
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/1_site_prefs.png" width="256"/>
2. Expand the entities section.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/2_entities.png" width="640"/>
3. Enable the first available CustomNonProjectEntity with the following settings. Set the value of module_entity in your tk-cpenv settings(env/includes/settings) to the original name of the entity (CustomNonProjectEntity##).
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/3_module_entity.png" width="640"/>
4. Add the following fields to the Module Entity.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/4_module_fields.png" width="640"/>
