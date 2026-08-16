
#> life_steal:player/set_hearts
#
# @within	string in life_steal:_debug/player {player:\"$(player)\",hearts:10}
#
# @args		hearts (int)
#			player (string)
#

# Convert the asked amount to the internal scale, which is doubled when half hearts mode is enabled
$scoreboard players set #wanted_hearts life_steal.data $(hearts)
execute if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation #wanted_hearts life_steal.data *= #2 life_steal.data
scoreboard players operation #asked_hearts life_steal.data = #wanted_hearts life_steal.data

# Compute the allowed range, a MIN_HEARTS of 1 stays a single half heart like everywhere else in the pack
scoreboard players operation #max_hearts life_steal.data = MAX_HEARTS life_steal.data
execute if score USE_HALF_HEARTS life_steal.data matches 1 run scoreboard players operation #max_hearts life_steal.data *= #2 life_steal.data
scoreboard players operation #min_hearts life_steal.data = MIN_HEARTS life_steal.data
execute if score USE_HALF_HEARTS life_steal.data matches 1 unless score #min_hearts life_steal.data matches 1 run scoreboard players operation #min_hearts life_steal.data *= #2 life_steal.data
execute if score #min_hearts life_steal.data matches ..0 run scoreboard players set #min_hearts life_steal.data 1

# Clamp the asked amount into that range
execute if score #wanted_hearts life_steal.data > #max_hearts life_steal.data run scoreboard players operation #wanted_hearts life_steal.data = #max_hearts life_steal.data
execute if score #wanted_hearts life_steal.data < #min_hearts life_steal.data run scoreboard players operation #wanted_hearts life_steal.data = #min_hearts life_steal.data

# Apply the amount, the last chance half heart does not apply to the new amount
$scoreboard players operation $(player) life_steal.hearts = #wanted_hearts life_steal.data
$tag $(player) remove life_steal.last_chance

# Update the health now if they are connected, else on their next join
$function life_steal:player/refresh_health {player:"$(player)"}

# Report what happened to the operator
$tellraw @s [{"text":"[LifeStealFR] Hearts score of '","color":"green"},{"text":"$(player)","color":"yellow"},{"text":"' is now ","color":"green"},{"score":{"name":"$(player)","objective":"life_steal.hearts"},"color":"red"},{"text":".","color":"green"}]
execute unless score #wanted_hearts life_steal.data = #asked_hearts life_steal.data run tellraw @s [{"text":"⚠ The asked amount was out of the configured range, it was clamped between ","color":"gold"},{"score":{"name":"#min_hearts","objective":"life_steal.data"},"color":"yellow"},{"text":" and ","color":"gold"},{"score":{"name":"#max_hearts","objective":"life_steal.data"},"color":"yellow"},{"text":" (hearts score).","color":"gold"}]
$execute unless entity @a[name=$(player)] run tellraw @s [{"text":"⚠ They are not connected, their health bar will be updated when they log in.","color":"gold"}]

# Tell the player and warn the operator when the player is still banned by LifeSteal
$execute as $(player) run tellraw @s [{"text":"[LifeStealFR] An operator set your hearts score to ","color":"gray"},{"score":{"name":"@s","objective":"life_steal.hearts"},"color":"red"},{"text":"!","color":"gray"}]
$execute if data storage life_steal:main banned_players.$(player) run tellraw @s [{"text":"⚠ '$(player)' is still banned by LifeSteal, ","color":"gold"},{"text":"[click here]","color":"aqua","click_event":{"action":"suggest_command","command":"/function life_steal:player/revive {player:\"$(player)\"}"}},{"text":" to revive them.","color":"gold"}]

