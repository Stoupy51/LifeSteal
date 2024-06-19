
#> life_steal:player/drop_heart_macro
#
# @within	life_steal:player/drop_heart_at_death with storage life_steal:main death_pos
#

$execute in $(dimension) run loot spawn $(x) $(y) $(z) loot life_steal:i/heart

