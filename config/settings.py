import os
from pathlib import Path
from .env_manager import EnvironmentManager

# Initialize environment manager
env_manager = EnvironmentManager()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
CACHE_DIR = DATA_DIR / 'cache'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# Database settings
ASTRA_DB_CONFIG = env_manager.get_db_config()

# Vector DB settings (Milvus)
MILVUS_CONFIG = env_manager.get_milvus_config()

# NeMo settings
NEMO_CONFIG = env_manager.get_nemo_config()

# Security settings
SECURITY_CONFIG = env_manager.get_security_config()

# API settings
API_CONFIG = env_manager.get_api_config()

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': DATA_DIR / 'agent_system.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
} 