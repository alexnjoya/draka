#!/usr/bin/env python3
"""
Setup script for Student Result Management System
This script helps with initial database setup and configuration
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from config.settings import DB_CONFIG

def create_database():
    """Create the database if it doesn't exist"""
    print("Setting up database...")
    
    # Connect to PostgreSQL server (not to specific database)
    temp_config = DB_CONFIG.copy()
    db_name = temp_config.pop('database')
    
    try:
        # Connect to default postgres database
        temp_config['database'] = 'postgres'
        conn = psycopg2.connect(**temp_config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if cursor.fetchone():
            print(f"✓ Database '{db_name}' already exists")
        else:
            # Create database
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"✓ Database '{db_name}' created successfully")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"✗ Error setting up database: {e}")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'data/reports',
        'config',
        'database',
        'utils'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory created/verified: {directory}")

def create_init_files():
    """Create __init__.py files for Python packages"""
    init_files = [
        'config/__init__.py',
        'database/__init__.py',
        'utils/__init__.py'
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# This file makes the directory a Python package\n')
            print(f"✓ Created: {init_file}")

def test_database_connection():
    """Test database connection"""
    try:
        from database.connection import DatabaseConnection
        db = DatabaseConnection()
        if db.connect():
            print("✓ Database connection test successful")
            db.create_table()
            print("✓ Student results table created/verified")
            db.close()
            return True
        else:
            print("✗ Database connection test failed")
            return False
    except Exception as e:
        print(f"✗ Database connection test error: {e}")
        return False

def main():
    """Main setup function"""
    print("="*60)
    print("    STUDENT RESULT MANAGEMENT SYSTEM - SETUP")
    print("="*60)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Creating __init__.py files...")
    create_init_files()
    
    print("\n3. Setting up database...")
    if not create_database():
        print("✗ Database setup failed. Please check your PostgreSQL installation and config/settings.py")
        return
    
    print("\n4. Testing database connection...")
    if test_database_connection():
        print("\n✓ Setup completed successfully!")
        print("You can now run the application with: python main.py")
    else:
        print("\n✗ Setup completed with errors.")
        print("Please check your database configuration in config/settings.py")

if __name__ == "__main__":
    main()