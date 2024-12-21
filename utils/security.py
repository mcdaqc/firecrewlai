from typing import Dict, List
import docker
import os
import subprocess
from pathlib import Path
import tempfile
import json
import bandit
from safety.safety import check as safety_check

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
        """Run comprehensive security scan."""
        results = {
            'vulnerabilities': [],
            'security_score': 1.0,
            'dependency_issues': [],
            'code_issues': []
        }
        
        # Run security checks
        self._check_dependencies(code_package, results)
        self._run_bandit_scan(code_package['code'], results)
        self._check_docker_security(results)
        
        return results
    
    def _run_bandit_scan(self, code: str, results: Dict) -> None:
        """Run Bandit security scanner on code."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as temp_file:
                temp_file.write(code)
                temp_file.flush()
                
                # Run Bandit scan
                cmd = f"bandit -r {temp_file.name} -f json"
                output = subprocess.check_output(cmd, shell=True)
                scan_results = json.loads(output)
                
                # Process results
                for issue in scan_results['results']:
                    results['code_issues'].append({
                        'severity': issue['issue_severity'],
                        'confidence': issue['issue_confidence'],
                        'description': issue['issue_text']
                    })
        except Exception as e:
            results['vulnerabilities'].append(f"Bandit scan failed: {str(e)}")
    
    def _check_docker_security(self, results: Dict) -> None:
        """Check Docker configuration security."""
        security_checks = [
            ('User directive', self._check_docker_user),
            ('Resource limits', self._check_resource_limits),
            ('Security options', self._check_security_opts)
        ]
        
        for check_name, check_func in security_checks:
            try:
                check_func(results)
            except Exception as e:
                results['vulnerabilities'].append(
                    f"Docker security check '{check_name}' failed: {str(e)}"
                )
    
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