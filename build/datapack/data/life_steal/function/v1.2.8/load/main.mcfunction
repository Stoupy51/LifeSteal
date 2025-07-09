
#> life_steal:v1.2.8/load/main
#
# @within	life_steal:v1.2.8/load/resolve
#

# Avoiding multiple executions of the same load function
execute unless score #life_steal.loaded load.status matches 1 run function life_steal:v1.2.8/load/secondary

