
# Python Datapack Template
## config.py
This file contains every single parameter you can adjust to the build process.
By default, everything is enabled and set to the default values.

If you want to ignore warning message for unset configurations, you can set "ignore_unset" to True to the final configuration.
The default value is False.

## build.py
To run the datapack build process, you can only need to run the build.py file.
This script depends on the following files in the user folder: "link.py", "setup_database.py", "setup_external_database.py".
These files are described in user/_README.md.

## optimize_textures.py
This script is an utility one, you can run it and it will try to optimize every .png file in the directory without losing quality.

## upgrade_build.py
This script is an utility one, you can run it and it upgrade the build system to the latest version.

