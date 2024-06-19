
# Imports
from python_datapack.constants import *
from python_datapack.utils.print import *
from python_datapack.utils.io import *

# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def main(config: dict) -> None:
	database: dict[str, dict] = config["database"]
	namespace: str = config["namespace"]
	functions: str = f"{config['build_datapack']}/data/{namespace}/function"
	version: str = config["version"]

	# Add scoreboard objectives
	confirm_load: str = f"{functions}/v{version}/load/confirm_load.mcfunction"
	# write_to_file(confirm_load, f"scoreboard objectives add {namespace}.kill playerKill\n", prepend = True)
	# write_to_file(confirm_load, f"scoreboard objectives add {namespace}.death deathCount\n", prepend = True)




	pass

