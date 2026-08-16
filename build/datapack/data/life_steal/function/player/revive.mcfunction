
#> life_steal:player/revive
#
# @executed	as the player & at current position
#
# @within	string in life_steal:player/set_hearts {player:\"$(player)\"}
#			life_steal:player/consume_beacon with storage life_steal:main
#			string in life_steal:_debug/player {player:\"$(player)\"}
#
# @args		player (string)
#

# Check if player is online and in spectator mode
$execute store success score #is_spectator life_steal.data if entity @a[name=$(player),gamemode=spectator]

# If player is in spectator mode, revive them
$execute if score #is_spectator life_steal.data matches 1 run gamemode survival @a[name=$(player)]
$execute if score #is_spectator life_steal.data matches 1 run tp @a[name=$(player)] @s
$execute if score #is_spectator life_steal.data matches 1 run tellraw @a [{"selector":"@s","color":"green"},{"text":" used a revive beacon to revive '$(player)'!"}]
execute if score #is_spectator life_steal.data matches 1 as @a at @s run playsound ui.toast.challenge_complete ambient @s
$execute if score #is_spectator life_steal.data matches 1 if score USE_HALF_HEARTS life_steal.data matches 0 run scoreboard players operation @a[name=$(player)] life_steal.hearts = REVIVED_HEARTS life_steal.data
$execute if score #is_spectator life_steal.data matches 1 if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation @a[name=$(player)] life_steal.hearts = REVIVED_HEARTS life_steal.data
$execute if score #is_spectator life_steal.data matches 1 if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation @a[name=$(player)] life_steal.hearts *= #2 life_steal.data
$execute if score #is_spectator life_steal.data matches 1 as @a[name=$(player)] run function life_steal:player/update_health
$execute if score #is_spectator life_steal.data matches 1 run data remove storage life_steal:main banned_players.$(player)
execute if score #is_spectator life_steal.data matches 1 run return 1

# Check if the player is in the list of players banned by LifeSteal
$execute store success score #is_banned life_steal.data if data storage life_steal:main banned_players.$(player)

# If the name is nowhere to be found, show what was checked and stop here
$execute if score #is_banned life_steal.data matches 0 run tellraw @s [{"text":"[LifeStealFR] There is no banned player named '","color":"red"},{"text":"$(player)","color":"yellow"},{"text":"', and nobody with that name is connected in spectator mode!","color":"red"}]
execute if score #is_banned life_steal.data matches 0 if data storage life_steal:main banned_players run tellraw @s [{"text":"Players banned by LifeSteal (names are case sensitive): ","color":"gray"},{"nbt":"banned_players","storage":"life_steal:main","color":"yellow"}]
execute if score #is_banned life_steal.data matches 0 unless data storage life_steal:main banned_players run tellraw @s [{"text":"No player was ever banned by LifeSteal on this world.","color":"gray"}]
execute if score #is_banned life_steal.data matches 0 run tellraw @s [{"text":"👉 ","color":"gray"},{"text":"[Click here]","color":"aqua","click_event":{"action":"suggest_command","command":"/function life_steal:_debug"}},{"text":" to diagnose the problem.","color":"gray"}]
execute if score #is_banned life_steal.data matches 0 run return fail

# Pardon the player, inline arguments are mandatory here since the storage may hold another name
$execute store success score #is_pardoned life_steal.data run function life_steal:player/pardon_player {player:"$(player)"}

# Revive the player: announce it, restore their hearts and flag them so the tick function fixes their health on join
$tellraw @a [{"selector":"@s","color":"green"},{"text":" used a revive beacon to revive '$(player)'!"}]
execute as @a at @s run playsound ui.toast.challenge_complete ambient @s
$scoreboard players operation $(player) life_steal.hearts = REVIVED_HEARTS life_steal.data
$execute if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation $(player) life_steal.hearts *= #2 life_steal.data
$scoreboard players set $(player) life_steal.data 1
$data remove storage life_steal:main banned_players.$(player)

# If the pardon silently failed while the player was really banned, tell the operator how to finish the job
$execute if score #is_pardoned life_steal.data matches 0 unless score SPECTATOR_INSTEAD life_steal.data matches 1 run tellraw @a [{"text":"[LifeStealFR] WARNING: '$(player)' got their hearts back but could not be unbanned!","color":"red"}]
$execute if score #is_pardoned life_steal.data matches 0 unless score SPECTATOR_INSTEAD life_steal.data matches 1 run tellraw @a [{"text":"👉 An operator must run ","color":"gray"},{"text":"/pardon $(player)","color":"aqua","click_event":{"action":"suggest_command","command":"/pardon $(player)"}},{"text":" from the console, and set ","color":"gray"},{"text":"function-permission-level=3","color":"red"},{"text":" in server.properties.","color":"gray"}]
return 1

