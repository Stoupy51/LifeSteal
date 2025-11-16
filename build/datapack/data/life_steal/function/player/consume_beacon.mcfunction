
#> life_steal:player/consume_beacon
#
# @executed	as the player & at current position
#
# @within	advancement life_steal:consume_beacon
#

# Revoke the advancement
advancement revoke @s only life_steal:consume_beacon

# Get username from beacon name
data remove storage life_steal:main player
execute if data entity @s SelectedItem.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage life_steal:main player set string entity @s SelectedItem.components."minecraft:custom_name"
execute unless data storage life_steal:main player if data entity @s equipment.offhand.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage life_steal:main player set string entity @s equipment.offhand.components."minecraft:custom_name"

# Try to revive
execute store success score #success life_steal.data run function life_steal:player/revive with storage life_steal:main
execute if score #success life_steal.data matches 1 run return 1

# If not success, regive the beacon and stop function
loot give @s[gamemode=!creative] loot life_steal:i/revive_beacon
return fail

