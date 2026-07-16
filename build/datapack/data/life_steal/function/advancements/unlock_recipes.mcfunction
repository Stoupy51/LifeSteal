
#> life_steal:advancements/unlock_recipes
#
# @executed	as the player & at current position
#
# @within	advancement life_steal:unlock_recipes
#

# Revoke advancement
advancement revoke @s only life_steal:unlock_recipes

## For each ingredient in inventory, unlock the recipes
# minecraft:trial_key
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:trial_key
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:crafted_heart

# minecraft:ghast_tear
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:ghast_tear
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:crafted_heart

# minecraft:ender_eye
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:ender_eye
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:crafted_heart

# minecraft:beacon
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:beacon
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:revive_beacon

# minecraft:elytra
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:elytra
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:revive_beacon

# minecraft:recovery_compass
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:recovery_compass
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:revive_beacon

# minecraft:heavy_core
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:heavy_core
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:revive_beacon

# minecraft:conduit
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:conduit
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:revive_beacon

# minecraft:skeleton_skull
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:skeleton_skull
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:revive_beacon

## Add result items
execute if items entity @s container.* *[custom_data~{"life_steal": {"crafted_heart":true} }] run recipe give @s life_steal:crafted_heart
execute if items entity @s container.* *[custom_data~{"life_steal": {"revive_beacon":true} }] run recipe give @s life_steal:revive_beacon

