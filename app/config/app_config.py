"""
It will either set the configuration from the .env file or from the environment variables or 
default values if not found.

"""

import os
from dotenv import load_dotenv

if not load_dotenv(override=True):
    print('Could not find any .env file. The module will depend on system env only')
else:
    print('.env file loaded successfully')

class Config:
    APP_NAME = os.getenv('APP_NAME','')

    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', '')
    REGION = os.getenv('REGION', 'LOC')
    LANGUAGE = os.getenv('APP_LANGUAGE', 'EN')

    # Log
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DIR = os.getenv('LOG_DIR', '..')
