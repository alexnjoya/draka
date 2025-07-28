import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from GUI.services.user_service import UserService

class SignupScreen(tb.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_service = UserService()

        # Card at the top center with padding
        card = tb.Frame(self, bootstyle="light", borderwidth=1, relief="solid")
        card.pack(pady=60, padx=0, anchor='n')

        # Optional: Logo or icon
        # tb.Label(card, text='📝', font=('Segoe UI Emoji', 40)).pack(pady=(20, 0))

        tb.Label(card, text='Sign Up', font=('Segoe UI', 24, 'bold')).pack(pady=(30, 10))

        form = tb.Frame(card, bootstyle="light")
        form.pack(pady=10)
        tb.Label(form, text='Username', font=('Segoe UI', 12)).grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.username_entry = tb.Entry(form, width=28, bootstyle=PRIMARY)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        tb.Label(form, text='Email', font=('Segoe UI', 12)).grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.email_entry = tb.Entry(form, width=28, bootstyle=PRIMARY)
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)
        tb.Label(form, text='Password', font=('Segoe UI', 12)).grid(row=2, column=0, sticky='e', padx=10, pady=10)
        self.password_entry = tb.Entry(form, show='*', width=28, bootstyle=PRIMARY)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        btn_frame = tb.Frame(card, bootstyle="light")
        btn_frame.pack(pady=20)
        tb.Button(btn_frame, text='Sign Up', bootstyle=SUCCESS, width=14, command=self.signup).grid(row=0, column=0, padx=8)
        tb.Button(btn_frame, text='Back to Login', bootstyle=SECONDARY, width=14, command=lambda: controller.show_frame('LoginScreen')).grid(row=0, column=1, padx=8)

    def signup(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        result = self.user_service.signup(username, email, password)
        if result is True:
            messagebox.showinfo('Sign Up', 'Account created!')
            self.controller.show_frame('LoginScreen')
        else:
            messagebox.showerror('Sign Up Failed', result) 