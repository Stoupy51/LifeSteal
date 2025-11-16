
#> life_steal:player/tick
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:v1.3.5/tick [ as @a[sort=random,scores={life_steal.death=1..}] ]
#			life_steal:v1.3.5/tick [ as @a[sort=random] ]
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
execute if score @s life_steal.kill matches 1.. run scoreboard players operation #temp life_steal.data = MAX_HEARTS life_steal.data
execute if score @s life_steal.kill matches 1.. if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation #temp life_steal.data *= #2 life_steal.data
execute if score @s life_steal.kill matches 1.. if score @s life_steal.hearts >= #temp life_steal.data run tellraw @s [{"text":"You stole a heart from a player, but you are already at max health!","color":"red"}]
execute if score @s life_steal.kill matches 1.. if score @s life_steal.hearts < #temp life_steal.data run scoreboard players operation #add life_steal.data = @s life_steal.kill
execute if score @s life_steal.kill matches 1.. if score @s life_steal.hearts < #temp life_steal.data if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation #add life_steal.data *= #2 life_steal.data
execute if score @s life_steal.kill matches 1.. if score @s life_steal.hearts < #temp life_steal.data run scoreboard players operation @s life_steal.hearts += #add life_steal.data
execute if score @s life_steal.kill matches 1.. if score @s life_steal.hearts < #temp life_steal.data run function life_steal:player/gain_heart_msg
execute if score @s life_steal.kill matches 1.. run function life_steal:player/update_health
execute if score @s life_steal.kill matches 1.. run scoreboard players set @s life_steal.kill 0

# If (died from a player), or (died from natural causes and configuration is 1), remove a heart
execute if score @s life_steal.death matches 1.. if entity @a[scores={life_steal.kill=1..}] run function life_steal:player/remove_one_heart
execute if score @s life_steal.death matches 1.. unless entity @a[scores={life_steal.kill=1..}] unless score NATURAL_DEATH_HEART_DROP life_steal.data matches 0 run function life_steal:player/remove_one_heart
execute if score @s life_steal.death matches 1.. run function life_steal:player/update_health
execute if score @s life_steal.death matches 1.. if score @s life_steal.hearts matches ..0 run function life_steal:player/reached_0_heart
execute if score @s life_steal.death matches 1.. run scoreboard players set @s life_steal.death 0

