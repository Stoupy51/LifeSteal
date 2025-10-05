
#> life_steal:player/consume_heart_msg
#
# @executed	as the player & at current position
#
# @within	life_steal:player/consume_heart
#

execute if score USE_HALF_HEARTS life_steal.data matches 0 run tellraw @s [{"text":"You ate a heart, you now have ","color":"gray"},{"score":{"name":"@s","objective":"life_steal.hearts"}, "color":"red"},{"text":" hearts!"}]
execute if score USE_HALF_HEARTS life_steal.data matches 1 run function life_steal:player/consume_heart_msg_half

