
# Imports
from beet import Context

from user.config import setup_config_functions
from user.config_display import setup_config_display
from user.initialization import setup_load_file, setup_tick_file
from user.player_ban import setup_reached_min_hearts
from user.player_core import setup_check_last_chance, setup_player_on_death, setup_player_on_kill, setup_player_tick, setup_remove_one_heart
from user.player_health import setup_update_health
from user.player_hearts import setup_consume_heart_functions, setup_drop_heart_functions, setup_withdraw_functions
from user.player_revive import setup_player_head_loot_table, setup_revive_beacon
from user.ui_messages import setup_consume_heart_messages, setup_gain_heart_messages, setup_lose_heart_messages, setup_withdraw_messages


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def beet_default(ctx: Context):

	# Setup initialization files (load.mcfunction and tick.mcfunction)
	setup_load_file(ctx)
	setup_tick_file(ctx)

	# Setup core player functions
	setup_player_tick(ctx)
	setup_player_on_kill(ctx)
	setup_player_on_death(ctx)
	setup_remove_one_heart(ctx)
	setup_check_last_chance(ctx)

	# Setup health management
	setup_update_health(ctx)

	# Setup heart management (consuming, withdrawing, dropping)
	setup_consume_heart_functions(ctx)
	setup_withdraw_functions(ctx)
	setup_drop_heart_functions(ctx)

	# Setup revive beacon functionality
	setup_revive_beacon(ctx)
	setup_player_head_loot_table(ctx)

	# Setup ban/min hearts handling
	setup_reached_min_hearts(ctx)

	# Setup configuration change handlers
	setup_config_functions(ctx)

	# Setup UI message functions
	setup_gain_heart_messages(ctx)
	setup_lose_heart_messages(ctx)
	setup_consume_heart_messages(ctx)
	setup_withdraw_messages(ctx)

	# Setup configuration display
	setup_config_display(ctx)

