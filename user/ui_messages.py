
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup functions for displaying gain heart messages
def setup_gain_heart_messages(ctx: Context) -> None:
	ns: str = ctx.project_id

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


# Setup functions for displaying lose heart messages
def setup_lose_heart_messages(ctx: Context) -> None:
	ns: str = ctx.project_id

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


# Functions for displaying consume heart messages
def setup_consume_heart_messages(ctx: Context) -> None:
	ns: str = ctx.project_id

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


# Setup functions for displaying withdraw messages
def setup_withdraw_messages(ctx: Context) -> None:
	ns: str = ctx.project_id

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

