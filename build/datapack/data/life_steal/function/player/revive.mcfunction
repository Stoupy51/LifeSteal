
#> life_steal:player/revive
#
# @executed	as the player & at current position
#
# @within	life_steal:player/consume_beacon with storage life_steal:main
#
# @args		player (unknown)
#

# If player is banned, pardon him and return success
$execute store success score #is_banned life_steal.data if data storage life_steal:main banned_players.$(player)
$execute if score #is_banned life_steal.data matches 1 run pardon $(player)
$execute if score #is_banned life_steal.data matches 1 run tellraw @a [{"selector":"@s","color":"green"},{"text":" used a revive beacon to revive '$(player)'!"}]
execute if score #is_banned life_steal.data matches 1 as @a at @s run playsound ui.toast.challenge_complete ambient @s
$execute if score #is_banned life_steal.data matches 1 if score USE_HALF_HEARTS life_steal.data matches 0 run scoreboard players operation $(player) life_steal.hearts = REVIVED_HEARTS life_steal.data
$execute if score #is_banned life_steal.data matches 1 if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation $(player) life_steal.hearts = REVIVED_HEARTS life_steal.data
$execute if score #is_banned life_steal.data matches 1 if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation $(player) life_steal.hearts *= #2 life_steal.data
$execute if score #is_banned life_steal.data matches 1 run scoreboard players set $(player) life_steal.data 1
$execute if score #is_banned life_steal.data matches 1 run data remove storage life_steal:main banned_players.$(player)
execute if score #is_banned life_steal.data matches 1 run return 1

# If player is not found, return fail
$tellraw @s [{"text":"Player '$(player)' not found in the banned list!","color":"red"}]
return fail

