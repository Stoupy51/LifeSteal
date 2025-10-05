
#> life_steal:player/withdraw_msg_half
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/withdraw_msg
#

scoreboard players operation #display_whole life_steal.data = @s life_steal.hearts
scoreboard players operation #display_whole life_steal.data /= #2 life_steal.data
scoreboard players operation #display_half life_steal.data = @s life_steal.hearts
scoreboard players operation #display_half life_steal.data %= #2 life_steal.data
execute if score #display_half life_steal.data matches 0 run tellraw @s [{"text":"You withdrew a heart, you now have ","color":"gray"},{"score":{"name":"#display_whole","objective":"life_steal.data"}, "color":"red"},{"text":".0","color":"red"},{"text":" hearts!"}]
execute if score #display_half life_steal.data matches 1 run tellraw @s [{"text":"You withdrew a heart, you now have ","color":"gray"},{"score":{"name":"#display_whole","objective":"life_steal.data"}, "color":"red"},{"text":".5","color":"red"},{"text":" hearts!"}]

