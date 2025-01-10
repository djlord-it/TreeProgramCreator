import os
import logging
from datetime import datetime

def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), ".directory_creator")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 
        f"directory_creator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)
