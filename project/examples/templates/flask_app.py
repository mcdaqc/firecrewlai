"""
Flask Application Template
This template is used by the generator agent to create Flask applications.
Variables in {{brackets}} will be replaced with actual values.
"""

from flask import Flask, jsonify, request
from typing import Dict, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

def load_config() -> Dict[str, Any]:
    """Load application configuration."""
    config = {
        'DEBUG': {{debug}},
        'SECRET_KEY': '{{secret_key}}',
        'ENVIRONMENT': '{{environment}}',
        'API_VERSION': '{{version}}',
        'CREATED_AT': datetime.utcnow().isoformat()
    }
    
    # Add additional configuration
    additional = {
        {{additional_config}}
    }
    config.update(additional)
    return config

# Apply configuration
app.config.update(load_config())

@app.route('/health', methods=['GET'])
def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': app.config['API_VERSION'],
        'environment': app.config['ENVIRONMENT'],
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/metrics', methods=['GET'])
def metrics() -> Dict[str, Any]:
    """Basic metrics endpoint."""
    return jsonify({
        'uptime': (datetime.utcnow() - datetime.fromisoformat(app.config['CREATED_AT'])).seconds,
        'memory_usage': '{{memory_limit}}',
        'cpu_usage': '{{cpu_limit}}'
    })

{{additional_routes}}

@app.errorhandler(Exception)
def handle_error(error: Exception) -> tuple[Dict[str, str], int]:
    """Global error handler."""
    logger.error(f"Error: {str(error)}", exc_info=True)
    return {
        'error': str(error),
        'type': error.__class__.__name__,
        'timestamp': datetime.utcnow().isoformat()
    }, 500

if __name__ == '__main__':
    app.run(
        host='{{host}}',
        port={{port}},
        debug=app.config['DEBUG']
    ) 