
#> life_steal:player/on_kill
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/tick
#

# Compute max hearts
scoreboard players operation #temp life_steal.data = MAX_HEARTS life_steal.data
execute if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation #temp life_steal.data *= #2 life_steal.data

# If at max hearts, send message
execute if score @s life_steal.hearts >= #temp life_steal.data run tellraw @s [{"text":"You stole a heart from a player, but you are already at max health!","color":"red"}]

# Else, add a heart (or half heart)
execute if score @s life_steal.hearts < #temp life_steal.data run scoreboard players operation @s life_steal.hearts += @s life_steal.kill
execute if score @s life_steal.hearts < #temp life_steal.data run function life_steal:player/gain_heart_msg

# Update health and reset kill score
function life_steal:player/update_health
scoreboard players set @s life_steal.kill 0

