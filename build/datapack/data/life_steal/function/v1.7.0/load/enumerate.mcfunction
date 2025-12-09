
#> life_steal:v1.7.0/load/enumerate
#
# @within	#life_steal:enumerate
#

# If current major is too low, set it to the current major
execute unless score #life_steal.major load.status matches 1.. run scoreboard players set #life_steal.major load.status 1

# If current minor is too low, set it to the current minor (only if major is correct)
execute if score #life_steal.major load.status matches 1 unless score #life_steal.minor load.status matches 7.. run scoreboard players set #life_steal.minor load.status 7

# If current patch is too low, set it to the current patch (only if major and minor are correct)
execute if score #life_steal.major load.status matches 1 if score #life_steal.minor load.status matches 7 unless score #life_steal.patch load.status matches 0.. run scoreboard players set #life_steal.patch load.status 0

