
# ruff: noqa: E501
# Imports
import json

from beet import Context
from stewbeet import create_gradient_text, write_function


# Setup the debugging functions used by operators to diagnose ban/revive issues
def setup_debug_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	DEBUG_TEXT: str = json.dumps(create_gradient_text(f"[Life Steal Debug v{ctx.project_version}]", "#FF0000", "#FF7300"))

	write_function(f"{ns}:_debug", f"""
# Probe the server ban list, it tells us at once if the datapack may run /ban and /pardon, and how many players are banned
scoreboard players set #ban_list_count {ns}.data 0
execute store success score #can_ban {ns}.data store result score #ban_list_count {ns}.data run function {ns}:_debug/ban_list_probe

# Display header
tellraw @s ["\\n",{DEBUG_TEXT}]

# Display whether the datapack is allowed to ban and pardon players
execute if score #can_ban {ns}.data matches 1 run tellraw @s [{{"text":"✔ /ban and /pardon: ","color":"gray"}},{{"text":"WORKING","color":"green"}},{{"text":" (the server ban list contains ","color":"gray"}},{{"score":{{"name":"#ban_list_count","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" entries)","color":"gray"}}]
execute if score #can_ban {ns}.data matches 0 run tellraw @s [{{"text":"✖ /ban and /pardon: ","color":"gray"}},{{"text":"NOT AVAILABLE","color":"red"}},{{"text":" (players cannot be banned nor unbanned by the datapack)","color":"gray"}}]
execute if score #can_ban {ns}.data matches 0 run tellraw @s [{{"text":"   • On a server: set ","color":"gray"}},{{"text":"function-permission-level=3","color":"red"}},{{"text":" in server.properties, then restart the server.","color":"gray"}}]
execute if score #can_ban {ns}.data matches 0 run tellraw @s [{{"text":"   • In singleplayer/LAN: those commands do not exist at all, ","color":"gray"}},{{"text":"[click here]","color":"aqua","click_event":{{"action":"suggest_command","command":"/scoreboard players set SPECTATOR_INSTEAD {ns}.data 1"}}}},{{"text":" to use spectator mode instead of bans.","color":"gray"}}]

# Display the configuration that decides what happens at minimum hearts
execute if score BAN_REACHING_MIN_HEARTS {ns}.data matches 0 run tellraw @s [{{"text":"• Ban Reaching Min Hearts is ","color":"gray"}},{{"text":"DISABLED","color":"yellow"}},{{"text":": nobody is ever banned by LifeSteal.","color":"gray"}}]
execute if score SPECTATOR_INSTEAD {ns}.data matches 1 run tellraw @s [{{"text":"• Spectator Instead is ","color":"gray"}},{{"text":"ENABLED","color":"yellow"}},{{"text":": players are put in spectator mode instead of being banned.","color":"gray"}}]

# Display the list of players banned by the datapack
execute if data storage {ns}:main banned_players run tellraw @s [{{"text":"Players banned by LifeSteal: ","color":"gray"}},{{"nbt":"banned_players","storage":"{ns}:main","color":"yellow"}}]
execute unless data storage {ns}:main banned_players run tellraw @s [{{"text":"Players banned by LifeSteal: ","color":"gray"}},{{"text":"none recorded on this world","color":"yellow"}}]

# Display how to inspect a single player
tellraw @s [{{"text":"👉 ","color":"gray"}},{{"text":"[Click here]","color":"aqua","click_event":{{"action":"suggest_command","command":"/function {ns}:_debug/player {{player:\\"Stoupy51\\"}}"}}}},{{"text":" to check a specific player (names are case sensitive).","color":"gray"}}]
""")

	# Isolated probe function, it fails silently when the datapack is not allowed to run /banlist (low permission level or singleplayer)
	write_function(f"{ns}:_debug/ban_list_probe", "return run banlist players")

	write_function(f"{ns}:_debug/player", f"""
# Collect every state of the given player
$execute store success score #dbg_recorded {ns}.data if data storage {ns}:main banned_players.$(player)
$execute store success score #dbg_online {ns}.data if entity @a[name=$(player)]
$execute store success score #dbg_spectator {ns}.data if entity @a[name=$(player),gamemode=spectator]
$execute store success score #dbg_hearts {ns}.data if score $(player) {ns}.hearts matches -2147483648..

# Display header
$tellraw @s ["\\n",{{"text":"[LifeSteal Debug] Player '","color":"gray"}},{{"text":"$(player)","color":"yellow"}},{{"text":"':","color":"gray"}}]

# Display connection state
execute if score #dbg_spectator {ns}.data matches 1 run tellraw @s [{{"text":"- Connected: ","color":"gray"}},{{"text":"YES, in spectator mode","color":"green"}}]
execute if score #dbg_online {ns}.data matches 1 if score #dbg_spectator {ns}.data matches 0 run tellraw @s [{{"text":"- Connected: ","color":"gray"}},{{"text":"YES, and not in spectator mode","color":"green"}}]
execute if score #dbg_online {ns}.data matches 0 run tellraw @s [{{"text":"- Connected: ","color":"gray"}},{{"text":"NO","color":"yellow"}}]

# Display LifeSteal states
execute if score #dbg_recorded {ns}.data matches 1 run tellraw @s [{{"text":"- Banned by LifeSteal: ","color":"gray"}},{{"text":"YES","color":"green"}},{{"text":" (the revive beacon will work on this name)","color":"gray"}}]
execute if score #dbg_recorded {ns}.data matches 0 run tellraw @s [{{"text":"- Banned by LifeSteal: ","color":"gray"}},{{"text":"NO","color":"red"}},{{"text":" (this exact name is not in the LifeSteal banned list)","color":"gray"}}]
$execute if score #dbg_hearts {ns}.data matches 1 run tellraw @s [{{"text":"- Hearts score: ","color":"gray"}},{{"score":{{"name":"$(player)","objective":"{ns}.hearts"}},"color":"red"}}]
execute if score #dbg_hearts {ns}.data matches 0 run tellraw @s [{{"text":"- Hearts score: ","color":"gray"}},{{"text":"none","color":"red"}},{{"text":" (this player never joined, or the name is misspelled)","color":"gray"}}]

# Display what to do next
$execute if score #dbg_recorded {ns}.data matches 1 run tellraw @s [{{"text":"👉 ","color":"gray"}},{{"text":"[Click here]","color":"aqua","click_event":{{"action":"suggest_command","command":"/function {ns}:player/revive {{player:\\"$(player)\\"}}"}}}},{{"text":" to revive them right now.","color":"gray"}}]
$execute if score #dbg_recorded {ns}.data matches 0 run tellraw @s [{{"text":"👉 LifeSteal did not ban this player. If they still cannot join, the ban comes from somewhere else (manual /ban, plugin, or a lost world storage): ","color":"gray"}},{{"text":"[click here]","color":"aqua","click_event":{{"action":"suggest_command","command":"/function {ns}:player/force_revive {{player:\\"$(player)\\"}}"}}}},{{"text":" to unban them and give them back ","color":"gray"}},{{"score":{{"name":"REVIVED_HEARTS","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" hearts anyway.","color":"gray"}}]
""")

