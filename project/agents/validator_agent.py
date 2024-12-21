from typing import Dict, Optional
import docker
import tempfile
import os
from .generator_agent import CodeGenerator
from .coordinator_agent import TaskCoordinator
from ..utils.rag_manager import RAGManager
from ..utils.security import SecurityManager

class CodeValidator:
    """Validates generated code through testing and security checks."""
    
    def __init__(self):
        self.docker_client = docker.from_env()
        self.code_generator = CodeGenerator()
        self.task_coordinator = TaskCoordinator()
        self.rag_manager = RAGManager()
        self.security_manager = SecurityManager()
        
        # Define paths for code execution and Docker
        self.base_path = os.path.join(os.getcwd(), 'project', 'generated')
        self.docker_path = os.path.join(self.base_path, 'docker')
        
        # Ensure Docker directory exists
        os.makedirs(self.docker_path, exist_ok=True)

    def validate_code(self, code_package: Dict) -> Dict:
        """
        Validates the generated code through multiple checks.
        Uses RAG for context-aware validation.
        """
        try:
            results = {
                'valid': True,
                'errors': [],
                'security_issues': [],
                'performance_metrics': {}
            }
            
            # Run validation checks with RAG context
            self._validate_syntax(code_package['code'], results)
            self._run_security_checks(code_package, results)
            self._test_in_container(code_package, results)
            self._check_dependencies(code_package['dependencies'], results)
            
            # If validation failed, attempt to fix with RAG context
            if not results['valid']:
                fixed_code = self._attempt_code_fix(code_package, results)
                if fixed_code:
                    return self.validate_code(fixed_code)
            
            return results
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [str(e)],
                'security_issues': [],
                'performance_metrics': {}
            }

    def _attempt_code_fix(self, code_package: Dict, validation_results: Dict) -> Optional[Dict]:
        """Attempt to fix invalid code by regenerating with error context."""
        try:
            # Prepare error context for regeneration
            error_context = {
                'original_code': code_package,
                'validation_errors': validation_results['errors'],
                'security_issues': validation_results['security_issues']
            }
            
            # Request code regeneration through coordinator
            self.task_coordinator.reassign_task(self.code_generator, error_context)
            
            # Return None if unable to fix
            return None
            
        except Exception as e:
            print(f"Error attempting to fix code: {str(e)}")
            return None

    def _validate_syntax(self, code: str, results: Dict) -> None:
        """Validate Python syntax with RAG context."""
        try:
            compile(code, '<string>', 'exec')
            
            # Get RAG validation context
            rag_validation = self.rag_manager.validate_with_context(code)
            
            # Add RAG-based suggestions
            if rag_validation['suggestions']:
                results['rag_suggestions'] = rag_validation['suggestions']
                
        except SyntaxError as e:
            results['valid'] = False
            results['errors'].append(f"Syntax error: {str(e)}")

    def _run_security_checks(self, code_package: Dict, results: Dict) -> None:
        """Run security checks using SecurityManager."""
        security_results = self.security_manager.run_security_scan(code_package)
        results['security_issues'].extend(security_results['vulnerabilities'])
        results['security_score'] = security_results['security_score']

    def _test_in_container(self, code_package: Dict, results: Dict) -> None:
        """Run code in isolated Docker container."""
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Create test environment
                self._setup_test_environment(tmpdir, code_package)
                
                # Run tests in container
                self.docker_client.containers.run(
                    'python:3.9-slim',
                    command=['python', '-m', 'pytest'],
                    volumes={tmpdir: {'bind': '/app', 'mode': 'ro'}},
                    working_dir='/app',
                    remove=True
                )
            except docker.errors.ContainerError as e:
                results['valid'] = False
                results['errors'].append(f"Tests failed: {str(e)}")

    def _check_dependencies(self, dependencies: Dict, results: Dict) -> None:
        """Verify all required dependencies are available and compatible."""
        try:
            import pkg_resources
            
            for dep in dependencies.get('requirements', []):
                try:
                    pkg_resources.require(dep)
                except pkg_resources.DistributionNotFound:
                    results['errors'].append(f"Missing dependency: {dep}")
                except pkg_resources.VersionConflict:
                    results['errors'].append(f"Version conflict for: {dep}")
                    
        except Exception as e:
            results['errors'].append(f"Dependency check failed: {str(e)}")

    def _setup_test_environment(self, tmpdir: str, code_package: Dict) -> None:
        """Set up testing environment in temporary directory."""
        # Write code to file
        with open(os.path.join(tmpdir, 'app.py'), 'w') as f:
            f.write(code_package['code'])
            
        # Create basic test file
        test_content = f"""
import pytest
from app import app

def test_app_creates():
    assert app is not None

def test_app_configuration():
    assert app.debug is True
"""
        with open(os.path.join(tmpdir, 'test_app.py'), 'w') as f:
            f.write(test_content) 