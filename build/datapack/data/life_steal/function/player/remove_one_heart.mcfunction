
#> life_steal:player/remove_one_heart
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/on_death
#

# Remove one heart
scoreboard players remove @s life_steal.hearts 1

# Tellraw message and update health
function life_steal:player/lose_heart_msg
function life_steal:player/update_health

# Drop a heart if player wasn't killed by another, and if NO_HEART_DROP is disabled
execute unless score NO_HEART_DROP life_steal.data matches 1 unless entity @a[scores={life_steal.kill=1..}] run function life_steal:player/drop_heart_at_death

