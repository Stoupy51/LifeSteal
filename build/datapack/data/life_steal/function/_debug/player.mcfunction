
#> life_steal:_debug/player
#
# @within	string in life_steal:_debug {player:\"Stoupy51\"}
#
# @args		player (string)
#

# Collect every state of the given player
$execute store success score #dbg_recorded life_steal.data if data storage life_steal:main banned_players.$(player)
$execute store success score #dbg_online life_steal.data if entity @a[name=$(player)]
$execute store success score #dbg_spectator life_steal.data if entity @a[name=$(player),gamemode=spectator]
$execute store success score #dbg_hearts life_steal.data if score $(player) life_steal.hearts matches -2147483648..

# Display header
$tellraw @s ["\n",{"text":"[LifeSteal Debug] Player '","color":"gray"},{"text":"$(player)","color":"yellow"},{"text":"':","color":"gray"}]

# Display connection state
execute if score #dbg_spectator life_steal.data matches 1 run tellraw @s [{"text":"- Connected: ","color":"gray"},{"text":"YES, in spectator mode","color":"green"}]
execute if score #dbg_online life_steal.data matches 1 if score #dbg_spectator life_steal.data matches 0 run tellraw @s [{"text":"- Connected: ","color":"gray"},{"text":"YES, and not in spectator mode","color":"green"}]
execute if score #dbg_online life_steal.data matches 0 run tellraw @s [{"text":"- Connected: ","color":"gray"},{"text":"NO","color":"yellow"}]

# Display LifeSteal states
execute if score #dbg_recorded life_steal.data matches 1 run tellraw @s [{"text":"- Banned by LifeSteal: ","color":"gray"},{"text":"YES","color":"green"},{"text":" (the revive beacon will work on this name)","color":"gray"}]
execute if score #dbg_recorded life_steal.data matches 0 run tellraw @s [{"text":"- Banned by LifeSteal: ","color":"gray"},{"text":"NO","color":"red"},{"text":" (this exact name is not in the LifeSteal banned list)","color":"gray"}]
$execute if score #dbg_hearts life_steal.data matches 1 run tellraw @s [{"text":"- Hearts score: ","color":"gray"},{"score":{"name":"$(player)","objective":"life_steal.hearts"},"color":"red"}]
execute if score #dbg_hearts life_steal.data matches 0 run tellraw @s [{"text":"- Hearts score: ","color":"gray"},{"text":"none","color":"red"},{"text":" (this player never joined, or the name is misspelled)","color":"gray"}]

# Display what to do next
$execute if score #dbg_recorded life_steal.data matches 1 run tellraw @s [{"text":"👉 ","color":"gray"},{"text":"[Click here]","color":"aqua","click_event":{"action":"suggest_command","command":"/function life_steal:player/revive {player:\"$(player)\"}"}},{"text":" to revive them right now.","color":"gray"}]
$execute if score #dbg_recorded life_steal.data matches 0 run tellraw @s [{"text":"👉 LifeSteal did not ban this player. If they still cannot join, the ban comes from somewhere else (manual /ban, plugin, or a lost world storage): ","color":"gray"},{"text":"[click here]","color":"aqua","click_event":{"action":"suggest_command","command":"/function life_steal:player/force_revive {player:\"$(player)\"}"}},{"text":" to unban them and give them back ","color":"gray"},{"score":{"name":"REVIVED_HEARTS","objective":"life_steal.data"},"color":"yellow"},{"text":" hearts anyway.","color":"gray"}]

