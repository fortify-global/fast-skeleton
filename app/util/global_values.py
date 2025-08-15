import traceback
import sys

def get_main_error():
    exc_type, exc_value, _ = sys.exc_info()
    main_error = "".join(traceback.format_exception_only(exc_type, exc_value)).strip()
    return main_error

def get_complete_traceback():
    return traceback.format_exc()

