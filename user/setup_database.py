
# Imports
from stewbeet.core import *


# Main function
def beet_default(ctx: Context):
	if Mem.ctx is None:
		Mem.ctx = ctx
	ns: str = ctx.project_id

	# Define custom items
	Mem.definitions = {
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
			"lore": [{"text":"Rename the item to the username","italic":False,"color":"gray"}, {"text":"of the player you want to revive.","italic":False,"color":"gray"}],
			OVERRIDE_MODEL: {"parent":"block/beacon","textures":{"beacon":f"{ns}:item/inner_beacon"}},
		},
	}

	# Final adjustments
	add_item_model_component()
	add_item_name_and_lore_if_missing()
	add_private_custom_data_for_namespace()
	add_smithed_ignore_vanilla_behaviours_convention()

