
#> life_steal:player/drop_heart_at_death
#
# @within	life_steal:player/tick
#

# If NATURAL_DEATH_HEART_DROP is 0, don't drop a heart, give back the lost heart
execute if score NATURAL_DEATH_HEART_DROP life_steal.data matches 0 run return scoreboard players add @s life_steal.hearts 1

# Copy in a storage the arguments for the macro
data modify storage life_steal:main death_pos set value {dimension:"minecraft:overworld",x:0,y:0,z:0}
data modify storage life_steal:main death_pos.dimension set from entity @s LastDeathLocation.dimension
data modify storage life_steal:main death_pos.x set from entity @s LastDeathLocation.pos[0]
data modify storage life_steal:main death_pos.y set from entity @s LastDeathLocation.pos[1]
data modify storage life_steal:main death_pos.z set from entity @s LastDeathLocation.pos[2]

# Drop the heart
function life_steal:player/drop_heart_macro with storage life_steal:main death_pos

