import pytest
from agents.collector_agent import RequirementCollector
from agents.generator_agent import CodeGenerator
from agents.validator_agent import CodeValidator
from agents.coordinator_agent import TaskCoordinator
from utils.rag_manager import RAGManager

def test_requirement_collector():
    collector = RequirementCollector()
    # Mock input
    requirements = collector._process_specifications("Create a Flask web crawler")
    assert requirements['type'] == 'web_crawler'

def test_code_generator():
    generator = CodeGenerator()
    requirements = {
        'framework_preferences': {'backend': 'flask'},
        'specifications': {'type': 'web_crawler'}
    }
    structured_data = {}
    result = generator.generate_code(requirements, structured_data)
    assert 'code' in result
    assert 'flask' in result['framework']

def test_validator():
    validator = CodeValidator()
    code_package = {
        'code': 'print("Hello, World!")',
        'dependencies': {'requirements': ['pytest']}
    }
    results = validator.validate_code(code_package)
    assert isinstance(results, dict)
    assert 'valid' in results

def test_coordinator():
    coordinator = TaskCoordinator()
    code_package = {
        'code': 'print("Hello, World!")',
        'framework': 'flask',
        'type': 'web_app',
        'dependencies': {'requirements': ['flask']}
    }
    coordinator.provide_feedback(code_package)
    history = coordinator.get_task_history()
    assert len(history) > 0 

def test_rag_integration():
    validator = CodeValidator()
    rag_manager = RAGManager()
    
    code_package = {
        'code': 'print("Hello, World!")',
        'dependencies': {'requirements': ['pytest']}
    }
    
    # Validate with RAG context
    results = validator.validate_code(code_package)
    assert 'rag_suggestions' in results or 'similar_examples' in results

def test_security_integration():
    validator = CodeValidator()
    code_package = {
        'code': 'os.system("rm -rf /")',  # Código inseguro para prueba
        'dependencies': {'requirements': ['pytest']}
    }
    
    results = validator.validate_code(code_package)
    assert len(results['security_issues']) > 0