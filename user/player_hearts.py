
# ruff: noqa: E501
# Imports
from beet import Advancement, Context
from stewbeet import JsonDict, set_json_encoder, write_function


# Setup functions for consuming hearts
def setup_consume_heart_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	# JSON advancement for consuming
	json_content: JsonDict = {"criteria":{"requirement":{"trigger":"minecraft:consume_item","conditions":{"item":{"predicates":{"minecraft:custom_data":f"{{\"{ns}\":{{\"heart\":true}}}}"}}}}}}
	json_content["rewards"] = {"function": f"{ns}:player/consume_heart"}
	ctx.data[ns].advancements["consume_heart"] = set_json_encoder(Advancement(json_content), max_level=-1)

	# JSON advancement for using (instant consume)
	json_content: JsonDict = {"criteria":{"requirement":{"trigger":"minecraft:using_item","conditions":{"item":{"predicates":{"minecraft:custom_data":f"{{\"{ns}\":{{\"heart\":true}}}}"}}}}}}
	json_content["rewards"] = {"function": f"{ns}:player/using_heart"}
	ctx.data[ns].advancements["using_heart"] = set_json_encoder(Advancement(json_content), max_level=-1)

	# Function for consuming heart
	write_function(f"{ns}:player/consume_heart", f"""
# Revoke the advancement
advancement revoke @s only {ns}:consume_heart

# If already at max health by consuming, regive the heart and stop function
scoreboard players operation #temp {ns}.data = MAX_HEARTS_BY_CONSUMING {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation #temp {ns}.data *= #2 {ns}.data
execute if score @s {ns}.hearts >= #temp {ns}.data if score MAX_HEARTS_BY_CONSUMING {ns}.data = MAX_HEARTS {ns}.data run tellraw @s {{"text":"You are already at max health!","color":"red"}}
execute if score @s {ns}.hearts >= #temp {ns}.data unless score MAX_HEARTS_BY_CONSUMING {ns}.data = MAX_HEARTS {ns}.data run tellraw @s {{"text":"You are already at max health from consuming hearts! You can only gain more hearts by killing players.","color":"red"}}
execute if score @s {ns}.hearts >= #temp {ns}.data at @s run playsound entity.villager.no ambient @s
execute if score @s {ns}.hearts >= #temp {ns}.data at @s run loot spawn ~ ~ ~ loot {ns}:i/heart
execute if score @s {ns}.hearts >= #temp {ns}.data run return fail

# Remove last_chance tag if player has it
tag @s remove {ns}.last_chance

# Give a heart and update health
scoreboard players add @s {ns}.hearts 1
function {ns}:player/update_health

# Tellraw message
function {ns}:player/consume_heart_msg
""")

	# Function for using heart (instant consume)
	write_function(f"{ns}:player/using_heart", f"""
# Revoke the advancement
advancement revoke @s only {ns}:using_heart

# Stop if INSTANTLY_CONSUME_HEARTS is disabled
execute unless score INSTANTLY_CONSUME_HEARTS {ns}.data matches 1 run return fail

# If already at max health by consuming, stop
scoreboard players operation #temp {ns}.data = MAX_HEARTS_BY_CONSUMING {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation #temp {ns}.data *= #2 {ns}.data
execute if score @s {ns}.hearts >= #temp {ns}.data if score MAX_HEARTS_BY_CONSUMING {ns}.data = MAX_HEARTS {ns}.data run tellraw @s {{"text":"You are already at max health!","color":"red"}}
execute if score @s {ns}.hearts >= #temp {ns}.data unless score MAX_HEARTS_BY_CONSUMING {ns}.data = MAX_HEARTS {ns}.data run tellraw @s {{"text":"You are already at max health from consuming hearts! You can only gain more hearts by killing players.","color":"red"}}
execute if score @s {ns}.hearts >= #temp {ns}.data at @s run playsound entity.villager.no ambient @s
execute if score @s {ns}.hearts >= #temp {ns}.data run return fail

# Give a heart and update health
scoreboard players add @s {ns}.hearts 1
function {ns}:player/update_health

# Clear one heart
clear @s *[custom_data~{{{ns}:{{"heart":true}}}}] 1

# Tellraw message
function {ns}:player/consume_heart_msg
""")


# Setup functions for withdrawing hearts
def setup_withdraw_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/withdraw", f"""
# Reset withdraw trigger
scoreboard players set @s {ns}.withdraw 0

# Check if player has more than minimum hearts (add 1 if banning is enabled to prevent withdrawing at min+1)
scoreboard players operation #temp {ns}.data = MIN_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 unless score #temp {ns}.data matches 1 run scoreboard players operation #temp {ns}.data *= #2 {ns}.data
execute if score BAN_REACHING_MIN_HEARTS {ns}.data matches 1 run scoreboard players add #temp {ns}.data 2
execute unless score BAN_REACHING_MIN_HEARTS {ns}.data matches 1 run scoreboard players add #temp {ns}.data 1

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


# Setup functions for dropping hearts at death location
def setup_drop_heart_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

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

