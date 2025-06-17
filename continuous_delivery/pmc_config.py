
# Imports
import os

from beet import ProjectConfig, load_config, locate_config

# Try to find and load the beet configuration file
cfg: ProjectConfig | None = None
if config_path := locate_config(os.getcwd(), parents=True):
	cfg = load_config(filename=config_path)
	if cfg:
		os.chdir(config_path.parent)
if not cfg:
	print(f"No beet config file found in the current directory '{os.getcwd()}'")

# Constants
PMC_URL: str = "https://www.planetminecraft.com/account/manage/data-packs/6311509/"

# Configuration
pmc_config: dict = {
	"project_url": PMC_URL,
	"version": cfg.version,
}

