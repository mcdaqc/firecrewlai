from typing import Dict, List
import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from config.settings import ASTRA_DB_CONFIG

class AstraDBManager:
    """Manages interactions with AstraDB for storing task progress and errors."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._connect()
        self._create_tables()

    def _connect(self):
        """Establish connection to AstraDB."""
        try:
            auth_provider = PlainTextAuthProvider(
                ASTRA_DB_CONFIG['client_id'],
                ASTRA_DB_CONFIG['client_secret']
            )
            
            self.cluster = Cluster(
                cloud={
                    'secure_connect_bundle': ASTRA_DB_CONFIG['secure_connect_bundle']
                },
                auth_provider=auth_provider
            )
            
            self.session = self.cluster.connect(ASTRA_DB_CONFIG['keyspace'])
            self.logger.info("Successfully connected to AstraDB")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to AstraDB: {str(e)}")
            raise

    def _create_tables(self):
        """Create necessary tables if they don't exist."""
        try:
            # Task history table
            self.session.execute("""
                CREATE TABLE IF NOT EXISTS task_history (
                    task_id uuid PRIMARY KEY,
                    timestamp timestamp,
                    action text,
                    framework text,
                    type text,
                    errors list<text>
                )
            """)
            
            # Code artifacts table
            self.session.execute("""
                CREATE TABLE IF NOT EXISTS code_artifacts (
                    artifact_id uuid PRIMARY KEY,
                    task_id uuid,
                    code text,
                    validation_status boolean,
                    created_at timestamp
                )
            """)
            
        except Exception as e:
            self.logger.error(f"Failed to create tables: {str(e)}")
            raise

    def save_task_history(self, task_data: Dict) -> None:
        """Save task history entry."""
        try:
            query = """
                INSERT INTO task_history (
                    task_id, timestamp, action, framework, type, errors
                ) VALUES (uuid(), ?, ?, ?, ?, ?)
            """
            self.session.execute(
                query,
                (
                    task_data['timestamp'],
                    task_data['action'],
                    task_data.get('framework'),
                    task_data.get('type'),
                    task_data.get('errors', [])
                )
            )
        except Exception as e:
            self.logger.error(f"Failed to save task history: {str(e)}")
            raise

    def save_code_artifact(self, code_data: Dict) -> None:
        """Save generated code artifact."""
        try:
            query = """
                INSERT INTO code_artifacts (
                    artifact_id, task_id, code, validation_status, created_at
                ) VALUES (uuid(), uuid(), ?, ?, toTimestamp(now()))
            """
            self.session.execute(
                query,
                (
                    code_data['code'],
                    code_data['validation_status']
                )
            )
        except Exception as e:
            self.logger.error(f"Failed to save code artifact: {str(e)}")
            raise 