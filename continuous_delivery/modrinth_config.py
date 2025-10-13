
# pyright: reportOptionalMemberAccess=false
# Imports
import os

from stewbeet import JsonDict, ProjectConfig, load_config, locate_config
from stouputils.io import get_root_path

# Try to find and load the beet configuration file
cfg: ProjectConfig | None = None
if config_path := locate_config(os.getcwd(), parents=True):
	cfg = load_config(filename=config_path)
	if cfg:
		os.chdir(config_path.parent)
if not cfg:
	print(f"No beet config file found in the current directory '{os.getcwd()}'")

# Constants
ROOT: str = get_root_path(__file__, go_up=1)
SUMMARY: str = "Life Steal FR is a simple datapack configurable aiming to add life steal behaviours from the original Lifesteal SMP:\nhttps://lifesteal.fandom.com/wiki/Season_1"

description_markdown: str = ""
if os.path.exists(f"{ROOT}/README.md"):
	with open(f"{ROOT}/README.md", encoding="utf-8") as file:
		description_markdown = file.read()
else:
	print("README.md not found, description_markdown will be empty")

# Dependencies (list of modrinth slugs)
DEPENDENCIES: list[JsonDict] = []

# Version type (release, beta, alpha)
VERSION_TYPE: str = "release"

# Configuration
modrinth_config: JsonDict = {
	"slug": "lifestealfr",
	"project_name": cfg.name,
	"version": cfg.version,
	"authors": cfg.author,
	"summary": SUMMARY,
	"description_markdown": description_markdown,
	"dependencies": DEPENDENCIES,
	"version_type": VERSION_TYPE,
	"build_folder": cfg.output,
	"package_as_mod": "separate",
}

