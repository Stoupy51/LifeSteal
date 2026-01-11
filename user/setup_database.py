
# Imports
from stewbeet import (
	Context,
	CraftingShapedRecipe,
	DamageTypeTag,
	Ingr,
	Item,
	Mem,
	add_item_model_component,
	add_item_name_and_lore_if_missing,
	add_private_custom_data_for_namespace,
	add_smithed_ignore_vanilla_behaviours_convention,
	set_json_encoder,
)


# Main function
def beet_default(ctx: Context):
	ns: str = ctx.project_id

	# Define custom items
	Item(
		id="heart",
		manual_category="misc",
		recipes=[
			CraftingShapedRecipe(
				category="misc",
				shape=["SNS","NCN","SNS"],
				ingredients={
					"S":Ingr("minecraft:nautilus_shell"),
					"N":Ingr("minecraft:netherite_ingot"),
					"C":Ingr(center)
				},
			)
			for center in [
				"minecraft:ominous_trial_key",
				"minecraft:dragon_head",
				"minecraft:wither_skeleton_skull"
			]
		],
		components={
			"damage_resistant": {"types":f"#{ns}:is_explosion_or_fire"},
			"consumable": {},
		},
	)

	Item(
		id="revive_beacon",
		manual_category="misc",
		recipes=[
			CraftingShapedRecipe(
				category="misc",
				shape=["ABA","CDE","AFA"],
				ingredients={
					"A":Ingr("minecraft:beacon"),
					"B":Ingr("minecraft:elytra"),
					"C":Ingr("minecraft:recovery_compass"),
					"D":Ingr("minecraft:heavy_core"),
					"E":Ingr("minecraft:conduit"),
					"F":Ingr("minecraft:skeleton_skull"),
				},
			),
		],
		override_model={
			"parent":"minecraft:block/beacon",
			"textures":{
				"beacon":f"{ns}:item/inner_beacon",
				"particle":"minecraft:block/glass",
				"glass":"minecraft:block/glass",
				"obsidian":"minecraft:block/obsidian"
			},
		},
		components={
			"consumable": {},
			"lore":[
				{"text":"Rename the item to the username","italic":False,"color":"gray"},
				{"text":"of the player you want to revive.","italic":False,"color":"gray"}
			],
		},
	)

	# Create damage resistant tag
	Mem.ctx.data[ns].damage_type_tags["is_explosion_or_fire"] = set_json_encoder(DamageTypeTag({"values": ["#minecraft:is_explosion", "#minecraft:is_fire"]}))

	# Final adjustments
	add_item_model_component()
	add_item_name_and_lore_if_missing()
	add_private_custom_data_for_namespace()
	add_smithed_ignore_vanilla_behaviours_convention()

