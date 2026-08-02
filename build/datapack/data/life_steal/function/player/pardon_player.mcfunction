
#> life_steal:player/pardon_player
#
# @executed	as the player & at current position
#
# @within	life_steal:player/revive {player:"$(player)"}
#			life_steal:player/force_revive {player:"$(player)"}
#
# @args		player (string)
#

$return run pardon $(player)

