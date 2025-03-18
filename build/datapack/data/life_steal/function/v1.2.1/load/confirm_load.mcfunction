
#> life_steal:v1.2.1/load/confirm_load
#
# @within	life_steal:v1.2.1/load/secondary
#

scoreboard objectives add life_steal.kill playerKillCount
scoreboard objectives add life_steal.death deathCount
scoreboard objectives add life_steal.withdraw trigger
scoreboard objectives add life_steal.hearts dummy
execute unless score MAX_HEARTS life_steal.data matches 1.. run scoreboard players set MAX_HEARTS life_steal.data 20
execute unless score REVIVED_HEARTS life_steal.data matches 1.. run scoreboard players set REVIVED_HEARTS life_steal.data 4

# Confirm load
tellraw @a[tag=convention.debug] {"text":"[Loaded LifeSteal v1.2.1]","color":"green"}
scoreboard players set #life_steal.loaded load.status 1

# Items storage
data modify storage life_steal:items all set value {}
data modify storage life_steal:items all.heart set value {"id": "minecraft:command_block","count": 1,"components": {"minecraft:item_model": "life_steal:heart","minecraft:consumable": {},"minecraft:item_name": {"text": "Heart","italic": false,"color": "white"},"minecraft:lore": [[{"text": "LifeSteal","italic": true,"color": "blue"}]],"minecraft:custom_data": {"life_steal": {"heart": true},"smithed": {"ignore": {"functionality": true,"crafting": true}}}}}
data modify storage life_steal:items all.revive_beacon set value {"id": "minecraft:command_block","count": 1,"components": {"minecraft:item_model": "life_steal:revive_beacon","minecraft:consumable": {},"minecraft:lore": [{"text": "Rename the item to the username","italic": false,"color": "gray"},{"text": "of the player you want to revive.","italic": false,"color": "gray"},[{"text": "LifeSteal","italic": true,"color": "blue"}]],"minecraft:item_name": {"text": "Revive Beacon","italic": false,"color": "white"},"minecraft:custom_data": {"life_steal": {"revive_beacon": true},"smithed": {"ignore": {"functionality": true,"crafting": true}}}}}

