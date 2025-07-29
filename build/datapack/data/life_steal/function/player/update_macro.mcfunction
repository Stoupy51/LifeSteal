
#> life_steal:player/update_macro
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/update_health with storage life_steal:main
#

$attribute @s max_health base set $(health)

