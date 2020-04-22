# tk-cpenv
Integrates cpenv with Shotgun Toolkit.

<img src="https://github.com/cpenv/tk-cpenv/blob/master/set_modules_dialog.png" width="425"/>

cpenv is used to manage plugins, project dependencies and environment
variables through the use of modules. Modules are simple folders containing a
dependency like Arnold for Maya and a module.yaml file that includes
environment variables. Modules can be as complex or as simple as you would
like.

The simplest module is a folder containing a module.yaml file that includes
the environment key.

A complex module may include all platform varieties of a particular plugin.
The module.yaml file can set environment variables that use the $PLATFORM
variable to choose which plugin to provision at runtime.

# Configuring tk-cpenv
The example_config folder includes all modifications you need to make to your
Shotgun Toolkit config in order to get cpenv working.
