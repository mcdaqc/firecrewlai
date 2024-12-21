import os
from pathlib import Path
import shutil

def setup_project_structure():
    """Create necessary project directories and initialize the environment."""
    base_dir = Path(__file__).parent.parent
    
    # Define project structure
    directories = [
        'generated/web_apps',      # For generated web applications
        'generated/apis',          # For generated APIs
        'generated/crawlers',      # For generated web crawlers
        'generated/tests',         # For generated tests
        'data/cache',             # For temporary data
        'data/logs',              # For system logs
        'examples/templates',      # Code templates
        'examples/generated_app',  # Example applications
        'config'                  # Configuration files
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