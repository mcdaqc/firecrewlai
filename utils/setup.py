import os
from pathlib import Path
import shutil

def setup_project_structure():
    """Create necessary project directories and initialize the environment."""
    base_dir = Path(__file__).parent.parent
    
    # Define project structure
    directories = [
        'agents',                    # Agent modules
        'config',                    # Configuration files
        'data/cache',               # Cache directory
        'data/logs',                # Log files
        'examples/templates',        # Code templates
        'examples/docker',          # Docker configurations
        'generated/web_apps',       # Generated web applications
        'generated/apis',           # Generated APIs
        'generated/crawlers',       # Generated web crawlers
        'generated/tests',          # Generated tests
        'tests',                    # Project tests
        'utils'                     # Utility modules
    ]
    
    # Create directories
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep to track empty directories
        if not any(dir_path.iterdir()):
            (dir_path / '.gitkeep').touch()
    
    # Initialize .gitignore if it doesn't exist
    gitignore_path = base_dir.parent / '.gitignore'
    if not gitignore_path.exists():
        _create_gitignore(gitignore_path)
    
    print("Project structure created successfully!")
    print("Don't forget to:")
    print("1. Configure your .env file")
    print("2. Install required dependencies")
    print("3. Set up your API keys for Firecrawl and NeMo")

def _create_gitignore(path: Path):
    """Create a .gitignore file with common Python patterns."""
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/

# Project specific
generated/
data/cache/
*.log
.env

# Docker
.docker/
"""
    path.write_text(gitignore_content)

if __name__ == "__main__":
    setup_project_structure() 