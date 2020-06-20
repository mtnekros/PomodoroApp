import tkinter as tk
from tkinter import ttk

class StartFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.is_active = False
        # add start button
        self.controller = root
        ttk.Button(self, text="Start Timer", command=self.controller.go_to_timer_page).place(relx=0.5, rely=0.5, anchor="center", width=100, height=30)
    
    def set_active(self, active: bool):
        self.is_active = active