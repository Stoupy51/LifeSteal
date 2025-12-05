
#> life_steal:player/update_health
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/tick
#			life_steal:player/on_kill
#			life_steal:player/on_death
#			life_steal:player/remove_one_heart
#			life_steal:player/withdraw
#			life_steal:player/consume_heart
#			life_steal:player/using_heart
#			life_steal:player/below_min_hearts
#			life_steal:config/convert_to_half_hearts [ as @a ]
#			life_steal:config/convert_to_full_hearts [ as @a ]
#

execute if score USE_HALF_HEARTS life_steal.data matches 0 store result storage life_steal:main health int 2 run scoreboard players get @s life_steal.hearts
execute if score USE_HALF_HEARTS life_steal.data matches 1 store result storage life_steal:main health int 1 run scoreboard players get @s life_steal.hearts
function life_steal:player/update_macro with storage life_steal:main
execute at @s run playsound entity.player.levelup ambient @s

