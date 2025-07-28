import ttkbootstrap as tb
from ttkbootstrap.constants import *
from GUI.components.students_view import StudentsView
from GUI.components.import_view import ImportView
from GUI.components.summary_view import SummaryView

class DashboardScreen(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Sidebar
        sidebar = tb.Frame(self, bootstyle=SECONDARY, width=180)
        sidebar.pack(side='left', fill='y')
        tb.Label(sidebar, text='Dashboard', font=('Segoe UI', 18, 'bold'), bootstyle=INVERSE).pack(pady=(30, 10), padx=10)
        tb.Button(sidebar, text='Students', bootstyle=OUTLINE, width=16, command=self.show_students).pack(pady=10, padx=10)
        tb.Button(sidebar, text='Import Data', bootstyle=OUTLINE, width=16, command=self.show_import).pack(pady=10, padx=10)
        tb.Button(sidebar, text='Summary', bootstyle=OUTLINE, width=16, command=self.show_summary).pack(pady=10, padx=10)
        tb.Button(sidebar, text='Logout', bootstyle=DANGER, width=16, command=lambda: controller.show_frame('LoginScreen')).pack(pady=(40, 10), padx=10)
        # Main content area
        self.main = tb.Frame(self)
        self.main.pack(side='left', fill='both', expand=True)
        self.current_view = None
        self.current_widget = None
        self.show_students()

    def clear_main(self):
        if self.current_widget:
            self.current_widget.destroy()
            self.current_widget = None
        for widget in self.main.winfo_children():
            widget.destroy()

    def show_students(self):
        self.clear_main()
        self.current_widget = StudentsView(self.main)
        self.current_widget.pack(fill='both', expand=True)
        self.current_view = 'students'

    def show_import(self):
        self.clear_main()
        self.current_widget = ImportView(self.main)
        self.current_widget.pack(fill='both', expand=True)
        self.current_view = 'import'

    def show_summary(self):
        self.clear_main()
        self.current_widget = SummaryView(self.main)
        self.current_widget.pack(fill='both', expand=True)
        self.current_view = 'summary' 