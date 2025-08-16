import traceback
import sys
from typing import Any
from app import logger
from app.config.app_setting import Setting

def get_main_error():
    exc_type, exc_value, _ = sys.exc_info()
    main_error = "".join(traceback.format_exception_only(exc_type, exc_value)).strip()
    return main_error

def get_complete_traceback():
    return traceback.format_exc()

def filter_sensitive_data(data: Any) -> Any:
    if isinstance(data, dict):
        filtered = {}
        for key, value in data.items():
            key_lower = key.lower()
            if any(sensitive in key_lower for sensitive in Setting.SENSITIVE_PATTERNS):
                logger.debug(f"Filtering {key}'s value from logs")
                filtered[key] = "******"
            else:
                filtered[key] = filter_sensitive_data(value)
        return filtered
    else:
        return data

