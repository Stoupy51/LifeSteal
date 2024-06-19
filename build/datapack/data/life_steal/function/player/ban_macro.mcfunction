
#> life_steal:player/ban_macro
#
# @within	life_steal:player/death with storage life_steal:main
#

# Tellraw message and ban player
$tellraw @a {"text":"Player '$(player)' just got banned for reaching 0 hearts!","color":"red"}
$ban $(player) You reached 0 hearts!

# Add player name to banned list
execute unless data storage life_steal:main banned_players run data modify storage life_steal:main banned_players set value {}
$data modify storage life_steal:main banned_players.$(player) set value true

