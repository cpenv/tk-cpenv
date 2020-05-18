# tk-cpenv
Integrates cpenv with Shotgun Toolkit.

<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/set_modules_dialog.png" width="425"/>

cpenv is used to manage plugins, project dependencies and environment
variables through the use of modules. Modules are simple folders containing a
dependency like Arnold for Maya and a module.yaml file that includes
environment variables. Modules can be as complex or as simple as you would
like.

The simplest module is a folder containing a module.yaml.

A complex module may include all platform varieties of a particular plugin.
The module.yaml file can set environment variables that use the $PLATFORM
variable to choose which plugin to provision at runtime.

# Configuring tk-cpenv
The example_config folder includes all modifications you need to make to your
Shotgun Toolkit config in order to get cpenv working. You will need to customize the value of the module_entity config key to when you enable a CustomNonProjectEntity in the next section.

## Enable a CustomNonProjectEntity named Module
1. Browse to site-preferences
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/1_site_prefs.png" width="242"/>
2. Expand the entities section.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/2_entities.png" width="643"/>
3. Enable the first available CustomNonProjectEntity with the following settings. Use the original name of the field (CustomNonProjectEntity##) as the value of the module_entity field of tk-cpenv in your shotgun config.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/3_module_entity.png" width="738"/>
4. Add the following fields to the Module Entity.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/4_module_fields.png" width="623"/>
