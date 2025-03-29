
# Imports
import stouputils as stp
from python_datapack.constants import *
from python_datapack.utils.io import *

# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def main(config: dict) -> None:
	ns: str = config["namespace"]

	# Add scoreboard objectives
	write_load_file(config, f"""
scoreboard objectives add {ns}.kill playerKillCount
scoreboard objectives add {ns}.death deathCount
scoreboard objectives add {ns}.withdraw trigger
scoreboard objectives add {ns}.hearts dummy
execute unless score MAX_HEARTS {ns}.data matches 1.. run scoreboard players set MAX_HEARTS {ns}.data 20
execute unless score REVIVED_HEARTS {ns}.data matches 1.. run scoreboard players set REVIVED_HEARTS {ns}.data 4
""", prepend = True)

	# Add tick function
	write_tick_file(config, f"""
execute as @a[sort=random,scores={{{ns}.death=1..}}] run function {ns}:player/tick
execute as @a[sort=random] run function {ns}:player/tick
""")

	# Add player function
	write_function(config, f"{ns}:player/tick", f"""
# Setup hearts objective if not set and get all recipes
execute unless score @s {ns}.hearts matches 0.. run function {ns}:utils/get_all_recipes
execute unless score @s {ns}.hearts matches 0.. store result score @s {ns}.hearts run attribute @s minecraft:max_health base get 0.5

# If data = 1, player is revived so update health
execute if score @s {ns}.data matches 1 run function {ns}:player/update_health
execute if score @s {ns}.data matches 1 run scoreboard players set @s {ns}.data 0

# Withdraw command trigger
scoreboard players enable @s {ns}.withdraw
execute unless score @s {ns}.withdraw matches 0 run function {ns}:player/withdraw

# If killed player, add a heart
execute if score @s {ns}.kill matches 1.. if score @s {ns}.hearts >= MAX_HEARTS {ns}.data run tellraw @s [{{"text":"You stole a heart from a player, but you are already at max health!","color":"red"}}]
execute if score @s {ns}.kill matches 1.. if score @s {ns}.hearts < MAX_HEARTS {ns}.data run scoreboard players operation @s {ns}.hearts += @s {ns}.kill
execute if score @s {ns}.kill matches 1.. if score @s {ns}.hearts < MAX_HEARTS {ns}.data run tellraw @s [{{"text":"You stole a heart from a player, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score @s {ns}.kill matches 1.. run function {ns}:player/update_health
execute if score @s {ns}.kill matches 1.. run scoreboard players set @s {ns}.kill 0

# If player died, remove a heart
execute if score @s {ns}.death matches 1.. run scoreboard players remove @s {ns}.hearts 1
execute if score @s {ns}.death matches 1.. run tellraw @s [{{"text":"You lost a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score @s {ns}.death matches 1.. run function {ns}:player/update_health
execute if score @s {ns}.death matches 1.. unless entity @a[scores={{{ns}.kill=1..}}] run function {ns}:player/drop_heart_at_death
execute if score @s {ns}.death matches 1.. run scoreboard players set @s {ns}.death 0
execute if score @s {ns}.hearts matches 0 run function {ns}:player/death
""")
	
	# Add update_health function
	write_function(config, f"{ns}:player/update_health", f"""
execute store result storage {ns}:main health int 2 run scoreboard players get @s {ns}.hearts
function {ns}:player/update_macro with storage {ns}:main
execute at @s run playsound entity.player.levelup ambient @s
""")
	write_function(config, f"{ns}:player/update_macro", "$attribute @s max_health base set $(health)")

	# Add withdraw function
	write_function(config, f"{ns}:player/withdraw", f"""
# Reset withdraw trigger and stop function if not enough hearts
scoreboard players set @s {ns}.withdraw 0
execute if score @s {ns}.hearts matches ..1 run tellraw @s {{"text":"You don't have enough hearts to withdraw!","color":"red"}}
execute if score @s {ns}.hearts matches ..1 run return fail

# Give heart, decrease score, and update health
loot give @s[gamemode=!creative] loot {ns}:i/heart
scoreboard players remove @s {ns}.hearts 1
function {ns}:player/update_health

# Tellraw message
tellraw @s [{{"text":"You withdrew a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
""")
	
	## Advancement when eating a heart
	# JSON advancement
	advancement: str = f"{config['build_datapack']}/data/{ns}/advancement/consume_heart.json"
	json_content: dict = {"criteria":{"requirement":{"trigger":"minecraft:consume_item","conditions":{"item":{"predicates":{"minecraft:custom_data":f"{{\"{ns}\":{{\"heart\":true}}}}"}}}}}}
	json_content["rewards"] = {"function": f"{ns}:player/consume_heart"}
	write_file(advancement, stp.super_json_dump(json_content, max_level = -1))

	# Function
	write_function(config, f"{ns}:player/consume_heart", f"""
# Revoke the advancement
advancement revoke @s only {ns}:consume_heart

# If already at max health, regive the heart and stop function
execute if score @s {ns}.hearts >= MAX_HEARTS {ns}.data run tellraw @s {{"text":"You are already at max health!","color":"red"}}
execute if score @s {ns}.hearts >= MAX_HEARTS {ns}.data at @s run loot spawn ~ ~ ~ loot {ns}:i/heart
execute if score @s {ns}.hearts >= MAX_HEARTS {ns}.data run return fail

# Give a heart and update health
scoreboard players add @s {ns}.hearts 1
function {ns}:player/update_health

# Tellraw message
tellraw @s [{{"text":"You ate a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
""")
	
	# Get player head loot table
	json_content: dict = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:item","name":"minecraft:player_head","functions":[{"function":"minecraft:fill_player_head","entity":"this"}]}]}]}
	write_file(f"{config['build_datapack']}/data/{ns}/loot_table/player_head.json", stp.super_json_dump(json_content, max_level = -1))

	# Function death (when reaching 0 heart)
	write_function(config, f"{ns}:player/death", f"""
# Get player username
tag @e[type=item] add {ns}.temp
execute at @s run loot spawn ~ ~ ~ loot {ns}:player_head
data modify storage {ns}:main player set from entity @e[type=item,tag=!{ns}.temp,limit=1] Item.components."minecraft:profile".name
kill @e[type=item,tag=!{ns}.temp]
tag @e[type=item,tag={ns}.temp] remove {ns}.temp

# Ban macro
function {ns}:player/ban_macro with storage {ns}:main
""")
	write_function(config, f"{ns}:player/ban_macro", f"""
# Tellraw message and ban player
$tellraw @a {{"text":"Player '$(player)' just got banned for reaching 0 hearts!","color":"red"}}
$ban $(player) You reached 0 hearts!

# Add player name to banned list
execute unless data storage {ns}:main banned_players run data modify storage {ns}:main banned_players set value {{}}
$data modify storage {ns}:main banned_players.$(player) set value true
""")


	## Revive beacon
	# JSON advancement
	advancement: str = f"{config['build_datapack']}/data/{ns}/advancement/consume_beacon.json"
	json_content: dict = {"criteria":{"requirement":{"trigger":"minecraft:consume_item","conditions":{"item":{"predicates":{"minecraft:custom_data":f"{{\"{ns}\":{{\"revive_beacon\":true}}}}"}}}}}}
	json_content["rewards"] = {"function": f"{ns}:player/consume_beacon"}
	write_file(advancement, stp.super_json_dump(json_content, max_level = -1))

	# Function
	write_function(config, f"{ns}:player/consume_beacon", f"""
# Revoke the advancement
advancement revoke @s only {ns}:consume_beacon

# Get username from beacon name
data remove storage {ns}:main player
scoreboard players set #success {ns}.data 0
execute if data entity @s SelectedItem.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage {ns}:main player set string entity @s SelectedItem.components."minecraft:custom_name"
execute unless data storage {ns}:main player if data entity @s equipment.offhand.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage {ns}:main player set string entity @s equipment.offhand.components."minecraft:custom_name"
function {ns}:player/revive with storage {ns}:main

# If not success, regive the beacon and stop function
execute if score #success {ns}.data matches 0 run loot give @s[gamemode=!creative] loot {ns}:i/revive_beacon
execute if score #success {ns}.data matches 0 run return fail
""")
	write_function(config, f"{ns}:player/revive", f"""
# If player is banned, pardon him and return success
$execute if data storage {ns}:main banned_players.$(player) run pardon $(player)
$execute if data storage {ns}:main banned_players.$(player) run tellraw @a [{{"selector":"@s","color":"green"}},{{"text":" used a revive beacon to revive '$(player)'!"}}]
$execute if data storage {ns}:main banned_players.$(player) as @a at @s run playsound ui.toast.challenge_complete ambient @s
$execute if data storage {ns}:main banned_players.$(player) run scoreboard players operation $(player) {ns}.hearts = REVIVED_HEARTS {ns}.data
$execute if data storage {ns}:main banned_players.$(player) run scoreboard players set $(player) {ns}.data 1
$execute if data storage {ns}:main banned_players.$(player) run scoreboard players set #success {ns}.data 1
$execute if data storage {ns}:main banned_players.$(player) run return run data remove storage {ns}:main banned_players.$(player)

# If player is not found, return fail
$tellraw @s [{{"text":"Player '$(player)' not found in the banned list!","color":"red"}}]
return fail
""")

	# Drop heart at death function
	write_function(config, f"{ns}:player/drop_heart_at_death", f"""
# Copy in a storage the arguments for the macro
data modify storage {ns}:main death_pos set value {{dimension:"minecraft:overworld",x:0,y:0,z:0}}
data modify storage {ns}:main death_pos.dimension set from entity @s LastDeathLocation.dimension
data modify storage {ns}:main death_pos.x set from entity @s LastDeathLocation.pos[0]
data modify storage {ns}:main death_pos.y set from entity @s LastDeathLocation.pos[1]
data modify storage {ns}:main death_pos.z set from entity @s LastDeathLocation.pos[2]

# Drop the heart
function {ns}:player/drop_heart_macro with storage {ns}:main death_pos
""")
	write_function(config, f"{ns}:player/drop_heart_macro", f"""
$execute in $(dimension) run loot spawn $(x) $(y) $(z) loot {ns}:i/heart
""")
	
	pass

