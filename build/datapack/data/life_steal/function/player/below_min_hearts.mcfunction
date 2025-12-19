
#> life_steal:player/below_min_hearts
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/on_death
#

# If died from a player but not BAN_BELOW_MIN_HEARTS configuration, do not reward the killer
execute unless score BAN_BELOW_MIN_HEARTS life_steal.data matches 1 run scoreboard players remove @a[scores={life_steal.kill=1..}] life_steal.kill 1

# Make sure player does not have less than minimum hearts
execute if score @s life_steal.hearts < #real_min_hearts life_steal.data run scoreboard players operation @s life_steal.hearts = #real_min_hearts life_steal.data
execute if score @s life_steal.hearts matches ..0 run scoreboard players set @s life_steal.hearts 1
function life_steal:player/update_health

# If not BAN_BELOW_MIN_HEARTS configuration, stop here
execute unless score BAN_BELOW_MIN_HEARTS life_steal.data matches 1 run return 1

# Get player username for macro
tag @e[type=item] add life_steal.temp
execute at @s run loot spawn ~ ~ ~ loot life_steal:player_head
data modify storage life_steal:main player set from entity @e[type=item,tag=!life_steal.temp,limit=1] Item.components."minecraft:profile".name
kill @e[type=item,tag=!life_steal.temp]
tag @e[type=item,tag=life_steal.temp] remove life_steal.temp

# Ban macro
scoreboard players set #banned life_steal.data 0
function life_steal:player/ban_macro with storage life_steal:main

# If banned player is still in the world, make him spectator and send an error message (function permission issue)
execute if score #banned life_steal.data matches 0 run gamemode spectator @s
execute if score #banned life_steal.data matches 0 run tellraw @a [{"text":"[LifeStealFR] ERROR: Could not ban player '","color":"red"},{"selector":"@s"},{"text":"'. Set 'function-permission-level' to 3 in server.properties!"}]

