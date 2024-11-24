
#> life_steal:calls/smithed_crafter/shaped_recipes
#
# @within	#smithed.crafter:event/recipes
#

execute if score @s smithed.data matches 0 store result score @s smithed.data if data storage smithed.crafter:input recipe{0:[{"Slot":0b, "id": "minecraft:netherite_ingot"},{"Slot":1b, "id": "minecraft:diamond_block"},{"Slot":2b, "id": "minecraft:netherite_ingot"}],1:[{"Slot":0b, "id": "minecraft:diamond_block"},{"Slot":1b, "id": "minecraft:totem_of_undying"},{"Slot":2b, "id": "minecraft:diamond_block"}],2:[{"Slot":0b, "id": "minecraft:netherite_ingot"},{"Slot":1b, "id": "minecraft:diamond_block"},{"Slot":2b, "id": "minecraft:netherite_ingot"}]} run loot replace block ~ ~ ~ container.16 loot life_steal:i/heart
execute if score @s smithed.data matches 0 store result score @s smithed.data if data storage smithed.crafter:input recipe{0:[{"Slot":0b, "id": "minecraft:totem_of_undying"},{"Slot":1b, "id": "minecraft:netherite_ingot"},{"Slot":2b, "id": "minecraft:totem_of_undying"}],1:[{"Slot":0b, "id": "minecraft:netherite_ingot"},{"Slot":1b, "id": "minecraft:beacon"},{"Slot":2b, "id": "minecraft:netherite_ingot"}],2:[{"Slot":0b, "id": "minecraft:totem_of_undying"},{"Slot":1b, "id": "minecraft:netherite_ingot"},{"Slot":2b, "id": "minecraft:totem_of_undying"}]} run loot replace block ~ ~ ~ container.16 loot life_steal:i/revive_beacon

