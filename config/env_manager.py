from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Dict, Any

class EnvironmentManager:
    """Manages environment variables and configuration."""
    
    def __init__(self):
        self._load_env()
        self._validate_required_vars()
        
    def _load_env(self) -> None:
        """Load environment variables from .env file."""
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        else:
            raise FileNotFoundError(
                "'.env' file not found. Please create one using the template."
            )

    def _validate_required_vars(self) -> None:
        """Validate that all required environment variables are set."""
        required_vars = [
            'ASTRA_DB_BUNDLE',
            'ASTRA_DB_CLIENT_ID',
            'ASTRA_DB_CLIENT_SECRET',
            'NEMO_API_KEY',
            'SECURITY_SECRET_KEY'
        ]
        
        missing_vars = [
            var for var in required_vars 
            if not os.getenv(var)
        ]
        
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    def get_db_config(self) -> Dict[str, Any]:
        """Get database configuration from environment."""
        return {
            'secure_connect_bundle': os.getenv('ASTRA_DB_BUNDLE'),
            'client_id': os.getenv('ASTRA_DB_CLIENT_ID'),
            'client_secret': os.getenv('ASTRA_DB_CLIENT_SECRET'),
            'keyspace': os.getenv('ASTRA_DB_KEYSPACE', 'agent_system')
        }

    def get_milvus_config(self) -> Dict[str, Any]:
        """Get Milvus configuration from environment."""
        return {
            'host': os.getenv('MILVUS_HOST', 'localhost'),
            'port': int(os.getenv('MILVUS_PORT', 19530))
        }

    def get_nemo_config(self) -> Dict[str, Any]:
        """Get NeMo configuration from environment."""
        return {
            'api_key': os.getenv('NEMO_API_KEY'),
            'model_name': 'nemo:megatron-t5',
            'precision': 'fp16',
            'device': 'cuda' if os.getenv('USE_GPU', '1') == '1' else 'cpu'
        }

    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration from environment."""
        return {
            'secret_key': os.getenv('SECURITY_SECRET_KEY'),
            'jwt_secret': os.getenv('JWT_SECRET_KEY'),
            'docker_registry': os.getenv('DOCKER_REGISTRY'),
            'docker_image_prefix': os.getenv('DOCKER_IMAGE_PREFIX')
        }

    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration from environment."""
        return {
            'host': os.getenv('API_HOST', '0.0.0.0'),
            'port': int(os.getenv('API_PORT', 8000)),
            'debug': os.getenv('DEBUG_MODE', 'True').lower() == 'true'
        } 