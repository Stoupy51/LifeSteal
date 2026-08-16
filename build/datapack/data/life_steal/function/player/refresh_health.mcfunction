
#> life_steal:player/refresh_health
#
# @within	life_steal:player/set_hearts {player:"$(player)"}
#
# @args		player (string)
#

# Update the health right away when the player is connected
$execute as $(player) run function life_steal:player/update_health

# Else, flag them so the tick function updates their health on their next join
$execute unless entity @a[name=$(player)] run scoreboard players set $(player) life_steal.data 2

