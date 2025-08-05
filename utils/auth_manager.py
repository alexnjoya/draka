import hashlib
import secrets
import string

class AuthManager:
    def __init__(self, db):
        self.db = db
        self.current_user = None
        self.user_type = None
    
    def generate_pin(self, length=5):
        """Generate a random PIN"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    def generate_student_id(self, length=8):
        """Generate a random student ID"""
        return ''.join(secrets.choice(string.digits) for _ in range(length))
    
    def login(self):
        """Handle user login"""
        print("\n" + "="*50)
        print("LOGIN SYSTEM")
        print("="*50)
        print("1. Admin Login (Email & Password)")
        print("2. Student Login (Student ID & PIN)")
        print("3. Staff Login (Staff ID & PIN)")
        print("4. Exit")
        print("-"*50)
        
        choice = input("Select login type (1-4): ").strip()
        
        if choice == '1':
            return self.admin_login()
        elif choice == '2':
            return self.student_login()
        elif choice == '3':
            return self.staff_login()
        elif choice == '4':
            return False
        else:
            print("✗ Invalid choice. Please try again.")
            return self.login()
    
    def admin_login(self):
        """Handle admin login"""
        print("\n" + "-"*30)
        print("ADMIN LOGIN")
        print("-"*30)
        
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        
        if not email or not password:
            print("✗ Email and password are required.")
            return False
        
        if self.db.authenticate_admin(email, password):
            self.current_user = self.db.current_user
            self.user_type = 'admin'
            print(f"✓ Welcome, {self.current_user['full_name']}!")
            return True
        else:
            print("✗ Invalid email or password.")
            return False
    
    def student_login(self):
        """Handle student login"""
        print("\n" + "-"*30)
        print("STUDENT LOGIN")
        print("-"*30)
        
        student_id = input("Student ID (8 digits): ").strip()
        pin = input("PIN (5 digits): ").strip()
        
        if not student_id or not pin:
            print("✗ Student ID and PIN are required.")
            return False
        
        if len(student_id) != 8 or len(pin) != 5:
            print("✗ Student ID must be 8 digits and PIN must be 5 digits.")
            return False
        
        if self.db.authenticate_student(student_id, pin):
            self.current_user = self.db.current_user
            self.user_type = 'student'
            print(f"✓ Welcome, {self.current_user['full_name']}!")
            return True
        else:
            print("✗ Invalid Student ID or PIN.")
            return False
    
    def staff_login(self):
        """Handle staff login"""
        print("\n" + "-"*30)
        print("STAFF LOGIN")
        print("-"*30)
        
        staff_id = input("Staff ID (8 digits): ").strip()
        pin = input("PIN (5 digits): ").strip()
        
        if not staff_id or not pin:
            print("✗ Staff ID and PIN are required.")
            return False
        
        if len(staff_id) != 8 or len(pin) != 5:
            print("✗ Staff ID must be 8 digits and PIN must be 5 digits.")
            return False
        
        if self.db.authenticate_staff(staff_id, pin):
            self.current_user = self.db.current_user
            self.user_type = 'staff'
            print(f"✓ Welcome, {self.current_user['full_name']}!")
            return True
        else:
            print("✗ Invalid Staff ID or PIN.")
            return False
    
    def logout(self):
        """Handle user logout"""
        if self.current_user:
            print(f"✓ Goodbye, {self.current_user['full_name']}!")
            self.current_user = None
            self.user_type = None
        return True
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def get_user_type(self):
        """Get current user type"""
        return self.user_type
    
    def is_admin(self):
        """Check if current user is admin"""
        return self.user_type == 'admin'
    
    def is_student(self):
        """Check if current user is student"""
        return self.user_type == 'student'
    
    def is_staff(self):
        """Check if current user is staff"""
        return self.user_type == 'staff'
    
    def admin_login_with_credentials(self, email, password):
        """Handle admin login with credentials (for GUI)"""
        if not email or not password:
            return False
        
        if self.db.authenticate_admin(email, password):
            self.current_user = self.db.current_user
            self.user_type = 'admin'
            return True
        else:
            return False
    
    def student_login_with_credentials(self, student_id, pin):
        """Handle student login with credentials (for GUI)"""
        if not student_id or not pin:
            return False
        
        if len(student_id) != 8 or len(pin) != 5:
            return False
        
        if self.db.authenticate_student(student_id, pin):
            self.current_user = self.db.current_user
            self.user_type = 'student'
            return True
        else:
            return False
    
    def staff_login_with_credentials(self, staff_id, pin):
        """Handle staff login with credentials (for GUI)"""
        if not staff_id or not pin:
            return False
        
        if len(staff_id) != 8 or len(pin) != 5:
            return False
        
        if self.db.authenticate_staff(staff_id, pin):
            self.current_user = self.db.current_user
            self.user_type = 'staff'
            return True
        else:
            return False 