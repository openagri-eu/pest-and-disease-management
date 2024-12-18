import logging

from core import settings

# Set to INFO
logging.basicConfig(level=logging.INFO)

def get_logger(api_path_name: str):
    if settings.LOGGING:
        return logging.getLogger(api_path_name)

    return None