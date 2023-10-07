# tk-cpenv
![GitHub release (latest by date)](https://img.shields.io/github/v/release/cpenv/tk-cpenv)

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
- Create required app fields on first launch
- Store modules directly in your shotgun site
- Localize modules when launching applications
- Build Environments (a list of modules) to be activated per job and toolkit engine.
- Drag and drop modules to build environments.
- Preview combined environment variables.
- Import Environments from other jobs, making it easy to setup new jobs.

# Configuring tk-cpenv
The example_config folder includes modifications you need to make to your
Shotgun Toolkit config in order to get cpenv working. The module_entity and
environment_entity keys will be specific to your shotgun site.

## tk-cpenv settings
- **home_path**: Where to store modules locally. Defaults to a local path available across all users on your machine. You may choose to use a network location here, so that all users in a network share modules.
- **module_paths**: List of additional paths used to lookup modules.
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
The app will ask you if you want to automatically create the required app fields when you launch the app.


If you prefer to create them manually, here are the fields you need to add.

1. Add the following fields to the Module Entity.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/4_module_fields.png" width="640"/>
2. Add the following fields to the Environment Entity.
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/4_environment_fields.png" width="640"/>

## Modify your shotgun toolkit config
1. Open env/includes/settings/tk-cpenv.yml.
2. Set the value of the `module_entity` to match the `CustomNonProjectEntity` you enabled. This would be `CustomNonProjectEntity01` according to the image above.
3. Set the value of the `environment_entity` to match the `CustomEntity` you enabled. This would be `CustomEntity03` according to the image above.

# Developing and publishing modules
Use the cpenv cli tool to create, test, and publish modules to your shotgun site. Only modules published to your site will appear in the Set Modules dialog.

## Configure a ShotgunRepo with the cpenv cli
In order to publish to your shotgun site, you'll need to configure a ShotgunRepo.
1. [Create a Shotgun script.](https://support.shotgunsoftware.com/hc/en-us/articles/219031368-Create-and-manage-API-scripts) Make sure the name of your script makes it clear what it will be used for, I named mine "cpenv".
2. Execute the following cli command using your own repo_name, baseurl, script_name, api_key and module_entity.
```
> cpenv repo add my_shotgun --type=shotgun --base_url=https://my.shotgunstudio.com --script_name=cpenv --api_key=<your_script_key> --module_entity=CustomNonProjectEntity01
```

If all is well, you should now see your new ShotgunRepo when running `cpenv repo list`.

## Create your first module
Let's create a quick test module named "my_first_module" in a temporary directory.
```
> mkdir tmp
> cd tmp
> cpenv create my_first_module
...
> cd my_first_module
```

Next open the module.yml file and modify the environment section.

> Tip: If you use sublime text use `subl .` to open the current directory in sublime text. You can also use `cpenv edit "some_module"` to quickly open a published module in sublime text. You can configure your own text editor by setting the `CPENV_EDITOR` environment variable.

```
name: my_first_module
version: 0.1.0
description: 'My very first module'
author: 'Me'
email: 'me@memail.com'
requires: []
environment:
  MY_FIRST_VAR: 'HelloWorld'
```
Include an icon.png file and that will be used as a thumbnail when you publish your module.

## Test your module
Activate your module to test it. You can use `cpenv activate .` to activate the current working directory.

```
> cpenv activate .
# Windows Powershell
> $env:MY_FIRST_VAR
# Bash
> echo $MY_FIRST_VAR
```

## Publish your first module
Now that we have a working module, let's publish it to Shotgun.
```
> cpenv publish my_first_module

  [0] cwd - C:/Users/user
  [1] user - C:/Users/user/AppData/Local/cpenv/modules
  [2] home - C:/ProgramData/cpenv/modules
  [3] my_shotgun - https://my.shotgunstudio.com

Choose a repo to publish to [2]: 3
```

This should upload your module to Shotgun and you'll be able to see it in the Set Modules dialog.

To quickly verify that your module has been uploaded, you can use the `cpenv list` command.

[Visit the cpenv repository for more info.](https://github.com/cpenv/cpenv)


# Using the Set Modules dialog
1. Create an Environment and set an engine for it.

<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/1_add_new_environment.png" width="548"/>

2. Drag and drop modules to build your Environment. The order of the modules here is important. Modules later in the list can override environment variables set earlier in the list. You can drag and drop to reorder them or move them back to the Available Modules list to remove them from the environment.

<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/2_drag_and_drop_modules.png" width="480"/>

3. Use the Preview Environment tool to view the combined environment variables for your Environment.

<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/3_preview_env_tool.png" width="548"/>
<img src="https://github.com/cpenv/tk-cpenv/blob/master/images/preview_env_dialog.png"/>

4. Use the Permissions dialog to restrict access to an Environment to certain users. This is great for development when you need to test an Environment before pushing it out to everyone.
    <img src="https://github.com/cpenv/tk-cpenv/blob/master/images/4_permissions_tool.png" width="548"/>
    <img src="https://github.com/cpenv/tk-cpenv/blob/master/images/permissions_dialog.png"/>
    * Users will be prompted to select an Environment when they launch an application if they have permissions to multiple Environments for an engine.
    <img src="https://github.com/cpenv/tk-cpenv/blob/master/images/env_selector.png"/>

5. Optionally restrict the Environment to certain software versions by enter the versions into the "Software Versions" field. Leaving it blank will make the Environment apply to all versions of the selected Engine's software. For example if you entered "2020 2022" for a "tk-maya" Environment, that would be activated for either Maya 2020 or Maya 2022.

6. Save your changes! You're ready to launch some software.

