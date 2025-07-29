
#> life_steal:player/consume_heart
#
# @executed	as the player & at current position
#
# @within	advancement life_steal:consume_heart
#

# Revoke the advancement
advancement revoke @s only life_steal:consume_heart

# If already at max health, regive the heart and stop function
execute if score @s life_steal.hearts >= MAX_HEARTS life_steal.data run tellraw @s {"text":"You are already at max health!","color":"red"}
execute if score @s life_steal.hearts >= MAX_HEARTS life_steal.data at @s run loot spawn ~ ~ ~ loot life_steal:i/heart
execute if score @s life_steal.hearts >= MAX_HEARTS life_steal.data run return fail

# Give a heart and update health
scoreboard players add @s life_steal.hearts 1
function life_steal:player/update_health

# Tellraw message
tellraw @s [{"text":"You ate a heart, you now have ","color":"gray"},{"score":{"name":"@s","objective":"life_steal.hearts"}, "color":"red"},{"text":" hearts!"}]

