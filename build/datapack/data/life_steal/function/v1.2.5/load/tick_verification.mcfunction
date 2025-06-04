
#> life_steal:v1.2.5/load/tick_verification
#
# @within	#minecraft:tick
#

execute if score #life_steal.major load.status matches 1 if score #life_steal.minor load.status matches 2 if score #life_steal.patch load.status matches 5 run function life_steal:v1.2.5/tick

