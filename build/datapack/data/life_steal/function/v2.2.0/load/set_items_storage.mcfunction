
#> life_steal:v2.2.0/load/set_items_storage
#
# @within	life_steal:v2.2.0/load/confirm_load
#

# Items storage
data modify storage life_steal:items all set value {}
data modify storage life_steal:items all.crafted_heart set value {"id": "minecraft:command_block","count": 1,"components": {"minecraft:item_model": "life_steal:crafted_heart","minecraft:damage_resistant": {"types": "#life_steal:is_explosion_or_fire"},"minecraft:consumable": {},"minecraft:item_name": {"text": "Crafted Heart"},"minecraft:lore": [["",{"text": "I","color": "white","italic": false,"font": "life_steal:icons"},{"text": " LifeSteal","italic": true,"color": "blue"}]],"minecraft:custom_data": {"life_steal": {"crafted_heart": true},"smithed": {"id": "life_steal:crafted_heart","origin": "life_steal","ignore": {"functionality": true,"crafting": true}}}}}
data modify storage life_steal:items all.heart set value {"id": "minecraft:command_block","count": 1,"components": {"minecraft:item_model": "life_steal:heart","minecraft:damage_resistant": {"types": "#life_steal:is_explosion_or_fire"},"minecraft:consumable": {},"minecraft:item_name": {"text": "Heart"},"minecraft:lore": [["",{"text": "I","color": "white","italic": false,"font": "life_steal:icons"},{"text": " LifeSteal","italic": true,"color": "blue"}]],"minecraft:custom_data": {"life_steal": {"heart": true},"smithed": {"id": "life_steal:heart","origin": "life_steal","ignore": {"functionality": true,"crafting": true}}}}}
data modify storage life_steal:items all.revive_beacon set value {"id": "minecraft:command_block","count": 1,"components": {"minecraft:item_model": "life_steal:revive_beacon","minecraft:consumable": {},"minecraft:lore": [{"text": "Rename the item to the username","italic": false,"color": "gray"},{"text": "of the player you want to revive.","italic": false,"color": "gray"},["",{"text": "I","color": "white","italic": false,"font": "life_steal:icons"},{"text": " LifeSteal","italic": true,"color": "blue"}]],"minecraft:item_name": {"text": "Revive Beacon"},"minecraft:custom_data": {"life_steal": {"revive_beacon": true},"smithed": {"id": "life_steal:revive_beacon","origin": "life_steal","ignore": {"functionality": true,"crafting": true}}}}}

