import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title('Student Result Management System')
        self.geometry('900x650')
        self.resizable(False, False)
        self.frames = {}
        self._init_frames()
        self.show_frame('LoginScreen')

    def _init_frames(self):
        from GUI.screens.login import LoginScreen
        from GUI.screens.signup import SignupScreen
        from GUI.screens.dashboard import DashboardScreen
        container = tb.Frame(self)
        container.pack(fill='both', expand=True)
        for F in (LoginScreen, SignupScreen, DashboardScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == '__main__':
    app = App()
    app.mainloop() 
    