"""
Error Handler Template
This template provides error handling and recovery mechanisms.
"""

import logging
from typing import Dict, Any, Optional, Callable
from functools import wraps
import traceback
import sys

logger = logging.getLogger(__name__)

class ErrorRecoveryManager:
    """Manages error recovery strategies."""
    
    def __init__(self):
        self.recovery_strategies: Dict[str, Callable] = {}
        self.error_history: List[Dict[str, Any]] = []
        
    def register_strategy(self, error_type: str, strategy: Callable) -> None:
        """Register a recovery strategy for an error type."""
        self.recovery_strategies[error_type] = strategy
        
    def handle_error(self, error: Exception, context: Dict[str, Any]) -> Optional[Any]:
        """Handle an error using registered strategies."""
        error_type = error.__class__.__name__
        
        # Log the error
        self.error_history.append({
            'type': error_type,
            'message': str(error),
            'traceback': traceback.format_exc(),
            'context': context
        })
        
        # Attempt recovery
        if error_type in self.recovery_strategies:
            try:
                return self.recovery_strategies[error_type](error, context)
            except Exception as recovery_error:
                logger.error(f"Recovery failed: {str(recovery_error)}")
                return None
                
        return None

def with_error_recovery(recovery_manager: ErrorRecoveryManager):
    """Decorator for functions that need error recovery."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = {
                    'function': func.__name__,
                    'args': args,
                    'kwargs': kwargs
                }
                result = recovery_manager.handle_error(e, context)
                if result is None:
                    raise
                return result
        return wrapper
    return decorator

# Example recovery strategies
def retry_strategy(max_attempts: int = 3, delay: float = 1.0):
    """Retry strategy with exponential backoff."""
    import time
    
    def _retry(error: Exception, context: Dict[str, Any]) -> Optional[Any]:
        attempts = 0
        while attempts < max_attempts:
            try:
                # Retry the function
                func = context['function']
                args = context.get('args', ())
                kwargs = context.get('kwargs', {})
                return func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                if attempts == max_attempts:
                    return None
                time.sleep(delay * (2 ** attempts))
        return None
        
    return _retry 