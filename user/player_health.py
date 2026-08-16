
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup the function that updates a player's health attribute
def setup_update_health(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/update_health", f"""
execute if score USE_HALF_HEARTS {ns}.data matches 0 store result storage {ns}:main health int 2 run scoreboard players get @s {ns}.hearts
execute if score USE_HALF_HEARTS {ns}.data matches 1 store result storage {ns}:main health int 1 run scoreboard players get @s {ns}.hearts

# Remove 1 health point if player has last_chance tag, since they are at MIN_HEARTS + 1 (we want to keep them at MIN_HEARTS .5)
execute if entity @s[tag={ns}.last_chance] store result score #temp {ns}.data run data get storage {ns}:main health
execute if entity @s[tag={ns}.last_chance] run scoreboard players remove #temp {ns}.data 1
execute if entity @s[tag={ns}.last_chance] store result storage {ns}:main health int 1 run scoreboard players get #temp {ns}.data

function {ns}:player/update_macro with storage {ns}:main
execute at @s run playsound entity.player.levelup ambient @s
""")

	write_function(f"{ns}:player/update_macro", "$attribute @s max_health base set $(health)")


# Setup the utility that sets the hearts amount of any player, connected or not
def setup_set_hearts(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:player/set_hearts", f"""
# Convert the asked amount to the internal scale, which is doubled when half hearts mode is enabled
$scoreboard players set #wanted_hearts {ns}.data $(hearts)
execute if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation #wanted_hearts {ns}.data *= #2 {ns}.data
scoreboard players operation #asked_hearts {ns}.data = #wanted_hearts {ns}.data

# Compute the allowed range, a MIN_HEARTS of 1 stays a single half heart like everywhere else in the pack
scoreboard players operation #max_hearts {ns}.data = MAX_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 run scoreboard players operation #max_hearts {ns}.data *= #2 {ns}.data
scoreboard players operation #min_hearts {ns}.data = MIN_HEARTS {ns}.data
execute if score USE_HALF_HEARTS {ns}.data matches 1 unless score #min_hearts {ns}.data matches 1 run scoreboard players operation #min_hearts {ns}.data *= #2 {ns}.data
execute if score #min_hearts {ns}.data matches ..0 run scoreboard players set #min_hearts {ns}.data 1

# Clamp the asked amount into that range
execute if score #wanted_hearts {ns}.data > #max_hearts {ns}.data run scoreboard players operation #wanted_hearts {ns}.data = #max_hearts {ns}.data
execute if score #wanted_hearts {ns}.data < #min_hearts {ns}.data run scoreboard players operation #wanted_hearts {ns}.data = #min_hearts {ns}.data

# Apply the amount, the last chance half heart does not apply to the new amount
$scoreboard players operation $(player) {ns}.hearts = #wanted_hearts {ns}.data
$tag $(player) remove {ns}.last_chance

# Update the health now if they are connected, else on their next join
$function {ns}:player/refresh_health {{player:"$(player)"}}

# Report what happened to the operator
$tellraw @s [{{"text":"[LifeStealFR] Hearts score of '","color":"green"}},{{"text":"$(player)","color":"yellow"}},{{"text":"' is now ","color":"green"}},{{"score":{{"name":"$(player)","objective":"{ns}.hearts"}},"color":"red"}},{{"text":".","color":"green"}}]
execute unless score #wanted_hearts {ns}.data = #asked_hearts {ns}.data run tellraw @s [{{"text":"⚠ The asked amount was out of the configured range, it was clamped between ","color":"gold"}},{{"score":{{"name":"#min_hearts","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" and ","color":"gold"}},{{"score":{{"name":"#max_hearts","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" (hearts score).","color":"gold"}}]
$execute unless entity @a[name=$(player)] run tellraw @s [{{"text":"⚠ They are not connected, their health bar will be updated when they log in.","color":"gold"}}]

# Tell the player and warn the operator when the player is still banned by LifeSteal
$execute as $(player) run tellraw @s [{{"text":"[LifeStealFR] An operator set your hearts score to ","color":"gray"}},{{"score":{{"name":"@s","objective":"{ns}.hearts"}},"color":"red"}},{{"text":"!","color":"gray"}}]
$execute if data storage {ns}:main banned_players.$(player) run tellraw @s [{{"text":"⚠ '$(player)' is still banned by LifeSteal, ","color":"gold"}},{{"text":"[click here]","color":"aqua","click_event":{{"action":"suggest_command","command":"/function {ns}:player/revive {{player:\\"$(player)\\"}}"}}}},{{"text":" to revive them.","color":"gold"}}]
""")

	write_function(f"{ns}:player/refresh_health", f"""
# Update the health right away when the player is connected
$execute as $(player) run function {ns}:player/update_health

# Else, flag them so the tick function updates their health on their next join
$execute unless entity @a[name=$(player)] run scoreboard players set $(player) {ns}.data 2
""")

