
# Imports
import stouputils as stp
from python_datapack.constants import *
from python_datapack.utils.io import *

# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def main(config: dict) -> None:
	namespace: str = config["namespace"]
	functions: str = f"{config['build_datapack']}/data/{namespace}/function"
	version: str = config["version"]

	# Add scoreboard objectives
	write_to_load_file(config, f"""
scoreboard objectives add {namespace}.kill playerKillCount
scoreboard objectives add {namespace}.death deathCount
scoreboard objectives add {namespace}.withdraw trigger
scoreboard objectives add {namespace}.hearts dummy
execute unless score MAX_HEARTS {namespace}.data matches 1.. run scoreboard players set MAX_HEARTS {namespace}.data 20
execute unless score REVIVED_HEARTS {namespace}.data matches 1.. run scoreboard players set REVIVED_HEARTS {namespace}.data 4
""", prepend = True)

	# Add tick function
	write_to_tick_file(config, f"""
execute as @a[sort=random,scores={{{namespace}.death=1..}}] run function {namespace}:player/tick
execute as @a[sort=random] run function {namespace}:player/tick
""")

	# Add player function
	write_to_file(f"{functions}/player/tick.mcfunction", f"""
# Setup hearts objective if not set and get all recipes
execute unless score @s {namespace}.hearts matches 0.. run function {namespace}:utils/get_all_recipes
execute unless score @s {namespace}.hearts matches 0.. store result score @s {namespace}.hearts run attribute @s minecraft:max_health base get 0.5

# If data = 1, player is revived so update health
execute if score @s {namespace}.data matches 1 run function {namespace}:player/update_health
execute if score @s {namespace}.data matches 1 run scoreboard players set @s {namespace}.data 0

# Withdraw command trigger
scoreboard players enable @s {namespace}.withdraw
execute unless score @s {namespace}.withdraw matches 0 run function {namespace}:player/withdraw

# If killed player, add a heart
execute if score @s {namespace}.kill matches 1.. if score @s {namespace}.hearts >= MAX_HEARTS {namespace}.data run tellraw @s [{{"text":"You stole a heart from a player, but you are already at max health!","color":"red"}}]
execute if score @s {namespace}.kill matches 1.. if score @s {namespace}.hearts < MAX_HEARTS {namespace}.data run scoreboard players operation @s {namespace}.hearts += @s {namespace}.kill
execute if score @s {namespace}.kill matches 1.. if score @s {namespace}.hearts < MAX_HEARTS {namespace}.data run tellraw @s [{{"text":"You stole a heart from a player, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{namespace}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score @s {namespace}.kill matches 1.. run function {namespace}:player/update_health
execute if score @s {namespace}.kill matches 1.. run scoreboard players set @s {namespace}.kill 0

# If player died, remove a heart
execute if score @s {namespace}.death matches 1.. run scoreboard players remove @s {namespace}.hearts 1
execute if score @s {namespace}.death matches 1.. run tellraw @s [{{"text":"You lost a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{namespace}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score @s {namespace}.death matches 1.. run function {namespace}:player/update_health
execute if score @s {namespace}.death matches 1.. unless entity @a[scores={{{namespace}.kill=1..}}] run function {namespace}:player/drop_heart_at_death
execute if score @s {namespace}.death matches 1.. run scoreboard players set @s {namespace}.death 0
execute if score @s {namespace}.hearts matches 0 run function {namespace}:player/death
""")
	
	# Add update_health function
	write_to_file(f"{functions}/player/update_health.mcfunction", f"""
execute store result storage {namespace}:main health int 2 run scoreboard players get @s {namespace}.hearts
function {namespace}:player/update_macro with storage {namespace}:main
execute at @s run playsound entity.player.levelup ambient @s
""")
	write_to_file(f"{functions}/player/update_macro.mcfunction", "$attribute @s max_health base set $(health)")

	# Add withdraw function
	write_to_file(f"{functions}/player/withdraw.mcfunction", f"""
# Reset withdraw trigger and stop function if not enough hearts
scoreboard players set @s {namespace}.withdraw 0
execute if score @s {namespace}.hearts matches ..1 run tellraw @s {{"text":"You don't have enough hearts to withdraw!","color":"red"}}
execute if score @s {namespace}.hearts matches ..1 run return fail

# Give heart, decrease score, and update health
loot give @s[gamemode=!creative] loot {namespace}:i/heart
scoreboard players remove @s {namespace}.hearts 1
function {namespace}:player/update_health

# Tellraw message
tellraw @s [{{"text":"You withdrew a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{namespace}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
""")
	
	## Advancement when eating a heart
	# JSON advancement
	advancement: str = f"{config['build_datapack']}/data/{namespace}/advancement/consume_heart.json"
	json_content: dict = {"criteria":{"requirement":{"trigger":"minecraft:consume_item","conditions":{"item":{"predicates":{"minecraft:custom_data":f"{{\"{namespace}\":{{\"heart\":true}}}}"}}}}}}
	json_content["rewards"] = {"function": f"{namespace}:player/consume_heart"}
	write_to_file(advancement, stp.super_json_dump(json_content, max_level = -1))

	# Function
	write_to_file(f"{functions}/player/consume_heart.mcfunction", f"""
# Revoke the advancement
advancement revoke @s only {namespace}:consume_heart

# If already at max health, regive the heart and stop function
execute if score @s {namespace}.hearts >= MAX_HEARTS {namespace}.data run tellraw @s {{"text":"You are already at max health!","color":"red"}}
execute if score @s {namespace}.hearts >= MAX_HEARTS {namespace}.data at @s run loot spawn ~ ~ ~ loot {namespace}:i/heart
execute if score @s {namespace}.hearts >= MAX_HEARTS {namespace}.data run return fail

# Give a heart and update health
scoreboard players add @s {namespace}.hearts 1
function {namespace}:player/update_health

# Tellraw message
tellraw @s [{{"text":"You ate a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{namespace}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
""")
	
	# Get player head loot table
	json_content: dict = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:item","name":"minecraft:player_head","functions":[{"function":"minecraft:fill_player_head","entity":"this"}]}]}]}
	write_to_file(f"{config['build_datapack']}/data/{namespace}/loot_table/player_head.json", stp.super_json_dump(json_content, max_level = -1))

	# Function death (when reaching 0 heart)
	write_to_file(f"{functions}/player/death.mcfunction", f"""
# Get player username
tag @e[type=item] add {namespace}.temp
execute at @s run loot spawn ~ ~ ~ loot {namespace}:player_head
data modify storage {namespace}:main player set from entity @e[type=item,tag=!{namespace}.temp,limit=1] Item.components."minecraft:profile".name
kill @e[type=item,tag=!{namespace}.temp]
tag @e[type=item,tag={namespace}.temp] remove {namespace}.temp

# Ban macro
function {namespace}:player/ban_macro with storage {namespace}:main
""")
	write_to_file(f"{functions}/player/ban_macro.mcfunction", f"""
# Tellraw message and ban player
$tellraw @a {{"text":"Player '$(player)' just got banned for reaching 0 hearts!","color":"red"}}
$ban $(player) You reached 0 hearts!

# Add player name to banned list
execute unless data storage {namespace}:main banned_players run data modify storage {namespace}:main banned_players set value {{}}
$data modify storage {namespace}:main banned_players.$(player) set value true
""")


	## Revive beacon
	# JSON advancement
	advancement: str = f"{config['build_datapack']}/data/{namespace}/advancement/consume_beacon.json"
	json_content: dict = {"criteria":{"requirement":{"trigger":"minecraft:consume_item","conditions":{"item":{"predicates":{"minecraft:custom_data":f"{{\"{namespace}\":{{\"revive_beacon\":true}}}}"}}}}}}
	json_content["rewards"] = {"function": f"{namespace}:player/consume_beacon"}
	write_to_file(advancement, stp.super_json_dump(json_content, max_level = -1))

	# Function
	write_to_file(f"{functions}/player/consume_beacon.mcfunction", f"""
# Revoke the advancement
advancement revoke @s only {namespace}:consume_beacon

# Get username from beacon name
data remove storage {namespace}:main player
scoreboard players set #success {namespace}.data 0
execute if data entity @s SelectedItem.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage {namespace}:main player set string entity @s SelectedItem.components."minecraft:custom_name"
execute unless data storage {namespace}:main player if data entity @s Inventory[-1].components."minecraft:custom_data".life_steal.revive_beacon run data modify storage {namespace}:main player set string entity @s Inventory[-1].components."minecraft:custom_name"
function {namespace}:player/revive with storage {namespace}:main

# If not success, regive the beacon and stop function
execute if score #success {namespace}.data matches 0 run loot give @s[gamemode=!creative] loot {namespace}:i/revive_beacon
execute if score #success {namespace}.data matches 0 run return fail
""")
	write_to_file(f"{functions}/player/revive.mcfunction", f"""
# If player is banned, pardon him and return success
$execute if data storage {namespace}:main banned_players.$(player) run pardon $(player)
$execute if data storage {namespace}:main banned_players.$(player) run tellraw @a [{{"selector":"@s","color":"green"}},{{"text":" used a revive beacon to revive '$(player)'!"}}]
$execute if data storage {namespace}:main banned_players.$(player) as @a at @s run playsound ui.toast.challenge_complete ambient @s
$execute if data storage {namespace}:main banned_players.$(player) run scoreboard players operation $(player) {namespace}.hearts = REVIVED_HEARTS {namespace}.data
$execute if data storage {namespace}:main banned_players.$(player) run scoreboard players set $(player) {namespace}.data 1
$execute if data storage {namespace}:main banned_players.$(player) run scoreboard players set #success {namespace}.data 1
$execute if data storage {namespace}:main banned_players.$(player) run return run data remove storage {namespace}:main banned_players.$(player)

# If player is not found, return fail
$tellraw @s [{{"text":"Player '$(player)' not found in the banned list!","color":"red"}}]
return fail
""")
	
	# Drop heart at death function
	write_to_file(f"{functions}/player/drop_heart_at_death.mcfunction", f"""
# Copy in a storage the arguments for the macro
data modify storage {namespace}:main death_pos set value {{dimension:"minecraft:overworld",x:0,y:0,z:0}}
data modify storage {namespace}:main death_pos.dimension set from entity @s LastDeathLocation.dimension
data modify storage {namespace}:main death_pos.x set from entity @s LastDeathLocation.pos[0]
data modify storage {namespace}:main death_pos.y set from entity @s LastDeathLocation.pos[1]
data modify storage {namespace}:main death_pos.z set from entity @s LastDeathLocation.pos[2]

# Drop the heart
function {namespace}:player/drop_heart_macro with storage {namespace}:main death_pos
""")
	write_to_file(f"{functions}/player/drop_heart_macro.mcfunction", f"""
$execute in $(dimension) run loot spawn $(x) $(y) $(z) loot {namespace}:i/heart
""")
	
	pass

