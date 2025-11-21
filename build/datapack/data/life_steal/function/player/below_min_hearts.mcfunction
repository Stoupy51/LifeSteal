
#> life_steal:player/below_min_hearts
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/on_death
#

# Make sure player does not have less than minimum hearts
scoreboard players operation #temp life_steal.data = MIN_HEARTS life_steal.data
execute if score USE_HALF_HEARTS life_steal.data matches 1 unless score #temp life_steal.data matches 1 run scoreboard players operation #temp life_steal.data *= #2 life_steal.data
execute if score @s life_steal.hearts < #temp life_steal.data run scoreboard players operation @s life_steal.hearts = #temp life_steal.data

# If not BAN_BELOW_MIN_HEARTS configuration, stop here
execute unless score BAN_BELOW_MIN_HEARTS life_steal.data matches 1 run return 1

# Get player username for macro
tag @e[type=item] add life_steal.temp
execute at @s run loot spawn ~ ~ ~ loot life_steal:player_head
data modify storage life_steal:main player set from entity @e[type=item,tag=!life_steal.temp,limit=1] Item.components."minecraft:profile".name
kill @e[type=item,tag=!life_steal.temp]
tag @e[type=item,tag=life_steal.temp] remove life_steal.temp

# Ban macro
function life_steal:player/ban_macro with storage life_steal:main

