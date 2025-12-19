
#> life_steal:v1.7.2/load/check_dependencies
#
# @within	life_steal:v1.7.2/load/secondary
#

## Check if LifeSteal is loadable (dependencies)
scoreboard players set #dependency_error life_steal.data 0
execute if score #dependency_error life_steal.data matches 0 unless score #smithed.crafter.major load.status matches 0.. run scoreboard players set #dependency_error life_steal.data 1
execute if score #dependency_error life_steal.data matches 0 if score #smithed.crafter.major load.status matches 0 unless score #smithed.crafter.minor load.status matches 7.. run scoreboard players set #dependency_error life_steal.data 1
execute if score #dependency_error life_steal.data matches 0 if score #smithed.crafter.major load.status matches 0 if score #smithed.crafter.minor load.status matches 7 unless score #smithed.crafter.patch load.status matches 1.. run scoreboard players set #dependency_error life_steal.data 1

