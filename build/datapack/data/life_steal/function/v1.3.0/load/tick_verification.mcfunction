
#> life_steal:v1.3.0/load/tick_verification
#
# @within	#minecraft:tick
#

execute if score #life_steal.major load.status matches 1 if score #life_steal.minor load.status matches 3 if score #life_steal.patch load.status matches 0 run function life_steal:v1.3.0/tick

