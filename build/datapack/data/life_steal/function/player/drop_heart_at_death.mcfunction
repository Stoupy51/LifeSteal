
#> life_steal:player/drop_heart_at_death
#
# @executed	as @a[sort=random,scores={life_steal.death=1..}]
#
# @within	life_steal:player/remove_one_heart
#

# Copy in a storage the arguments for the macro
data modify storage life_steal:main death_pos set value {dimension:"minecraft:overworld",x:0,y:0,z:0}
data modify storage life_steal:main death_pos.dimension set from entity @s LastDeathLocation.dimension
data modify storage life_steal:main death_pos.x set from entity @s LastDeathLocation.pos[0]
data modify storage life_steal:main death_pos.y set from entity @s LastDeathLocation.pos[1]
data modify storage life_steal:main death_pos.z set from entity @s LastDeathLocation.pos[2]

# Drop the heart
function life_steal:player/drop_heart_macro with storage life_steal:main death_pos

