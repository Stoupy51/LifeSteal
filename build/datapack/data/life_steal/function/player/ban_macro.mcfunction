
#> life_steal:player/ban_macro
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/reached_min_hearts with storage life_steal:main
#
# @args		player (unknown)
#

# Tellraw message
$tellraw @a {"text":"Player '$(player)' just got banned for reaching minimum hearts!","color":"red"}

# Ban player (isolated to prevent crashes if permission denied)
execute store success score #banned life_steal.data run function life_steal:player/ban_player with storage life_steal:main

# Add player name to banned list
execute unless data storage life_steal:main banned_players run data modify storage life_steal:main banned_players set value {}
function life_steal:player/add_to_banned_list with storage life_steal:main
scoreboard players set #banned life_steal.data 1

