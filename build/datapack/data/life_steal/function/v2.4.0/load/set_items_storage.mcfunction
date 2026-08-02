
#> life_steal:v2.4.0/load/set_items_storage
#
# @within	life_steal:v2.4.0/load/confirm_load
#

# Items storage
data modify storage life_steal:items all set value {}
data modify storage life_steal:items all.crafted_heart set value {"id": "minecraft:recovery_compass","count": 1,"components": {"minecraft:item_model": "life_steal:crafted_heart","minecraft:damage_resistant": {"types": "#life_steal:is_explosion_or_fire"},"minecraft:consumable": {},"minecraft:item_name": {"text": "Crafted Heart"},"minecraft:lore": [["",{"text": "ꀁ","color": "white","italic": false,"font": "life_steal:tooltip"},{"text": "뀁LifeSteal","italic": false,"color": "white","font": "life_steal:tooltip"}]],"minecraft:custom_data": {"life_steal": {"crafted_heart": true},"smithed": {"id": "life_steal:crafted_heart","origin": "life_steal","ignore": {"functionality": true,"crafting": true}}}}}
data modify storage life_steal:items all.heart set value {"id": "minecraft:recovery_compass","count": 1,"components": {"minecraft:item_model": "life_steal:heart","minecraft:damage_resistant": {"types": "#life_steal:is_explosion_or_fire"},"minecraft:consumable": {},"minecraft:item_name": {"text": "Heart"},"minecraft:lore": [["",{"text": "ꀁ","color": "white","italic": false,"font": "life_steal:tooltip"},{"text": "뀁LifeSteal","italic": false,"color": "white","font": "life_steal:tooltip"}]],"minecraft:custom_data": {"life_steal": {"heart": true},"smithed": {"id": "life_steal:heart","origin": "life_steal","ignore": {"functionality": true,"crafting": true}}}}}
data modify storage life_steal:items all.revive_beacon set value {"id": "minecraft:recovery_compass","count": 1,"components": {"minecraft:item_model": "life_steal:revive_beacon","minecraft:consumable": {},"minecraft:lore": [{"text": "Rename the item to the username","italic": false,"color": "gray"},{"text": "of the player you want to revive.","italic": false,"color": "gray"},{"text": "Then, consume it to revive the player.","italic": false,"color": "gray"},["",{"text": "ꀁ","color": "white","italic": false,"font": "life_steal:tooltip"},{"text": "뀁LifeSteal","italic": false,"color": "white","font": "life_steal:tooltip"}]],"minecraft:item_name": {"text": "Revive Beacon"},"minecraft:custom_data": {"life_steal": {"revive_beacon": true},"smithed": {"id": "life_steal:revive_beacon","origin": "life_steal","ignore": {"functionality": true,"crafting": true}}}}}

