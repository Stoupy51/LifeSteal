
#> life_steal:player/withdraw_msg
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/withdraw
#

execute if score USE_HALF_HEARTS life_steal.data matches 0 run tellraw @s [{"text":"You withdrew a heart, you now have ","color":"gray"},{"score":{"name":"@s","objective":"life_steal.hearts"}, "color":"red"},{"text":" hearts!"}]
execute if score USE_HALF_HEARTS life_steal.data matches 1 run function life_steal:player/withdraw_msg_half

