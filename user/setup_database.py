
# Import database helper (from python_datapack, containing database helper functions)
from python_datapack.utils.database_helper import *

# Main function should return a database
def main(config: dict) -> dict[str, dict]:
	namespace: str = config["namespace"]

	# Define custom items
	database: dict[str, dict] = {
		"heart": {
			"id": CUSTOM_ITEM_VANILLA,
			RESULT_OF_CRAFTING: [{
				"type":"crafting_shaped", "result_count":1, "category":"misc", "shape":["NDN","DTD","NDN"],
	 			"ingredients":{"N":ingr_repr("minecraft:netherite_ingot"), "D":ingr_repr("minecraft:diamond_block"), "T":ingr_repr("minecraft:totem_of_undying")}
			}],
			CATEGORY: "food",
			"consumable": {},
		},

		"revive_beacon": {
			"id": CUSTOM_ITEM_VANILLA,
			RESULT_OF_CRAFTING: [{
				"type":"crafting_shaped", "result_count":1, "category":"misc", "shape":["TNT","NBN","TNT"],
	 			"ingredients":{"T":ingr_repr("minecraft:totem_of_undying"), "N":ingr_repr("minecraft:netherite_ingot"), "B":ingr_repr("minecraft:beacon")}
			}],
			CATEGORY: "food",
			"consumable": {},
			"lore": ['{"text":"Rename the item to the username","italic":false,"color":"gray"}', '{"text":"of the player you want to revive.","italic":false,"color":"gray"}'],
			OVERRIDE_MODEL: {"parent":"block/beacon","textures":{"beacon":f"{namespace}:item/inner_beacon"}},
		},
	}

	# Final adjustments
	add_item_model_component(config, database)
	add_item_name_and_lore_if_missing(config, database)
	add_private_custom_data_for_namespace(config, database)
	add_smithed_ignore_vanilla_behaviours_convention(database)

	# Return database
	return database

