#!/usr/bin/env python3
"""
Enhanced Student Result Management System
A comprehensive CLI application with role-based access control
"""

import os
import sys
from database.operations import StudentResultsDB
from utils.auth_manager import AuthManager
from utils.admin_menu import AdminMenu
from utils.staff_menu import StaffMenu
from utils.student_menu import StudentMenu

def print_banner():
    """Print application banner"""
    print("\n" + "="*80)
    print("          ENHANCED STUDENT RESULT MANAGEMENT SYSTEM")
    print("="*80)
    print("Features:")
    print("• Role-based access control (Admin, Staff, Student)")
    print("• Course enrollment management")
    print("• GPA calculation and academic tracking")
    print("• Comprehensive reporting system")
    print("="*80)

def setup_initial_admin(db):
    """Setup initial admin user if none exists"""
    admin_check_query = "SELECT COUNT(*) as count FROM users WHERE user_type = 'admin'"
    result = db.db.execute_query(admin_check_query)
    
    if result and result[0]['count'] == 0:
        print("\n" + "="*50)
        print("INITIAL SETUP")
        print("="*50)
        print("No admin user found. Creating initial admin account...")
        
        email = input("Admin Email: ").strip()
        password = input("Admin Password: ").strip()
        full_name = input("Admin Full Name: ").strip()
        
        if email and password and full_name:
            if db.create_admin(email, password, full_name):
                print("✓ Initial admin account created successfully!")
                print("You can now login with these credentials.")
            else:
                print("✗ Failed to create admin account.")
        else:
            print("✗ All fields are required for admin setup.")

def main():
    """Main application function"""
    print_banner()
    
    # Initialize database connection
    db = StudentResultsDB()
    if not db.connect():
        print("✗ Failed to connect to database. Please check your configuration.")
        return
    
    # Setup initial admin if needed
    setup_initial_admin(db)
    
    # Initialize authentication manager
    auth_manager = AuthManager(db)
    
    print("\n" + "="*50)
    print("WELCOME TO STUDENT RESULT MANAGEMENT SYSTEM")
    print("="*50)
    
    while True:
        # Handle login
        if not auth_manager.login():
            print("Goodbye!")
            break
        
        # Route to appropriate menu based on user type
        user_type = auth_manager.get_user_type()
        
        if auth_manager.is_admin():
            admin_menu = AdminMenu(db, auth_manager)
            if not admin_menu.show_menu():
                print("Goodbye!")
                break
        elif auth_manager.is_staff():
            staff_menu = StaffMenu(db, auth_manager)
            if not staff_menu.show_menu():
                print("Goodbye!")
                break
        elif auth_manager.is_student():
            student_menu = StudentMenu(db, auth_manager)
            if not student_menu.show_menu():
                print("Goodbye!")
                break
        else:
            print("✗ Unknown user type. Please contact administrator.")
            auth_manager.logout()
    
    # Close database connection
    db.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
        print("Please check your database configuration and try again.") 