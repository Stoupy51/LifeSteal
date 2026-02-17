
# Imports
from beet import Context
from stewbeet import write_load_file, write_tick_file


# Setup the load.mcfunction file with scoreboard objectives and default values
def setup_load_file(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_load_file(f"""
scoreboard objectives add {ns}.kill playerKillCount
scoreboard objectives add {ns}.death deathCount
scoreboard objectives add {ns}.withdraw trigger
scoreboard objectives add {ns}.hearts dummy

scoreboard players set #2 {ns}.data 2

execute unless score MAX_HEARTS {ns}.data matches 1.. run scoreboard players set MAX_HEARTS {ns}.data 20
execute unless score MAX_HEARTS_BY_CONSUMING {ns}.data matches 0.. run scoreboard players set MAX_HEARTS_BY_CONSUMING {ns}.data 20
execute unless score MIN_HEARTS {ns}.data matches 0.. run scoreboard players set MIN_HEARTS {ns}.data 0
execute unless score REVIVED_HEARTS {ns}.data matches 1.. run scoreboard players set REVIVED_HEARTS {ns}.data 4
execute unless score NATURAL_DEATH_HEART_LOSE {ns}.data matches 0..1 run scoreboard players set NATURAL_DEATH_HEART_LOSE {ns}.data 1
execute unless score NATURAL_DEATH_HEART_DROP {ns}.data matches 0..1 run scoreboard players set NATURAL_DEATH_HEART_DROP {ns}.data 1
execute unless score USE_HALF_HEARTS {ns}.data matches 0..1 run scoreboard players set USE_HALF_HEARTS {ns}.data 0
execute unless score USE_HALF_HEARTS_PREV {ns}.data matches 0..1 run scoreboard players operation USE_HALF_HEARTS_PREV {ns}.data = USE_HALF_HEARTS {ns}.data
execute unless score BAN_REACHING_MIN_HEARTS {ns}.data matches 0..1 run scoreboard players set BAN_REACHING_MIN_HEARTS {ns}.data 1
execute unless score STEAL_ON_KILL {ns}.data matches 0..1 run scoreboard players set STEAL_ON_KILL {ns}.data 1
execute unless score INSTANTLY_CONSUME_HEARTS {ns}.data matches 0..1 run scoreboard players set INSTANTLY_CONSUME_HEARTS {ns}.data 0
execute unless score NO_HEART_DROP_OR_STEAL {ns}.data matches 0..1 run scoreboard players set NO_HEART_DROP_OR_STEAL {ns}.data 0
execute unless score SPECTATOR_INSTEAD {ns}.data matches 0..1 run scoreboard players set SPECTATOR_INSTEAD {ns}.data 0
execute unless score LAST_CHANCE {ns}.data matches 0..1 run scoreboard players set LAST_CHANCE {ns}.data 0
""", prepend = True)


# Setup the tick.mcfunction file with main game loop logic
def setup_tick_file(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_tick_file(f"""
# Check for USE_HALF_HEARTS configuration change
execute unless score USE_HALF_HEARTS {ns}.data = USE_HALF_HEARTS_PREV {ns}.data run function {ns}:config/half_hearts_changed

execute as @a[sort=random,scores={{{ns}.death=1..}}] run function {ns}:player/tick
execute as @a[sort=random] run function {ns}:player/tick
""")

