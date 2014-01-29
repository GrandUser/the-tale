# coding: utf-8
import datetime

from dext.utils.app_settings import app_settings

from the_tale.game.balance import constants as c

heroes_settings = app_settings('HEROES',
                               USE_ABILITY_CHANCE=0.1,
                               MESSAGES_LOG_LENGTH=10,
                               DIARY_LOG_LENGTH=20,

                               UI_CACHING_KEY='hero_ui_%d',
                               UI_CACHING_TIME=10*60, # not cache livetime, but time period after setupped ui_caching_started_at in which ui_caching is turned on
                               UI_CACHING_CONTINUE_TIME=60, # time before caching end, when we send next cache command
                               UI_CACHING_TIMEOUT=15*60, # cache livetime

                               DUMP_CACHED_HEROES=False, # should we dump cached heroes to database

                               ABILITIES_RESET_TIMEOUT=datetime.timedelta(days=30),
                               PLACE_HELP_HISTORY_SIZE=200,
                               UNLOAD_TIMEOUT=c.TURN_DELTA * 3,
                               RARE_OPERATIONS_INTERVAL=100)
