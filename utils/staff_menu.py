class StaffMenu:
    def __init__(self, db, auth_manager):
        self.db = db
        self.auth_manager = auth_manager
        self.current_staff = auth_manager.get_current_user()
    
    def show_menu(self):
        """Display staff menu"""
        while True:
            print("\n" + "="*60)
            print("          STAFF DASHBOARD")
            print("="*60)
            print(f"Welcome, {self.current_staff['full_name']}!")
            print("1. View My Courses")
            print("2. View Course Enrollments")
            print("3. Record Student Scores")
            print("4. View Student Grades")
            print("5. Logout")
            print("6. Exit")
            print("-"*60)
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.view_my_courses()
            elif choice == '2':
                self.view_course_enrollments()
            elif choice == '3':
                self.record_student_scores()
            elif choice == '4':
                self.view_student_grades()
            elif choice == '5':
                self.auth_manager.logout()
                return True
            elif choice == '6':
                return False
            else:
                print("✗ Invalid choice. Please try again.")
    
    def view_my_courses(self):
        """View courses assigned to the staff member"""
        print("\n" + "="*60)
        print("MY COURSES")
        print("="*60)
        
        staff_id = self.current_staff['id']
        courses = self.db.get_staff_courses(staff_id)
        
        if not courses:
            print("No courses assigned to you.")
            return
        
        print(f"{'ID':<4} {'Code':<10} {'Name':<30} {'Credits':<8} {'Year':<12} {'Semester':<10}")
        print("-" * 80)
        
        for course in courses:
            print(f"{course['id']:<4} {course['course_code']:<10} {course['course_name']:<30} "
                  f"{course['credits']:<8} {course['academic_year']:<12} {course['semester']:<10}")
        
        print(f"\nTotal courses: {len(courses)}")
    
    def view_course_enrollments(self):
        """View enrollments for a specific course"""
        print("\n" + "="*50)
        print("COURSE ENROLLMENTS")
        print("="*50)
        
        staff_id = self.current_staff['id']
        courses = self.db.get_staff_courses(staff_id)
        
        if not courses:
            print("No courses assigned to you.")
            return
        
        print("Your Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['course_code']} - {course['course_name']} ({course['academic_year']} {course['semester']})")
        
        try:
            choice = int(input("\nSelect course (number): ")) - 1
            if 0 <= choice < len(courses):
                selected_course = courses[choice]
                self.show_course_enrollments(selected_course)
            else:
                print("✗ Invalid selection.")
        except ValueError:
            print("✗ Please enter a valid number.")
    
    def show_course_enrollments(self, course):
        """Show enrollments for a specific course"""
        print(f"\n" + "="*60)
        print(f"ENROLLMENTS FOR {course['course_code']} - {course['course_name']}")
        print(f"Academic Year: {course['academic_year']} | Semester: {course['semester']}")
        print("="*60)
        
        enrollments = self.db.get_course_enrollments(
            course['id'], 
            course['academic_year'], 
            course['semester']
        )
        
        if not enrollments:
            print("No students enrolled in this course.")
            return
        
        print(f"{'ID':<4} {'Student ID':<12} {'Name':<25} {'Email':<25} {'Status':<10}")
        print("-" * 80)
        
        for enrollment in enrollments:
            print(f"{enrollment['id']:<4} {enrollment['student_id']:<12} {enrollment['full_name']:<25} "
                  f"{enrollment['email'] or 'N/A':<25} {enrollment['status']:<10}")
        
        print(f"\nTotal enrollments: {len(enrollments)}")
    
    def record_student_scores(self):
        """Record scores for students in a course"""
        print("\n" + "="*50)
        print("RECORD STUDENT SCORES")
        print("="*50)
        
        staff_id = self.current_staff['id']
        courses = self.db.get_staff_courses(staff_id)
        
        if not courses:
            print("No courses assigned to you.")
            return
        
        print("Your Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['course_code']} - {course['course_name']} ({course['academic_year']} {course['semester']})")
        
        try:
            choice = int(input("\nSelect course (number): ")) - 1
            if 0 <= choice < len(courses):
                selected_course = courses[choice]
                self.record_scores_for_course(selected_course)
            else:
                print("✗ Invalid selection.")
        except ValueError:
            print("✗ Please enter a valid number.")
    
    def record_scores_for_course(self, course):
        """Record scores for students in a specific course"""
        print(f"\n" + "="*60)
        print(f"RECORD SCORES FOR {course['course_code']} - {course['course_name']}")
        print("="*60)
        
        enrollments = self.db.get_course_enrollments(
            course['id'], 
            course['academic_year'], 
            course['semester']
        )
        
        if not enrollments:
            print("No students enrolled in this course.")
            return
        
        print("Students enrolled:")
        for i, enrollment in enumerate(enrollments, 1):
            print(f"{i}. {enrollment['student_id']} - {enrollment['full_name']}")
        
        try:
            choice = int(input("\nSelect student (number): ")) - 1
            if 0 <= choice < len(enrollments):
                selected_student = enrollments[choice]
                self.record_score_for_student(selected_student, course)
            else:
                print("✗ Invalid selection.")
        except ValueError:
            print("✗ Please enter a valid number.")
    
    def record_score_for_student(self, student, course):
        """Record score for a specific student"""
        print(f"\n" + "-"*40)
        print(f"RECORD SCORE FOR {student['full_name']}")
        print(f"Course: {course['course_code']} - {course['course_name']}")
        print("-"*40)
        
        # Check if score already exists
        existing_score_query = """
        SELECT score, grade FROM academic_records 
        WHERE student_id = %s AND course_id = %s AND academic_year = %s AND semester = %s
        """
        existing = self.db.db.execute_query(existing_score_query, (
            student['student_id'], course['id'], course['academic_year'], course['semester']
        ))
        
        if existing:
            current_score = existing[0]['score']
            current_grade = existing[0]['grade']
            print(f"Current Score: {current_score} (Grade: {current_grade})")
        
        try:
            score = int(input("Enter new score (0-100): "))
            if 0 <= score <= 100:
                if self.db.record_student_score(
                    student['student_id'], 
                    course['id'], 
                    self.current_staff['id'],
                    course['academic_year'], 
                    course['semester'], 
                    score
                ):
                    grade = self.db.db.execute_query("SELECT grade FROM academic_records WHERE student_id = %s AND course_id = %s AND academic_year = %s AND semester = %s", 
                                                   (student['student_id'], course['id'], course['academic_year'], course['semester']))[0]['grade']
                    print(f"✓ Score recorded successfully! Grade: {grade}")
                else:
                    print("✗ Failed to record score.")
            else:
                print("✗ Score must be between 0 and 100.")
        except ValueError:
            print("✗ Please enter a valid score.")
    
    def view_student_grades(self):
        """View grades for students in a course"""
        print("\n" + "="*50)
        print("VIEW STUDENT GRADES")
        print("="*50)
        
        staff_id = self.current_staff['id']
        courses = self.db.get_staff_courses(staff_id)
        
        if not courses:
            print("No courses assigned to you.")
            return
        
        print("Your Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['course_code']} - {course['course_name']} ({course['academic_year']} {course['semester']})")
        
        try:
            choice = int(input("\nSelect course (number): ")) - 1
            if 0 <= choice < len(courses):
                selected_course = courses[choice]
                self.show_course_grades(selected_course)
            else:
                print("✗ Invalid selection.")
        except ValueError:
            print("✗ Please enter a valid number.")
    
    def show_course_grades(self, course):
        """Show grades for students in a specific course"""
        print(f"\n" + "="*80)
        print(f"GRADES FOR {course['course_code']} - {course['course_name']}")
        print(f"Academic Year: {course['academic_year']} | Semester: {course['semester']}")
        print("="*80)
        
        # Get academic records for this course
        grades_query = """
        SELECT ar.*, s.student_id, s.full_name, s.email
        FROM academic_records ar
        JOIN students s ON ar.student_id = s.id
        WHERE ar.course_id = %s AND ar.academic_year = %s AND ar.semester = %s
        ORDER BY s.full_name
        """
        grades = self.db.db.execute_query(grades_query, (course['id'], course['academic_year'], course['semester']))
        
        if not grades:
            print("No grades recorded for this course.")
            return
        
        print(f"{'Student ID':<12} {'Name':<25} {'Score':<6} {'Grade':<6} {'GPA Points':<10}")
        print("-" * 80)
        
        for grade in grades:
            print(f"{grade['student_id']:<12} {grade['full_name']:<25} {grade['score']:<6} "
                  f"{grade['grade']:<6} {grade['gpa_points']:<10}")
        
        print(f"\nTotal students with grades: {len(grades)}")
        
        # Calculate average score
        total_score = sum(grade['score'] for grade in grades)
        avg_score = total_score / len(grades)
        print(f"Average Score: {avg_score:.1f}") 