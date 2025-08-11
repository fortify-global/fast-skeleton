import os
import logging.config


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
            'level': os.getenv('LOG_LEVEL'),
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'info_file_handler': {
            'level': os.getenv('LOG_LEVEL'),
            'formatter': 'info',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.getenv('LOG_FILE_INFO'),
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'error_file_handler': {
            'level': 'WARNING',
            'formatter': 'error',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.getenv('LOG_FILE_ERROR'),
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
    logging.config.dictConfig(app_logging_config)
