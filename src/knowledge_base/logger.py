import logging
import sys
import yaml
from knowledge_base.utils.config_reader import ConfigReader 
from knowledge_base.utils import constants 
# logger.py

def setup_logger(name=constants.APP_NAME, config_path=constants.CONFIG_YMAL_PATH):
    # Load log level from config.yaml
    try:
        config = ConfigReader(constants.CONFIG_YMAL_PATH)   
        level_str = config[constants.LOGGING][constants.LEVEL]
        level = getattr(logging, level_str, logging.INFO)

        log_path_str = config[constants.LOGGING][constants.PATH]
        log_path = getattr(logging, log_path_str, constants.DEFAULT_LOG_PATH)

    except Exception as e:
        print(f"Failed to load logging config: {e}")
        level = logging.INFO
        log_path =  constants.DEFAULT_LOG_PATH


    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)


    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)
 # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

   
    if logger.hasHandlers():
        return logger  # Prevent duplicate handlers

    return logger

logger = setup_logger(constants.APP_NAME,constants.CONFIG_YMAL_PATH)



