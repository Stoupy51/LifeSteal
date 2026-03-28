
#> life_steal:player/withdraw
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/tick
#

# Reset withdraw trigger
scoreboard players set @s life_steal.withdraw 0

# Check if player has more than minimum hearts (add 1 if banning is enabled to prevent withdrawing at min+1)
scoreboard players operation #temp life_steal.data = MIN_HEARTS life_steal.data
execute if score USE_HALF_HEARTS life_steal.data matches 1 unless score #temp life_steal.data matches 1 run scoreboard players operation #temp life_steal.data *= #2 life_steal.data
execute if score BAN_REACHING_MIN_HEARTS life_steal.data matches 1 run scoreboard players add #temp life_steal.data 2
execute unless score BAN_REACHING_MIN_HEARTS life_steal.data matches 1 run scoreboard players add #temp life_steal.data 1

# Stop function if not enough hearts
execute if score @s life_steal.hearts < #temp life_steal.data run tellraw @s {"text":"You don't have enough hearts to withdraw!","color":"red"}
execute if score @s life_steal.hearts < #temp life_steal.data run return fail

# Give heart, decrease score, and update health
execute at @s[gamemode=!creative] run loot spawn ~ ~ ~ loot life_steal:i/heart
execute at @s[gamemode=!creative] run data modify entity @n[type=item,distance=..1,nbt={Age:0s}] Owner set from entity @s UUID
execute at @s[gamemode=!creative] run data modify entity @n[type=item,distance=..1,nbt={Age:0s}] PickupDelay set value 0s
scoreboard players remove @s life_steal.hearts 1
function life_steal:player/update_health

# Tellraw message
function life_steal:player/withdraw_msg

