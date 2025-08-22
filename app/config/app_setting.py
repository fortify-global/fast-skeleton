import os
from app import PROJECT_ROOT


class Setting:
    MAX_RETRY = 3
    # Project directories
    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = PROJECT_ROOT
    SENSITIVE_PATTERNS = [
    'password', 'passwd', 'pwd', 'secret', 'token', 'key',
    'credential', 'auth', 'authorization', 'cookie', 'session',
    'private_key', 'api_key', 'access_token', 'refresh_token',
    'ssn', 'credit_card', 'bank_account', 'pin'
]


    