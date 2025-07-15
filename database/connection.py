import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DB_CONFIG

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("✓ Database connection established successfully")
            return True
        except psycopg2.Error as e:
            print(f"✗ Error connecting to database: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("✓ Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"✗ Error executing query: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """Execute an update/insert query"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except psycopg2.Error as e:
            print(f"✗ Error executing update: {e}")
            self.connection.rollback()
            return False
    
    def create_table(self):
        """Create the student_results table if it doesn't exist"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS student_results (
            id SERIAL PRIMARY KEY,
            index_number VARCHAR(10) NOT NULL,
            full_name TEXT NOT NULL,
            course TEXT NOT NULL,
            score INTEGER NOT NULL,
            grade CHAR(1)
        );
        """
        return self.execute_update(create_table_query)