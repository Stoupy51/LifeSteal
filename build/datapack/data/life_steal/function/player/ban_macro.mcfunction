
#> life_steal:player/ban_macro
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/reached_min_hearts with storage life_steal:main
#
# @args		player (unknown)
#

# Tellraw message and ban player
$tellraw @a {"text":"Player '$(player)' just got banned for reaching minimum hearts!","color":"red"}
$ban $(player) You reached the minimum hearts!

# Add player name to banned list
execute unless data storage life_steal:main banned_players run data modify storage life_steal:main banned_players set value {}
$data modify storage life_steal:main banned_players.$(player) set value true

