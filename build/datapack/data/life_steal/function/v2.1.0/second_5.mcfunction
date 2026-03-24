
#> life_steal:v2.1.0/second_5
#
# @within	life_steal:v2.1.0/tick
#

# Reset timer
scoreboard players set #second_5 life_steal.data -10

# Keep dropped LifeSteal items from despawning when enabled.
execute if score HEARTS_NEVER_DESPAWN life_steal.data matches 1 as @e[type=item,nbt={Item:{components:{"minecraft:custom_data":{life_steal:{}}}}}] run data modify entity @s Age set value 0s

