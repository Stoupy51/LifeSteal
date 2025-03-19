
#> life_steal:player/consume_beacon
#
# @within	advancement life_steal:consume_beacon
#

# Revoke the advancement
advancement revoke @s only life_steal:consume_beacon

# Get username from beacon name
data remove storage life_steal:main player
scoreboard players set #success life_steal.data 0
execute if data entity @s SelectedItem.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage life_steal:main player set string entity @s SelectedItem.components."minecraft:custom_name"
execute unless data storage life_steal:main player if data entity @s Inventory[-1].components."minecraft:custom_data".life_steal.revive_beacon run data modify storage life_steal:main player set string entity @s Inventory[-1].components."minecraft:custom_name"
function life_steal:player/revive with storage life_steal:main

# If not success, regive the beacon and stop function
execute if score #success life_steal.data matches 0 run loot give @s[gamemode=!creative] loot life_steal:i/revive_beacon
execute if score #success life_steal.data matches 0 run return fail

