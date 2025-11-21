
# ruff: noqa: E501
# Imports
from beet import Advancement, Context, LootTable
from stewbeet import JsonDict, set_json_encoder, write_function, write_load_file, write_tick_file


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def beet_default(ctx: Context):
	ns: str = ctx.project_id

	# Add scoreboard objectives
	write_load_file(f"""
scoreboard objectives add {ns}.kill playerKillCount
scoreboard objectives add {ns}.death deathCount
scoreboard objectives add {ns}.withdraw trigger
scoreboard objectives add {ns}.hearts dummy

scoreboard players set #2 {ns}.data 2

execute unless score MAX_HEARTS {ns}.data matches 1.. run scoreboard players set MAX_HEARTS {ns}.data 20
execute unless score MIN_HEARTS {ns}.data matches 1.. run scoreboard players set MIN_HEARTS {ns}.data 1
execute unless score REVIVED_HEARTS {ns}.data matches 1.. run scoreboard players set REVIVED_HEARTS {ns}.data 4
execute unless score NATURAL_DEATH_HEART_DROP {ns}.data matches 0..1 run scoreboard players set NATURAL_DEATH_HEART_DROP {ns}.data 1
execute unless score USE_HALF_HEARTS {ns}.data matches 0..1 run scoreboard players set USE_HALF_HEARTS {ns}.data 0
execute unless score USE_HALF_HEARTS_PREV {ns}.data matches 0..1 run scoreboard players operation USE_HALF_HEARTS_PREV {ns}.data = USE_HALF_HEARTS {ns}.data
execute unless score BAN_BELOW_MIN_HEARTS {ns}.data matches 0..1 run scoreboard players set BAN_BELOW_MIN_HEARTS {ns}.data 1
""", prepend = True)

	# Add tick function
	write_tick_file(f"""
# Check for USE_HALF_HEARTS configuration change
execute unless score USE_HALF_HEARTS {ns}.data = USE_HALF_HEARTS_PREV {ns}.data run function {ns}:config/half_hearts_changed

execute as @a[sort=random,scores={{{ns}.death=1..}}] run function {ns}:player/tick
execute as @a[sort=random] run function {ns}:player/tick
""")

	# Add player function
	write_function(f"{ns}:player/tick", f"""
# Setup hearts objective if not set and get all recipes
execute unless score @s {ns}.hearts matches 0.. run function {ns}:utils/get_all_recipes
execute unless score @s {ns}.hearts matches 0.. if score USE_HALF_HEARTS {ns}.data matches 0 store result score @s {ns}.hearts run attribute @s minecraft:max_health base get 0.5
execute unless score @s {ns}.hearts matches 0.. if score USE_HALF_HEARTS {ns}.data matches 1 store result score @s {ns}.hearts run attribute @s minecraft:max_health base get 1.0

# If data = 1, player is revived so update health
execute if score @s {ns}.data matches 1 run function {ns}:player/update_health
execute if score @s {ns}.data matches 1 run scoreboard players set @s {ns}.data 0

# Withdraw command trigger
scoreboard players enable @s {ns}.withdraw
execute unless score @s {ns}.withdraw matches 0 run function {ns}:player/withdraw

# If killed player, add a heart
execute if score @s {ns}.kill matches 1.. run function {ns}:player/on_kill

# On any death, run on_death function
execute if score @s {ns}.death matches 1.. run function {ns}:player/on_death
""")
	write_function(f"{ns}:player/on_kill", f"""
# Compute max hearts
scoreboard players operation #temp {ns}.data = MAX_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation #temp {ns}.data *= #2 {ns}.data

# If at max hearts, send message
execute if score @s {ns}.hearts >= #temp {ns}.data run tellraw @s [{{"text":"You stole a heart from a player, but you are already at max health!","color":"red"}}]

# Else, add a heart (or half heart)
execute if score @s {ns}.hearts < #temp {ns}.data run scoreboard players operation @s {ns}.hearts += @s {ns}.kill
execute if score @s {ns}.hearts < #temp {ns}.data run function {ns}:player/gain_heart_msg

# Update health and reset kill score
function {ns}:player/update_health
scoreboard players set @s {ns}.kill 0
""")
	write_function(f"{ns}:player/on_death", f"""
# If (died from a player), or (died from natural causes and configuration is 1), remove a heart
execute if entity @a[scores={{{ns}.kill=1..}}] run function {ns}:player/remove_one_heart
execute unless entity @a[scores={{{ns}.kill=1..}}] unless score NATURAL_DEATH_HEART_DROP {ns}.data matches 0 run function {ns}:player/remove_one_heart

# Update health
function {ns}:player/update_health

# Check if fall below minimum hearts
execute store result score #temp {ns}.data run scoreboard players get MIN_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 unless score #temp {ns}.data matches 1 run scoreboard players operation #temp {ns}.data *= #2 {ns}.data
execute if score @s {ns}.hearts < #temp {ns}.data run function {ns}:player/below_min_hearts

# Reset death score
scoreboard players set @s {ns}.death 0
""")
	# Add remove_one_heart function
	write_function(f"{ns}:player/remove_one_heart", f"""
scoreboard players remove @s {ns}.hearts 1
function {ns}:player/lose_heart_msg
function {ns}:player/update_health

# Drop a heart if player wasn't killed by another player
execute unless entity @a[scores={{{ns}.kill=1..}}] run function {ns}:player/drop_heart_at_death
""")

	# Add update_health function
	write_function(f"{ns}:player/update_health", f"""
execute if score USE_HALF_HEARTS {ns}.data matches 0 store result storage {ns}:main health int 2 run scoreboard players get @s {ns}.hearts
execute if score USE_HALF_HEARTS {ns}.data matches 1 store result storage {ns}:main health int 1 run scoreboard players get @s {ns}.hearts
function {ns}:player/update_macro with storage {ns}:main
execute at @s run playsound entity.player.levelup ambient @s
""")
	write_function(f"{ns}:player/update_macro", "$attribute @s max_health base set $(health)")

	# Add helper functions for displaying hearts
	write_function(f"{ns}:player/gain_heart_msg", f"""
execute if score USE_HALF_HEARTS {ns}.data matches 0 run tellraw @s [{{"text":"You stole a heart from a player, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score USE_HALF_HEARTS {ns}.data matches 1 run function {ns}:player/gain_heart_msg_half
""")
	write_function(f"{ns}:player/gain_heart_msg_half", f"""
scoreboard players operation #display_whole {ns}.data = @s {ns}.hearts
scoreboard players operation #display_whole {ns}.data /= #2 {ns}.data
scoreboard players operation #display_half {ns}.data = @s {ns}.hearts
scoreboard players operation #display_half {ns}.data %= #2 {ns}.data
execute if score #display_half {ns}.data matches 0 run tellraw @s [{{"text":"You stole a heart from a player, you now have ","color":"gray"}},{{"score":{{"name":"#display_whole","objective":"{ns}.data"}}, "color":"red"}},{{"text":".0","color":"red"}},{{"text":" hearts!"}}]
execute if score #display_half {ns}.data matches 1 run tellraw @s [{{"text":"You stole a heart from a player, you now have ","color":"gray"}},{{"score":{{"name":"#display_whole","objective":"{ns}.data"}}, "color":"red"}},{{"text":".5","color":"red"}},{{"text":" hearts!"}}]
""")
	write_function(f"{ns}:player/lose_heart_msg", f"""
execute if score USE_HALF_HEARTS {ns}.data matches 0 run tellraw @s [{{"text":"You lost a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score USE_HALF_HEARTS {ns}.data matches 1 run function {ns}:player/lose_heart_msg_half
""")
	write_function(f"{ns}:player/lose_heart_msg_half", f"""
scoreboard players operation #display_whole {ns}.data = @s {ns}.hearts
scoreboard players operation #display_whole {ns}.data /= #2 {ns}.data
scoreboard players operation #display_half {ns}.data = @s {ns}.hearts
scoreboard players operation #display_half {ns}.data %= #2 {ns}.data
execute if score #display_half {ns}.data matches 0 run tellraw @s [{{"text":"You lost a heart, you now have ","color":"gray"}},{{"score":{{"name":"#display_whole","objective":"{ns}.data"}}, "color":"red"}},{{"text":".0","color":"red"}},{{"text":" hearts!"}}]
execute if score #display_half {ns}.data matches 1 run tellraw @s [{{"text":"You lost a heart, you now have ","color":"gray"}},{{"score":{{"name":"#display_whole","objective":"{ns}.data"}}, "color":"red"}},{{"text":".5","color":"red"}},{{"text":" hearts!"}}]
""")

	# Add withdraw function
	write_function(f"{ns}:player/withdraw", f"""
# Reset withdraw trigger
scoreboard players set @s {ns}.withdraw 0

# Check if player has more than minimum hearts
scoreboard players operation #temp {ns}.data = MIN_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 unless score #temp {ns}.data matches 1 run scoreboard players operation #temp {ns}.data *= #2 {ns}.data
scoreboard players add #temp {ns}.data 1

# Stop function if not enough hearts
execute if score @s {ns}.hearts < #temp {ns}.data run tellraw @s {{"text":"You don't have enough hearts to withdraw!","color":"red"}}
execute if score @s {ns}.hearts < #temp {ns}.data run return fail

# Give heart, decrease score, and update health
loot give @s[gamemode=!creative] loot {ns}:i/heart
scoreboard players remove @s {ns}.hearts 1
function {ns}:player/update_health

# Tellraw message
function {ns}:player/withdraw_msg
""")
	write_function(f"{ns}:player/withdraw_msg", f"""
execute if score USE_HALF_HEARTS {ns}.data matches 0 run tellraw @s [{{"text":"You withdrew a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score USE_HALF_HEARTS {ns}.data matches 1 run function {ns}:player/withdraw_msg_half
""")
	write_function(f"{ns}:player/withdraw_msg_half", f"""
scoreboard players operation #display_whole {ns}.data = @s {ns}.hearts
scoreboard players operation #display_whole {ns}.data /= #2 {ns}.data
scoreboard players operation #display_half {ns}.data = @s {ns}.hearts
scoreboard players operation #display_half {ns}.data %= #2 {ns}.data
execute if score #display_half {ns}.data matches 0 run tellraw @s [{{"text":"You withdrew a heart, you now have ","color":"gray"}},{{"score":{{"name":"#display_whole","objective":"{ns}.data"}}, "color":"red"}},{{"text":".0","color":"red"}},{{"text":" hearts!"}}]
execute if score #display_half {ns}.data matches 1 run tellraw @s [{{"text":"You withdrew a heart, you now have ","color":"gray"}},{{"score":{{"name":"#display_whole","objective":"{ns}.data"}}, "color":"red"}},{{"text":".5","color":"red"}},{{"text":" hearts!"}}]
""")

	## Advancement when eating a heart
	# JSON advancement
	json_content: JsonDict = {"criteria":{"requirement":{"trigger":"minecraft:consume_item","conditions":{"item":{"predicates":{"minecraft:custom_data":f"{{\"{ns}\":{{\"heart\":true}}}}"}}}}}}
	json_content["rewards"] = {"function": f"{ns}:player/consume_heart"}
	ctx.data[ns].advancements["consume_heart"] = set_json_encoder(Advancement(json_content), max_level=-1)

	# Function
	write_function(f"{ns}:player/consume_heart", f"""
# Revoke the advancement
advancement revoke @s only {ns}:consume_heart

# If already at max health, regive the heart and stop function
scoreboard players operation #temp {ns}.data = MAX_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation #temp {ns}.data *= #2 {ns}.data
execute if score @s {ns}.hearts >= #temp {ns}.data run tellraw @s {{"text":"You are already at max health!","color":"red"}}
execute if score @s {ns}.hearts >= #temp {ns}.data at @s run loot spawn ~ ~ ~ loot {ns}:i/heart
execute if score @s {ns}.hearts >= #temp {ns}.data run return fail

# Give a heart and update health
scoreboard players add @s {ns}.hearts 1
function {ns}:player/update_health

# Tellraw message
function {ns}:player/consume_heart_msg
""")
	write_function(f"{ns}:player/consume_heart_msg", f"""
execute if score USE_HALF_HEARTS {ns}.data matches 0 run tellraw @s [{{"text":"You ate a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score USE_HALF_HEARTS {ns}.data matches 1 run function {ns}:player/consume_heart_msg_half
""")
	write_function(f"{ns}:player/consume_heart_msg_half", f"""
scoreboard players operation #display_whole {ns}.data = @s {ns}.hearts
scoreboard players operation #display_whole {ns}.data /= #2 {ns}.data
scoreboard players operation #display_half {ns}.data = @s {ns}.hearts
scoreboard players operation #display_half {ns}.data %= #2 {ns}.data
execute if score #display_half {ns}.data matches 0 run tellraw @s [{{"text":"You ate a heart, you now have ","color":"gray"}},{{"score":{{"name":"#display_whole","objective":"{ns}.data"}}, "color":"red"}},{{"text":".0","color":"red"}},{{"text":" hearts!"}}]
execute if score #display_half {ns}.data matches 1 run tellraw @s [{{"text":"You ate a heart, you now have ","color":"gray"}},{{"score":{{"name":"#display_whole","objective":"{ns}.data"}}, "color":"red"}},{{"text":".5","color":"red"}},{{"text":" hearts!"}}]
""")

	# Get player head loot table
	json_content: JsonDict = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:item","name":"minecraft:player_head","functions":[{"function":"minecraft:fill_player_head","entity":"this"}]}]}]}
	ctx.data[ns].loot_tables["player_head"] = set_json_encoder(LootTable(json_content), max_level=-1)

	# Function death (when reaching minimum hearts)
	write_function(f"{ns}:player/below_min_hearts", f"""
# Make sure player does not have less than minimum hearts
scoreboard players operation #temp {ns}.data = MIN_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 unless score #temp {ns}.data matches 1 run scoreboard players operation #temp {ns}.data *= #2 {ns}.data
execute if score @s {ns}.hearts < #temp {ns}.data run scoreboard players operation @s {ns}.hearts = #temp {ns}.data

# If not BAN_BELOW_MIN_HEARTS configuration, stop here
execute unless score BAN_BELOW_MIN_HEARTS {ns}.data matches 1 run return 1

# Get player username for macro
tag @e[type=item] add {ns}.temp
execute at @s run loot spawn ~ ~ ~ loot {ns}:player_head
data modify storage {ns}:main player set from entity @e[type=item,tag=!{ns}.temp,limit=1] Item.components."minecraft:profile".name
kill @e[type=item,tag=!{ns}.temp]
tag @e[type=item,tag={ns}.temp] remove {ns}.temp

# Ban macro
function {ns}:player/ban_macro with storage {ns}:main
""")
	write_function(f"{ns}:player/ban_macro", f"""
# Tellraw message and ban player
$tellraw @a {{"text":"Player '$(player)' just got banned for reaching minimum hearts!","color":"red"}}
$ban $(player) You reached the minimum hearts!

# Add player name to banned list
execute unless data storage {ns}:main banned_players run data modify storage {ns}:main banned_players set value {{}}
$data modify storage {ns}:main banned_players.$(player) set value true
""")


	## Revive beacon
	# JSON advancement
	json_content: JsonDict = {"criteria":{"requirement":{"trigger":"minecraft:consume_item","conditions":{"item":{"predicates":{"minecraft:custom_data":f"{{\"{ns}\":{{\"revive_beacon\":true}}}}"}}}}}}
	json_content["rewards"] = {"function": f"{ns}:player/consume_beacon"}
	ctx.data[ns].advancements["consume_beacon"] = set_json_encoder(Advancement(json_content), max_level=-1)

	# Function
	write_function(f"{ns}:player/consume_beacon", f"""
# Revoke the advancement
advancement revoke @s only {ns}:consume_beacon

# Get username from beacon name
data remove storage {ns}:main player
execute if data entity @s SelectedItem.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage {ns}:main player set string entity @s SelectedItem.components."minecraft:custom_name"
execute unless data storage {ns}:main player if data entity @s equipment.offhand.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage {ns}:main player set string entity @s equipment.offhand.components."minecraft:custom_name"

# Try to revive
execute store success score #success {ns}.data run function {ns}:player/revive with storage {ns}:main
execute if score #success {ns}.data matches 1 run return 1

# If not success, regive the beacon and stop function
loot give @s[gamemode=!creative] loot {ns}:i/revive_beacon
return fail
""")
	write_function(f"{ns}:player/revive", f"""
# If player is banned, pardon him and return success
$execute store success score #is_banned {ns}.data if data storage {ns}:main banned_players.$(player)
$execute if score #is_banned {ns}.data matches 1 run pardon $(player)
$execute if score #is_banned {ns}.data matches 1 run tellraw @a [{{"selector":"@s","color":"green"}},{{"text":" used a revive beacon to revive '$(player)'!"}}]
execute if score #is_banned {ns}.data matches 1 as @a at @s run playsound ui.toast.challenge_complete ambient @s
$execute if score #is_banned {ns}.data matches 1 if score USE_HALF_HEARTS {ns}.data matches 0 run scoreboard players operation $(player) {ns}.hearts = REVIVED_HEARTS {ns}.data
$execute if score #is_banned {ns}.data matches 1 if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation $(player) {ns}.hearts = REVIVED_HEARTS {ns}.data
$execute if score #is_banned {ns}.data matches 1 if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation $(player) {ns}.hearts *= #2 {ns}.data
$execute if score #is_banned {ns}.data matches 1 run scoreboard players set $(player) {ns}.data 1
$execute if score #is_banned {ns}.data matches 1 run data remove storage {ns}:main banned_players.$(player)
execute if score #is_banned {ns}.data matches 1 run return 1

# If player is not found, return fail
$tellraw @s [{{"text":"Player '$(player)' not found in the banned list!","color":"red"}}]
return fail
""")

	# Drop heart at death function
	write_function(f"{ns}:player/drop_heart_at_death", f"""
# Copy in a storage the arguments for the macro
data modify storage {ns}:main death_pos set value {{dimension:"minecraft:overworld",x:0,y:0,z:0}}
data modify storage {ns}:main death_pos.dimension set from entity @s LastDeathLocation.dimension
data modify storage {ns}:main death_pos.x set from entity @s LastDeathLocation.pos[0]
data modify storage {ns}:main death_pos.y set from entity @s LastDeathLocation.pos[1]
data modify storage {ns}:main death_pos.z set from entity @s LastDeathLocation.pos[2]

# Drop the heart
function {ns}:player/drop_heart_macro with storage {ns}:main death_pos
""")
	write_function(f"{ns}:player/drop_heart_macro", f"""
$execute in $(dimension) run loot spawn $(x) $(y) $(z) loot {ns}:i/heart
""")

	# Configuration change detection
	write_function(f"{ns}:config/half_hearts_changed", f"""
# Convert hearts for all players based on new configuration
execute if score USE_HALF_HEARTS {ns}.data matches 1 if score USE_HALF_HEARTS_PREV {ns}.data matches 0 run function {ns}:config/convert_to_half_hearts
execute if score USE_HALF_HEARTS {ns}.data matches 0 if score USE_HALF_HEARTS_PREV {ns}.data matches 1 run function {ns}:config/convert_to_full_hearts

# Update previous value
scoreboard players operation USE_HALF_HEARTS_PREV {ns}.data = USE_HALF_HEARTS {ns}.data
""")

	write_function(f"{ns}:config/convert_to_half_hearts", f"""
# Convert all players from full hearts to half hearts (multiply by 2)
execute as @a run scoreboard players operation @s {ns}.hearts *= #2 {ns}.data
execute as @a run function {ns}:player/update_health

# Notify all players
tellraw @a [{{"text":"[Life Steal] Configuration changed to half hearts mode! All hearts score have been doubled.","color":"green"}}]
execute as @a at @s run playsound entity.experience_orb.pickup ambient @s
""")

	write_function(f"{ns}:config/convert_to_full_hearts", f"""
# Convert all players from half hearts to full hearts (divide by 2)
execute as @a run scoreboard players operation @s {ns}.hearts /= #2 {ns}.data
execute as @a run function {ns}:player/update_health

# Notify all players
tellraw @a [{{"text":"[Life Steal] Configuration changed to full hearts mode! All hearts score have been halved.","color":"yellow"}}]
execute as @a at @s run playsound entity.experience_orb.pickup ambient @s
""")

	pass

