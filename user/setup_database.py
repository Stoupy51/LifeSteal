
# Imports
from stewbeet import (
	CATEGORY,
	CUSTOM_ITEM_VANILLA,
	OVERRIDE_MODEL,
	RESULT_OF_CRAFTING,
	Context,
	DamageTypeTag,
	Mem,
	add_item_model_component,
	add_item_name_and_lore_if_missing,
	add_private_custom_data_for_namespace,
	add_smithed_ignore_vanilla_behaviours_convention,
	ingr_repr,
	set_json_encoder,
)


# Main function
def beet_default(ctx: Context):
	ns: str = ctx.project_id

	# Define custom items
	Mem.definitions = {
		"heart": {
			"id": CUSTOM_ITEM_VANILLA,
			"damage_resistant": {"types":f"#{ns}:is_explosion_or_fire"},
			"consumable": {},
			CATEGORY: "food",
			RESULT_OF_CRAFTING: [{
				"type":"crafting_shaped", "result_count":1, "category":"misc", "shape":["NDN","DTD","NDN"],
				"ingredients":{"N":ingr_repr("minecraft:netherite_ingot"), "D":ingr_repr("minecraft:diamond_block"), "T":ingr_repr("minecraft:totem_of_undying")}
			}],
		},

		"revive_beacon": {
			"id": CUSTOM_ITEM_VANILLA,
			"consumable": {},
			"lore": [{"text":"Rename the item to the username","italic":False,"color":"gray"}, {"text":"of the player you want to revive.","italic":False,"color":"gray"}],
			CATEGORY: "food",
			RESULT_OF_CRAFTING: [{
				"type":"crafting_shaped", "result_count":1, "category":"misc", "shape":["TNT","NBN","TNT"],
				"ingredients":{"T":ingr_repr("minecraft:totem_of_undying"), "N":ingr_repr("minecraft:netherite_ingot"), "B":ingr_repr("minecraft:beacon")}
			}],
			OVERRIDE_MODEL: {
				"parent":"minecraft:block/beacon","textures":{
					"beacon":f"{ns}:item/inner_beacon",
					"particle":"minecraft:block/glass",
					"glass":"minecraft:block/glass",
					"obsidian":"minecraft:block/obsidian"
			}},
		},
	}

	# Create damage resistant tag
	Mem.ctx.data[ns].damage_type_tags["is_explosion_or_fire"] = set_json_encoder(DamageTypeTag({"values": ["#minecraft:is_explosion", "#minecraft:is_fire"]}))

	# Final adjustments
	add_item_model_component()
	add_item_name_and_lore_if_missing()
	add_private_custom_data_for_namespace()
	add_smithed_ignore_vanilla_behaviours_convention()

