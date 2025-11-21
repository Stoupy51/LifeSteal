
#> life_steal:player/reached_min_hearts
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/tick
#

# Get player username
tag @e[type=item] add life_steal.temp
execute at @s run loot spawn ~ ~ ~ loot life_steal:player_head
data modify storage life_steal:main player set from entity @e[type=item,tag=!life_steal.temp,limit=1] Item.components."minecraft:profile".name
kill @e[type=item,tag=!life_steal.temp]
tag @e[type=item,tag=life_steal.temp] remove life_steal.temp

# Make sure player does not have less than minimum hearts
scoreboard players operation #temp life_steal.data = MIN_HEARTS life_steal.data
execute if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation #temp life_steal.data *= #2 life_steal.data
scoreboard players operation @s life_steal.hearts > #temp life_steal.data

# Ban macro if configuration is enabled
execute if score BAN_AT_MIN_HEARTS life_steal.data matches 1 run function life_steal:player/ban_macro with storage life_steal:main
execute if score BAN_AT_MIN_HEARTS life_steal.data matches 0 run function life_steal:player/min_hearts_reached_msg with storage life_steal:main

