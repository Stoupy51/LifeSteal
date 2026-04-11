
#> life_steal:v2.1.1/load/confirm_load
#
# @within	life_steal:v2.1.1/load/secondary
#

scoreboard objectives add life_steal.kill playerKillCount
scoreboard objectives add life_steal.death deathCount
scoreboard objectives add life_steal.withdraw trigger
scoreboard objectives add life_steal.hearts dummy

scoreboard players set #2 life_steal.data 2

execute unless score MAX_HEARTS life_steal.data matches 1.. run scoreboard players set MAX_HEARTS life_steal.data 20
execute unless score MAX_HEARTS_BY_CONSUMING life_steal.data matches 0.. run scoreboard players set MAX_HEARTS_BY_CONSUMING life_steal.data 20
execute unless score MIN_HEARTS life_steal.data matches 0.. run scoreboard players set MIN_HEARTS life_steal.data 0
execute unless score REVIVED_HEARTS life_steal.data matches 1.. run scoreboard players set REVIVED_HEARTS life_steal.data 4
execute unless score NATURAL_DEATH_HEART_LOSE life_steal.data matches 0..1 run scoreboard players set NATURAL_DEATH_HEART_LOSE life_steal.data 1
execute unless score NATURAL_DEATH_HEART_DROP life_steal.data matches 0..1 run scoreboard players set NATURAL_DEATH_HEART_DROP life_steal.data 1
execute unless score USE_HALF_HEARTS life_steal.data matches 0..1 run scoreboard players set USE_HALF_HEARTS life_steal.data 0
execute unless score USE_HALF_HEARTS_PREV life_steal.data matches 0..1 run scoreboard players operation USE_HALF_HEARTS_PREV life_steal.data = USE_HALF_HEARTS life_steal.data
execute unless score BAN_REACHING_MIN_HEARTS life_steal.data matches 0..1 run scoreboard players set BAN_REACHING_MIN_HEARTS life_steal.data 1
execute unless score STEAL_ON_KILL life_steal.data matches 0..1 run scoreboard players set STEAL_ON_KILL life_steal.data 1
execute unless score INSTANTLY_CONSUME_HEARTS life_steal.data matches 0..1 run scoreboard players set INSTANTLY_CONSUME_HEARTS life_steal.data 0
execute unless score NO_HEART_DROP_OR_STEAL life_steal.data matches 0..1 run scoreboard players set NO_HEART_DROP_OR_STEAL life_steal.data 0
execute unless score HEARTS_NEVER_DESPAWN life_steal.data matches 0..1 run scoreboard players set HEARTS_NEVER_DESPAWN life_steal.data 1
execute unless score SPECTATOR_INSTEAD life_steal.data matches 0..1 run scoreboard players set SPECTATOR_INSTEAD life_steal.data 0
execute unless score LAST_CHANCE life_steal.data matches 0..1 run scoreboard players set LAST_CHANCE life_steal.data 0

# Register the manual to the universal manual
execute unless data storage stewbeet:main universal_manual run data modify storage stewbeet:main universal_manual set value []
data remove storage stewbeet:main universal_manual[{"name":"LifeSteal"}]
data modify storage stewbeet:main universal_manual append value {"name":"LifeSteal","loot_table":"life_steal:i/manual","hover":[{"text": ""}, {"text": "LifeSteal Manual\\n"}, {"text": "ဠ\\n\\n\\n\\n\\n\\n", "font": "life_steal:manual", "color": "white"}, [{"text": "", "font": "minecraft:default", "color": "black"}]]}

# Confirm load
tellraw @a[tag=convention.debug] {"text":"[Loaded LifeSteal v2.1.1]","color":"green"}
scoreboard players set #life_steal.loaded load.status 1
function life_steal:v2.1.1/load/set_items_storage

