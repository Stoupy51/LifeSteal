
# Imports
from beet import Context
from stewbeet import write_function


# Setup the function that updates a player's health attribute
def setup_update_health(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/update_health", f"""
execute if score USE_HALF_HEARTS {ns}.data matches 0 store result storage {ns}:main health int 2 run scoreboard players get @s {ns}.hearts
execute if score USE_HALF_HEARTS {ns}.data matches 1 store result storage {ns}:main health int 1 run scoreboard players get @s {ns}.hearts

# Remove 1 health point if player has last_chance tag, since they are at MIN_HEARTS + 1 (we want to keep them at MIN_HEARTS .5)
execute if entity @s[tag={ns}.last_chance] store result score #temp {ns}.data run data get storage {ns}:main health
execute if entity @s[tag={ns}.last_chance] run scoreboard players remove #temp {ns}.data 1
execute if entity @s[tag={ns}.last_chance] store result storage {ns}:main health int 1 run scoreboard players get #temp {ns}.data

function {ns}:player/update_macro with storage {ns}:main
execute at @s run playsound entity.player.levelup ambient @s
""")

	write_function(f"{ns}:player/update_macro", "$attribute @s max_health base set $(health)")

