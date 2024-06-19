
# Imports
from python_datapack.constants import *
from python_datapack.utils.print import *
from python_datapack.utils.io import *

# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def main(config: dict) -> None:
	namespace: str = config["namespace"]
	functions: str = f"{config['build_datapack']}/data/{namespace}/function"
	version: str = config["version"]

	# Add scoreboard objectives
	confirm_load: str = f"{functions}/v{version}/load/confirm_load.mcfunction"
	write_to_file(confirm_load, f"scoreboard objectives add {namespace}.kill playerKillCount\n", prepend = True)
	write_to_file(confirm_load, f"scoreboard objectives add {namespace}.death deathCount\n", prepend = True)
	write_to_file(confirm_load, f"scoreboard objectives add {namespace}.withdraw trigger\n", prepend = True)
	write_to_file(confirm_load, f"scoreboard objectives add {namespace}.hearts dummy\n", prepend = True)
	write_to_file(confirm_load, f"execute unless score MAX_HEARTS {namespace}.data matches 1.. run scoreboard players set MAX_HEARTS {namespace}.data 20\n", prepend = True)

	# Add tick function
	write_to_file(f"{functions}/v{version}/tick.mcfunction", f"execute as @a[sort=random] run function {namespace}:player/tick\n")

	# Add player function
	write_to_file(f"{functions}/player/tick.mcfunction", f"""
# Setup hearts objective if not set
execute unless score @s {namespace}.hearts matches 0.. store result score @s {namespace}.hearts run attribute @s minecraft:generic.max_health base get 0.5

# Withdraw command trigger
scoreboard players enable @s {namespace}.withdraw
execute unless score @s {namespace}.withdraw matches 0 run function {namespace}:player/withdraw

# If killed player, add a heart
execute if score @s {namespace}.kill matches 1.. run scoreboard players operation @s {namespace}.hearts += @s {namespace}.kill
execute if score @s {namespace}.kill matches 1.. run tellraw @s [{{"text":"You stole a heart from a player, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{namespace}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score @s {namespace}.kill matches 1.. run function {namespace}:player/update_health
execute if score @s {namespace}.kill matches 1.. run scoreboard players set @s {namespace}.kill 0

# If player died, remove a heart
execute if score @s {namespace}.death matches 1.. run scoreboard players remove @s {namespace}.hearts 1
execute if score @s {namespace}.death matches 1.. run tellraw @s [{{"text":"You lost a heart, you now have ","color":"gray"}},{{"score":{{"name":"@s","objective":"{namespace}.hearts"}}, "color":"red"}},{{"text":" hearts!"}}]
execute if score @s {namespace}.death matches 1.. run function {namespace}:player/update_health
execute if score @s {namespace}.death matches 1.. run scoreboard players set @s {namespace}.death 0
execute if score @s {namespace}.hearts matches 0 run function {namespace}:player/death
""")
	
	# Add update_health function
	write_to_file(f"{functions}/player/update_health.mcfunction", f"""
execute store result storage {namespace}:main health int 2 run scoreboard players get @s {namespace}.hearts
function {namespace}:player/update_macro with storage {namespace}:main
execute at @s run playsound entity.player.levelup ambient @s
""")
	write_to_file(f"{functions}/player/update_macro.mcfunction", "$attribute @s minecraft:generic.max_health base set $(health)")

	# Add withdraw function
	write_to_file(f"{functions}/player/withdraw.mcfunction", f"""
# Reset withdraw trigger and stop function if not enough hearts
scoreboard players set @s {namespace}.withdraw 0
execute if score @s {namespace}.hearts matches ..1 run tellraw @s {{"text":"You don't have enough hearts to withdraw!","color":"red"}}
execute if score @s {namespace}.hearts matches ..1 run return fail

# Give heart, decrease score, and update health
loot give @s loot {namespace}:i/heart
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
	write_to_file(advancement, super_json_dump(json_content, max_level = -1))

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


	pass

