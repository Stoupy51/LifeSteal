
#> life_steal:player/tick
#
# @within	life_steal:v1.0.0/tick
#

# Setup hearts objective if not set and get all recipes
execute unless score @s life_steal.hearts matches 0.. run function life_steal:utils/get_all_recipes
execute unless score @s life_steal.hearts matches 0.. store result score @s life_steal.hearts run attribute @s minecraft:generic.max_health base get 0.5

# If data = 1, player is revived so update health
execute if score @s life_steal.data matches 1 run function life_steal:player/update_health
execute if score @s life_steal.data matches 1 run scoreboard players set @s life_steal.data 0

# Withdraw command trigger
scoreboard players enable @s life_steal.withdraw
execute unless score @s life_steal.withdraw matches 0 run function life_steal:player/withdraw

# If killed player, add a heart
execute if score @s life_steal.kill matches 1.. if score @s life_steal.hearts >= MAX_HEARTS life_steal.data run tellraw @s [{"text":"You stole a heart from a player, but you are already at max health!","color":"red"}]
execute if score @s life_steal.kill matches 1.. if score @s life_steal.hearts < MAX_HEARTS life_steal.data run scoreboard players operation @s life_steal.hearts += @s life_steal.kill
execute if score @s life_steal.kill matches 1.. if score @s life_steal.hearts < MAX_HEARTS life_steal.data run tellraw @s [{"text":"You stole a heart from a player, you now have ","color":"gray"},{"score":{"name":"@s","objective":"life_steal.hearts"}, "color":"red"},{"text":" hearts!"}]
execute if score @s life_steal.kill matches 1.. run function life_steal:player/update_health
execute if score @s life_steal.kill matches 1.. run scoreboard players set @s life_steal.kill 0

# If player died, remove a heart
execute if score @s life_steal.death matches 1.. run scoreboard players remove @s life_steal.hearts 1
execute if score @s life_steal.death matches 1.. run tellraw @s [{"text":"You lost a heart, you now have ","color":"gray"},{"score":{"name":"@s","objective":"life_steal.hearts"}, "color":"red"},{"text":" hearts!"}]
execute if score @s life_steal.death matches 1.. run function life_steal:player/update_health
execute if score @s life_steal.death matches 1.. unless entity @a[scores={life_steal.kill=1..}] run function life_steal:player/drop_heart_at_death
execute if score @s life_steal.death matches 1.. run scoreboard players set @s life_steal.death 0
execute if score @s life_steal.hearts matches 0 run function life_steal:player/death

