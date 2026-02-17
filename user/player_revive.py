
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
execute if data entity @s SelectedItem.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage {ns}:main player set string entity @s SelectedItem.components."minecraft:custom_name"
execute unless data storage {ns}:main player if data entity @s equipment.offhand.components."minecraft:custom_data".life_steal.revive_beacon run data modify storage {ns}:main player set string entity @s equipment.offhand.components."minecraft:custom_name"

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
execute if score #is_spectator {ns}.data matches 1 run return 1

# If player is banned, pardon them and return success
$execute store success score #is_banned {ns}.data if data storage {ns}:main banned_players.$(player)
execute if score #is_banned {ns}.data matches 1 run function {ns}:player/pardon_player with storage {ns}:main
$execute if score #is_banned {ns}.data matches 1 run tellraw @a [{{"selector":"@s","color":"green"}},{{"text":" used a revive beacon to revive '$(player)'!"}}]
execute if score #is_banned {ns}.data matches 1 as @a at @s run playsound ui.toast.challenge_complete ambient @s
$execute if score #is_banned {ns}.data matches 1 if score USE_HALF_HEARTS {ns}.data matches 0 run scoreboard players operation $(player) {ns}.hearts = REVIVED_HEARTS {ns}.data
$execute if score #is_banned {ns}.data matches 1 if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation $(player) {ns}.hearts = REVIVED_HEARTS {ns}.data
$execute if score #is_banned {ns}.data matches 1 if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation $(player) {ns}.hearts *= #2 {ns}.data
$execute if score #is_banned {ns}.data matches 1 run scoreboard players set $(player) {ns}.data 1
$execute if score #is_banned {ns}.data matches 1 run data remove storage {ns}:main banned_players.$(player)
execute if score #is_banned {ns}.data matches 1 run return 1

# If player is not found in spectator or banned list, return fail
$tellraw @s [{{"text":"Player '$(player)' not found in the banned list or connected in spectator mode!","color":"red"}}]
return fail
""")

	# Separate function for pardon command (isolated to prevent crashes if permission denied)
	write_function(f"{ns}:player/pardon_player", "$return run pardon $(player)")


# Setup loot table for getting player heads
def setup_player_head_loot_table(ctx: Context) -> None:
	ns: str = ctx.project_id

	json_content: JsonDict = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:item","name":"minecraft:player_head","functions":[{"function":"minecraft:fill_player_head","entity":"this"}]}]}]}
	ctx.data[ns].loot_tables["player_head"] = set_json_encoder(LootTable(json_content), max_level=-1)

