from astrapy.db import AstraDB
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from pathlib import Path
import os
from typing import List, Dict
from dotenv import load_dotenv
from ..utils.logger import LogManager

class RAGManager:
    """Manages RAG operations for code generation and validation using AstraDB."""
    
    def __init__(self):
        load_dotenv()
        self.logger = LogManager(Path("data/logs")).get_logger(__name__)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize AstraDB connection
        self.astra_db = AstraDB(
            astra_db_id=os.getenv("ASTRA_DB_ID"),
            astra_db_region=os.getenv("ASTRA_DB_REGION"),
            astra_token=os.getenv("ASTRA_DB_TOKEN")
        )
        
        # Create collection for code examples
        self.collection = self.astra_db.create_collection(
            "code_examples",
            dimension=384  # Dimension of the MiniLM-L6-v2 embeddings
        )
        
        self.initialize_knowledge_base()
    
    def initialize_knowledge_base(self):
        """Initialize the knowledge base with code templates and examples."""
        templates_dir = Path(__file__).parent.parent / 'examples' / 'templates'
        
        # Load and process templates
        for template_file in templates_dir.glob('*.py'):
            loader = TextLoader(str(template_file))
            documents = loader.load()
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(documents)
            
            # Store in AstraDB
            for split in splits:
                embedding = self.embeddings.embed_query(split.page_content)
                self.collection.insert_one({
                    "content": split.page_content,
                    "metadata": {
                        "source": template_file.name,
                        "type": template_file.stem.split('_')[0]  # e.g., 'flask' from 'flask_app.py'
                    },
                    "$vector": embedding
                })
        
        self.logger.info("Knowledge base initialized successfully")
    
    def get_relevant_context(self, query: str, k: int = 3) -> List[Dict]:
        """Retrieve relevant code examples and patterns from AstraDB."""
        query_embedding = self.embeddings.embed_query(query)
        
        results = self.collection.find_many(
            {"$vector": query_embedding},
            limit=k
        )
        
        return [{
            'content': doc['content'],
            'metadata': doc['metadata'],
            'relevance': doc.get('$similarity', 0.0)  # AstraDB provides similarity scores
        } for doc in results]
    
    def validate_with_context(self, code: str) -> Dict:
        """Validate code using RAG context from AstraDB."""
        context = self.get_relevant_context(code)
        
        validation_results = {
            'suggestions': [],
            'patterns': [],
            'similar_examples': []
        }
        
        for item in context:
            if item['relevance'] > 0.8:
                validation_results['similar_examples'].append({
                    'content': item['content'],
                    'source': item['metadata']['source'],
                    'type': item['metadata']['type']
                })
        
        return validation_results