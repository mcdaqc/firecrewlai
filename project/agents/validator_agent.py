from typing import Dict
import docker
import tempfile
import os

class CodeValidator:
    """Validates generated code through testing and security checks."""
    
    def __init__(self):
        self.docker_client = docker.from_env()
    
    def validate_code(self, code_package: Dict) -> Dict:
        """
        Validates the generated code through multiple checks.
        
        Args:
            code_package: Dict containing code and metadata
            
        Returns:
            Dict with validation results
        """
        try:
            results = {
                'valid': True,
                'errors': [],
                'security_issues': [],
                'performance_metrics': {}
            }
            
            # Run various validation checks
            self._validate_syntax(code_package['code'], results)
            self._run_security_checks(code_package, results)
            self._test_in_container(code_package, results)
            self._check_dependencies(code_package['dependencies'], results)
            
            return results
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [str(e)],
                'security_issues': [],
                'performance_metrics': {}
            }

    def _validate_syntax(self, code: str, results: Dict) -> None:
        """Validate Python syntax."""
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            results['valid'] = False
            results['errors'].append(f"Syntax error: {str(e)}")

    def _run_security_checks(self, code_package: Dict, results: Dict) -> None:
        """Run basic security checks on the code."""
        security_patterns = [
            'eval(',
            'exec(',
            'os.system(',
            'subprocess.call('
        ]
        
        code = code_package['code']
        for pattern in security_patterns:
            if pattern in code:
                results['security_issues'].append(
                    f"Potentially unsafe function used: {pattern}"
                )

    def _test_in_container(self, code_package: Dict, results: Dict) -> None:
        """Run code in isolated Docker container."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test environment
            self._setup_test_environment(tmpdir, code_package)
            
            try:
                # Build and run container
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