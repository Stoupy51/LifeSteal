
#> life_steal:advancements/unlock_recipes
#
# @executed	as the player & at current position
#
# @within	advancement life_steal:unlock_recipes
#

# Revoke advancement
advancement revoke @s only life_steal:unlock_recipes

## For each ingredient in inventory, unlock the recipes
# minecraft:nautilus_shell
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:nautilus_shell
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart_2
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart_3

# minecraft:netherite_ingot
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:netherite_ingot
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart_2
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart_3

# minecraft:ominous_trial_key
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:ominous_trial_key
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart

# minecraft:dragon_head
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:dragon_head
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart_2

# minecraft:wither_skeleton_skull
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:wither_skeleton_skull
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart_3

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
execute if items entity @s container.* *[custom_data~{"life_steal": {"heart":true} }] run recipe give @s life_steal:heart
execute if items entity @s container.* *[custom_data~{"life_steal": {"heart":true} }] run recipe give @s life_steal:heart_2
execute if items entity @s container.* *[custom_data~{"life_steal": {"heart":true} }] run recipe give @s life_steal:heart_3
execute if items entity @s container.* *[custom_data~{"life_steal": {"revive_beacon":true} }] run recipe give @s life_steal:revive_beacon

