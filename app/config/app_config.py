"""
This module is used to load the configuration for the application.
It uses the dotenv module to load the configuration from the .env file.
It will either set the configuration from the .env file or from the environment variables or 
default values if not found.

"""

import os
from dotenv import load_dotenv

load_dotenv(override=False)


class Config:
    APP_NAME = os.getenv('APP_NAME', 'SKELETON')

    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEVELOPMENT')
    REGION = os.getenv('REGION', 'LOC')
    LANGUAGE = os.getenv('APP_LANGUAGE', 'EN')

    # Log
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
