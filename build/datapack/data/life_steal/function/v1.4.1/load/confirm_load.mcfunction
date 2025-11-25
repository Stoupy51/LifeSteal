
#> life_steal:v1.4.1/load/confirm_load
#
# @within	life_steal:v1.4.1/load/secondary
#

scoreboard objectives add life_steal.kill playerKillCount
scoreboard objectives add life_steal.death deathCount
scoreboard objectives add life_steal.withdraw trigger
scoreboard objectives add life_steal.hearts dummy

scoreboard players set #2 life_steal.data 2

execute unless score MAX_HEARTS life_steal.data matches 1.. run scoreboard players set MAX_HEARTS life_steal.data 20
execute unless score MIN_HEARTS life_steal.data matches 1.. run scoreboard players set MIN_HEARTS life_steal.data 1
execute unless score REVIVED_HEARTS life_steal.data matches 1.. run scoreboard players set REVIVED_HEARTS life_steal.data 4
execute unless score NATURAL_DEATH_HEART_DROP life_steal.data matches 0..1 run scoreboard players set NATURAL_DEATH_HEART_DROP life_steal.data 1
execute unless score USE_HALF_HEARTS life_steal.data matches 0..1 run scoreboard players set USE_HALF_HEARTS life_steal.data 0
execute unless score USE_HALF_HEARTS_PREV life_steal.data matches 0..1 run scoreboard players operation USE_HALF_HEARTS_PREV life_steal.data = USE_HALF_HEARTS life_steal.data
execute unless score BAN_BELOW_MIN_HEARTS life_steal.data matches 0..1 run scoreboard players set BAN_BELOW_MIN_HEARTS life_steal.data 1

# Confirm load
tellraw @a[tag=convention.debug] {"text":"[Loaded LifeSteal v1.4.1]","color":"green"}
scoreboard players set #life_steal.loaded load.status 1

# Items storage
data modify storage life_steal:items all set value {}
data modify storage life_steal:items all.heart set value {"id": "minecraft:command_block","count": 1,"components": {"minecraft:item_model": "life_steal:heart","minecraft:damage_resistant": {"types": "#life_steal:is_explosion_or_fire"},"minecraft:consumable": {},"minecraft:item_name": {"text": "Heart"},"minecraft:lore": [["",{"text": "I","color": "white","italic": false,"font": "life_steal:icons"},{"text": " LifeSteal","italic": true,"color": "blue"}]],"minecraft:custom_data": {"life_steal": {"heart": true},"smithed": {"ignore": {"functionality": true,"crafting": true}}}}}
data modify storage life_steal:items all.revive_beacon set value {"id": "minecraft:command_block","count": 1,"components": {"minecraft:item_model": "life_steal:revive_beacon","minecraft:consumable": {},"minecraft:lore": [{"text": "Rename the item to the username","italic": false,"color": "gray"},{"text": "of the player you want to revive.","italic": false,"color": "gray"},["",{"text": "I","color": "white","italic": false,"font": "life_steal:icons"},{"text": " LifeSteal","italic": true,"color": "blue"}]],"minecraft:item_name": {"text": "Revive Beacon"},"minecraft:custom_data": {"life_steal": {"revive_beacon": true},"smithed": {"ignore": {"functionality": true,"crafting": true}}}}}

