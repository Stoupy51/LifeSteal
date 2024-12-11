
#> life_steal:advancements/unlock_recipes
#
# @within	advancement life_steal:unlock_recipes
#

# Revoke advancement
advancement revoke @s only life_steal:unlock_recipes

## For each ingredient in inventory, unlock the recipes
# minecraft:netherite_ingot
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:netherite_ingot
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:revive_beacon

# minecraft:diamond_block
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:diamond_block
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart

# minecraft:totem_of_undying
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:totem_of_undying
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:heart
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:revive_beacon

# minecraft:beacon
scoreboard players set #success life_steal.data 0
execute store success score #success life_steal.data if items entity @s container.* minecraft:beacon
execute if score #success life_steal.data matches 1 run recipe give @s life_steal:revive_beacon

## Add result items
execute if items entity @s container.* *[custom_data~{"life_steal": {"heart":true} }] run recipe give @s life_steal:heart
execute if items entity @s container.* *[custom_data~{"life_steal": {"revive_beacon":true} }] run recipe give @s life_steal:revive_beacon

