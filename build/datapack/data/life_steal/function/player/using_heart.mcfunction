
#> life_steal:player/using_heart
#
# @executed	as the player & at current position
#
# @within	advancement life_steal:using_heart
#

# Revoke the advancement
advancement revoke @s only life_steal:using_heart

# Stop if INSTANTLY_CONSUME_HEARTS is disabled
execute unless score INSTANTLY_CONSUME_HEARTS life_steal.data matches 1 run return fail

# If already at max health, stop
scoreboard players operation #temp life_steal.data = MAX_HEARTS life_steal.data
execute if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation #temp life_steal.data *= #2 life_steal.data
execute if score @s life_steal.hearts >= #temp life_steal.data run tellraw @s {"text":"You are already at max health!","color":"red"}
execute if score @s life_steal.hearts >= #temp life_steal.data run return fail

# Give a heart and update health
scoreboard players add @s life_steal.hearts 1
function life_steal:player/update_health

# Clear one heart
clear @s *[custom_data~{life_steal:{"heart":true}}] 1

# Tellraw message
function life_steal:player/consume_heart_msg

