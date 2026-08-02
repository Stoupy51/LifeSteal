
#> life_steal:player/force_revive
#
# @within	string in life_steal:_debug/player {player:\"$(player)\"}
#
# @args		player (string)
#

# Pardon the player, it silently fails when they were not banned or when the datapack lacks permissions
$execute store success score #is_pardoned life_steal.data run function life_steal:player/pardon_player {player:"$(player)"}

# Restore their hearts and flag them so the tick function fixes their health and gamemode on join
$scoreboard players operation $(player) life_steal.hearts = REVIVED_HEARTS life_steal.data
$execute if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation $(player) life_steal.hearts *= #2 life_steal.data
$scoreboard players set $(player) life_steal.data 1
$data remove storage life_steal:main banned_players.$(player)
$gamemode survival @a[name=$(player),gamemode=spectator]
$execute as @a[name=$(player)] run function life_steal:player/update_health

# Report what happened
$tellraw @s [{"text":"[LifeStealFR] Force revived '$(player)', they are unbanned and back to the revived hearts amount.","color":"green"}]
execute if score #is_pardoned life_steal.data matches 0 run tellraw @s [{"text":"⚠ /pardon did not run: either they were not banned at all, or the datapack lacks permissions (function-permission-level=3).","color":"gold"}]

