
# Imports
from beet import Context
from stewbeet import write_function


# Setup configuration change detection and conversion functions
def setup_config_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	# Configuration change detection
	write_function(f"{ns}:config/half_hearts_changed", f"""
# Convert hearts for all players based on new configuration
execute if score USE_HALF_HEARTS {ns}.data matches 1 if score USE_HALF_HEARTS_PREV {ns}.data matches 0 run function {ns}:config/convert_to_half_hearts
execute if score USE_HALF_HEARTS {ns}.data matches 0 if score USE_HALF_HEARTS_PREV {ns}.data matches 1 run function {ns}:config/convert_to_full_hearts

# Update previous value
scoreboard players operation USE_HALF_HEARTS_PREV {ns}.data = USE_HALF_HEARTS {ns}.data
""")

	# Convert to half hearts
	write_function(f"{ns}:config/convert_to_half_hearts", f"""
# Convert all players from full hearts to half hearts (multiply by 2)
execute as @a run scoreboard players operation @s {ns}.hearts *= #2 {ns}.data
execute as @a run function {ns}:player/update_health

# Notify all players
tellraw @a [{{"text":"[Life Steal] Configuration changed to half hearts mode! All hearts score have been doubled.","color":"green"}}]
execute as @a at @s run playsound entity.experience_orb.pickup ambient @s
""")

	# Convert to full hearts
	write_function(f"{ns}:config/convert_to_full_hearts", f"""
# Convert all players from half hearts to full hearts (divide by 2)
execute as @a run scoreboard players operation @s {ns}.hearts /= #2 {ns}.data
execute as @a run function {ns}:player/update_health

# Notify all players
tellraw @a [{{"text":"[Life Steal] Configuration changed to full hearts mode! All hearts score have been halved.","color":"yellow"}}]
execute as @a at @s run playsound entity.experience_orb.pickup ambient @s
""")

