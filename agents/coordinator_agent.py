from typing import Dict, Optional
import logging
import json
from datetime import datetime

class TaskCoordinator:
    """Coordinates workflow between agents and manages task progression."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.task_history = []
        
    def reassign_task(self, generator_agent, errors: list) -> None:
        """
        Reassign task to code generator with error context.
        
        Args:
            generator_agent: The code generator agent
            errors: List of errors from validation
        """
        try:
            # Log the reassignment
            self.task_history.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'reassign',
                'errors': errors
            })
            
            self.logger.info(f"Reassigning task due to errors: {errors}")
            
            # In a real implementation, this would include logic to:
            # 1. Analyze errors and determine required changes
            # 2. Update requirements based on validation feedback
            # 3. Trigger code regeneration with updated context
            
        except Exception as e:
            self.logger.error(f"Error in task reassignment: {str(e)}")
            raise

    def provide_feedback(self, code_package: Dict) -> None:
        """
        Provide feedback and documentation for the generated code.
        
        Args:
            code_package: Dict containing generated code and metadata
        """
        try:
            # Generate documentation
            docs = self._generate_documentation(code_package)
            
            # Log successful completion
            self.task_history.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'complete',
                'framework': code_package.get('framework'),
                'type': code_package.get('type')
            })
            
            # Output results
            print("\n=== Generated Code Documentation ===")
            print(docs)
            print("\n=== Generated Code ===")
            print(code_package['code'])
            
        except Exception as e:
            self.logger.error(f"Error providing feedback: {str(e)}")
            raise

    def _generate_documentation(self, code_package: Dict) -> str:
        """Generate documentation for the code package."""
        docs = []
        docs.append("# Generated Application Documentation")
        docs.append(f"\n## Framework: {code_package.get('framework', 'unknown')}")
        docs.append(f"\n## Application Type: {code_package.get('type', 'unknown')}")
        
        # Add dependencies section
        docs.append("\n## Dependencies")
        for dep in code_package.get('dependencies', {}).get('requirements', []):
            docs.append(f"- {dep}")
        
        # Add setup instructions
        docs.append("\n## Setup Instructions")
        docs.append("1. Create a virtual environment")
        docs.append("2. Install dependencies: `pip install -r requirements.txt`")
        docs.append("3. Run the application: `python app.py`")
        
        return "\n".join(docs)

    def get_task_history(self) -> list:
        """Return the task execution history."""
        return self.task_history 