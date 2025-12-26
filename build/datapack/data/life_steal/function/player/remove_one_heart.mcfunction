
#> life_steal:player/remove_one_heart
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/on_death
#

# Check for last chance condition (only when half hearts mode is disabled)
scoreboard players set #lose_heart_msg life_steal.data 1
execute if score LAST_CHANCE life_steal.data matches 1 unless score USE_HALF_HEARTS life_steal.data matches 1 unless entity @s[tag=life_steal.last_chance] run function life_steal:player/check_last_chance

# Remove one heart
scoreboard players remove @s life_steal.hearts 1

# Tellraw message and update health
execute if score #lose_heart_msg life_steal.data matches 1 run function life_steal:player/lose_heart_msg
function life_steal:player/update_health

# Drop a heart if player wasn't killed by another, and if NO_HEART_DROP_OR_STEAL and NATURAL_DEATH_HEART_DROP are enabled
execute unless score NO_HEART_DROP_OR_STEAL life_steal.data matches 1 unless entity @a[scores={life_steal.kill=1..}] if score NATURAL_DEATH_HEART_DROP life_steal.data matches 1 run function life_steal:player/drop_heart_at_death

