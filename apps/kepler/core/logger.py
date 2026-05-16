import logging
import sys
from logging.handlers import RotatingFileHandler

def get_logger(name="Kepler"):
    """
    Configures and returns a logger instance with dual handlers.
    
    Args:
        name (str): The name of the logger instance. Defaults to "Kepler".
        
    Returns:
        logging.Logger: A logger configured with both a RotatingFileHandler 
                        (level INFO) and a StreamHandler (level DEBUG).
    """
    import os
    import config.settings as settings

    # Ensure log directory exists
    os.makedirs(os.path.dirname(settings.SYSTEM_LOG), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) 

    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', 
                                  datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = RotatingFileHandler(settings.SYSTEM_LOG, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG) 

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger