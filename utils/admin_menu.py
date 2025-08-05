from utils.auth_manager import AuthManager

class AdminMenu:
    def __init__(self, db, auth_manager):
        self.db = db
        self.auth_manager = auth_manager
    
    def show_menu(self):
        """Display admin menu"""
        while True:
            print("\n" + "="*60)
            print("          ADMIN DASHBOARD")
            print("="*60)
            print("1. Manage Students")
            print("2. Manage Staff")
            print("3. Manage Courses")
            print("4. Course Assignments")
            print("5. View System Reports")
            print("6. Legacy System (Student Results)")
            print("7. Logout")
            print("8. Exit")
            print("-"*60)
            
            choice = input("Select option (1-8): ").strip()
            
            if choice == '1':
                self.manage_students()
            elif choice == '2':
                self.manage_staff()
            elif choice == '3':
                self.manage_courses()
            elif choice == '4':
                self.manage_course_assignments()
            elif choice == '5':
                self.view_system_reports()
            elif choice == '6':
                self.legacy_system()
            elif choice == '7':
                self.auth_manager.logout()
                return True
            elif choice == '8':
                return False
            else:
                print("✗ Invalid choice. Please try again.")
    
    def manage_students(self):
        """Manage students menu"""
        while True:
            print("\n" + "-"*40)
            print("STUDENT MANAGEMENT")
            print("-"*40)
            print("1. Add New Student")
            print("2. View All Students")
            print("3. Search Student")

            print("4. View Student Credentials")
            print("5. Back to Admin Menu")
            print("-"*40)
            
            choice = input("Select option (1-5): ").strip()
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_all_students()
            elif choice == '3':
                self.search_student()
            elif choice == '4':
                self.view_student_credentials()
            elif choice == '5':
                break
            else:
                print("✗ Invalid choice. Please try again.")
    
    def add_student(self):
        """Add a new student"""
        print("\n" + "="*40)
        print("ADD NEW STUDENT")
        print("="*40)
        
        full_name = input("Full Name: ").strip()
        email = input("Email (optional): ").strip()
        phone = input("Phone (optional): ").strip()
        
        if not full_name:
            print("✗ Full name is required.")
            return
        
        # Generate student ID and PIN
        student_id = self.auth_manager.generate_student_id()
        pin = self.auth_manager.generate_pin()
        
        if self.db.create_student(student_id, pin, full_name, email, phone):
            print(f"✓ Student created successfully!")
            print(f"Student ID: {student_id}")
            print(f"PIN: {pin}")
            print("Please provide these credentials to the student.")
            print("\n" + "="*40)
            print("IMPORTANT: Save these credentials securely!")
            print("="*40)
        else:
            print("✗ Failed to create student.")
    
    def view_all_students(self):
        """View all students"""
        print("\n" + "="*80)
        print("ALL STUDENTS")
        print("="*80)
        
        query = "SELECT * FROM students ORDER BY full_name"
        students = self.db.db.execute_query(query)
        
        if not students:
            print("No students found.")
            return
        
        print(f"{'ID':<4} {'Student ID':<10} {'Name':<25} {'Email':<25} {'Phone':<15}")
        print("-" * 80)
        
        for student in students:
            print(f"{student['id']:<4} {student['student_id']:<10} {student['full_name']:<25} "
                  f"{student['email'] or 'N/A':<25} {student['phone'] or 'N/A':<15}")
        
        print(f"\nTotal students: {len(students)}")
        print("\nNote: Use 'View Student Credentials' to see PINs")
    
    def search_student(self):
        """Search for a student"""
        print("\n" + "-"*40)
        print("SEARCH STUDENT")
        print("-"*40)
        
        student_id = input("Enter Student ID: ").strip()
        
        if not student_id:
            print("✗ Student ID is required.")
            return
        
        query = "SELECT * FROM students WHERE student_id = %s"
        result = self.db.db.execute_query(query, (student_id,))
        
        if result:
            student = result[0]
            print(f"\nStudent Found:")
            print(f"ID: {student['id']}")
            print(f"Student ID: {student['student_id']}")
            print(f"Full Name: {student['full_name']}")
            print(f"Email: {student['email'] or 'N/A'}")
            print(f"Phone: {student['phone'] or 'N/A'}")
            print("\nNote: Use 'View Student Credentials' to see PIN")
        else:
            print(f"✗ No student found with ID: {student_id}")
    
    def view_student_credentials(self):
        """View student credentials securely"""
        print("\n" + "="*50)
        print("VIEW STUDENT CREDENTIALS")
        print("="*50)
        print("This will show student ID and PIN for login purposes.")
        print("Use this to help students who forgot their credentials.")
        print("-"*50)
        
        # Show all students first
        query = "SELECT student_id, full_name FROM students ORDER BY full_name"
        students = self.db.db.execute_query(query)
        
        if not students:
            print("No students found.")
            return
        
        print("Available Students:")
        for i, student in enumerate(students, 1):
            print(f"{i}. {student['full_name']} ({student['student_id']})")
        
        try:
            choice = int(input("\nSelect student (number): ")) - 1
            if 0 <= choice < len(students):
                selected_student = students[choice]
                self.show_student_credentials(selected_student['student_id'])
            else:
                print("✗ Invalid selection.")
        except ValueError:
            print("✗ Please enter a valid number.")
    
    def show_student_credentials(self, student_id):
        """Show credentials for a specific student"""
        query = "SELECT * FROM students WHERE student_id = %s"
        result = self.db.db.execute_query(query, (student_id,))
        
        if result:
            student = result[0]
            print(f"\n" + "="*50)
            print(f"CREDENTIALS FOR {student['full_name']}")
            print("="*50)
            print(f"Student ID: {student['student_id']}")
            print(f"PIN: {student['pin']}")
            print(f"Full Name: {student['full_name']}")
            print(f"Email: {student['email'] or 'N/A'}")
            print(f"Phone: {student['phone'] or 'N/A'}")
            print("="*50)
            print("Login Instructions:")
            print("1. Select 'Student Login' from main menu")
            print("2. Enter Student ID and PIN above")
            print("="*50)
        else:
            print(f"✗ No student found with ID: {student_id}")
    
    def manage_staff(self):
        """Manage staff menu"""
        while True:
            print("\n" + "-"*40)
            print("STAFF MANAGEMENT")
            print("-"*40)
            print("1. Add New Staff")
            print("2. View All Staff")
            print("3. Search Staff")
            print("4. View Staff Credentials")
            print("5. Back to Admin Menu")
            print("-"*40)
            
            choice = input("Select option (1-5): ").strip()
            
            if choice == '1':
                self.add_staff()
            elif choice == '2':
                self.view_all_staff()
            elif choice == '3':
                self.search_staff()
            elif choice == '4':
                self.view_staff_credentials()
            elif choice == '5':
                break
            else:
                print("✗ Invalid choice. Please try again.")
    
    def add_staff(self):
        """Add a new staff member"""
        print("\n" + "="*40)
        print("ADD NEW STAFF")
        print("="*40)
        
        full_name = input("Full Name: ").strip()
        email = input("Email (optional): ").strip()
        department = input("Department (optional): ").strip()
        
        if not full_name:
            print("✗ Full name is required.")
            return
        
        # Generate staff ID and PIN
        staff_id = self.auth_manager.generate_student_id()  # Reuse the function
        pin = self.auth_manager.generate_pin()
        
        if self.db.create_staff(staff_id, pin, full_name, email, department):
            print(f"✓ Staff created successfully!")
            print(f"Staff ID: {staff_id}")
            print(f"PIN: {pin}")
            print("Please provide these credentials to the staff member.")
            print("\n" + "="*40)
            print("IMPORTANT: Save these credentials securely!")
            print("="*40)
        else:
            print("✗ Failed to create staff member.")
    
    def view_all_staff(self):
        """View all staff"""
        print("\n" + "="*80)
        print("ALL STAFF")
        print("="*80)
        
        query = "SELECT * FROM staff ORDER BY full_name"
        staff_list = self.db.db.execute_query(query)
        
        if not staff_list:
            print("No staff found.")
            return
        
        print(f"{'ID':<4} {'Staff ID':<10} {'Name':<25} {'Email':<25} {'Department':<20}")
        print("-" * 80)
        
        for staff in staff_list:
            print(f"{staff['id']:<4} {staff['staff_id']:<10} {staff['full_name']:<25} "
                  f"{staff['email'] or 'N/A':<25} {staff['department'] or 'N/A':<20}")
        
        print(f"\nTotal staff: {len(staff_list)}")
        print("\nNote: Use 'View Staff Credentials' to see PINs")
    
    def search_staff(self):
        """Search for a staff member"""
        print("\n" + "-"*40)
        print("SEARCH STAFF")
        print("-"*40)
        
        staff_id = input("Enter Staff ID: ").strip()
        
        if not staff_id:
            print("✗ Staff ID is required.")
            return
        
        query = "SELECT * FROM staff WHERE staff_id = %s"
        result = self.db.db.execute_query(query, (staff_id,))
        
        if result:
            staff = result[0]
            print(f"\nStaff Found:")
            print(f"ID: {staff['id']}")
            print(f"Staff ID: {staff['staff_id']}")
            print(f"Full Name: {staff['full_name']}")
            print(f"Email: {staff['email'] or 'N/A'}")
            print(f"Department: {staff['department'] or 'N/A'}")
            print("\nNote: Use 'View Staff Credentials' to see PIN")
        else:
            print(f"✗ No staff found with ID: {staff_id}")
    
    def view_staff_credentials(self):
        """View staff credentials securely"""
        print("\n" + "="*50)
        print("VIEW STAFF CREDENTIALS")
        print("="*50)
        print("This will show staff ID and PIN for login purposes.")
        print("Use this to help staff who forgot their credentials.")
        print("-"*50)
        
        # Show all staff first
        query = "SELECT staff_id, full_name FROM staff ORDER BY full_name"
        staff_list = self.db.db.execute_query(query)
        
        if not staff_list:
            print("No staff found.")
            return
        
        print("Available Staff:")
        for i, staff in enumerate(staff_list, 1):
            print(f"{i}. {staff['full_name']} ({staff['staff_id']})")
        
        try:
            choice = int(input("\nSelect staff (number): ")) - 1
            if 0 <= choice < len(staff_list):
                selected_staff = staff_list[choice]
                self.show_staff_credentials(selected_staff['staff_id'])
            else:
                print("✗ Invalid selection.")
        except ValueError:
            print("✗ Please enter a valid number.")
    
    def show_staff_credentials(self, staff_id):
        """Show credentials for a specific staff member"""
        query = "SELECT * FROM staff WHERE staff_id = %s"
        result = self.db.db.execute_query(query, (staff_id,))
        
        if result:
            staff = result[0]
            print(f"\n" + "="*50)
            print(f"CREDENTIALS FOR {staff['full_name']}")
            print("="*50)
            print(f"Staff ID: {staff['staff_id']}")
            print(f"PIN: {staff['pin']}")
            print(f"Full Name: {staff['full_name']}")
            print(f"Email: {staff['email'] or 'N/A'}")
            print(f"Department: {staff['department'] or 'N/A'}")
            print("="*50)
            print("Login Instructions:")
            print("1. Select 'Staff Login' from main menu")
            print("2. Enter Staff ID and PIN above")
            print("="*50)
        else:
            print(f"✗ No staff found with ID: {staff_id}")
    
    def manage_courses(self):
        """Manage courses menu"""
        while True:
            print("\n" + "-"*40)
            print("COURSE MANAGEMENT")
            print("-"*40)
            print("1. Add New Course")
            print("2. View All Courses")
            print("3. Search Course")
            print("4. Back to Admin Menu")
            print("-"*40)
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == '1':
                self.add_course()
            elif choice == '2':
                self.view_all_courses()
            elif choice == '3':
                self.search_course()
            elif choice == '4':
                break
            else:
                print("✗ Invalid choice. Please try again.")
    
    def add_course(self):
        """Add a new course"""
        print("\n" + "="*40)
        print("ADD NEW COURSE")
        print("="*40)
        
        course_code = input("Course Code: ").strip()
        course_name = input("Course Name: ").strip()
        credits = input("Credits (1-3, default 3): ").strip()
        description = input("Description (optional): ").strip()
        
        if not course_code or not course_name:
            print("✗ Course code and name are required.")
            return
        
        try:
            credits = int(credits) if credits else 3
            if credits < 1 or credits > 3:
                print("✗ Credits must be between 1 and 3.")
                return
        except ValueError:
            credits = 3
        
        if self.db.add_course(course_code, course_name, credits, description):
            print("✓ Course created successfully!")
        else:
            print("✗ Failed to create course.")
    
    def view_all_courses(self):
        """View all courses"""
        print("\n" + "="*80)
        print("ALL COURSES")
        print("="*80)
        
        courses = self.db.get_all_courses()
        
        if not courses:
            print("No courses found.")
            return
        
        print(f"{'ID':<4} {'Code':<10} {'Name':<30} {'Credits':<8} {'Description':<25}")
        print("-" * 80)
        
        for course in courses:
            desc = course['description'] or 'N/A'
            if len(desc) > 22:
                desc = desc[:19] + "..."
            print(f"{course['id']:<4} {course['course_code']:<10} {course['course_name']:<30} "
                  f"{course['credits']:<8} {desc:<25}")
        
        print(f"\nTotal courses: {len(courses)}")
    
    def search_course(self):
        """Search for a course"""
        print("\n" + "-"*40)
        print("SEARCH COURSE")
        print("-"*40)
        
        course_code = input("Enter Course Code: ").strip()
        
        if not course_code:
            print("✗ Course code is required.")
            return
        
        query = "SELECT * FROM courses WHERE course_code = %s"
        result = self.db.db.execute_query(query, (course_code,))
        
        if result:
            course = result[0]
            print(f"\nCourse Found:")
            print(f"ID: {course['id']}")
            print(f"Course Code: {course['course_code']}")
            print(f"Course Name: {course['course_name']}")
            print(f"Credits: {course['credits']}")
            print(f"Description: {course['description'] or 'N/A'}")
        else:
            print(f"✗ No course found with code: {course_code}")
    
    def manage_course_assignments(self):
        """Manage course assignments"""
        print("\n" + "="*50)
        print("COURSE ASSIGNMENTS")
        print("="*50)
        
        # Get all staff
        staff_query = "SELECT * FROM staff ORDER BY full_name"
        staff_list = self.db.db.execute_query(staff_query)
        
        if not staff_list:
            print("No staff available. Please add staff first.")
            return
        
        # Get all courses
        courses = self.db.get_all_courses()
        if not courses:
            print("No courses available. Please add courses first.")
            return
        
        print("Available Staff:")
        for staff in staff_list:
            print(f"{staff['id']}. {staff['full_name']} ({staff['staff_id']})")
        
        print("\nAvailable Courses:")
        for course in courses:
            print(f"{course['id']}. {course['course_code']} - {course['course_name']}")
        
        print("\n" + "-"*50)
        
        try:
            staff_id = int(input("Enter Staff ID: "))
            course_id = int(input("Enter Course ID: "))
            academic_year = input("Academic Year (e.g., 2023-2024): ").strip()
            semester = input("Semester (First Semester, Second Semester): ").strip()
            
            if not academic_year or not semester:
                print("✗ Academic year and semester are required.")
                return
            
            if self.db.assign_course_to_staff(staff_id, course_id, academic_year, semester):
                print("✓ Course assigned successfully!")
            else:
                print("✗ Failed to assign course.")
                
        except ValueError:
            print("✗ Invalid ID format.")
    
    def view_system_reports(self):
        """View system reports"""
        print("\n" + "="*50)
        print("SYSTEM REPORTS")
        print("="*50)
        
        # Get counts
        students_query = "SELECT COUNT(*) as count FROM students"
        staff_query = "SELECT COUNT(*) as count FROM staff"
        courses_query = "SELECT COUNT(*) as count FROM courses"
        enrollments_query = "SELECT COUNT(*) as count FROM enrollments"
        
        students_count = self.db.db.execute_query(students_query)[0]['count']
        staff_count = self.db.db.execute_query(staff_query)[0]['count']
        courses_count = self.db.db.execute_query(courses_query)[0]['count']
        enrollments_count = self.db.db.execute_query(enrollments_query)[0]['count']
        
        print(f"Total Students: {students_count}")
        print(f"Total Staff: {staff_count}")
        print(f"Total Courses: {courses_count}")
        print(f"Total Enrollments: {enrollments_count}")
        
        # Grade distribution
        grade_query = """
        SELECT grade, COUNT(*) as count 
        FROM academic_records 
        GROUP BY grade 
        ORDER BY grade
        """
        grade_distribution = self.db.db.execute_query(grade_query)
        
        if grade_distribution:
            print("\nGrade Distribution:")
            for grade in grade_distribution:
                print(f"{grade['grade']}: {grade['count']}")
    
    def legacy_system(self):
        """Access legacy student results system"""
        from main import main as legacy_main
        print("\n" + "="*50)
        print("LEGACY STUDENT RESULTS SYSTEM")
        print("="*50)
        print("Switching to legacy system...")
        legacy_main() 