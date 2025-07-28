import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from utils.file_handler import read_student_data
from database.operations import StudentResultsDB

class ImportView(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = StudentResultsDB()
        self.db.connect()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self, text='Import Students from File', font=('Segoe UI', 18, 'bold')).pack(pady=20)
        tb.Button(self, text='Select File', bootstyle=PRIMARY, command=self.import_file).pack(pady=10)
        self.summary_label = tb.Label(self, text='', font=('Segoe UI', 12))
        self.summary_label.pack(pady=10)

    def import_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV/TXT Files', '*.csv *.txt')])
        if not file_path:
            return
        students = read_student_data(file_path)
        if not students:
            messagebox.showerror('Import Error', 'No valid student data found in file.')
            return
        success_count = 0
        duplicate_count = 0
        error_count = 0
        for student in students:
            try:
                if self.db.student_exists(student['index_number']):
                    duplicate_count += 1
                    continue
                if self.db.insert_student(
                    student['index_number'],
                    student['full_name'],
                    student['course'],
                    student['score']
                ):
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
        summary = f"Import complete!\nSuccessfully inserted: {success_count}\nDuplicates skipped: {duplicate_count}\nErrors: {error_count}"
        self.summary_label.config(text=summary)
        messagebox.showinfo('Import Summary', summary)

    def destroy(self):
        self.db.close()
        super().destroy() 