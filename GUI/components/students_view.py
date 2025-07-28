import ttkbootstrap as tb
from ttkbootstrap.constants import *
from database.operations import StudentResultsDB
from utils.grade_calculator import validate_score
from tkinter import messagebox, simpledialog

class StudentsView(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = StudentResultsDB()
        self.db.connect()
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        tb.Label(self, text='Students', font=('Segoe UI', 18, 'bold')).pack(pady=10)
        # Table
        columns = ('index_number', 'full_name', 'course', 'score', 'grade')
        self.table = tb.Treeview(self, columns=columns, show='headings', height=12, bootstyle=PRIMARY)
        for col in columns:
            self.table.heading(col, text=col.replace('_', ' ').title())
            self.table.column(col, width=120, anchor='center')
        self.table.pack(pady=10, padx=10, fill='x')
        # Buttons
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=10)
        tb.Button(btn_frame, text='Add Student', bootstyle=SUCCESS, command=self.add_student).pack(side='left', padx=5)
        tb.Button(btn_frame, text='Update Score', bootstyle=WARNING, command=self.update_score).pack(side='left', padx=5)
        tb.Button(btn_frame, text='Delete Student', bootstyle=DANGER, command=self.delete_student).pack(side='left', padx=5)
        tb.Button(btn_frame, text='Refresh', bootstyle=SECONDARY, command=self.refresh_table).pack(side='left', padx=5)

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        students = self.db.get_all_students() or []
        for student in students:
            self.table.insert('', 'end', values=(student['index_number'], student['full_name'], student['course'], student['score'], student['grade']))

    def add_student(self):
        # Simple dialogs for input
        index_number = simpledialog.askstring('Index Number', 'Enter index number:')
        if not index_number:
            return
        if self.db.student_exists(index_number):
            messagebox.showerror('Error', f'Student {index_number} already exists.')
            return
        full_name = simpledialog.askstring('Full Name', 'Enter full name:')
        if not full_name:
            return
        course = simpledialog.askstring('Course', 'Enter course:')
        if not course:
            return
        score = simpledialog.askstring('Score', 'Enter score (0-100):')
        if not validate_score(score):
            messagebox.showerror('Error', 'Invalid score. Please enter a number between 0 and 100.')
            return
        if self.db.insert_student(index_number, full_name, course, int(score)):
            messagebox.showinfo('Success', 'Student added successfully!')
            self.refresh_table()
        else:
            messagebox.showerror('Error', 'Failed to add student.')

    def update_score(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror('Error', 'Select a student to update.')
            return
        index_number = self.table.item(selected[0])['values'][0]
        new_score = simpledialog.askstring('Update Score', 'Enter new score (0-100):')
        if not validate_score(new_score):
            messagebox.showerror('Error', 'Invalid score. Please enter a number between 0 and 100.')
            return
        if self.db.update_student_score(index_number, int(new_score)):
            messagebox.showinfo('Success', f'Student {index_number} score updated!')
            self.refresh_table()
        else:
            messagebox.showerror('Error', 'Failed to update score.')

    def delete_student(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror('Error', 'Select a student to delete.')
            return
        index_number = self.table.item(selected[0])['values'][0]
        confirm = messagebox.askyesno('Delete Student', f'Are you sure you want to delete student {index_number}?')
        if confirm:
            if self.db.delete_student(index_number):
                messagebox.showinfo('Success', 'Student deleted.')
                self.refresh_table()
            else:
                messagebox.showerror('Error', 'Failed to delete student.')

    def destroy(self):
        self.db.close()
        super().destroy() 