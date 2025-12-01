
#> life_steal:player/on_death
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/tick
#

# Reset death score
scoreboard players set @s life_steal.death 0

# Calculate minimum hearts threshold
execute store result score #real_min_hearts life_steal.data run scoreboard players get MIN_HEARTS life_steal.data
execute if score USE_HALF_HEARTS life_steal.data matches 1 unless score #real_min_hearts life_steal.data matches 1 run scoreboard players operation #real_min_hearts life_steal.data *= #2 life_steal.data

# If (died from a player), or (died from natural causes and configuration is 1), remove a heart (only if above minimum)
execute if score @s life_steal.hearts > #real_min_hearts life_steal.data if entity @a[scores={life_steal.kill=1..}] run function life_steal:player/remove_one_heart
execute if score @s life_steal.hearts > #real_min_hearts life_steal.data unless entity @a[scores={life_steal.kill=1..}] unless score NATURAL_DEATH_HEART_DROP life_steal.data matches 0 run function life_steal:player/remove_one_heart

# Check if fall below minimum hearts
execute if score @s life_steal.hearts <= #real_min_hearts life_steal.data run function life_steal:player/below_min_hearts

# Update health
function life_steal:player/update_health

