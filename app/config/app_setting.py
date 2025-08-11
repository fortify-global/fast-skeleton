import os

class Setting:
    MAX_RETRY = 3
    # Project directories
    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(SRC_DIR)


    