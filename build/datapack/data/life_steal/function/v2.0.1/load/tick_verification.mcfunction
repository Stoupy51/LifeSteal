
#> life_steal:v2.0.1/load/tick_verification
#
# @within	#minecraft:tick
#

execute if score #life_steal.major load.status matches 2 if score #life_steal.minor load.status matches 0 if score #life_steal.patch load.status matches 1 run function life_steal:v2.0.1/tick

