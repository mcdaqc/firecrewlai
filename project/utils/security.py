from typing import Dict
import docker
import os
import subprocess
from pathlib import Path

class SecurityManager:
    """Manages security aspects of code execution and validation."""
    
    def __init__(self):
        self.docker_client = docker.from_env()
        
    def create_secure_environment(self, code_package: Dict) -> Path:
        """Create a secure environment for code execution."""
        # Create isolated directory
        env_path = Path('/tmp/secure_env')
        env_path.mkdir(exist_ok=True)
        
        # Set up environment
        self._setup_environment(env_path, code_package)
        
        return env_path
        
    def run_security_scan(self, code_package: Dict) -> Dict:
        """Run security scan on the code."""
        results = {
            'vulnerabilities': [],
            'security_score': 1.0
        }
        
        # Run various security checks
        self._check_dependencies(code_package, results)
        self._scan_for_vulnerabilities(code_package, results)
        self._check_permissions(code_package, results)
        
        return results
        
    def _setup_environment(self, env_path: Path, code_package: Dict) -> None:
        """Set up secure environment with necessary restrictions."""
        # Create necessary files
        (env_path / 'code').mkdir(exist_ok=True)
        (env_path / 'data').mkdir(exist_ok=True)
        
        # Set up Docker volume mounts
        self.volume_config = {
            str(env_path / 'code'): {'bind': '/app/code', 'mode': 'ro'},
            str(env_path / 'data'): {'bind': '/app/data', 'mode': 'rw'}
        }
        
    def _check_dependencies(self, code_package: Dict, results: Dict) -> None:
        """Check dependencies for known vulnerabilities."""
        try:
            # Run safety check on dependencies
            deps = code_package.get('dependencies', {}).get('requirements', [])
            for dep in deps:
                process = subprocess.run(
                    ['safety', 'check', dep],
                    capture_output=True,
                    text=True
                )
                if process.returncode != 0:
                    results['vulnerabilities'].append(
                        f"Vulnerability found in {dep}: {process.stdout}"
                    )
                    results['security_score'] *= 0.8
        except Exception as e:
            results['vulnerabilities'].append(f"Dependency check failed: {str(e)}")
            results['security_score'] *= 0.7
            
    def _scan_for_vulnerabilities(self, code_package: Dict, results: Dict) -> None:
        """Scan code for potential security vulnerabilities."""
        dangerous_patterns = [
            'eval(',
            'exec(',
            'os.system(',
            '__import__(',
            'subprocess.call(',
            'input(',
            'pickle.loads('
        ]
        
        code = code_package.get('code', '')
        for pattern in dangerous_patterns:
            if pattern in code:
                results['vulnerabilities'].append(
                    f"Potentially dangerous function used: {pattern}"
                )
                results['security_score'] *= 0.9
                
    def _check_permissions(self, code_package: Dict, results: Dict) -> None:
        """Check for excessive permission requirements."""
        sensitive_operations = [
            'os.chmod(',
            'os.access(',
            'os.chown(',
            'open(',
            'file.',
            'socket.'
        ]
        
        code = code_package.get('code', '')
        for op in sensitive_operations:
            if op in code:
                results['vulnerabilities'].append(
                    f"Sensitive operation detected: {op}"
                )
                results['security_score'] *= 0.95 