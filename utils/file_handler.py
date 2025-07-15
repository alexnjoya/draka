import csv
import os
from datetime import datetime

def read_student_data(file_path):
    """
    Read student data from CSV or TXT file
    
    Args:
        file_path (str): Path to the data file
    
    Returns:
        list: List of student records as dictionaries
    """
    students = []
    
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return students
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Try to detect if it's CSV or TXT
            if file_path.endswith('.csv'):
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    students.append({
                        'index_number': row['IndexNumber'].strip(),
                        'full_name': row['FullName'].strip(),
                        'course': row['Course'].strip(),
                        'score': int(row['Score'].strip())
                    })
            else:
                # Handle TXT file with comma-separated values
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if line:  # Skip empty lines
                        try:
                            parts = [part.strip() for part in line.split(',')]
                            if len(parts) == 4:
                                students.append({
                                    'index_number': parts[0],
                                    'full_name': parts[1],
                                    'course': parts[2],
                                    'score': int(parts[3])
                                })
                            else:
                                print(f"✗ Invalid format at line {line_num}: {line}")
                        except ValueError as e:
                            print(f"✗ Error parsing line {line_num}: {e}")
        
        print(f"✓ Successfully read {len(students)} student records from {file_path}")
        
    except Exception as e:
        print(f"✗ Error reading file {file_path}: {e}")
    
    return students

def write_summary_report(total_students, grade_distribution, output_path=None):
    """
    Write summary report to a text file
    
    Args:
        total_students (int): Total number of students
        grade_distribution (list): List of grade distribution dictionaries
        output_path (str, optional): Output file path
    
    Returns:
        str: Path to the generated report file
    """
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/reports/summary_report_{timestamp}.txt"
    
    # Create reports directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("Summary Report\n")
            file.write("==============\n\n")
            file.write(f"Total Students: {total_students}\n\n")
            file.write("Grade Distribution:\n")
            
            # Create a dictionary for easy lookup
            grade_counts = {item['grade']: item['count'] for item in grade_distribution}
            
            # Write grades in order
            for grade in ['A', 'B', 'C', 'D', 'F']:
                count = grade_counts.get(grade, 0)
                file.write(f"{grade}: {count}\n")
            
            file.write(f"\nReport generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"✓ Summary report saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"✗ Error writing report: {e}")
        return None

def create_sample_data():
    """
    Create sample student data file for testing
    """
    sample_data = [
        "STU001,John Doe,Computer Science,85",
        "STU002,Jane Smith,Mathematics,92",
        "STU003,Bob Johnson,Physics,78",
        "STU004,Alice Brown,Chemistry,67",
        "STU005,Charlie Wilson,Biology,45",
        "STU006,Diana Ross,English,88",
        "STU007,Edward Norton,History,72",
        "STU008,Fiona Green,Psychology,59",
        "STU009,George Lucas,Art,91",
        "STU010,Helen Troy,Philosophy,83"
    ]
    
    os.makedirs('data', exist_ok=True)
    
    with open('data/sample_students.csv', 'w', encoding='utf-8') as file:
        file.write("IndexNumber,FullName,Course,Score\n")
        for record in sample_data:
            file.write(record + "\n")
    
    print("✓ Sample data file created: data/sample_students.csv")