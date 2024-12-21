import logging
import logging.config
from pathlib import Path
from typing import Dict
import json
from datetime import datetime

class LogManager:
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging with rotating file handler."""
        log_file = self.log_dir / f"agent_system_{datetime.now():%Y%m%d}.log"
        
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'detailed'
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'detailed',
                    'filename': str(log_file),
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5
                }
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': True
                }
            }
        }
        
        logging.config.dictConfig(config) 
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance for the given name."""
        return logging.getLogger(name)