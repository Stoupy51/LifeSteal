
#> life_steal:player/reached_0_heart
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

# Make sure player does not have negative hearts
scoreboard players set @s life_steal.hearts 0

# Ban macro
function life_steal:player/ban_macro with storage life_steal:main

