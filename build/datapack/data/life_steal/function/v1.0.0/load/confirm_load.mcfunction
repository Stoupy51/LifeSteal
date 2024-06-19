
#> life_steal:v1.0.0/load/confirm_load
#
# @within	life_steal:v1.0.0/load/secondary
#

execute unless score MAX_HEARTS life_steal.data matches 1.. run scoreboard players set MAX_HEARTS life_steal.data 20
scoreboard objectives add life_steal.hearts dummy
scoreboard objectives add life_steal.withdraw trigger
scoreboard objectives add life_steal.death deathCount
scoreboard objectives add life_steal.kill playerKillCount

tellraw @a[tag=convention.debug] {"text":"[Loaded LifeSteal v1.0.0]","color":"green"}

scoreboard players set #life_steal.loaded load.status 1

# Items storage
data modify storage life_steal:items all set value {}
data modify storage life_steal:items all.heart set value {"id": "minecraft:command_block","count": 1,"components": {"custom_model_data": 2010100,"food": {"can_always_eat": true,"nutrition": 0,"saturation": 0},"item_name": "{'text': 'Heart', 'italic': false, 'color': 'white'}","lore": ["{'text': 'LifeSteal', 'italic': true, 'color': 'blue'}"],"custom_data": {"life_steal": {"heart": true},"smithed": {"ignore": {"functionality": true,"crafting": true}}}}}
data modify storage life_steal:items all.revive_beacon set value {"id": "minecraft:command_block","count": 1,"components": {"custom_model_data": 2010101,"food": {"can_always_eat": true,"nutrition": 0,"saturation": 0},"item_name": "{'text': 'Revive Beacon', 'italic': false, 'color': 'white'}","lore": ["{'text': 'LifeSteal', 'italic': true, 'color': 'blue'}"],"custom_data": {"life_steal": {"revive_beacon": true},"smithed": {"ignore": {"functionality": true,"crafting": true}}}}}

