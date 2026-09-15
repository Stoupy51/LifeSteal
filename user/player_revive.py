
# ruff: noqa: E501
# Imports
from beet import Advancement, Context, LootTable
from stewbeet import JsonDict, set_json_encoder, write_function


# Setup revive beacon advancement and functions
def setup_revive_beacon(ctx: Context) -> None:
	ns: str = ctx.project_id

	# JSON advancement
	json_content: JsonDict = {"criteria":{"requirement":{"trigger":"minecraft:consume_item","conditions":{"item":{"predicates":{"minecraft:custom_data":f"{{\"{ns}\":{{\"revive_beacon\":true}}}}"}}}}}}
	json_content["rewards"] = {"function": f"{ns}:player/consume_beacon"}
	ctx.data[ns].advancements["consume_beacon"] = set_json_encoder(Advancement(json_content), max_level=-1)

	# Function for consuming beacon
	write_function(f"{ns}:player/consume_beacon", f"""
# Revoke the advancement
advancement revoke @s only {ns}:consume_beacon

# Get username from beacon name
data remove storage {ns}:main player
execute if data entity @s SelectedItem.components."minecraft:custom_data".{ns}.revive_beacon run data modify storage {ns}:main player set string entity @s SelectedItem.components."minecraft:custom_name"
execute unless data storage {ns}:main player if data entity @s equipment.offhand.components."minecraft:custom_data".{ns}.revive_beacon run data modify storage {ns}:main player set string entity @s equipment.offhand.components."minecraft:custom_name"

# If the beacon was never renamed, give it back and explain how to use it
execute unless data storage {ns}:main player run loot give @s[gamemode=!creative] loot {ns}:i/revive_beacon
execute unless data storage {ns}:main player run tellraw @s [{{"text":"[LifeStealFR] This revive beacon has no name! Rename it in an anvil to the exact username of the player you want to revive.","color":"red"}}]
execute unless data storage {ns}:main player run return fail

# Try to revive
execute store success score #success {ns}.data run function {ns}:player/revive with storage {ns}:main
execute if score #success {ns}.data matches 1 run return 1

# If not success, regive the beacon and stop function
loot give @s[gamemode=!creative] loot {ns}:i/revive_beacon
return fail
""")

	# Function for reviving player
	write_function(f"{ns}:player/revive", f"""
# Check if player is online and in spectator mode
$execute store success score #is_spectator {ns}.data if entity @a[name=$(player),gamemode=spectator]

# If player is in spectator mode, revive them
$execute if score #is_spectator {ns}.data matches 1 run gamemode survival @a[name=$(player)]
$execute if score #is_spectator {ns}.data matches 1 run tp @a[name=$(player)] @s
$execute if score #is_spectator {ns}.data matches 1 run tellraw @a [{{"selector":"@s","color":"green"}},{{"text":" used a revive beacon to revive '$(player)'!"}}]
execute if score #is_spectator {ns}.data matches 1 as @a at @s run playsound ui.toast.challenge_complete ambient @s
$execute if score #is_spectator {ns}.data matches 1 if score USE_HALF_HEARTS {ns}.data matches 0 run scoreboard players operation @a[name=$(player)] {ns}.hearts = REVIVED_HEARTS {ns}.data
$execute if score #is_spectator {ns}.data matches 1 if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation @a[name=$(player)] {ns}.hearts = REVIVED_HEARTS {ns}.data
$execute if score #is_spectator {ns}.data matches 1 if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation @a[name=$(player)] {ns}.hearts *= #2 {ns}.data
$execute if score #is_spectator {ns}.data matches 1 as @a[name=$(player)] run function {ns}:player/update_health
$execute if score #is_spectator {ns}.data matches 1 run data remove storage {ns}:main banned_players.$(player)
execute if score #is_spectator {ns}.data matches 1 run return 1

# Check if the player is in the list of players banned by LifeSteal
$execute store success score #is_banned {ns}.data if data storage {ns}:main banned_players.$(player)

# If the name is nowhere to be found, show what was checked and stop here
$execute if score #is_banned {ns}.data matches 0 run tellraw @s [{{"text":"[LifeStealFR] There is no banned player named '","color":"red"}},{{"text":"$(player)","color":"yellow"}},{{"text":"', and nobody with that name is connected in spectator mode!","color":"red"}}]
execute if score #is_banned {ns}.data matches 0 if data storage {ns}:main banned_players run tellraw @s [{{"text":"Players banned by LifeSteal (names are case sensitive): ","color":"gray"}},{{"nbt":"banned_players","storage":"{ns}:main","color":"yellow"}}]
execute if score #is_banned {ns}.data matches 0 unless data storage {ns}:main banned_players run tellraw @s [{{"text":"No player was ever banned by LifeSteal on this world.","color":"gray"}}]
execute if score #is_banned {ns}.data matches 0 run tellraw @s [{{"text":"👉 ","color":"gray"}},{{"text":"[Click here]","color":"aqua","click_event":{{"action":"suggest_command","command":"/function {ns}:_debug"}}}},{{"text":" to diagnose the problem.","color":"gray"}}]
execute if score #is_banned {ns}.data matches 0 run return fail

# Pardon the player, inline arguments are mandatory here since the storage may hold another name
$execute store success score #is_pardoned {ns}.data run function {ns}:player/pardon_player {{player:"$(player)"}}

# Revive the player: announce it, restore their hearts and flag them so the tick function fixes their health on join
$tellraw @a [{{"selector":"@s","color":"green"}},{{"text":" used a revive beacon to revive '$(player)'!"}}]
execute as @a at @s run playsound ui.toast.challenge_complete ambient @s
$scoreboard players operation $(player) {ns}.hearts = REVIVED_HEARTS {ns}.data
$execute if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation $(player) {ns}.hearts *= #2 {ns}.data
$scoreboard players set $(player) {ns}.data 1
$data remove storage {ns}:main banned_players.$(player)

# If the pardon silently failed while the player was really banned, tell the operator how to finish the job
$execute if score #is_pardoned {ns}.data matches 0 unless score SPECTATOR_INSTEAD {ns}.data matches 1 run tellraw @a [{{"text":"[LifeStealFR] WARNING: '$(player)' got their hearts back but could not be unbanned!","color":"red"}}]
$execute if score #is_pardoned {ns}.data matches 0 unless score SPECTATOR_INSTEAD {ns}.data matches 1 run tellraw @a [{{"text":"👉 An operator must run ","color":"gray"}},{{"text":"/pardon $(player)","color":"aqua","click_event":{{"action":"suggest_command","command":"/pardon $(player)"}}}},{{"text":" from the console, and set ","color":"gray"}},{{"text":"function-permission-level=3","color":"red"}},{{"text":" in server.properties.","color":"gray"}}]
return 1
""")

	# Separate function for pardon command (isolated to prevent crashes if permission denied)
	write_function(f"{ns}:player/pardon_player", "$return run pardon $(player)")

	# Administration function that revives a player whatever their state is, used when the world storage lost track of them
	write_function(f"{ns}:player/force_revive", f"""
# Pardon the player, it silently fails when they were not banned or when the datapack lacks permissions
$execute store success score #is_pardoned {ns}.data run function {ns}:player/pardon_player {{player:"$(player)"}}

# Restore their hearts and flag them so the tick function fixes their health and gamemode on join
$scoreboard players operation $(player) {ns}.hearts = REVIVED_HEARTS {ns}.data
$execute if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation $(player) {ns}.hearts *= #2 {ns}.data
$scoreboard players set $(player) {ns}.data 1
$data remove storage {ns}:main banned_players.$(player)
$gamemode survival @a[name=$(player),gamemode=spectator]
$execute as @a[name=$(player)] run function {ns}:player/update_health

# Report what happened
$tellraw @s [{{"text":"[LifeStealFR] Force revived '$(player)', they are unbanned and back to the revived hearts amount.","color":"green"}}]
execute if score #is_pardoned {ns}.data matches 0 run tellraw @s [{{"text":"⚠ /pardon did not run: either they were not banned at all, or the datapack lacks permissions (function-permission-level=3).","color":"gold"}}]
""")


# Setup loot table for getting player heads
def setup_player_head_loot_table(ctx: Context) -> None:
	ns: str = ctx.project_id

	json_content: JsonDict = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:item","name":"minecraft:player_head","modifier":[{"type":"minecraft:fill_player_head","entity":"this"}]}]}]}
	ctx.data[ns].loot_tables["player_head"] = set_json_encoder(LootTable(json_content), max_level=-1)

