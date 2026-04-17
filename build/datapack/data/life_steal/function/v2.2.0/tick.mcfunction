
#> life_steal:v2.2.0/tick
#
# @within	life_steal:v2.2.0/load/tick_verification
#

# Timers
scoreboard players add #second_5 life_steal.data 1
execute if score #second_5 life_steal.data matches 90.. run function life_steal:v2.2.0/second_5

# Check for USE_HALF_HEARTS configuration change
execute unless score USE_HALF_HEARTS life_steal.data = USE_HALF_HEARTS_PREV life_steal.data run function life_steal:config/half_hearts_changed

# Run player tick function for players that have died to handle death logic, then run it for all players to handle other logic.
execute as @a[sort=random,scores={life_steal.death=1..}] run function life_steal:player/tick
execute as @a[sort=random] run function life_steal:player/tick

