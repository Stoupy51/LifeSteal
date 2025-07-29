
#> life_steal:player/remove_one_heart
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/tick
#

scoreboard players remove @s life_steal.hearts 1
tellraw @s [{"text":"You lost a heart, you now have ","color":"gray"},{"score":{"name":"@s","objective":"life_steal.hearts"}, "color":"red"},{"text":" hearts!"}]

# Drop a heart if player wasn't killed by another player
execute unless entity @a[scores={life_steal.kill=1..}] run function life_steal:player/drop_heart_at_death

