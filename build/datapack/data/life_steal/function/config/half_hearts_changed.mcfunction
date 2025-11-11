
#> life_steal:config/half_hearts_changed
#
# @within	life_steal:v1.3.3/tick
#

# Convert hearts for all players based on new configuration
execute if score USE_HALF_HEARTS life_steal.data matches 1 if score USE_HALF_HEARTS_PREV life_steal.data matches 0 run function life_steal:config/convert_to_half_hearts
execute if score USE_HALF_HEARTS life_steal.data matches 0 if score USE_HALF_HEARTS_PREV life_steal.data matches 1 run function life_steal:config/convert_to_full_hearts

# Update previous value
scoreboard players operation USE_HALF_HEARTS_PREV life_steal.data = USE_HALF_HEARTS life_steal.data

