
#> life_steal:v1.7.2/load/valid_dependencies
#
# @within	life_steal:v1.7.2/load/secondary
#			life_steal:v1.7.2/load/valid_dependencies 1t replace [ scheduled ]
#

# Waiting for a player to get the game version, but stop function if no player found
execute unless entity @p run schedule function life_steal:v1.7.2/load/valid_dependencies 1t replace
execute unless entity @p run return 0
execute store result score #game_version life_steal.data run data get entity @p DataVersion

# Check if the game version is supported
scoreboard players set #mcload_error life_steal.data 0
execute unless score #game_version life_steal.data matches 4325.. run scoreboard players set #mcload_error life_steal.data 1

# Decode errors
execute if score #mcload_error life_steal.data matches 1 run tellraw @a {"text":"LifeSteal Error: This version is made for Minecraft 1.21.5+.","color":"red"}
execute if score #dependency_error life_steal.data matches 1 run tellraw @a {"text":"LifeSteal Error: Libraries are missing\nplease download the right LifeSteal datapack\nor download each of these libraries one by one:","color":"red"}
execute if score #dependency_error life_steal.data matches 1 unless score #smithed.crafter.major load.status matches 0.. run tellraw @a {"text":"- [Smithed Crafter (v0.7.1+)]","color":"gold","click_event":{"action":"open_url","url":"https://wiki.smithed.dev/libraries/crafter/"}}
execute if score #dependency_error life_steal.data matches 1 if score #smithed.crafter.major load.status matches 0 unless score #smithed.crafter.minor load.status matches 7.. run tellraw @a {"text":"- [Smithed Crafter (v0.7.1+)]","color":"gold","click_event":{"action":"open_url","url":"https://wiki.smithed.dev/libraries/crafter/"}}
execute if score #dependency_error life_steal.data matches 1 if score #smithed.crafter.major load.status matches 0 if score #smithed.crafter.minor load.status matches 7 unless score #smithed.crafter.patch load.status matches 1.. run tellraw @a {"text":"- [Smithed Crafter (v0.7.1+)]","color":"gold","click_event":{"action":"open_url","url":"https://wiki.smithed.dev/libraries/crafter/"}}

# Load LifeSteal
execute if score #game_version life_steal.data matches 1.. if score #mcload_error life_steal.data matches 0 if score #dependency_error life_steal.data matches 0 run function life_steal:v1.7.2/load/confirm_load

