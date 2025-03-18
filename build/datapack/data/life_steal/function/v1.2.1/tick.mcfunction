
#> life_steal:v1.2.1/tick
#
# @within	life_steal:v1.2.1/load/tick_verification
#

execute as @a[sort=random,scores={life_steal.death=1..}] run function life_steal:player/tick
execute as @a[sort=random] run function life_steal:player/tick

