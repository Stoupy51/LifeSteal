
#> life_steal:config/convert_to_full_hearts
#
# @within	life_steal:config/half_hearts_changed
#

# Convert all players from half hearts to full hearts (divide by 2)
execute as @a run scoreboard players operation @s life_steal.hearts /= #2 life_steal.data
execute as @a run function life_steal:player/update_health

# Notify all players
tellraw @a [{"text":"[Life Steal] Configuration changed to full hearts mode! All hearts score have been halved.","color":"yellow"}]
execute as @a at @s run playsound entity.experience_orb.pickup ambient @s

