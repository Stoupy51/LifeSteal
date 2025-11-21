
#> life_steal:player/min_hearts_reached_msg
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/reached_min_hearts with storage life_steal:main
#
# @args		player (unknown)
#

# Tellraw message when reaching minimum hearts without banning
$tellraw @a [{"text":"Player '$(player)' reached the minimum hearts!","color":"yellow"}]
execute as @a at @s run playsound entity.player.hurt ambient @s

