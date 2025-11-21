
#> life_steal:player/withdraw
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/tick
#

# Reset withdraw trigger and stop function if not enough hearts
scoreboard players set @s life_steal.withdraw 0
execute if score @s life_steal.hearts matches ..1 run tellraw @s {"text":"You don't have enough hearts to withdraw!","color":"red"}
execute if score @s life_steal.hearts matches ..1 run return fail

# Give heart, decrease score, and update health
loot give @s[gamemode=!creative] loot life_steal:i/heart
scoreboard players remove @s life_steal.hearts 1
function life_steal:player/update_health

# Tellraw message
function life_steal:player/withdraw_msg

