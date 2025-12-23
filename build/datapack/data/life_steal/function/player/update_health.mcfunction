
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
#			life_steal:player/revive
#			life_steal:config/convert_to_half_hearts [ as @a ]
#			life_steal:config/convert_to_full_hearts [ as @a ]
#

execute if score USE_HALF_HEARTS life_steal.data matches 0 store result storage life_steal:main health int 2 run scoreboard players get @s life_steal.hearts
execute if score USE_HALF_HEARTS life_steal.data matches 1 store result storage life_steal:main health int 1 run scoreboard players get @s life_steal.hearts

# Remove 1 health point if player has last_chance tag, since they are at MIN_HEARTS + 1 (we want to keep them at MIN_HEARTS .5)
execute if entity @s[tag=life_steal.last_chance] store result score #temp life_steal.data run data get storage life_steal:main health
execute if entity @s[tag=life_steal.last_chance] run scoreboard players remove #temp life_steal.data 1
execute if entity @s[tag=life_steal.last_chance] store result storage life_steal:main health int 1 run scoreboard players get #temp life_steal.data

function life_steal:player/update_macro with storage life_steal:main
execute at @s run playsound entity.player.levelup ambient @s

