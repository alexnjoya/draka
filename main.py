#!/usr/bin/env python3
"""
Student Result Management CLI Tool
A command-line application for managing student results with PostgreSQL database
"""

import os
import sys
from database.operations import StudentResultsDB
from utils.file_handler import read_student_data, write_summary_report, create_sample_data
from utils.grade_calculator import validate_score, get_grade_description

def print_banner():
    """Print application banner"""
    print("\n" + "="*60)
    print("          STUDENT RESULT MANAGEMENT SYSTEM")
    print("="*60)

def print_menu():
    """Print main menu options"""
    print("\n" + "-"*40)
    print("MAIN MENU")
    print("-"*40)
    print("1. View all records")
    print("2. View student by index number")
    print("3. Update student score")
    print("4. Export summary report to file")
    print("5. Load data from file")
    print("6. Exit")
    print("-"*40)

def view_all_records(db):
    """Display all student records"""
    print("\n" + "="*80)
    print("ALL STUDENT RECORDS")
    print("="*80)
    
    students = db.get_all_students()
    
    if not students:
        print("No student records found.")
        return
    
    print(f"{'ID':<4} {'Index':<8} {'Name':<20} {'Course':<15} {'Score':<6} {'Grade':<6}")
    print("-" * 80)
    
    for student in students:
        print(f"{student['id']:<4} {student['index_number']:<8} {student['full_name']:<20} "
              f"{student['course']:<15} {student['score']:<6} {student['grade']:<6}")
    
    print(f"\nTotal students: {len(students)}")

def view_student_by_index(db):
    """Display student by index number"""
    print("\n" + "="*50)
    print("SEARCH STUDENT BY INDEX NUMBER")
    print("="*50)
    
    index_number = input("Enter student index number: ").strip()
    
    if not index_number:
        print("✗ Index number cannot be empty.")
        return
    
    student = db.get_student_by_index(index_number)
    
    if student:
        print(f"\nStudent Found:")
        print(f"ID: {student['id']}")
        print(f"Index Number: {student['index_number']}")
        print(f"Full Name: {student['full_name']}")
        print(f"Course: {student['course']}")
        print(f"Score: {student['score']}")
        print(f"Grade: {student['grade']} - {get_grade_description(student['grade'])}")
    else:
        print(f"✗ No student found with index number: {index_number}")

def update_student_score(db):
    """Update student score"""
    print("\n" + "="*50)
    print("UPDATE STUDENT SCORE")
    print("="*50)
    
    index_number = input("Enter student index number: ").strip()
    
    if not index_number:
        print("✗ Index number cannot be empty.")
        return
    
    # Check if student exists
    if not db.student_exists(index_number):
        print(f"✗ No student found with index number: {index_number}")
        return
    
    # Display current student info
    student = db.get_student_by_index(index_number)
    print(f"\nCurrent student information:")
    print(f"Name: {student['full_name']}")
    print(f"Course: {student['course']}")
    print(f"Current Score: {student['score']}")
    print(f"Current Grade: {student['grade']}")
    
    # Get new score
    new_score_input = input("\nEnter new score (0-100): ").strip()
    
    if not validate_score(new_score_input):
        print("✗ Invalid score. Please enter a number between 0 and 100.")
        return
    
    new_score = int(new_score_input)
    
    # Confirm update
    confirm = input(f"Are you sure you want to update the score to {new_score}? (y/n): ").strip().lower()
    
    if confirm == 'y':
        if db.update_student_score(index_number, new_score):
            print("✓ Student score updated successfully!")
            
            # Show updated information
            updated_student = db.get_student_by_index(index_number)
            print(f"New Score: {updated_student['score']}")
            print(f"New Grade: {updated_student['grade']} - {get_grade_description(updated_student['grade'])}")
        else:
            print("✗ Failed to update student score.")
    else:
        print("Update cancelled.")

def export_summary_report(db):
    """Export summary report to file"""
    print("\n" + "="*50)
    print("EXPORT SUMMARY REPORT")
    print("="*50)
    
    total_students = db.get_total_students()
    grade_distribution = db.get_grade_distribution()
    
    if total_students == 0:
        print("✗ No student records found. Cannot generate report.")
        return
    
    # Display summary before saving
    print(f"\nSummary:")
    print(f"Total Students: {total_students}")
    print("\nGrade Distribution:")
    
    grade_counts = {item['grade']: item['count'] for item in grade_distribution}
    for grade in ['A', 'B', 'C', 'D', 'F']:
        count = grade_counts.get(grade, 0)
        print(f"{grade}: {count}")
    
    # Save to file
    report_path = write_summary_report(total_students, grade_distribution)
    
    if report_path:
        print(f"\n✓ Summary report exported successfully!")
        print(f"Report saved to: {report_path}")
    else:
        print("✗ Failed to export summary report.")

def load_data_from_file(db):
    """Load student data from file"""
    print("\n" + "="*50)
    print("LOAD DATA FROM FILE")
    print("="*50)
    
    print("Available options:")
    print("1. Load from sample data (data/sample_students.csv)")
    print("2. Load from custom file")
    print("3. Create sample data file")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        file_path = 'data/sample_students.csv'
        if not os.path.exists(file_path):
            print("✗ Sample data file not found. Creating it first...")
            create_sample_data()
    elif choice == '2':
        file_path = input("Enter file path: ").strip()
        if not file_path:
            print("✗ File path cannot be empty.")
            return
    elif choice == '3':
        create_sample_data()
        return
    else:
        print("✗ Invalid choice.")
        return
    
    # Read data from file
    students = read_student_data(file_path)
    
    if not students:
        print("✗ No valid student data found in file.")
        return
    
    # Insert students into database
    success_count = 0
    duplicate_count = 0
    error_count = 0
    
    for student in students:
        try:
            # Check if student already exists
            if db.student_exists(student['index_number']):
                print(f"Student {student['index_number']} already exists. Skipping...")
                duplicate_count += 1
                continue
            
            # Insert student
            if db.insert_student(
                student['index_number'],
                student['full_name'],
                student['course'],
                student['score']
            ):
                success_count += 1
            else:
                error_count += 1
                
        except Exception as e:
            print(f"✗ Error inserting student {student.get('index_number', 'Unknown')}: {e}")
            error_count += 1
    
    print(f"\n✓ Data loading completed!")
    print(f"Successfully inserted: {success_count}")
    print(f"Duplicates skipped: {duplicate_count}")
    print(f"Errors encountered: {error_count}")

def main():
    """Main application function"""
    print_banner()
    
    # Initialize database connection
    db = StudentResultsDB()
    
    if not db.connect():
        print("✗ Failed to connect to database. Please check your configuration.")
        return
    
    print("✓ Application initialized successfully!")
    
    try:
        while True:
            print_menu()
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                view_all_records(db)
            elif choice == '2':
                view_student_by_index(db)
            elif choice == '3':
                update_student_score(db)
            elif choice == '4':
                export_summary_report(db)
            elif choice == '5':
                load_data_from_file(db)
            elif choice == '6':
                print("\n✓ Thank you for using Student Result Management System!")
                break
            else:
                print("✗ Invalid choice. Please select 1-6.")
            
            # Wait for user input before showing menu again
            input("\nPress Enter to continue...")
    
    except KeyboardInterrupt:
        print("\n\n✓ Application terminated by user.")
    
    finally:
        db.close()

if __name__ == "__main__":
    main()