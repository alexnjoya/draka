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
            # Check if connection and cursor exist
            if not self.connection or not self.cursor:
                print("✗ No database connection available")
                return None
            
            # Check if connection is in error state
            if self.connection and self.connection.closed == 0:
                # Reset any aborted transaction
                self.connection.rollback()
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"✗ Error executing query: {e}")
            # Rollback on error
            if self.connection and not self.connection.closed:
                self.connection.rollback()
            return None
    
    def execute_update(self, query, params=None):
        """Execute an update/insert query"""
        try:
            # Check if connection and cursor exist
            if not self.connection or not self.cursor:
                print("✗ No database connection available")
                return False
            
            # Check if connection is in error state
            if self.connection and self.connection.closed == 0:
                # Reset any aborted transaction
                self.connection.rollback()
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except psycopg2.Error as e:
            print(f"✗ Error executing update: {e}")
            # Rollback on error
            if self.connection and not self.connection.closed:
                self.connection.rollback()
            return False
    
    def create_table(self):
        """Create all necessary tables for the enhanced system"""
        # Only create tables if they don't exist - don't drop existing data
        tables = [
            # Users table for authentication
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                user_type VARCHAR(20) NOT NULL CHECK (user_type IN ('admin', 'staff', 'student')),
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Students table
            """
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                student_id VARCHAR(8) UNIQUE NOT NULL,
                pin VARCHAR(5) NOT NULL,
                full_name TEXT NOT NULL,
                email VARCHAR(100),
                phone VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Staff table
            """
            CREATE TABLE IF NOT EXISTS staff (
                id SERIAL PRIMARY KEY,
                staff_id VARCHAR(8) UNIQUE NOT NULL,
                pin VARCHAR(5) NOT NULL,
                full_name TEXT NOT NULL,
                email VARCHAR(100),
                department TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Courses table
            """
            CREATE TABLE IF NOT EXISTS courses (
                id SERIAL PRIMARY KEY,
                course_code VARCHAR(10) UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                credits INTEGER NOT NULL DEFAULT 3 CHECK (credits >= 1 AND credits <= 3),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            
            # Course assignments (which staff teaches which course)
            """
            CREATE TABLE IF NOT EXISTS course_assignments (
                id SERIAL PRIMARY KEY,
                staff_id INTEGER REFERENCES staff(id),
                course_id INTEGER REFERENCES courses(id),
                academic_year VARCHAR(9) NOT NULL,
                semester VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(staff_id, course_id, academic_year, semester)
            );
            """,
            
            # Enrollments (which students are enrolled in which courses)
            """
            CREATE TABLE IF NOT EXISTS enrollments (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id),
                course_id INTEGER REFERENCES courses(id),
                academic_year VARCHAR(9) NOT NULL,
                semester VARCHAR(20) NOT NULL,
                enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, course_id, academic_year, semester)
            );
            """,
            
            # Academic records (student scores and grades)
            """
            CREATE TABLE IF NOT EXISTS academic_records (
                id SERIAL PRIMARY KEY,
                student_id INTEGER REFERENCES students(id),
                course_id INTEGER REFERENCES courses(id),
                staff_id INTEGER REFERENCES staff(id),
                academic_year VARCHAR(9) NOT NULL,
                semester VARCHAR(20) NOT NULL,
                score INTEGER NOT NULL CHECK (score >= 0 AND score <= 100),
                grade CHAR(1) NOT NULL,
                gpa_points DECIMAL(3,2) NOT NULL,
                credits INTEGER NOT NULL DEFAULT 3 CHECK (credits >= 1 AND credits <= 3),
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, course_id, academic_year, semester)
            );
            """,
            
            # Legacy student_results table (for backward compatibility)
            """
            CREATE TABLE IF NOT EXISTS student_results (
                id SERIAL PRIMARY KEY,
                index_number VARCHAR(10) NOT NULL,
                full_name TEXT NOT NULL,
                course TEXT NOT NULL,
                score INTEGER NOT NULL,
                grade CHAR(1)
            );
            """
        ]
        
        for table_query in tables:
            if not self.execute_update(table_query):
                return False
        
        return True
    
    def is_connected(self):
        """Check if database connection is active"""
        try:
            if self.connection and not self.connection.closed:
                # Test the connection with a simple query
                self.cursor.execute("SELECT 1")
                return True
            return False
        except:
            return False
    
    def ensure_connection(self):
        """Ensure database connection is active, reconnect if needed"""
        if not self.is_connected():
            return self.connect()
        return True