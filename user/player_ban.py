
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup function that runs when a player reaches minimum hearts
def setup_reached_min_hearts(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/reached_min_hearts", f"""
# If died from a player but not BAN_REACHING_MIN_HEARTS configuration, do not reward the killer
execute unless score BAN_REACHING_MIN_HEARTS {ns}.data matches 1 run scoreboard players remove @a[scores={{{ns}.kill=1..}}] {ns}.kill 1

# Make sure player does not have less than minimum hearts
execute if score @s {ns}.hearts < #real_min_hearts {ns}.data run scoreboard players operation @s {ns}.hearts = #real_min_hearts {ns}.data
execute if score @s {ns}.hearts matches ..0 run scoreboard players set @s {ns}.hearts 1
function {ns}:player/update_health

# If not BAN_REACHING_MIN_HEARTS configuration, stop here
execute unless score BAN_REACHING_MIN_HEARTS {ns}.data matches 1 run return 1

# If SPECTATOR_INSTEAD is enabled, move to spectator and announce
execute if score SPECTATOR_INSTEAD {ns}.data matches 1 run gamemode spectator @s
execute if score SPECTATOR_INSTEAD {ns}.data matches 1 run return run tellraw @a [{{"selector":"@s","color":"red"}},{{"text":" reached minimum hearts and was moved to spectator mode!"}}]

# Get player username for macro
tag @e[type=item] add {ns}.temp
execute at @s run loot spawn ~ ~ ~ loot {ns}:player_head
data modify storage {ns}:main player set from entity @e[type=item,tag=!{ns}.temp,limit=1] Item.components."minecraft:profile".name
kill @e[type=item,tag=!{ns}.temp]
tag @e[type=item,tag={ns}.temp] remove {ns}.temp

# Ban macro
scoreboard players set #banned {ns}.data 0
function {ns}:player/ban_macro with storage {ns}:main

# If banned player is still in the world, make him spectator and send an error message (function permission issue)
execute if score #banned {ns}.data matches 0 run gamemode spectator @s
execute if score #banned {ns}.data matches 0 run tellraw @a [{{"text":"[LifeStealFR] ERROR: Could not ban player '","color":"red"}},{{"selector":"@s"}},{{"text":"'. Set 'function-permission-level' to 3 in server.properties!"}}]
""")

	write_function(f"{ns}:player/ban_macro", f"""
# Tellraw message and ban player
$tellraw @a {{"text":"Player '$(player)' just got banned for reaching minimum hearts!","color":"red"}}
$ban $(player) You reached the minimum hearts!

# Add player name to banned list
execute unless data storage {ns}:main banned_players run data modify storage {ns}:main banned_players set value {{}}
$data modify storage {ns}:main banned_players.$(player) set value true
scoreboard players set #banned {ns}.data 1
""")

