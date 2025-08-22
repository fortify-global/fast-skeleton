import logging
import os
from dotenv import load_dotenv

print('Configuring app')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from app.config.app_config import Config
from app.config.app_setting import Setting
from app.config import logging_config

logging_config.configure_logging()

# [MUST] Please use this logger everywhere in the application 
# from app import logger
print(f'Starting app {Config.APP_NAME}')
logger = logging.getLogger(Config.APP_NAME)

# [NOTE] f string will always get processes irespective of log level. 
# So this is not the most efficient way but it is better for readibility .
logger.debug(f"Starting app {Config.APP_NAME} in {Setting.PROJECT_ROOT}")
logger.info(f"Starting app {Config.APP_NAME} in {Setting.PROJECT_ROOT}")
logger.warning(f"Starting app {Config.APP_NAME} in {Setting.PROJECT_ROOT}")
logger.error(f"Starting app {Config.APP_NAME} in {Setting.PROJECT_ROOT}")
logger.critical(f"Starting app {Config.APP_NAME} in {Setting.PROJECT_ROOT}")
