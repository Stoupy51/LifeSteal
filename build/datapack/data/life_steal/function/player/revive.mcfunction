
#> life_steal:player/revive
#
# @executed	as the player & at current position
#
# @within	life_steal:player/consume_beacon with storage life_steal:main
#
# @args		player (unknown)
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
execute if score #is_spectator life_steal.data matches 1 run return 1

# If player is banned, pardon them and return success
$execute store success score #is_banned life_steal.data if data storage life_steal:main banned_players.$(player)
execute if score #is_banned life_steal.data matches 1 run function life_steal:player/pardon_player with storage life_steal:main
$execute if score #is_banned life_steal.data matches 1 run tellraw @a [{"selector":"@s","color":"green"},{"text":" used a revive beacon to revive '$(player)'!"}]
execute if score #is_banned life_steal.data matches 1 as @a at @s run playsound ui.toast.challenge_complete ambient @s
$execute if score #is_banned life_steal.data matches 1 if score USE_HALF_HEARTS life_steal.data matches 0 run scoreboard players operation $(player) life_steal.hearts = REVIVED_HEARTS life_steal.data
$execute if score #is_banned life_steal.data matches 1 if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation $(player) life_steal.hearts = REVIVED_HEARTS life_steal.data
$execute if score #is_banned life_steal.data matches 1 if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation $(player) life_steal.hearts *= #2 life_steal.data
$execute if score #is_banned life_steal.data matches 1 run scoreboard players set $(player) life_steal.data 1
$execute if score #is_banned life_steal.data matches 1 run data remove storage life_steal:main banned_players.$(player)
execute if score #is_banned life_steal.data matches 1 run return 1

# If player is not found in spectator or banned list, return fail
$tellraw @s [{"text":"Player '$(player)' not found in the banned list or connected in spectator mode!","color":"red"}]
return fail

