
#> life_steal:player/gain_heart_msg
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/on_kill
#

execute if score USE_HALF_HEARTS life_steal.data matches 0 run tellraw @s [{"text":"You stole a heart from a player, you now have ","color":"gray"},{"score":{"name":"@s","objective":"life_steal.hearts"}, "color":"red"},{"text":" hearts!"}]
execute if score USE_HALF_HEARTS life_steal.data matches 1 run function life_steal:player/gain_heart_msg_half

