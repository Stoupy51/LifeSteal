
# pyright: reportUnknownVariableType=false
# Imports
from beet import ProjectConfig
from stewbeet import JsonDict
from stewbeet.continuous_delivery import load_credentials, upload_to_github, upload_to_modrinth, upload_to_pmc, upload_to_smithed
from stewbeet.utils import get_project_config
from stouputils.io import read_file

# Get credentials and try to find the beet configuration
credentials: dict[str, str] = load_credentials("~/stewbeet/credentials.yml")
cfg: ProjectConfig = get_project_config()


## Uploads
# Upload to GitHub
github_config: JsonDict = {
    "project_name": cfg.name,
    "version": cfg.version,
    "build_folder": cfg.output,
    "endswith": [".zip", ".jar"]
}
changelog: str = upload_to_github(credentials, github_config)

# Upload to Modrinth
modrinth_config: JsonDict = {
	"slug": "lifestealfr",
	"project_name": cfg.name,
	"version": cfg.version,
	"authors": cfg.author,
	"summary": "Life Steal FR is a simple datapack configurable aiming to add life steal behaviours from the original Lifesteal SMP:\nhttps://lifesteal.fandom.com/wiki/Season_1",
	"description_markdown": read_file(f"{cfg.directory}/README.md"),
	"version_type": "release",
	"build_folder": cfg.output,
	"package_as_mod": "separate",
}
upload_to_modrinth(credentials, modrinth_config, changelog)

# Upload to Smithed
smithed_config: JsonDict = {
	"project_id": "lifestealfr",
	"project_name": cfg.name,
	"version": cfg.version,
}
upload_to_smithed(credentials, smithed_config, changelog)

# Upload to PlanetMinecraft
pmc_config: JsonDict = {
	"project_url": "https://www.planetminecraft.com/account/manage/data-packs/6311509/",
	"version": cfg.version,
}
upload_to_pmc(pmc_config, changelog)

