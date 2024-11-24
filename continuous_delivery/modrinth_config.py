
# Configuration for Modrinth
from config import *

# Constants
SUMMARY: str = """
Life Steal FR is a simple datapack aiming to add life steal behaviours from the original Lifesteal SMP:
https://lifesteal.fandom.com/wiki/Season_1

This datapack adds texture for the revive beacon and use 1.21 food components for interactions with the system (eating a heart, consuming a renamed revive beacon)
"""

DESCRIPTION_MARKDOWN: str = ""
if os.path.exists(f"{ROOT}/README.md"):
	with open(f"{ROOT}/README.md", "r", encoding="utf-8") as file:
		DESCRIPTION_MARKDOWN = file.read()
else:
	print("README.md not found, description_markdown will be empty")

# Dependencies (list of modrinth slugs)
DEPENDENCIES: list[dict] = []

# Version type (release, beta, alpha)
VERSION_TYPE: str = "release"

# Configuration
modrinth_config: dict = {
	"slug": "lifestealfr",
	"project_name": PROJECT_NAME,
	"version": VERSION,
	"summary": SUMMARY,
	"description_markdown": DESCRIPTION_MARKDOWN,
	"dependencies": DEPENDENCIES,
	"version_type": VERSION_TYPE,
	"build_folder": BUILD_FOLDER,
}

