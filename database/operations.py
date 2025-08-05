import hashlib
import secrets
from database.connection import DatabaseConnection
from utils.grade_calculator import calculate_grade, calculate_gpa_points

class StudentResultsDB:
    def __init__(self):
        self.db = DatabaseConnection()
        self.current_user = None
    
    def connect(self):
        """Connect to database and create table if needed"""
        try:
            if self.db.connect():
                return self.db.create_table()
            return False
        except Exception as e:
            print(f"✗ Database connection error: {e}")
            return False
    
    def reset_connection(self):
        """Reset database connection if it's in a bad state"""
        try:
            self.db.close()
            return self.db.connect()
        except Exception as e:
            print(f"✗ Failed to reset connection: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        self.db.close()
    
    # Authentication methods
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_admin(self, email, password):
        """Authenticate admin user"""
        try:
            # Ensure database connection is active
            if not self.db.ensure_connection():
                print("✗ Database connection failed")
                return False
            
            password_hash = self.hash_password(password)
            query = """
            SELECT * FROM users 
            WHERE email = %s AND password_hash = %s AND user_type = 'admin'
            """
            result = self.db.execute_query(query, (email, password_hash))
            if result and len(result) > 0:
                self.current_user = result[0]
                return True
            return False
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return False
    
    def authenticate_student(self, student_id, pin):
        """Authenticate student"""
        try:
            # Ensure database connection is active
            if not self.db.ensure_connection():
                print("✗ Database connection failed")
                return False
            
            query = """
            SELECT * FROM students 
            WHERE student_id = %s AND pin = %s
            """
            result = self.db.execute_query(query, (student_id, pin))
            if result and len(result) > 0:
                self.current_user = result[0]
                return True
            return False
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return False
    
    def authenticate_staff(self, staff_id, pin):
        """Authenticate staff member"""
        try:
            # Ensure database connection is active
            if not self.db.ensure_connection():
                print("✗ Database connection failed")
                return False
            
            query = """
            SELECT * FROM staff 
            WHERE staff_id = %s AND pin = %s
            """
            result = self.db.execute_query(query, (staff_id, pin))
            if result and len(result) > 0:
                self.current_user = result[0]
                return True
            return False
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return False
    
    # User management methods
    def create_admin(self, email, password, full_name):
        """Create a new admin user"""
        password_hash = self.hash_password(password)
        query = """
        INSERT INTO users (username, email, password_hash, user_type, full_name)
        VALUES (%s, %s, %s, 'admin', %s)
        """
        username = email.split('@')[0]
        return self.db.execute_update(query, (username, email, password_hash, full_name))
    
    def create_student(self, student_id, pin, full_name, email=None, phone=None):
        """Create a new student"""
        query = """
        INSERT INTO students (student_id, pin, full_name, email, phone)
        VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.execute_update(query, (student_id, pin, full_name, email, phone))
    
    def create_staff(self, staff_id, pin, full_name, email=None, department=None):
        """Create a new staff member"""
        query = """
        INSERT INTO staff (staff_id, pin, full_name, email, department)
        VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.execute_update(query, (staff_id, pin, full_name, email, department))
    
    # Course management methods
    def add_course(self, course_code, course_name, credits=3, description=None):
        """Add a new course"""
        query = """
        INSERT INTO courses (course_code, course_name, credits, description)
        VALUES (%s, %s, %s, %s)
        """
        return self.db.execute_update(query, (course_code, course_name, credits, description))
    
    def get_all_courses(self):
        """Get all courses"""
        query = "SELECT * FROM courses ORDER BY course_code"
        return self.db.execute_query(query)
    
    def assign_course_to_staff(self, staff_id, course_id, academic_year, semester):
        """Assign a course to a staff member"""
        query = """
        INSERT INTO course_assignments (staff_id, course_id, academic_year, semester)
        VALUES (%s, %s, %s, %s)
        """
        return self.db.execute_update(query, (staff_id, course_id, academic_year, semester))
    
    def get_staff_courses(self, staff_id, academic_year=None, semester=None):
        """Get courses assigned to a staff member"""
        query = """
        SELECT c.*, ca.academic_year, ca.semester
        FROM courses c
        JOIN course_assignments ca ON c.id = ca.course_id
        WHERE ca.staff_id = %s
        """
        params = [staff_id]
        if academic_year:
            query += " AND ca.academic_year = %s"
            params.append(academic_year)
        if semester:
            query += " AND ca.semester = %s"
            params.append(semester)
        query += " ORDER BY c.course_code"
        return self.db.execute_query(query, tuple(params))
    
    # Enrollment methods
    def enroll_student(self, student_id, course_id, academic_year, semester):
        """Enroll a student in a course"""
        query = """
        INSERT INTO enrollments (student_id, course_id, academic_year, semester)
        VALUES (%s, %s, %s, %s)
        """
        return self.db.execute_update(query, (student_id, course_id, academic_year, semester))
    
    def unenroll_student(self, student_id, course_id, academic_year, semester):
        """Unenroll a student from a course"""
        query = """
        DELETE FROM enrollments 
        WHERE student_id = %s AND course_id = %s AND academic_year = %s AND semester = %s
        """
        return self.db.execute_update(query, (student_id, course_id, academic_year, semester))
    
    def get_student_enrollments(self, student_id, academic_year=None, semester=None):
        """Get all enrollments for a student"""
        query = """
        SELECT e.*, c.course_code, c.course_name, c.credits
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE e.student_id = %s
        """
        params = [student_id]
        if academic_year:
            query += " AND e.academic_year = %s"
            params.append(academic_year)
        if semester:
            query += " AND e.semester = %s"
            params.append(semester)
        query += " ORDER BY c.course_code"
        return self.db.execute_query(query, tuple(params))
    
    def get_course_enrollments(self, course_id, academic_year, semester):
        """Get all students enrolled in a specific course"""
        query = """
        SELECT e.*, s.student_id, s.full_name, s.email
        FROM enrollments e
        JOIN students s ON e.student_id = s.id
        WHERE e.course_id = %s AND e.academic_year = %s AND e.semester = %s
        ORDER BY s.full_name
        """
        return self.db.execute_query(query, (course_id, academic_year, semester))
    
    # Academic records methods
    def record_student_score(self, student_id, course_id, staff_id, academic_year, semester, score):
        """Record a student's score for a course"""
        grade = calculate_grade(score)
        gpa_points = calculate_gpa_points(score)
        
        query = """
        INSERT INTO academic_records (student_id, course_id, staff_id, academic_year, semester, score, grade, gpa_points)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (student_id, course_id, academic_year, semester)
        DO UPDATE SET score = EXCLUDED.score, grade = EXCLUDED.grade, gpa_points = EXCLUDED.gpa_points
        """
        return self.db.execute_update(query, (student_id, course_id, staff_id, academic_year, semester, score, grade, gpa_points))
    
    def get_student_academic_record(self, student_id, academic_year=None, semester=None):
        """Get academic records for a student"""
        query = """
        SELECT ar.*, c.course_code, c.course_name, c.credits, s.full_name as staff_name
        FROM academic_records ar
        JOIN courses c ON ar.course_id = c.id
        JOIN staff s ON ar.staff_id = s.id
        WHERE ar.student_id = %s
        """
        params = [student_id]
        if academic_year:
            query += " AND ar.academic_year = %s"
            params.append(academic_year)
        if semester:
            query += " AND ar.semester = %s"
            params.append(semester)
        query += " ORDER BY c.course_code"
        return self.db.execute_query(query, tuple(params))
    
    def calculate_student_gpa(self, student_id, academic_year=None, semester=None):
        """Calculate GPA for a student"""
        records = self.get_student_academic_record(student_id, academic_year, semester)
        if not records:
            return 0.0
        
        total_points = 0
        total_credits = 0
        
        for record in records:
            if record['gpa_points'] is not None:
                total_points += record['gpa_points'] * record['credits']
                total_credits += record['credits']
        
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0
    
    # Legacy methods for backward compatibility
    def insert_student(self, index_number, full_name, course, score):
        """Insert a new student record (legacy)"""
        grade = calculate_grade(score)
        query = """
        INSERT INTO student_results (index_number, full_name, course, score, grade)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (index_number, full_name, course, score, grade)
        return self.db.execute_update(query, params)
    
    def get_all_students(self):
        """Retrieve all student records (legacy)"""
        query = "SELECT * FROM student_results ORDER BY full_name"
        return self.db.execute_query(query)
    
    def get_student_by_index(self, index_number):
        """Retrieve a student by index number (legacy)"""
        query = "SELECT * FROM student_results WHERE index_number = %s"
        result = self.db.execute_query(query, (index_number,))
        return result[0] if result else None
    
    def update_student_score(self, index_number, new_score):
        """Update a student's score and recalculate grade (legacy)"""
        new_grade = calculate_grade(new_score)
        query = """
        UPDATE student_results 
        SET score = %s, grade = %s 
        WHERE index_number = %s
        """
        params = (new_score, new_grade, index_number)
        return self.db.execute_update(query, params)
    
    def get_grade_distribution(self):
        """Get count of students by grade (legacy)"""
        query = """
        SELECT grade, COUNT(*) as count 
        FROM student_results 
        GROUP BY grade 
        ORDER BY grade
        """
        return self.db.execute_query(query)
    
    def get_total_students(self):
        """Get total number of students (legacy)"""
        query = "SELECT COUNT(*) as total FROM student_results"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def student_exists(self, index_number):
        """Check if student with given index number exists (legacy)"""
        query = "SELECT COUNT(*) as count FROM student_results WHERE index_number = %s"
        result = self.db.execute_query(query, (index_number,))
        return result[0]['count'] > 0 if result else False
    
    def clear_all_records(self):
        """Clear all student records (for testing purposes)"""
        query = "DELETE FROM student_results"
        return self.db.execute_update(query)

    def delete_student(self, index_number):
        """Delete a student by index number (legacy)"""
        query = "DELETE FROM student_results WHERE index_number = %s"
        return self.db.execute_update(query, (index_number,))