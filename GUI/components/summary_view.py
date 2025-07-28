import ttkbootstrap as tb
from ttkbootstrap.constants import *
from database.operations import StudentResultsDB
from utils.grade_calculator import get_grade_description
from utils.file_handler import write_summary_report
from tkinter import messagebox

class SummaryView(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = StudentResultsDB()
        self.db.connect()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self, text='Summary', font=('Segoe UI', 18, 'bold')).pack(pady=10)
        total = self.db.get_total_students()
        tb.Label(self, text=f'Total Students: {total}', font=('Segoe UI', 14)).pack(pady=5)
        # Grade distribution
        dist = self.db.get_grade_distribution() or []
        dist_dict = {d['grade']: d['count'] for d in dist}
        grades = ['A', 'B', 'C', 'D', 'F']
        dist_str = '  '.join([f"{g}: {dist_dict.get(g, 0)}" for g in grades])
        tb.Label(self, text=f'Grade Distribution: {dist_str}', font=('Segoe UI', 12)).pack(pady=5)
        # Download summary button
        tb.Button(self, text='Download Summary Report', bootstyle=PRIMARY, command=self.download_summary).pack(pady=10)
        # Table of students
        tb.Label(self, text='Student List', font=('Segoe UI', 14, 'bold')).pack(pady=(15, 5))
        columns = ('full_name', 'index_number', 'course', 'score', 'grade')
        table = tb.Treeview(self, columns=columns, show='headings', height=10, bootstyle=PRIMARY)
        for col in columns:
            table.heading(col, text=col.replace('_', ' ').title())
            table.column(col, width=120, anchor='center')
        table.pack(pady=10, padx=10, fill='x')
        students = self.db.get_all_students() or []
        for student in students:
            table.insert('', 'end', values=(student['full_name'], student['index_number'], student['course'], student['score'], f"{student['grade']} - {get_grade_description(student['grade'])}"))

    def download_summary(self):
        total = self.db.get_total_students()
        dist = self.db.get_grade_distribution() or []
        path = write_summary_report(total, dist)
        if path:
            messagebox.showinfo('Summary Report', f'Summary report saved to:\n{path}')
        else:
            messagebox.showerror('Error', 'Failed to save summary report.')

    def destroy(self):
        self.db.close()
        super().destroy() 