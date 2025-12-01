
#> life_steal:player/tick
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:v1.5.0/tick [ as @a[sort=random,scores={life_steal.death=1..}] ]
#			life_steal:v1.5.0/tick [ as @a[sort=random] ]
#

# Setup hearts objective if not set and get all recipes
execute unless score @s life_steal.hearts matches 0.. run function life_steal:utils/get_all_recipes
execute unless score @s life_steal.hearts matches 0.. if score USE_HALF_HEARTS life_steal.data matches 0 store result score @s life_steal.hearts run attribute @s minecraft:max_health base get 0.5
execute unless score @s life_steal.hearts matches 0.. if score USE_HALF_HEARTS life_steal.data matches 1 store result score @s life_steal.hearts run attribute @s minecraft:max_health base get 1.0

# If data = 1, player is revived so update health
execute if score @s life_steal.data matches 1 run function life_steal:player/update_health
execute if score @s life_steal.data matches 1 run scoreboard players set @s life_steal.data 0

# Withdraw command trigger
scoreboard players enable @s life_steal.withdraw
execute unless score @s life_steal.withdraw matches 0 run function life_steal:player/withdraw

# If killed player, add a heart
execute if score @s life_steal.kill matches 1.. run function life_steal:player/on_kill

# On any death, run on_death function
execute if score @s life_steal.death matches 1.. run function life_steal:player/on_death

