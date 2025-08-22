import os
import logging.config
from app.config.app_setting import Setting
from app.config.app_config import Config
from pathlib import Path


app_logging_config = {
    'version': 1,
    'loggers': {
        '': {  # root logger
            'level': 'NOTSET',
            'handlers': ['console', 'info_file_handler', 'error_file_handler'],
        },
        'uvicorn.access': {  # uvicorn default access logger
            'level': 'NOTSET',
            'handlers': ['console', 'info_file_handler'],
        },
        'uvicorn.error': {  # uvicorn default error logger
            'level': 'NOTSET',
            'handlers': ['console', 'error_file_handler'],
        },
    },
    'handlers': {
        'console': {
            'level': Config.LOG_LEVEL,
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'info_file_handler': {
            'level': Config.LOG_LEVEL,
            'formatter': 'info',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{Config.LOG_DIR}/info.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'error_file_handler': {
            'level': 'WARNING',
            'formatter': 'error',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{Config.LOG_DIR}/error.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        }
    },
    'formatters': {
        'info': {
            'format': '%(asctime)s-%(module)s-%(lineno)s::%(levelname)s:: %(message)s'
        },
        'error': {
            'format': '%(asctime)s-%(module)s-%(lineno)s::%(levelname)s:: %(message)s'
        },
    },
}

def configure_logging():
    log_dir = Path(f'{Setting.PROJECT_ROOT}/{Config.LOG_DIR}')
    log_dir.mkdir(exist_ok=True)
    logging.config.dictConfig(app_logging_config)
