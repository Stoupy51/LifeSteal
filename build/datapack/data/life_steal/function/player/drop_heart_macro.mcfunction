
#> life_steal:player/drop_heart_macro
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/drop_heart_at_death with storage life_steal:main death_pos
#

$execute in $(dimension) run loot spawn $(x) $(y) $(z) loot life_steal:i/heart

