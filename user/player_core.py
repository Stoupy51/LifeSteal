
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup the main player tick function
def setup_player_tick(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/tick", f"""
# Setup hearts objective if not set and get all recipes
execute unless score @s {ns}.hearts matches 0.. run function {ns}:utils/get_all_recipes
execute unless score @s {ns}.hearts matches 0.. if score USE_HALF_HEARTS {ns}.data matches 0 store result score @s {ns}.hearts run attribute @s minecraft:max_health base get 0.5
execute unless score @s {ns}.hearts matches 0.. if score USE_HALF_HEARTS {ns}.data matches 1 store result score @s {ns}.hearts run attribute @s minecraft:max_health base get 1.0

# If data = 1, player is revived so update health and set gamemode
execute if score @s {ns}.data matches 1 run gamemode survival @s[gamemode=spectator]
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


# Setup the function that runs when a player kills another player
def setup_player_on_kill(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/on_kill", f"""
# If STEAL_ON_KILL is disabled, or NO_HEART_DROP_OR_STEAL is enabled, do nothing
execute unless score STEAL_ON_KILL {ns}.data matches 1 run return run scoreboard players set @s {ns}.kill 0
execute if score NO_HEART_DROP_OR_STEAL {ns}.data matches 1 run return run scoreboard players set @s {ns}.kill 0

# Compute max hearts
scoreboard players operation #temp {ns}.data = MAX_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation #temp {ns}.data *= #2 {ns}.data

# If at max hearts, send message
execute if score @s {ns}.hearts >= #temp {ns}.data run tellraw @s [{{"text":"You stole a heart from a player, but you are already at max health!","color":"red"}}]

# Else, add a heart (or half heart) and remove last_chance tag
execute if score @s {ns}.hearts < #temp {ns}.data run tag @s remove {ns}.last_chance
execute if score @s {ns}.hearts < #temp {ns}.data run scoreboard players operation @s {ns}.hearts += @s {ns}.kill
execute if score @s {ns}.hearts < #temp {ns}.data run function {ns}:player/gain_heart_msg

# Update health and reset kill score
function {ns}:player/update_health
scoreboard players set @s {ns}.kill 0
""")


# Setup the function that runs when a player dies
def setup_player_on_death(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/on_death", f"""
# Reset death score
scoreboard players set @s {ns}.death 0

# Calculate minimum hearts threshold
execute store result score #real_min_hearts {ns}.data run scoreboard players get MIN_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 unless score #real_min_hearts {ns}.data matches 1 run scoreboard players operation #real_min_hearts {ns}.data *= #2 {ns}.data

# If (died from a player AND STEAL_ON_KILL is enabled), or (died from natural causes and NATURAL_DEATH_HEART_LOSE is 1), remove a heart (only if above minimum)
execute if score @s {ns}.hearts > #real_min_hearts {ns}.data if entity @a[scores={{{ns}.kill=1..}}] if score STEAL_ON_KILL {ns}.data matches 1 run function {ns}:player/remove_one_heart
execute if score @s {ns}.hearts > #real_min_hearts {ns}.data unless entity @a[scores={{{ns}.kill=1..}}] unless score NATURAL_DEATH_HEART_LOSE {ns}.data matches 0 run function {ns}:player/remove_one_heart

# Check if reached minimum hearts
execute if score @s {ns}.hearts <= #real_min_hearts {ns}.data run function {ns}:player/reached_min_hearts

# Update health
function {ns}:player/update_health
""")


# Setup the function that removes one heart from a player
def setup_remove_one_heart(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/remove_one_heart", f"""
# Check for last chance condition (only when half hearts mode is disabled)
scoreboard players set #lose_heart_msg {ns}.data 1
execute if score LAST_CHANCE {ns}.data matches 1 unless score USE_HALF_HEARTS {ns}.data matches 1 unless entity @s[tag={ns}.last_chance] run function {ns}:player/check_last_chance

# Remove one heart
scoreboard players remove @s {ns}.hearts 1

# Tellraw message and update health
execute if score #lose_heart_msg {ns}.data matches 1 run function {ns}:player/lose_heart_msg
function {ns}:player/update_health

# Drop a heart if player wasn't killed by another, and if NO_HEART_DROP_OR_STEAL and NATURAL_DEATH_HEART_DROP are enabled
execute unless score NO_HEART_DROP_OR_STEAL {ns}.data matches 1 unless entity @a[scores={{{ns}.kill=1..}}] if score NATURAL_DEATH_HEART_DROP {ns}.data matches 1 run function {ns}:player/drop_heart_at_death
""")


# Setup the function that checks and applies last chance conditions
def setup_check_last_chance(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/check_last_chance", f"""
# Calculate if player is at MIN_HEARTS + 1
scoreboard players operation #check_hearts {ns}.data = MIN_HEARTS {ns}.data
scoreboard players add #check_hearts {ns}.data 1

# If player is at MIN_HEARTS + 1, give them last chance tag
execute if score @s {ns}.hearts = #check_hearts {ns}.data run tag @s add {ns}.last_chance
execute if score @s {ns}.hearts = #check_hearts {ns}.data run tellraw @s [{{"text":"⚠ Last Chance! You now have ","color":"gold"}},{{"score":{{"name":"MIN_HEARTS","objective":"{ns}.data"}},"color":"red"}},{{"text":".5 hearts!","color":"red"}}]
execute if score @s {ns}.hearts = #check_hearts {ns}.data run scoreboard players set #lose_heart_msg {ns}.data 0

# Add 1 heart back (to prevent going below MIN_HEARTS)
execute if score @s {ns}.hearts = #check_hearts {ns}.data run scoreboard players add @s {ns}.hearts 1
""")

