
#> life_steal:player/consume_heart
#
# @executed	as the player & at current position
#
# @within	advancement life_steal:consume_heart
#

# Revoke the advancement
advancement revoke @s only life_steal:consume_heart

# If already at max health by consuming, regive the heart and stop function
scoreboard players operation #temp life_steal.data = MAX_HEARTS_BY_CONSUMING life_steal.data
execute if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation #temp life_steal.data *= #2 life_steal.data
execute if score @s life_steal.hearts >= #temp life_steal.data if score MAX_HEARTS_BY_CONSUMING life_steal.data = MAX_HEARTS life_steal.data run tellraw @s {"text":"You are already at max health!","color":"red"}
execute if score @s life_steal.hearts >= #temp life_steal.data unless score MAX_HEARTS_BY_CONSUMING life_steal.data = MAX_HEARTS life_steal.data run tellraw @s {"text":"You are already at max health from consuming hearts! You can only gain more hearts by killing players.","color":"red"}
execute if score @s life_steal.hearts >= #temp life_steal.data at @s run playsound entity.villager.no ambient @s
execute if score @s life_steal.hearts >= #temp life_steal.data at @s run loot spawn ~ ~ ~ loot life_steal:i/heart
execute if score @s life_steal.hearts >= #temp life_steal.data run return fail

# Remove last_chance tag if player has it
tag @s remove life_steal.last_chance

# Give a heart and update health
scoreboard players add @s life_steal.hearts 1
function life_steal:player/update_health

# Tellraw message
function life_steal:player/consume_heart_msg

