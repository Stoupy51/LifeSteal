
#> life_steal:v1.8.0/tick
#
# @within	life_steal:v1.8.0/load/tick_verification
#

# Check for USE_HALF_HEARTS configuration change
execute unless score USE_HALF_HEARTS life_steal.data = USE_HALF_HEARTS_PREV life_steal.data run function life_steal:config/half_hearts_changed

execute as @a[sort=random,scores={life_steal.death=1..}] run function life_steal:player/tick
execute as @a[sort=random] run function life_steal:player/tick

