
#> life_steal:config/convert_to_half_hearts
#
# @within	life_steal:config/half_hearts_changed
#

# Convert all players from full hearts to half hearts (multiply by 2)
execute as @a run scoreboard players operation @s life_steal.hearts *= #2 life_steal.data
execute as @a run function life_steal:player/update_health

# Notify all players
tellraw @a [{"text":"[Life Steal] Configuration changed to half hearts mode! All hearts score have been doubled.","color":"green"}]
execute as @a at @s run playsound entity.experience_orb.pickup ambient @s

