
#> life_steal:v1.5.1/load/resolve
#
# @within	#life_steal:resolve
#

# If correct version, load the datapack
execute if score #life_steal.major load.status matches 1 if score #life_steal.minor load.status matches 5 if score #life_steal.patch load.status matches 1 run function life_steal:v1.5.1/load/main

