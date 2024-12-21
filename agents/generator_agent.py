from typing import Dict
import os

class CodeGenerator:
    """Generates code based on requirements and structured data."""
    
    def generate_code(self, requirements: Dict, structured_data: Dict) -> Dict:
        """
        Generate code based on requirements and structured data.
        
        Args:
            requirements: Processed user requirements
            structured_data: Processed data from NeMo
            
        Returns:
            Dict containing generated code and metadata
        """
        try:
            framework = requirements['framework_preferences']['backend']
            app_type = requirements['specifications']['type']
            
            # Generate appropriate code based on framework and type
            if framework == "flask" and app_type == "web_crawler":
                code = self._generate_flask_crawler()
            else:
                code = self._generate_basic_app(framework)
            
            return {
                "code": code,
                "framework": framework,
                "type": app_type,
                "dependencies": self._get_dependencies(framework)
            }
            
        except Exception as e:
            print(f"Error generating code: {str(e)}")
            raise

    def _generate_flask_crawler(self) -> str:
        """Generate Flask web crawler boilerplate."""
        return """
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/crawl/<path:url>')
def crawl(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = {
            'title': soup.title.string if soup.title else None,
            'links': [link.get('href') for link in soup.find_all('a')]
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
"""

    def _get_dependencies(self, framework: str) -> Dict:
        """Get required dependencies for the generated code."""
        deps = {
            "flask": ["flask", "requests", "beautifulsoup4"],
            "django": ["django", "requests"]
        }
        return {"requirements": deps.get(framework, [])} 