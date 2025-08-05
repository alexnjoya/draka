#!/usr/bin/env python3
"""
Enhanced Student Result Management System - GUI
A modern GUI application for managing student results with role-based access
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.operations import StudentResultsDB
from utils.auth_manager import AuthManager
from utils.grade_calculator import calculate_grade, calculate_gpa_points, calculate_cumulative_gpa

class StudentManagementGUI:
    def __init__(self):
        self.root = ttk.Window(themename="flatly")
        self.root.title("🎓 Student Result Management System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass  # No icon file available
        
        # Initialize database and auth
        self.db = StudentResultsDB()
        if not self.db.connect():
            messagebox.showerror("Database Error", "Failed to connect to database. Please check your configuration.")
            self.root.quit()
            return
        
        self.auth_manager = AuthManager(self.db)
        
        # Current user state
        self.current_user = None
        self.user_type = None
        
        # Create main container with enhanced modern styling
        self.main_container = ttk.Frame(self.root, bootstyle="light")
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Start with login screen
        self.show_login_screen()
    
    def __del__(self):
        """Cleanup database connection when GUI is destroyed"""
        if hasattr(self, 'db'):
            self.db.close()
    
    def show_login_screen(self):
        """Show the modern login screen"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create main login container with enhanced styling
        main_login_frame = ttk.Frame(self.main_container, bootstyle="light")
        main_login_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Create a centered container for the login content
        center_frame = ttk.Frame(main_login_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Modern card container with enhanced shadow effect
        card_frame = ttk.Frame(center_frame, bootstyle="light")
        card_frame.pack(padx=25, pady=25)
        
        # Add enhanced padding around the card
        card_inner = ttk.Frame(card_frame, bootstyle="light")
        card_inner.pack(padx=40, pady=50)
        
        # Logo/Icon section
        logo_frame = ttk.Frame(card_inner)
        logo_frame.pack(pady=(0, 20))
        
        # Modern icon (using text as icon for now)
        ttk.Label(
            logo_frame,
            text="🎓",
            font=("Segoe UI Emoji", 48),
            bootstyle="primary"
        ).pack()
        
        # Main title with modern typography
        ttk.Label(
            card_inner,
            text="Student Result Management",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 5))
        
        # Subtitle
        ttk.Label(
            card_inner,
            text="Secure Access Portal",
            font=("Segoe UI", 12),
            bootstyle="secondary"
        ).pack(pady=(0, 30))
        
        # Login options with enhanced modern styling
        options_frame = ttk.Frame(card_inner)
        options_frame.pack()
        
        # Enhanced button styles with icons and better spacing
        login_buttons = [
            ("👨‍💼 Admin Login", self.show_admin_login, "success", "Admin access to system management"),
            ("👨‍🏫 Staff Login", self.show_staff_login, "info", "Staff access to course management"),
            ("👨‍🎓 Student Login", self.show_student_login, "warning", "Student access to academic records")
        ]
        
        for text, command, style, tooltip in login_buttons:
            btn_frame = ttk.Frame(options_frame)
            btn_frame.pack(fill='x', pady=12)
            
            btn = ttk.Button(
                btn_frame,
                text=text,
                bootstyle=f"{style}-outline",
                width=28,
                command=command
            )
            btn.pack(fill='x', pady=(0, 5))
            
            # Add tooltip-like subtitle with enhanced styling
            ttk.Label(
                btn_frame,
                text=tooltip,
                font=("Segoe UI", 9),
                bootstyle="secondary"
            ).pack(pady=(3, 0))
        
        # Exit button with enhanced modern styling
        exit_frame = ttk.Frame(card_inner)
        exit_frame.pack(pady=(25, 0))
        
        ttk.Button(
            exit_frame,
            text="🚪 Exit System",
            bootstyle="danger-outline",
            width=28,
            command=self.root.quit
        ).pack()
        
        # Footer with enhanced version info
        footer_frame = ttk.Frame(main_login_frame)
        footer_frame.pack(side='bottom', fill='x', pady=15)
        
        ttk.Label(
            footer_frame,
            text="© 2024 Student Result Management System | v2.0",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack()
    
    def show_admin_login(self):
        """Show admin login form"""
        self.show_login_form("Admin", self.admin_login_callback)
    
    def show_staff_login(self):
        """Show staff login form"""
        self.show_login_form("Staff", self.staff_login_callback)
    
    def show_student_login(self):
        """Show student login form"""
        self.show_login_form("Student", self.student_login_callback)
    
    def show_login_form(self, user_type, callback):
        """Show enhanced modern login form for specified user type"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create main container with enhanced modern styling
        main_frame = ttk.Frame(self.main_container, bootstyle="light")
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Centered container
        center_frame = ttk.Frame(main_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Enhanced modern card design
        card_frame = ttk.Frame(center_frame, bootstyle="light")
        card_frame.pack(padx=25, pady=25)
        
        card_inner = ttk.Frame(card_frame, bootstyle="light")
        card_inner.pack(padx=50, pady=50)
        
        # Header section with icon and title
        header_frame = ttk.Frame(card_inner)
        header_frame.pack(pady=(0, 30))
        
        # User type icon
        icons = {
            "Admin": "👨‍💼",
            "Staff": "👨‍🏫", 
            "Student": "👨‍🎓"
        }
        
        ttk.Label(
            header_frame,
            text=icons.get(user_type, "👤"),
            font=("Segoe UI Emoji", 36),
            bootstyle="primary"
        ).pack()
        
        # Title with modern typography
        ttk.Label(
            card_inner,
            text=f"{user_type} Login",
            font=("Segoe UI", 24, "bold"),
            bootstyle="primary"
        ).pack(pady=(10, 5))
        
        # Subtitle
        ttk.Label(
            card_inner,
            text="Enter your credentials to continue",
            font=("Segoe UI", 11),
            bootstyle="secondary"
        ).pack(pady=(0, 30))
        
        # Enhanced modern form container
        form_frame = ttk.Frame(card_inner)
        form_frame.pack(fill='x')
        
        # Username/ID field with enhanced modern styling
        if user_type == "Admin":
            field_label = "📧 Email Address"
            field_placeholder = "Enter your email"
        else:
            field_label = f"🆔 {user_type} ID"
            field_placeholder = f"Enter your {user_type.lower()} ID"
        
        # Username field container with enhanced spacing
        username_container = ttk.Frame(form_frame)
        username_container.pack(fill='x', pady=12)
        
        ttk.Label(
            username_container,
            text=field_label,
            font=("Segoe UI", 11, "bold"),
            bootstyle="primary"
        ).pack(anchor='w', pady=(0, 8))
        
        username_entry = ttk.Entry(
            username_container,
            width=40,
            font=("Segoe UI", 11),
            bootstyle="primary"
        )
        username_entry.pack(fill='x', pady=(0, 20))
        
        # Password field container with enhanced spacing
        password_container = ttk.Frame(form_frame)
        password_container.pack(fill='x', pady=12)
        
        ttk.Label(
            password_container,
            text="🔒 Password/PIN",
            font=("Segoe UI", 11, "bold"),
            bootstyle="primary"
        ).pack(anchor='w', pady=(0, 8))
        
        password_entry = ttk.Entry(
            password_container,
            show="•",
            width=40,
            font=("Segoe UI", 11),
            bootstyle="primary"
        )
        password_entry.pack(fill='x', pady=(0, 30))
        
        # Enhanced modern button container
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill='x', pady=15)
        
        # Login button with enhanced modern styling
        login_btn = ttk.Button(
            button_frame,
            text="🔐 Sign In",
            bootstyle="success",
            width=25,
            command=lambda: callback(username_entry.get(), password_entry.get())
        )
        login_btn.pack(fill='x', pady=(0, 15))
        
        # Back button with enhanced modern styling
        back_btn = ttk.Button(
            button_frame,
            text="⬅️ Back to Menu",
            bootstyle="secondary-outline",
            width=25,
            command=self.show_login_screen
        )
        back_btn.pack(fill='x')
        
        # Focus on username entry for better UX
        username_entry.focus()
        
        # Bind Enter key to login
        def on_enter(event):
            callback(username_entry.get(), password_entry.get())
        
        username_entry.bind('<Return>', on_enter)
        password_entry.bind('<Return>', on_enter)
    
    def admin_login_callback(self, email, password):
        """Handle admin login"""
        if self.auth_manager.admin_login_with_credentials(email, password):
            self.current_user = self.auth_manager.get_current_user()
            self.user_type = "admin"
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Login Error", "Invalid email or password")
    
    def staff_login_callback(self, staff_id, pin):
        """Handle staff login"""
        if self.auth_manager.staff_login_with_credentials(staff_id, pin):
            self.current_user = self.auth_manager.get_current_user()
            self.user_type = "staff"
            self.show_staff_dashboard()
        else:
            messagebox.showerror("Login Error", "Invalid staff ID or PIN")
    
    def student_login_callback(self, student_id, pin):
        """Handle student login"""
        if self.auth_manager.student_login_with_credentials(student_id, pin):
            self.current_user = self.auth_manager.get_current_user()
            self.user_type = "student"
            self.show_student_dashboard()
        else:
            messagebox.showerror("Login Error", "Invalid student ID or PIN")
    
    def show_admin_dashboard(self):
        """Show enhanced admin dashboard"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create dashboard frame with enhanced styling
        dashboard_frame = ttk.Frame(self.main_container)
        dashboard_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Enhanced header with better spacing
        header_frame = ttk.Frame(dashboard_frame)
        header_frame.pack(fill='x', pady=(0, 30))
        
        ttk.Label(
            header_frame,
            text="Admin Dashboard",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Logout",
            bootstyle="danger",
            command=self.logout
        ).pack(side='right')
        
        # Enhanced menu buttons with better spacing
        menu_frame = ttk.Frame(dashboard_frame)
        menu_frame.pack(fill='both', expand=True, pady=20)
        
        # Create enhanced menu grid
        buttons = [
            ("Manage Students", self.show_student_management, "success"),
            ("Manage Staff", self.show_staff_management, "info"),
            ("Manage Courses", self.show_course_management, "warning"),
            ("Course Assignments", self.show_course_assignments, "primary"),
            ("System Reports", self.show_system_reports, "secondary"),
            ("Legacy System", self.show_legacy_system, "outline")
        ]
        
        for i, (text, command, style) in enumerate(buttons):
            row = i // 3
            col = i % 3
            
            btn = ttk.Button(
                menu_frame,
                text=text,
                bootstyle=style,
                command=command,
                width=30
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky='ew')
        
        # Configure grid weights
        for i in range(3):
            menu_frame.columnconfigure(i, weight=1)
    
    def show_student_management(self):
        """Show enhanced student management interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create student management frame with enhanced styling
        mgmt_frame = ttk.Frame(self.main_container)
        mgmt_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Enhanced header with better spacing
        header_frame = ttk.Frame(mgmt_frame)
        header_frame.pack(fill='x', pady=(0, 30))
        
        ttk.Label(
            header_frame,
            text="Student Management",
            font=("Segoe UI", 24, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_admin_dashboard
        ).pack(side='right')
        
        # Enhanced buttons with better spacing
        button_frame = ttk.Frame(mgmt_frame)
        button_frame.pack(pady=25)
        
        ttk.Button(
            button_frame,
            text="Add New Student",
            bootstyle="success",
            command=self.show_add_student_form
        ).pack(side='left', padx=8)
        
        ttk.Button(
            button_frame,
            text="View All Students",
            bootstyle="info",
            command=self.show_all_students
        ).pack(side='left', padx=8)
        
        ttk.Button(
            button_frame,
            text="View Student Credentials",
            bootstyle="warning",
            command=self.show_student_credentials
        ).pack(side='left', padx=8)
        
        # Enhanced content area
        self.content_frame = ttk.Frame(mgmt_frame)
        self.content_frame.pack(fill='both', expand=True, pady=25)
        
        # Show enhanced welcome message
        ttk.Label(
            self.content_frame,
            text="Select an option above to manage students",
            font=("Segoe UI", 14)
        ).pack(expand=True)
    
    def show_add_student_form(self):
        """Show form to add new student"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create form
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(
            form_frame,
            text="Add New Student",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Form fields
        ttk.Label(form_frame, text="Full Name:").pack(pady=5)
        name_entry = ttk.Entry(form_frame, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Email (optional):").pack(pady=5)
        email_entry = ttk.Entry(form_frame, width=40)
        email_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Phone (optional):").pack(pady=5)
        phone_entry = ttk.Entry(form_frame, width=40)
        phone_entry.pack(pady=5)
        
        # Submit button
        def submit_student():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Full name is required")
                return
            
            # Generate credentials
            student_id = self.auth_manager.generate_student_id()
            pin = self.auth_manager.generate_pin()
            
            if self.db.create_student(student_id, pin, name, email, phone):
                messagebox.showinfo(
                    "Success", 
                    f"Student created successfully!\n\nStudent ID: {student_id}\nPIN: {pin}\n\nPlease save these credentials securely."
                )
                # Clear form
                name_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                phone_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to create student")
        
        ttk.Button(
            form_frame,
            text="Create Student",
            bootstyle="success",
            command=submit_student
        ).pack(pady=20)
    
    def show_all_students(self):
        """Show all students in a table"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get students from database
        query = "SELECT * FROM students ORDER BY full_name"
        students = self.db.db.execute_query(query)
        
        if not students:
            ttk.Label(
                self.content_frame,
                text="No students found",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            return
        
        # Create table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Table headers
        headers = ['ID', 'Student ID', 'Name', 'Email', 'Phone']
        for i, header in enumerate(headers):
            ttk.Label(
                table_frame,
                text=header,
                font=("Segoe UI", 10, "bold")
            ).grid(row=0, column=i, padx=5, pady=5, sticky='w')
        
        # Table data
        for i, student in enumerate(students, 1):
            ttk.Label(table_frame, text=student['id']).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=student['student_id']).grid(row=i, column=1, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=student['full_name']).grid(row=i, column=2, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=student['email'] or 'N/A').grid(row=i, column=3, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=student['phone'] or 'N/A').grid(row=i, column=4, padx=5, pady=2, sticky='w')
        
        # Summary
        ttk.Label(
            self.content_frame,
            text=f"Total students: {len(students)}",
            font=("Segoe UI", 10, "italic")
        ).pack(pady=10)
    
    def show_student_credentials(self):
        """Show student credentials interface"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get students
        query = "SELECT student_id, full_name FROM students ORDER BY full_name"
        students = self.db.db.execute_query(query)
        
        if not students:
            ttk.Label(
                self.content_frame,
                text="No students found",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            return
        
        # Create selection interface
        ttk.Label(
            self.content_frame,
            text="Select a student to view credentials:",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=20)
        
        # Student list
        listbox_frame = ttk.Frame(self.content_frame)
        listbox_frame.pack(fill='both', expand=True, pady=20)
        
        listbox = tk.Listbox(listbox_frame, height=10)
        listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=listbox.yview)
        scrollbar.pack(side='right', fill='y')
        listbox.configure(yscrollcommand=scrollbar.set)
        
        # Populate listbox
        for student in students:
            listbox.insert(tk.END, f"{student['full_name']} ({student['student_id']})")
        
        # View credentials button
        def view_credentials():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a student")
                return
            
            selected_index = selection[0]
            selected_student = students[selected_index]
            
            # Get full student data
            query = "SELECT * FROM students WHERE student_id = %s"
            result = self.db.db.execute_query(query, (selected_student['student_id'],))
            
            if result:
                student = result[0]
                credentials_text = f"""
Credentials for {student['full_name']}

Student ID: {student['student_id']}
PIN: {student['pin']}
Full Name: {student['full_name']}
Email: {student['email'] or 'N/A'}
Phone: {student['phone'] or 'N/A'}

Login Instructions:
1. Select 'Student Login' from main menu
2. Enter Student ID and PIN above
                """
                
                messagebox.showinfo("Student Credentials", credentials_text)
        
        ttk.Button(
            self.content_frame,
            text="View Credentials",
            bootstyle="warning",
            command=view_credentials
        ).pack(pady=10)
    
    def show_staff_management(self):
        """Show staff management interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create staff management frame
        mgmt_frame = ttk.Frame(self.main_container)
        mgmt_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(mgmt_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="Staff Management",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_admin_dashboard
        ).pack(side='right')
        
        # Buttons
        button_frame = ttk.Frame(mgmt_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Add New Staff",
            bootstyle="success",
            command=self.show_add_staff_form
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="View All Staff",
            bootstyle="info",
            command=self.show_all_staff
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="View Staff Credentials",
            bootstyle="warning",
            command=self.show_staff_credentials
        ).pack(side='left', padx=5)
        
        # Content area
        self.content_frame = ttk.Frame(mgmt_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Show welcome message
        ttk.Label(
            self.content_frame,
            text="Select an option above to manage staff",
            font=("Segoe UI", 12)
        ).pack(expand=True)
    
    def show_add_staff_form(self):
        """Show form to add new staff"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create form
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(
            form_frame,
            text="Add New Staff",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Form fields
        ttk.Label(form_frame, text="Full Name:").pack(pady=5)
        name_entry = ttk.Entry(form_frame, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Email (optional):").pack(pady=5)
        email_entry = ttk.Entry(form_frame, width=40)
        email_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Department (optional):").pack(pady=5)
        department_entry = ttk.Entry(form_frame, width=40)
        department_entry.pack(pady=5)
        
        # Submit button
        def submit_staff():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            department = department_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Full name is required")
                return
            
            # Generate credentials
            staff_id = self.auth_manager.generate_student_id()  # Reuse the function
            pin = self.auth_manager.generate_pin()
            
            if self.db.create_staff(staff_id, pin, name, email, department):
                messagebox.showinfo(
                    "Success", 
                    f"Staff created successfully!\n\nStaff ID: {staff_id}\nPIN: {pin}\n\nPlease save these credentials securely."
                )
                # Clear form
                name_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                department_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to create staff member")
        
        ttk.Button(
            form_frame,
            text="Create Staff",
            bootstyle="success",
            command=submit_staff
        ).pack(pady=20)
    
    def show_all_staff(self):
        """Show all staff in a table"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get staff from database
        query = "SELECT * FROM staff ORDER BY full_name"
        staff_list = self.db.db.execute_query(query)
        
        if not staff_list:
            ttk.Label(
                self.content_frame,
                text="No staff found",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            return
        
        # Create table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Table headers
        headers = ['ID', 'Staff ID', 'Name', 'Email', 'Department']
        for i, header in enumerate(headers):
            ttk.Label(
                table_frame,
                text=header,
                font=("Segoe UI", 10, "bold")
            ).grid(row=0, column=i, padx=5, pady=5, sticky='w')
        
        # Table data
        for i, staff in enumerate(staff_list, 1):
            ttk.Label(table_frame, text=staff['id']).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=staff['staff_id']).grid(row=i, column=1, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=staff['full_name']).grid(row=i, column=2, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=staff['email'] or 'N/A').grid(row=i, column=3, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=staff['department'] or 'N/A').grid(row=i, column=4, padx=5, pady=2, sticky='w')
        
        # Summary
        ttk.Label(
            self.content_frame,
            text=f"Total staff: {len(staff_list)}",
            font=("Segoe UI", 10, "italic")
        ).pack(pady=10)
    
    def show_staff_credentials(self):
        """Show staff credentials interface"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get staff
        query = "SELECT staff_id, full_name FROM staff ORDER BY full_name"
        staff_list = self.db.db.execute_query(query)
        
        if not staff_list:
            ttk.Label(
                self.content_frame,
                text="No staff found",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            return
        
        # Create selection interface
        ttk.Label(
            self.content_frame,
            text="Select a staff member to view credentials:",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=20)
        
        # Staff list
        listbox_frame = ttk.Frame(self.content_frame)
        listbox_frame.pack(fill='both', expand=True, pady=20)
        
        listbox = tk.Listbox(listbox_frame, height=10)
        listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=listbox.yview)
        scrollbar.pack(side='right', fill='y')
        listbox.configure(yscrollcommand=scrollbar.set)
        
        # Populate listbox
        for staff in staff_list:
            listbox.insert(tk.END, f"{staff['full_name']} ({staff['staff_id']})")
        
        # View credentials button
        def view_credentials():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a staff member")
                return
            
            selected_index = selection[0]
            selected_staff = staff_list[selected_index]
            
            # Get full staff data
            query = "SELECT * FROM staff WHERE staff_id = %s"
            result = self.db.db.execute_query(query, (selected_staff['staff_id'],))
            
            if result:
                staff = result[0]
                credentials_text = f"""
Credentials for {staff['full_name']}

Staff ID: {staff['staff_id']}
PIN: {staff['pin']}
Full Name: {staff['full_name']}
Email: {staff['email'] or 'N/A'}
Department: {staff['department'] or 'N/A'}

Login Instructions:
1. Select 'Staff Login' from main menu
2. Enter Staff ID and PIN above
                """
                
                messagebox.showinfo("Staff Credentials", credentials_text)
        
        ttk.Button(
            self.content_frame,
            text="View Credentials",
            bootstyle="warning",
            command=view_credentials
        ).pack(pady=10)
    
    def show_course_management(self):
        """Show course management interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create course management frame
        mgmt_frame = ttk.Frame(self.main_container)
        mgmt_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(mgmt_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="Course Management",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_admin_dashboard
        ).pack(side='right')
        
        # Buttons
        button_frame = ttk.Frame(mgmt_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Add New Course",
            bootstyle="success",
            command=self.show_add_course_form
        ).pack(side='left', padx=5)
        
        ttk.Button(
            button_frame,
            text="View All Courses",
            bootstyle="info",
            command=self.show_all_courses
        ).pack(side='left', padx=5)
        
        # Content area
        self.content_frame = ttk.Frame(mgmt_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Show welcome message
        ttk.Label(
            self.content_frame,
            text="Select an option above to manage courses",
            font=("Segoe UI", 12)
        ).pack(expand=True)
    
    def show_add_course_form(self):
        """Show form to add new course"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create form
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(
            form_frame,
            text="Add New Course",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Form fields
        ttk.Label(form_frame, text="Course Code:").pack(pady=5)
        code_entry = ttk.Entry(form_frame, width=40)
        code_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Course Name:").pack(pady=5)
        name_entry = ttk.Entry(form_frame, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Credits (1-3, default 3):").pack(pady=5)
        credits_entry = ttk.Entry(form_frame, width=40)
        credits_entry.insert(0, "3")
        credits_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Description (optional):").pack(pady=5)
        desc_entry = ttk.Entry(form_frame, width=40)
        desc_entry.pack(pady=5)
        
        # Submit button
        def submit_course():
            code = code_entry.get().strip()
            name = name_entry.get().strip()
            credits = credits_entry.get().strip()
            description = desc_entry.get().strip()
            
            if not code or not name:
                messagebox.showerror("Error", "Course code and name are required")
                return
            
            try:
                credits = int(credits) if credits else 3
                if credits < 1 or credits > 3:
                    messagebox.showerror("Error", "Credits must be between 1 and 3")
                    return
            except ValueError:
                credits = 3
            
            if self.db.add_course(code, name, credits, description):
                messagebox.showinfo("Success", "Course created successfully!")
                # Clear form
                code_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                credits_entry.delete(0, tk.END)
                credits_entry.insert(0, "3")
                desc_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to create course")
        
        ttk.Button(
            form_frame,
            text="Create Course",
            bootstyle="success",
            command=submit_course
        ).pack(pady=20)
    
    def show_all_courses(self):
        """Show all courses in a table"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get courses from database
        courses = self.db.get_all_courses()
        
        if not courses:
            ttk.Label(
                self.content_frame,
                text="No courses found",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            return
        
        # Create table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Table headers
        headers = ['ID', 'Code', 'Name', 'Credits', 'Description']
        for i, header in enumerate(headers):
            ttk.Label(
                table_frame,
                text=header,
                font=("Segoe UI", 10, "bold")
            ).grid(row=0, column=i, padx=5, pady=5, sticky='w')
        
        # Table data
        for i, course in enumerate(courses, 1):
            ttk.Label(table_frame, text=course['id']).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=course['course_code']).grid(row=i, column=1, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=course['course_name']).grid(row=i, column=2, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=course['credits']).grid(row=i, column=3, padx=5, pady=2, sticky='w')
            desc = course['description'] or 'N/A'
            if len(desc) > 30:
                desc = desc[:27] + "..."
            ttk.Label(table_frame, text=desc).grid(row=i, column=4, padx=5, pady=2, sticky='w')
        
        # Summary
        ttk.Label(
            self.content_frame,
            text=f"Total courses: {len(courses)}",
            font=("Segoe UI", 10, "italic")
        ).pack(pady=10)
    
    def show_course_assignments(self):
        """Show course assignments interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create course assignments frame
        mgmt_frame = ttk.Frame(self.main_container)
        mgmt_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(mgmt_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="Course Assignments",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_admin_dashboard
        ).pack(side='right')
        
        # Content area
        self.content_frame = ttk.Frame(mgmt_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Show assignment form
        self.show_assignment_form()
    
    def show_assignment_form(self):
        """Show form to assign courses to staff"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get staff and courses
        staff_query = "SELECT * FROM staff ORDER BY full_name"
        staff_list = self.db.db.execute_query(staff_query)
        
        courses = self.db.get_all_courses()
        
        if not staff_list:
            ttk.Label(
                self.content_frame,
                text="No staff available. Please add staff first.",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            return
        
        if not courses:
            ttk.Label(
                self.content_frame,
                text="No courses available. Please add courses first.",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            return
        
        # Create form
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(
            form_frame,
            text="Assign Course to Staff",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Staff selection
        ttk.Label(form_frame, text="Select Staff:").pack(pady=5)
        staff_var = tk.StringVar()
        staff_combo = ttk.Combobox(form_frame, textvariable=staff_var, width=40, state="readonly")
        staff_combo['values'] = [f"{s['full_name']} ({s['staff_id']})" for s in staff_list]
        staff_combo.pack(pady=5)
        
        # Course selection
        ttk.Label(form_frame, text="Select Course:").pack(pady=5)
        course_var = tk.StringVar()
        course_combo = ttk.Combobox(form_frame, textvariable=course_var, width=40, state="readonly")
        course_combo['values'] = [f"{c['course_code']} - {c['course_name']}" for c in courses]
        course_combo.pack(pady=5)
        
        # Academic year
        ttk.Label(form_frame, text="Academic Year (e.g., 2023-2024):").pack(pady=5)
        year_entry = ttk.Entry(form_frame, width=40)
        year_entry.pack(pady=5)
        
        # Semester
        ttk.Label(form_frame, text="Semester:").pack(pady=5)
        semester_var = tk.StringVar()
        semester_combo = ttk.Combobox(
            form_frame,
            textvariable=semester_var,
            width=40,
            state="readonly"
        )
        semester_combo['values'] = ["First Semester", "Second Semester"]
        semester_combo.pack(pady=5)
        
        # Submit button
        def submit_assignment():
            staff_selection = staff_var.get()
            course_selection = course_var.get()
            academic_year = year_entry.get().strip()
            semester = semester_var.get()
            
            if not staff_selection or not course_selection or not academic_year or not semester:
                messagebox.showerror("Error", "All fields are required")
                return
            
            # Extract staff ID and course ID
            staff_id = staff_selection.split('(')[1].split(')')[0]
            course_code = course_selection.split(' - ')[0]
            
            # Get staff and course IDs
            staff_query = "SELECT id FROM staff WHERE staff_id = %s"
            staff_result = self.db.db.execute_query(staff_query, (staff_id,))
            
            course_query = "SELECT id FROM courses WHERE course_code = %s"
            course_result = self.db.db.execute_query(course_query, (course_code,))
            
            if not staff_result or not course_result:
                messagebox.showerror("Error", "Invalid staff or course selection")
                return
            
            staff_id = staff_result[0]['id']
            course_id = course_result[0]['id']
            
            if self.db.assign_course_to_staff(staff_id, course_id, academic_year, semester):
                messagebox.showinfo("Success", "Course assigned successfully!")
                # Clear form
                staff_var.set('')
                course_var.set('')
                year_entry.delete(0, tk.END)
                semester_var.set('')
            else:
                messagebox.showerror("Error", "Failed to assign course")
        
        ttk.Button(
            form_frame,
            text="Assign Course",
            bootstyle="success",
            command=submit_assignment
        ).pack(pady=20)
    
    def show_system_reports(self):
        """Show system reports interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create system reports frame
        mgmt_frame = ttk.Frame(self.main_container)
        mgmt_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(mgmt_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="System Reports",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_admin_dashboard
        ).pack(side='right')
        
        # Content area
        self.content_frame = ttk.Frame(mgmt_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Show reports
        self.show_reports_summary()
    
    def show_reports_summary(self):
        """Show system reports summary"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create reports frame
        reports_frame = ttk.Frame(self.content_frame)
        reports_frame.pack(expand=True)
        
        ttk.Label(
            reports_frame,
            text="System Overview",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Get counts
        students_query = "SELECT COUNT(*) as count FROM students"
        staff_query = "SELECT COUNT(*) as count FROM staff"
        courses_query = "SELECT COUNT(*) as count FROM courses"
        enrollments_query = "SELECT COUNT(*) as count FROM enrollments"
        
        students_count = self.db.db.execute_query(students_query)[0]['count']
        staff_count = self.db.db.execute_query(staff_query)[0]['count']
        courses_count = self.db.db.execute_query(courses_query)[0]['count']
        enrollments_count = self.db.db.execute_query(enrollments_query)[0]['count']
        
        # Display counts
        counts_frame = ttk.Frame(reports_frame)
        counts_frame.pack(pady=20)
        
        ttk.Label(counts_frame, text=f"Total Students: {students_count}", font=("Segoe UI", 12)).pack(pady=5)
        ttk.Label(counts_frame, text=f"Total Staff: {staff_count}", font=("Segoe UI", 12)).pack(pady=5)
        ttk.Label(counts_frame, text=f"Total Courses: {courses_count}", font=("Segoe UI", 12)).pack(pady=5)
        ttk.Label(counts_frame, text=f"Total Enrollments: {enrollments_count}", font=("Segoe UI", 12)).pack(pady=5)
        
        # Grade distribution
        grade_query = """
        SELECT grade, COUNT(*) as count 
        FROM academic_records 
        GROUP BY grade 
        ORDER BY grade
        """
        grade_distribution = self.db.db.execute_query(grade_query)
        
        if grade_distribution:
            ttk.Label(
                reports_frame,
                text="Grade Distribution:",
                font=("Segoe UI", 14, "bold")
            ).pack(pady=(20, 10))
            
            grade_frame = ttk.Frame(reports_frame)
            grade_frame.pack(pady=10)
            
            for grade in grade_distribution:
                ttk.Label(
                    grade_frame,
                    text=f"{grade['grade']}: {grade['count']} students",
                    font=("Segoe UI", 10)
                ).pack(pady=2)
        else:
            ttk.Label(
                reports_frame,
                text="No academic records found",
                font=("Segoe UI", 10, "italic")
            ).pack(pady=20)
    
    def show_legacy_system(self):
        """Show legacy system interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create legacy system frame
        mgmt_frame = ttk.Frame(self.main_container)
        mgmt_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(mgmt_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="Legacy Student Results System",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_admin_dashboard
        ).pack(side='right')
        
        # Content area
        self.content_frame = ttk.Frame(mgmt_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Show legacy options
        self.show_legacy_options()
    
    def show_legacy_options(self):
        """Show legacy system options"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create options frame
        options_frame = ttk.Frame(self.content_frame)
        options_frame.pack(expand=True)
        
        ttk.Label(
            options_frame,
            text="Legacy System Options",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Buttons
        ttk.Button(
            options_frame,
            text="View All Legacy Records",
            bootstyle="info",
            command=self.show_legacy_records
        ).pack(pady=10)
        
        ttk.Button(
            options_frame,
            text="Add Legacy Record",
            bootstyle="success",
            command=self.show_add_legacy_record
        ).pack(pady=10)
        
        ttk.Button(
            options_frame,
            text="Update Legacy Record",
            bootstyle="warning",
            command=self.show_update_legacy_record
        ).pack(pady=10)
    
    def show_legacy_records(self):
        """Show all legacy student records"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get legacy records
        query = "SELECT * FROM student_results ORDER BY full_name"
        records = self.db.db.execute_query(query)
        
        if not records:
            ttk.Label(
                self.content_frame,
                text="No legacy records found",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            return
        
        # Create table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Table headers
        headers = ['ID', 'Index Number', 'Name', 'Course', 'Score', 'Grade']
        for i, header in enumerate(headers):
            ttk.Label(
                table_frame,
                text=header,
                font=("Segoe UI", 10, "bold")
            ).grid(row=0, column=i, padx=5, pady=5, sticky='w')
        
        # Table data
        for i, record in enumerate(records, 1):
            ttk.Label(table_frame, text=record['id']).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['index_number']).grid(row=i, column=1, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['full_name']).grid(row=i, column=2, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['course']).grid(row=i, column=3, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['score']).grid(row=i, column=4, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['grade'] or 'N/A').grid(row=i, column=5, padx=5, pady=2, sticky='w')
        
        # Summary
        ttk.Label(
            self.content_frame,
            text=f"Total legacy records: {len(records)}",
            font=("Segoe UI", 10, "italic")
        ).pack(pady=10)
    
    def show_add_legacy_record(self):
        """Show form to add legacy record"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create form
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(
            form_frame,
            text="Add Legacy Record",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Form fields
        ttk.Label(form_frame, text="Index Number:").pack(pady=5)
        index_entry = ttk.Entry(form_frame, width=40)
        index_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Full Name:").pack(pady=5)
        name_entry = ttk.Entry(form_frame, width=40)
        name_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Course:").pack(pady=5)
        course_entry = ttk.Entry(form_frame, width=40)
        course_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Score (0-100):").pack(pady=5)
        score_entry = ttk.Entry(form_frame, width=40)
        score_entry.pack(pady=5)
        
        # Submit button
        def submit_legacy():
            index_number = index_entry.get().strip()
            full_name = name_entry.get().strip()
            course = course_entry.get().strip()
            score = score_entry.get().strip()
            
            if not index_number or not full_name or not course or not score:
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                score = int(score)
                if score < 0 or score > 100:
                    messagebox.showerror("Error", "Score must be between 0 and 100")
                    return
            except ValueError:
                messagebox.showerror("Error", "Score must be a number")
                return
            
            if self.db.insert_student(index_number, full_name, course, score):
                messagebox.showinfo("Success", "Legacy record created successfully!")
                # Clear form
                index_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                course_entry.delete(0, tk.END)
                score_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to create legacy record")
        
        ttk.Button(
            form_frame,
            text="Create Record",
            bootstyle="success",
            command=submit_legacy
        ).pack(pady=20)
    
    def show_update_legacy_record(self):
        """Show form to update legacy record"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create form
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(
            form_frame,
            text="Update Legacy Record",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Form fields
        ttk.Label(form_frame, text="Index Number:").pack(pady=5)
        index_entry = ttk.Entry(form_frame, width=40)
        index_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="New Score (0-100):").pack(pady=5)
        score_entry = ttk.Entry(form_frame, width=40)
        score_entry.pack(pady=5)
        
        # Submit button
        def submit_update():
            index_number = index_entry.get().strip()
            score = score_entry.get().strip()
            
            if not index_number or not score:
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                score = int(score)
                if score < 0 or score > 100:
                    messagebox.showerror("Error", "Score must be between 0 and 100")
                    return
            except ValueError:
                messagebox.showerror("Error", "Score must be a number")
                return
            
            if self.db.update_student_score(index_number, score):
                messagebox.showinfo("Success", "Legacy record updated successfully!")
                # Clear form
                index_entry.delete(0, tk.END)
                score_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to update legacy record")
        
        ttk.Button(
            form_frame,
            text="Update Record",
            bootstyle="warning",
            command=submit_update
        ).pack(pady=20)
    
    def show_staff_dashboard(self):
        """Show enhanced staff dashboard"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create staff dashboard frame with enhanced styling
        dashboard_frame = ttk.Frame(self.main_container)
        dashboard_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Enhanced header with better spacing
        header_frame = ttk.Frame(dashboard_frame)
        header_frame.pack(fill='x', pady=(0, 30))
        
        ttk.Label(
            header_frame,
            text="Staff Dashboard",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Logout",
            bootstyle="danger",
            command=self.logout
        ).pack(side='right')
        
        # Enhanced welcome message
        if self.current_user:
            ttk.Label(
                dashboard_frame,
                text=f"Welcome, {self.current_user['full_name']}!",
                font=("Segoe UI", 18)
            ).pack(pady=25)
        
        # Enhanced menu buttons with better spacing
        menu_frame = ttk.Frame(dashboard_frame)
        menu_frame.pack(fill='both', expand=True, pady=20)
        
        # Create enhanced menu grid
        buttons = [
            ("View Assigned Courses", self.show_staff_courses, "info"),
            ("Record Student Scores", self.show_score_recording, "success"),
            ("View Academic Records", self.show_academic_records, "warning")
        ]
        
        for i, (text, command, style) in enumerate(buttons):
            row = i // 2
            col = i % 2
            
            btn = ttk.Button(
                menu_frame,
                text=text,
                bootstyle=style,
                command=command,
                width=30
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky='ew')
        
        # Configure grid weights
        for i in range(2):
            menu_frame.columnconfigure(i, weight=1)
    
    def show_staff_courses(self):
        """Show courses assigned to current staff"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create courses frame
        courses_frame = ttk.Frame(self.main_container)
        courses_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(courses_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="My Assigned Courses",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_staff_dashboard
        ).pack(side='right')
        
        # Content area
        self.content_frame = ttk.Frame(courses_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Get staff courses
        if self.current_user:
            staff_id = self.current_user['id']
            courses = self.db.get_staff_courses(staff_id)
            
            if not courses:
                ttk.Label(
                    self.content_frame,
                    text="No courses assigned to you yet.",
                    font=("Segoe UI", 12)
                ).pack(expand=True)
                return
            
            # Create table
            table_frame = ttk.Frame(self.content_frame)
            table_frame.pack(fill='both', expand=True)
            
            # Table headers
            headers = ['Course Code', 'Course Name', 'Academic Year', 'Semester']
            for i, header in enumerate(headers):
                ttk.Label(
                    table_frame,
                    text=header,
                    font=("Segoe UI", 10, "bold")
                ).grid(row=0, column=i, padx=5, pady=5, sticky='w')
            
            # Table data
            for i, course in enumerate(courses, 1):
                ttk.Label(table_frame, text=course['course_code']).grid(row=i, column=0, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=course['course_name']).grid(row=i, column=1, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=course['academic_year']).grid(row=i, column=2, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=course['semester']).grid(row=i, column=3, padx=5, pady=2, sticky='w')
            
            # Summary
            ttk.Label(
                self.content_frame,
                text=f"Total assigned courses: {len(courses)}",
                font=("Segoe UI", 10, "italic")
            ).pack(pady=10)
    
    def show_score_recording(self):
        """Show score recording interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create score recording frame
        recording_frame = ttk.Frame(self.main_container)
        recording_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(recording_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="Record Student Scores",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_staff_dashboard
        ).pack(side='right')
        
        # Content area
        self.content_frame = ttk.Frame(recording_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Show recording form
        self.show_recording_form()
    
    def show_recording_form(self):
        """Show form to record student scores"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create form
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(
            form_frame,
            text="Record Student Score",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Form fields
        ttk.Label(form_frame, text="Student ID:").pack(pady=5)
        student_entry = ttk.Entry(form_frame, width=40)
        student_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Course Code:").pack(pady=5)
        course_entry = ttk.Entry(form_frame, width=40)
        course_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Academic Year:").pack(pady=5)
        year_entry = ttk.Entry(form_frame, width=40)
        year_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Semester:").pack(pady=5)
        semester_var = tk.StringVar()
        semester_combo = ttk.Combobox(
            form_frame,
            textvariable=semester_var,
            width=40,
            state="readonly"
        )
        semester_combo['values'] = ["First Semester", "Second Semester"]
        semester_combo.pack(pady=5)
        
        ttk.Label(form_frame, text="Score (0-100):").pack(pady=5)
        score_entry = ttk.Entry(form_frame, width=40)
        score_entry.pack(pady=5)
        
        # Submit button
        def submit_score():
            student_id = student_entry.get().strip()
            course_code = course_entry.get().strip()
            academic_year = year_entry.get().strip()
            semester = semester_var.get()
            score = score_entry.get().strip()
            
            if not student_id or not course_code or not academic_year or not semester or not score:
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                score = int(score)
                if score < 0 or score > 100:
                    messagebox.showerror("Error", "Score must be between 0 and 100")
                    return
            except ValueError:
                messagebox.showerror("Error", "Score must be a number")
                return
            
            # Get student and course IDs
            student_query = "SELECT id FROM students WHERE student_id = %s"
            student_result = self.db.db.execute_query(student_query, (student_id,))
            
            course_query = "SELECT id FROM courses WHERE course_code = %s"
            course_result = self.db.db.execute_query(course_query, (course_code,))
            
            if not student_result or not course_result:
                messagebox.showerror("Error", "Invalid student ID or course code")
                return
            
            student_id = student_result[0]['id']
            course_id = course_result[0]['id']
            staff_id = self.current_user['id']
            
            if self.db.record_student_score(student_id, course_id, staff_id, academic_year, semester, score):
                messagebox.showinfo("Success", "Score recorded successfully!")
                # Clear form
                student_entry.delete(0, tk.END)
                course_entry.delete(0, tk.END)
                year_entry.delete(0, tk.END)
                semester_var.set('')
                score_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to record score")
        
        ttk.Button(
            form_frame,
            text="Record Score",
            bootstyle="success",
            command=submit_score
        ).pack(pady=20)
    
    def show_academic_records(self):
        """Show academic records interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create academic records frame
        records_frame = ttk.Frame(self.main_container)
        records_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(records_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="Academic Records",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_staff_dashboard
        ).pack(side='right')
        
        # Content area
        self.content_frame = ttk.Frame(records_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Show records
        self.show_records_summary()
    
    def show_records_summary(self):
        """Show academic records summary"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get all academic records
        query = """
        SELECT ar.*, s.full_name as student_name, c.course_name, st.full_name as staff_name
        FROM academic_records ar
        JOIN students s ON ar.student_id = s.id
        JOIN courses c ON ar.course_id = c.id
        JOIN staff st ON ar.staff_id = st.id
        ORDER BY ar.recorded_at DESC
        """
        records = self.db.db.execute_query(query)
        
        if not records:
            ttk.Label(
                self.content_frame,
                text="No academic records found",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            return
        
        # Create table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True)
        
        # Table headers
        headers = ['Student', 'Course', 'Score', 'Grade', 'GPA Points', 'Academic Year', 'Semester']
        for i, header in enumerate(headers):
            ttk.Label(
                table_frame,
                text=header,
                font=("Segoe UI", 10, "bold")
            ).grid(row=0, column=i, padx=5, pady=5, sticky='w')
        
        # Table data
        for i, record in enumerate(records, 1):
            ttk.Label(table_frame, text=record['student_name']).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['course_name']).grid(row=i, column=1, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['score']).grid(row=i, column=2, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['grade']).grid(row=i, column=3, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['gpa_points']).grid(row=i, column=4, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['academic_year']).grid(row=i, column=5, padx=5, pady=2, sticky='w')
            ttk.Label(table_frame, text=record['semester']).grid(row=i, column=6, padx=5, pady=2, sticky='w')
        
        # Summary
        ttk.Label(
            self.content_frame,
            text=f"Total academic records: {len(records)}",
            font=("Segoe UI", 10, "italic")
        ).pack(pady=10)
    
    def show_student_dashboard(self):
        """Show enhanced student dashboard"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create student dashboard frame with enhanced styling
        dashboard_frame = ttk.Frame(self.main_container)
        dashboard_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Enhanced header with better spacing
        header_frame = ttk.Frame(dashboard_frame)
        header_frame.pack(fill='x', pady=(0, 30))
        
        ttk.Label(
            header_frame,
            text="Student Dashboard",
            font=("Segoe UI", 28, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Logout",
            bootstyle="danger",
            command=self.logout
        ).pack(side='right')
        
        # Enhanced welcome message
        if self.current_user:
            ttk.Label(
                dashboard_frame,
                text=f"Welcome, {self.current_user['full_name']}!",
                font=("Segoe UI", 18)
            ).pack(pady=25)
        
        # Enhanced menu buttons with better spacing
        menu_frame = ttk.Frame(dashboard_frame)
        menu_frame.pack(fill='both', expand=True, pady=20)
        
        # Create enhanced menu grid
        buttons = [
            ("View My Grades", self.show_student_grades, "info"),
            ("View My GPA", self.show_student_gpa, "success"),
            ("View Enrolled Courses", self.show_student_courses, "warning"),
            ("Enroll in Courses", self.show_course_enrollment, "primary")
        ]
        
        for i, (text, command, style) in enumerate(buttons):
            row = i // 2
            col = i % 2
            
            btn = ttk.Button(
                menu_frame,
                text=text,
                bootstyle=style,
                command=command,
                width=30
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky='ew')
        
        # Configure grid weights
        for i in range(2):
            menu_frame.columnconfigure(i, weight=1)
    
    def show_student_grades(self):
        """Show student grades"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create grades frame
        grades_frame = ttk.Frame(self.main_container)
        grades_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(grades_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="My Grades",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_student_dashboard
        ).pack(side='right')
        
        # Content area
        self.content_frame = ttk.Frame(grades_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Get student grades
        if self.current_user:
            student_id = self.current_user['id']
            records = self.db.get_student_academic_record(student_id)
            
            if not records:
                ttk.Label(
                    self.content_frame,
                    text="No grades found for you yet.",
                    font=("Segoe UI", 12)
                ).pack(expand=True)
                return
            
            # Create table
            table_frame = ttk.Frame(self.content_frame)
            table_frame.pack(fill='both', expand=True)
            
            # Table headers
            headers = ['Course', 'Score', 'Grade', 'GPA Points', 'Credits', 'Academic Year', 'Semester']
            for i, header in enumerate(headers):
                ttk.Label(
                    table_frame,
                    text=header,
                    font=("Segoe UI", 10, "bold")
                ).grid(row=0, column=i, padx=5, pady=5, sticky='w')
            
            # Table data
            for i, record in enumerate(records, 1):
                ttk.Label(table_frame, text=record['course_name']).grid(row=i, column=0, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=record['score']).grid(row=i, column=1, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=record['grade']).grid(row=i, column=2, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=record['gpa_points']).grid(row=i, column=3, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=record['credits']).grid(row=i, column=4, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=record['academic_year']).grid(row=i, column=5, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=record['semester']).grid(row=i, column=6, padx=5, pady=2, sticky='w')
            
            # Summary
            ttk.Label(
                self.content_frame,
                text=f"Total grades: {len(records)}",
                font=("Segoe UI", 10, "italic")
            ).pack(pady=10)
    
    def show_student_gpa(self):
        """Show student GPA"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create GPA frame
        gpa_frame = ttk.Frame(self.main_container)
        gpa_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(gpa_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="My GPA",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_student_dashboard
        ).pack(side='right')
        
        # Content area
        self.content_frame = ttk.Frame(gpa_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Get student GPA
        if self.current_user:
            student_id = self.current_user['id']
            gpa = self.db.calculate_student_gpa(student_id)
            
            # Create GPA display
            gpa_display = ttk.Frame(self.content_frame)
            gpa_display.pack(expand=True)
            
            ttk.Label(
                gpa_display,
                text="Your Cumulative GPA",
                font=("Segoe UI", 16, "bold")
            ).pack(pady=20)
            
            ttk.Label(
                gpa_display,
                text=f"{gpa:.2f}",
                font=("Segoe UI", 48, "bold"),
                bootstyle="success"
            ).pack(pady=20)
            
            ttk.Label(
                gpa_display,
                text="(4.0 Scale)",
                font=("Segoe UI", 12, "italic")
            ).pack(pady=10)
    
    def show_student_courses(self):
        """Show student enrolled courses"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create courses frame
        courses_frame = ttk.Frame(self.main_container)
        courses_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(courses_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="My Enrolled Courses",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_student_dashboard
        ).pack(side='right')
        
        # Content area
        self.content_frame = ttk.Frame(courses_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Get student enrollments
        if self.current_user:
            student_id = self.current_user['id']
            enrollments = self.db.get_student_enrollments(student_id)
            
            if not enrollments:
                ttk.Label(
                    self.content_frame,
                    text="You are not enrolled in any courses yet.",
                    font=("Segoe UI", 12)
                ).pack(expand=True)
                return
            
            # Create table
            table_frame = ttk.Frame(self.content_frame)
            table_frame.pack(fill='both', expand=True)
            
            # Table headers
            headers = ['Course Code', 'Course Name', 'Credits', 'Academic Year', 'Semester', 'Enrollment Date']
            for i, header in enumerate(headers):
                ttk.Label(
                    table_frame,
                    text=header,
                    font=("Segoe UI", 10, "bold")
                ).grid(row=0, column=i, padx=5, pady=5, sticky='w')
            
            # Table data
            for i, enrollment in enumerate(enrollments, 1):
                ttk.Label(table_frame, text=enrollment['course_code']).grid(row=i, column=0, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=enrollment['course_name']).grid(row=i, column=1, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=enrollment['credits']).grid(row=i, column=2, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=enrollment['academic_year']).grid(row=i, column=3, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=enrollment['semester']).grid(row=i, column=4, padx=5, pady=2, sticky='w')
                ttk.Label(table_frame, text=str(enrollment['enrollment_date'])[:10]).grid(row=i, column=5, padx=5, pady=2, sticky='w')
            
            # Summary
            ttk.Label(
                self.content_frame,
                text=f"Total enrolled courses: {len(enrollments)}",
                font=("Segoe UI", 10, "italic")
            ).pack(pady=10)
    
    def show_course_enrollment(self):
        """Show course enrollment interface"""
        # Clear main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Create enrollment frame
        enrollment_frame = ttk.Frame(self.main_container)
        enrollment_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(enrollment_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="Course Enrollment",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary"
        ).pack(side='left')
        
        ttk.Button(
            header_frame,
            text="Back to Dashboard",
            bootstyle="secondary",
            command=self.show_student_dashboard
        ).pack(side='right')
        
        ttk.Button(
            header_frame,
            text="Refresh",
            bootstyle="info-outline",
            command=self.show_enrollment_form
        ).pack(side='right', padx=(0, 10))
        
        # Content area
        self.content_frame = ttk.Frame(enrollment_frame)
        self.content_frame.pack(fill='both', expand=True, pady=20)
        
        # Show enrollment form
        self.show_enrollment_form()
    
    def show_enrollment_form(self):
        """Show form to enroll in courses"""
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create form
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(expand=True)
        
        ttk.Label(
            form_frame,
            text="Enroll in a Course",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=20)
        
        # Get available courses
        courses = self.db.get_all_courses()
        if not courses:
            ttk.Label(
                form_frame,
                text="No courses available for enrollment.",
                font=("Segoe UI", 12)
            ).pack(pady=20)
            return
        
        # Course selection
        ttk.Label(form_frame, text="Select Course:").pack(pady=5)
        course_var = tk.StringVar()
        course_combo = ttk.Combobox(
            form_frame, 
            textvariable=course_var,
            width=40,
            state="readonly"
        )
        course_combo['values'] = [f"{course['course_code']} - {course['course_name']}" for course in courses]
        course_combo.pack(pady=5)
        
        # Academic year
        ttk.Label(form_frame, text="Academic Year:").pack(pady=5)
        year_entry = ttk.Entry(form_frame, width=40)
        year_entry.pack(pady=5)
        year_entry.insert(0, "2024")  # Default year
        
        # Semester selection
        ttk.Label(form_frame, text="Semester:").pack(pady=5)
        semester_var = tk.StringVar()
        semester_combo = ttk.Combobox(
            form_frame,
            textvariable=semester_var,
            width=40,
            state="readonly"
        )
        semester_combo['values'] = ["First Semester", "Second Semester"]
        semester_combo.pack(pady=5)
        
        # Submit button
        def submit_enrollment():
            selected_course = course_var.get()
            academic_year = year_entry.get().strip()
            semester = semester_var.get()
            
            if not selected_course or not academic_year or not semester:
                messagebox.showerror("Error", "All fields are required")
                return
            
            # Extract course code from selection
            course_code = selected_course.split(" - ")[0]
            
            # Get course ID
            course_query = "SELECT id FROM courses WHERE course_code = %s"
            course_result = self.db.db.execute_query(course_query, (course_code,))
            
            if not course_result:
                messagebox.showerror("Error", "Invalid course selection")
                return
            
            course_id = course_result[0]['id']
            student_id = self.current_user['id']
            
            # Check if already enrolled
            enrollment_query = """
            SELECT * FROM enrollments 
            WHERE student_id = %s AND course_id = %s AND academic_year = %s AND semester = %s
            """
            existing = self.db.db.execute_query(enrollment_query, (student_id, course_id, academic_year, semester))
            
            if existing:
                messagebox.showerror("Error", "You are already enrolled in this course for the specified period")
                return
            
            # Enroll student
            if self.db.enroll_student(student_id, course_id, academic_year, semester):
                messagebox.showinfo("Success", "Successfully enrolled in the course!")
                # Clear form
                course_var.set("")
                year_entry.delete(0, tk.END)
                year_entry.insert(0, "2024")
                semester_var.set("")
            else:
                messagebox.showerror("Error", "Failed to enroll in course")
        
        ttk.Button(
            form_frame,
            text="Enroll in Course",
            bootstyle="success",
            command=submit_enrollment
        ).pack(pady=20)
        
        # Show current enrollments
        ttk.Separator(form_frame, orient='horizontal').pack(fill='x', pady=20)
        
        ttk.Label(
            form_frame,
            text="Your Current Enrollments",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)
        
        # Get current enrollments
        if self.current_user:
            student_id = self.current_user['id']
            enrollments = self.db.get_student_enrollments(student_id)
            
            if not enrollments:
                ttk.Label(
                    form_frame,
                    text="You are not enrolled in any courses yet.",
                    font=("Segoe UI", 12)
                ).pack(pady=10)
            else:
                # Create enrollments list with unenroll buttons
                for enrollment in enrollments:
                    enrollment_frame = ttk.Frame(form_frame)
                    enrollment_frame.pack(fill='x', pady=2)
                    
                    enrollment_text = f"{enrollment['course_code']} - {enrollment['course_name']} ({enrollment['academic_year']}, {enrollment['semester']})"
                    ttk.Label(
                        enrollment_frame,
                        text=enrollment_text,
                        font=("Segoe UI", 10)
                    ).pack(side='left', padx=(0, 10))
                    
                    def unenroll_course(course_id=enrollment['course_id'], 
                                      academic_year=enrollment['academic_year'], 
                                      semester=enrollment['semester']):
                        """Unenroll from a specific course"""
                        if messagebox.askyesno("Confirm Unenrollment", 
                                             f"Are you sure you want to unenroll from {enrollment['course_code']} - {enrollment['course_name']}?"):
                            if self.db.unenroll_student(student_id, course_id, academic_year, semester):
                                messagebox.showinfo("Success", "Successfully unenrolled from the course!")
                                # Refresh the enrollment list
                                self.show_enrollment_form()
                            else:
                                messagebox.showerror("Error", "Failed to unenroll from course")
                    
                    ttk.Button(
                        enrollment_frame,
                        text="Unenroll",
                        bootstyle="danger-outline",
                        command=unenroll_course
                    ).pack(side='right')
    
    def logout(self):
        """Logout current user with confirmation"""
        if self.current_user:
            user_name = self.current_user.get('name', 'User')
            if messagebox.askyesno("Confirm Logout", f"Are you sure you want to logout, {user_name}?"):
                self.auth_manager.logout()
                self.current_user = None
                self.user_type = None
                messagebox.showinfo("Logged Out", "You have been successfully logged out.")
                self.show_login_screen()
        else:
            self.auth_manager.logout()
            self.current_user = None
            self.user_type = None
            self.show_login_screen()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function to start the GUI application"""
    try:
        # Start GUI (database connection is handled in constructor)
        app = StudentManagementGUI()
        app.run()
        
    except Exception as e:
        messagebox.showerror("Error", f"Application error: {str(e)}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 