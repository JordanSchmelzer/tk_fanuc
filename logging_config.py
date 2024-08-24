import logging
from logging.handlers import RotatingFileHandler


def configure_logging(log_file_path):
    NUMBER_OF_LOG_FILES_TO_KEEP = 5
    MAX_LOG_BYTES = 5 * 1024 * 1024 # 5mb

    # Create a logger with a unique name
    logger = logging.getLogger(log_file_path)
   
    # Configure logger to log messages of certain level and above
    logger.setLevel(logging.DEBUG)
   
    # Define a basic formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')    

    # Define a handler ot specify where to log the messages
    handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_BYTES, backupCount=NUMBER_OF_LOG_FILES_TO_KEEP)
    handler.setLevel(logging.DEBUG)    
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
