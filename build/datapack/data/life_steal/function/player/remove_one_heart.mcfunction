
#> life_steal:player/remove_one_heart
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/on_death
#

# Remove one heart
scoreboard players remove @s life_steal.hearts 1

# Stop not BAN_BELOW_MIN_HEARTS configuration and under minimum hearts
execute if score @s life_steal.hearts < #real_min_hearts life_steal.data unless score BAN_BELOW_MIN_HEARTS life_steal.data matches 1 run return 1

# Tellraw message and update health
function life_steal:player/lose_heart_msg
function life_steal:player/update_health

# Drop a heart if player wasn't killed by another player
execute unless entity @a[scores={life_steal.kill=1..}] run function life_steal:player/drop_heart_at_death

