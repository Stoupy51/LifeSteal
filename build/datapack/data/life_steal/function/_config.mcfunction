
#> life_steal:_config
#
# @within	???
#

# Display configuration header
tellraw @s {"text":"[Life Steal Configuration]","color":"gold"}

# Numeric settings
tellraw @s {"text":"\nNumeric Settings:","color":"aqua"}
tellraw @s [{"text":"- Max Hearts: ","color":"aqua"},{"score":{"name":"MAX_HEARTS","objective":"life_steal.data"},"color":"yellow"},{"text":" [click]","color":"gray","click_event":{"action":"suggest_command","command":"/scoreboard players set MAX_HEARTS life_steal.data 20"},"hover_event":{"action":"show_text","value":{"text":"Enter the maximum number of hearts a player can have\nDefault: 20","color":"gray"}}}]
tellraw @s [{"text":"- Min Hearts: ","color":"aqua"},{"score":{"name":"MIN_HEARTS","objective":"life_steal.data"},"color":"yellow"},{"text":" [click]","color":"gray","click_event":{"action":"suggest_command","command":"/scoreboard players set MIN_HEARTS life_steal.data 1"},"hover_event":{"action":"show_text","value":{"text":"Enter the minimum number of hearts a player can have\nDefault: 1","color":"gray"}}}]
tellraw @s [{"text":"- Revived Hearts: ","color":"aqua"},{"score":{"name":"REVIVED_HEARTS","objective":"life_steal.data"},"color":"yellow"},{"text":" [click]","color":"gray","click_event":{"action":"suggest_command","command":"/scoreboard players set REVIVED_HEARTS life_steal.data 4"},"hover_event":{"action":"show_text","value":{"text":"Enter the number of hearts a player respawns with when revived\nDefault: 4","color":"gray"}}}]

# Boolean settings
tellraw @s {"text":"\nToggle Settings (1 = enabled, 0 = disabled):","color":"aqua"}
execute if score NATURAL_DEATH_HEART_DROP life_steal.data matches 1 run tellraw @s [{"text":"- Natural Death Heart Drop: ","color":"aqua"},{"text":"Enabled","color":"green"},{"text":" [click]","color":"gray","click_event":{"action":"suggest_command","command":"/scoreboard players set NATURAL_DEATH_HEART_DROP life_steal.data 0"},"hover_event":{"action":"show_text","value":{"text":"Click to disable - Players won't drop hearts when dying to non-player causes\nDefault: Enabled","color":"gray"}}}]
execute if score NATURAL_DEATH_HEART_DROP life_steal.data matches 0 run tellraw @s [{"text":"- Natural Death Heart Drop: ","color":"aqua"},{"text":"Disabled","color":"red"},{"text":" [click]","color":"gray","click_event":{"action":"suggest_command","command":"/scoreboard players set NATURAL_DEATH_HEART_DROP life_steal.data 1"},"hover_event":{"action":"show_text","value":{"text":"Click to enable - Players will drop hearts when dying to non-player causes\nDefault: Enabled","color":"gray"}}}]
execute if score USE_HALF_HEARTS life_steal.data matches 1 run tellraw @s [{"text":"- Half Hearts Mode: ","color":"aqua"},{"text":"Enabled","color":"green"},{"text":" [click]","color":"gray","click_event":{"action":"suggest_command","command":"/scoreboard players set USE_HALF_HEARTS life_steal.data 0"},"hover_event":{"action":"show_text","value":{"text":"Click to disable - Hearts will be tracked in whole numbers\nWarning: This will convert all players' hearts!\nDefault: Disabled","color":"gray"}}}]
execute if score USE_HALF_HEARTS life_steal.data matches 0 run tellraw @s [{"text":"- Half Hearts Mode: ","color":"aqua"},{"text":"Disabled","color":"red"},{"text":" [click]","color":"gray","click_event":{"action":"suggest_command","command":"/scoreboard players set USE_HALF_HEARTS life_steal.data 1"},"hover_event":{"action":"show_text","value":{"text":"Click to enable - Hearts will be tracked in 0.5 increments\nWarning: This will convert all players' hearts!\nDefault: Disabled","color":"gray"}}}]
execute if score BAN_BELOW_MIN_HEARTS life_steal.data matches 1 run tellraw @s [{"text":"- Ban Below Min Hearts: ","color":"aqua"},{"text":"Enabled","color":"green"},{"text":" [click]","color":"gray","click_event":{"action":"suggest_command","command":"/scoreboard players set BAN_BELOW_MIN_HEARTS life_steal.data 0"},"hover_event":{"action":"show_text","value":{"text":"Click to disable - Players won't be banned when reaching minimum hearts\nDefault: Enabled","color":"gray"}}}]
execute if score BAN_BELOW_MIN_HEARTS life_steal.data matches 0 run tellraw @s [{"text":"- Ban Below Min Hearts: ","color":"aqua"},{"text":"Disabled","color":"red"},{"text":" [click]","color":"gray","click_event":{"action":"suggest_command","command":"/scoreboard players set BAN_BELOW_MIN_HEARTS life_steal.data 1"},"hover_event":{"action":"show_text","value":{"text":"Click to enable - Players will be banned when reaching minimum hearts\nDefault: Enabled","color":"gray"}}}]

