class StudentMenu:
    def __init__(self, db, auth_manager):
        self.db = db
        self.auth_manager = auth_manager
        self.current_student = auth_manager.get_current_user()
    
    def show_menu(self):
        """Display student menu"""
        while True:
            print("\n" + "="*60)
            print("          STUDENT DASHBOARD")
            print("="*60)
            print(f"Welcome, {self.current_student['full_name']}!")
            print("1. View My Enrollments")
            print("2. View My Grades")
            print("3. View My GPA")
            print("4. Enroll in Course")
            print("5. Logout")
            print("6. Exit")
            print("-"*60)
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.view_my_enrollments()
            elif choice == '2':
                self.view_my_grades()
            elif choice == '3':
                self.view_my_gpa()
            elif choice == '4':
                self.enroll_in_course()
            elif choice == '5':
                self.auth_manager.logout()
                return True
            elif choice == '6':
                return False
            else:
                print("✗ Invalid choice. Please try again.")
    
    def view_my_enrollments(self):
        """View student's course enrollments"""
        print("\n" + "="*60)
        print("MY ENROLLMENTS")
        print("="*60)
        
        student_id = self.current_student['id']
        enrollments = self.db.get_student_enrollments(student_id)
        
        if not enrollments:
            print("You are not enrolled in any courses.")
            return
        
        print(f"{'ID':<4} {'Course Code':<12} {'Course Name':<30} {'Credits':<8} {'Year':<12} {'Semester':<10} {'Status':<10}")
        print("-" * 100)
        
        for enrollment in enrollments:
            print(f"{enrollment['id']:<4} {enrollment['course_code']:<12} {enrollment['course_name']:<30} "
                  f"{enrollment['credits']:<8} {enrollment['academic_year']:<12} {enrollment['semester']:<10} {enrollment['status']:<10}")
        
        print(f"\nTotal enrollments: {len(enrollments)}")
    
    def view_my_grades(self):
        """View student's grades"""
        print("\n" + "="*60)
        print("MY GRADES")
        print("="*60)
        
        student_id = self.current_student['id']
        academic_records = self.db.get_student_academic_record(student_id)
        
        if not academic_records:
            print("No grades recorded yet.")
            return
        
        print(f"{'Course Code':<12} {'Course Name':<30} {'Score':<6} {'Grade':<6} {'GPA Points':<10} {'Credits':<8} {'Staff':<20}")
        print("-" * 100)
        
        for record in academic_records:
            print(f"{record['course_code']:<12} {record['course_name']:<30} {record['score']:<6} "
                  f"{record['grade']:<6} {record['gpa_points']:<10} {record['credits']:<8} {record['staff_name']:<20}")
        
        print(f"\nTotal courses with grades: {len(academic_records)}")
        
        # Calculate average score
        total_score = sum(record['score'] for record in academic_records)
        avg_score = total_score / len(academic_records)
        print(f"Average Score: {avg_score:.1f}")
    
    def view_my_gpa(self):
        """View student's GPA"""
        print("\n" + "="*50)
        print("MY GPA")
        print("="*50)
        
        student_id = self.current_student['id']
        
        # Get GPA for current academic year
        current_year = input("Enter academic year (e.g., 2023-2024) or press Enter for all: ").strip()
        semester = input("Enter semester (First Semester, Second Semester) or press Enter for all: ").strip()
        
        if not current_year:
            current_year = None
        if not semester:
            semester = None
        
        gpa = self.db.calculate_student_gpa(student_id, current_year, semester)
        
        print(f"\nStudent: {self.current_student['full_name']}")
        print(f"Student ID: {self.current_student['student_id']}")
        if current_year:
            print(f"Academic Year: {current_year}")
        if semester:
            print(f"Semester: {semester}")
        print(f"GPA: {gpa:.2f}")
        
        # Show grade breakdown
        academic_records = self.db.get_student_academic_record(student_id, current_year, semester)
        
        if academic_records:
            print(f"\nGrade Breakdown:")
            print(f"{'Course':<15} {'Score':<6} {'Grade':<6} {'GPA Points':<10} {'Credits':<8}")
            print("-" * 50)
            
            for record in academic_records:
                print(f"{record['course_code']:<15} {record['score']:<6} {record['grade']:<6} "
                      f"{record['gpa_points']:<10} {record['credits']:<8}")
    
    def enroll_in_course(self):
        """Enroll in a new course"""
        print("\n" + "="*50)
        print("ENROLL IN COURSE")
        print("="*50)
        
        # Get available courses
        courses = self.db.get_all_courses()
        
        if not courses:
            print("No courses available for enrollment.")
            return
        
        print("Available Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['course_code']} - {course['course_name']} ({course['credits']} credits)")
        
        try:
            choice = int(input("\nSelect course (number): ")) - 1
            if 0 <= choice < len(courses):
                selected_course = courses[choice]
                self.process_enrollment(selected_course)
            else:
                print("✗ Invalid selection.")
        except ValueError:
            print("✗ Please enter a valid number.")
    
    def process_enrollment(self, course):
        """Process course enrollment"""
        print(f"\n" + "-"*40)
        print(f"ENROLL IN {course['course_code']} - {course['course_name']}")
        print("-"*40)
        
        academic_year = input("Academic Year (e.g., 2023-2024): ").strip()
        semester = input("Semester (First Semester, Second Semester): ").strip()
        
        if not academic_year or not semester:
            print("✗ Academic year and semester are required.")
            return
        
        student_id = self.current_student['id']
        
        # Check if already enrolled
        existing_enrollment_query = """
        SELECT * FROM enrollments 
        WHERE student_id = %s AND course_id = %s AND academic_year = %s AND semester = %s
        """
        existing = self.db.db.execute_query(existing_enrollment_query, (
            student_id, course['id'], academic_year, semester
        ))
        
        if existing:
            print("✗ You are already enrolled in this course for this academic year and semester.")
            return
        
        if self.db.enroll_student(student_id, course['id'], academic_year, semester):
            print("✓ Successfully enrolled in the course!")
        else:
            print("✗ Failed to enroll in the course.") 