
#> life_steal:player/add_to_banned_list
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/reached_min_hearts with storage life_steal:main
#			life_steal:player/ban_macro with storage life_steal:main
#
# @args		player (unknown)
#

$data modify storage life_steal:main banned_players.$(player) set value true

