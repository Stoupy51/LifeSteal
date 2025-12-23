
#> life_steal:player/check_last_chance
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/remove_one_heart
#

# Calculate if player is at MIN_HEARTS + 1
scoreboard players operation #check_hearts life_steal.data = MIN_HEARTS life_steal.data
scoreboard players add #check_hearts life_steal.data 1

# If player is at MIN_HEARTS + 1, give them last chance tag
execute if score @s life_steal.hearts = #check_hearts life_steal.data run tag @s add life_steal.last_chance
execute if score @s life_steal.hearts = #check_hearts life_steal.data run tellraw @s [{"text":"⚠ Last Chance! You now have ","color":"gold"},{"score":{"name":"MIN_HEARTS","objective":"life_steal.data"},"color":"red"},{"text":".5 hearts!","color":"red"}]
execute if score @s life_steal.hearts = #check_hearts life_steal.data run scoreboard players set #lose_heart_msg life_steal.data 0

# Add 1 heart back (to prevent going below MIN_HEARTS)
execute if score @s life_steal.hearts = #check_hearts life_steal.data run scoreboard players add @s life_steal.hearts 1

