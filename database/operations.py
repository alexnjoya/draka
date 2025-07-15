from database.connection import DatabaseConnection
from utils.grade_calculator import calculate_grade

class StudentResultsDB:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def connect(self):
        """Connect to database and create table if needed"""
        if self.db.connect():
            return self.db.create_table()
        return False
    
    def close(self):
        """Close database connection"""
        self.db.close()
    
    def insert_student(self, index_number, full_name, course, score):
        """Insert a new student record"""
        grade = calculate_grade(score)
        query = """
        INSERT INTO student_results (index_number, full_name, course, score, grade)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (index_number, full_name, course, score, grade)
        return self.db.execute_update(query, params)
    
    def get_all_students(self):
        """Retrieve all student records"""
        query = "SELECT * FROM student_results ORDER BY full_name"
        return self.db.execute_query(query)
    
    def get_student_by_index(self, index_number):
        """Retrieve a student by index number"""
        query = "SELECT * FROM student_results WHERE index_number = %s"
        result = self.db.execute_query(query, (index_number,))
        return result[0] if result else None
    
    def update_student_score(self, index_number, new_score):
        """Update a student's score and recalculate grade"""
        new_grade = calculate_grade(new_score)
        query = """
        UPDATE student_results 
        SET score = %s, grade = %s 
        WHERE index_number = %s
        """
        params = (new_score, new_grade, index_number)
        return self.db.execute_update(query, params)
    
    def get_grade_distribution(self):
        """Get count of students by grade"""
        query = """
        SELECT grade, COUNT(*) as count 
        FROM student_results 
        GROUP BY grade 
        ORDER BY grade
        """
        return self.db.execute_query(query)
    
    def get_total_students(self):
        """Get total number of students"""
        query = "SELECT COUNT(*) as total FROM student_results"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def student_exists(self, index_number):
        """Check if student with given index number exists"""
        query = "SELECT COUNT(*) as count FROM student_results WHERE index_number = %s"
        result = self.db.execute_query(query, (index_number,))
        return result[0]['count'] > 0 if result else False
    
    def clear_all_records(self):
        """Clear all student records (for testing purposes)"""
        query = "DELETE FROM student_results"
        return self.db.execute_update(query)