
#> life_steal:player/update_health
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/tick
#			life_steal:player/withdraw
#			life_steal:player/consume_heart
#

execute store result storage life_steal:main health int 2 run scoreboard players get @s life_steal.hearts
function life_steal:player/update_macro with storage life_steal:main
execute at @s run playsound entity.player.levelup ambient @s

