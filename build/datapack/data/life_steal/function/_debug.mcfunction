
#> life_steal:_debug
#
# @within	string in life_steal:player/revive
#

# Probe the server ban list, it tells us at once if the datapack may run /ban and /pardon, and how many players are banned
scoreboard players set #ban_list_count life_steal.data 0
execute store success score #can_ban life_steal.data store result score #ban_list_count life_steal.data run function life_steal:_debug/ban_list_probe

# Display header
tellraw @s ["\n",[{"text": "[", "color": "#ff0000", "italic": false}, {"text": "L", "color": "#ff0400"}, {"text": "i", "color": "#ff0900"}, {"text": "f", "color": "#ff0e00"}, {"text": "e", "color": "#ff1300"}, {"text": " ", "color": "#ff1700"}, {"text": "S", "color": "#ff1c00"}, {"text": "t", "color": "#ff2100"}, {"text": "e", "color": "#ff2600"}, {"text": "a", "color": "#ff2b00"}, {"text": "l", "color": "#ff2f00"}, {"text": " ", "color": "#ff3400"}, {"text": "D", "color": "#ff3900"}, {"text": "e", "color": "#ff3e00"}, {"text": "b", "color": "#ff4300"}, {"text": "u", "color": "#ff4700"}, {"text": "g", "color": "#ff4c00"}, {"text": " ", "color": "#ff5100"}, {"text": "v", "color": "#ff5600"}, {"text": "2", "color": "#ff5b00"}, {"text": ".", "color": "#ff5f00"}, {"text": "3", "color": "#ff6400"}, {"text": ".", "color": "#ff6900"}, {"text": "1", "color": "#ff6e00"}, {"text": "]", "color": "#ff7300"}]]

# Display whether the datapack is allowed to ban and pardon players
execute if score #can_ban life_steal.data matches 1 run tellraw @s [{"text":"✔ /ban and /pardon: ","color":"gray"},{"text":"WORKING","color":"green"},{"text":" (the server ban list contains ","color":"gray"},{"score":{"name":"#ban_list_count","objective":"life_steal.data"},"color":"yellow"},{"text":" entries)","color":"gray"}]
execute if score #can_ban life_steal.data matches 0 run tellraw @s [{"text":"✖ /ban and /pardon: ","color":"gray"},{"text":"NOT AVAILABLE","color":"red"},{"text":" (players cannot be banned nor unbanned by the datapack)","color":"gray"}]
execute if score #can_ban life_steal.data matches 0 run tellraw @s [{"text":"   • On a server: set ","color":"gray"},{"text":"function-permission-level=3","color":"red"},{"text":" in server.properties, then restart the server.","color":"gray"}]
execute if score #can_ban life_steal.data matches 0 run tellraw @s [{"text":"   • In singleplayer/LAN: those commands do not exist at all, ","color":"gray"},{"text":"[click here]","color":"aqua","click_event":{"action":"suggest_command","command":"/scoreboard players set SPECTATOR_INSTEAD life_steal.data 1"}},{"text":" to use spectator mode instead of bans.","color":"gray"}]

# Display the configuration that decides what happens at minimum hearts
execute if score BAN_REACHING_MIN_HEARTS life_steal.data matches 0 run tellraw @s [{"text":"• Ban Reaching Min Hearts is ","color":"gray"},{"text":"DISABLED","color":"yellow"},{"text":": nobody is ever banned by LifeSteal.","color":"gray"}]
execute if score SPECTATOR_INSTEAD life_steal.data matches 1 run tellraw @s [{"text":"• Spectator Instead is ","color":"gray"},{"text":"ENABLED","color":"yellow"},{"text":": players are put in spectator mode instead of being banned.","color":"gray"}]

# Display the list of players banned by the datapack
execute if data storage life_steal:main banned_players run tellraw @s [{"text":"Players banned by LifeSteal: ","color":"gray"},{"nbt":"banned_players","storage":"life_steal:main","color":"yellow"}]
execute unless data storage life_steal:main banned_players run tellraw @s [{"text":"Players banned by LifeSteal: ","color":"gray"},{"text":"none recorded on this world","color":"yellow"}]

# Display how to inspect a single player
tellraw @s [{"text":"👉 ","color":"gray"},{"text":"[Click here]","color":"aqua","click_event":{"action":"suggest_command","command":"/function life_steal:_debug/player {player:\"Stoupy51\"}"}},{"text":" to check a specific player (names are case sensitive).","color":"gray"}]

