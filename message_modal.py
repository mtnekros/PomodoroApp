from tkinter import Toplevel, Label, StringVar, Frame
import tkinter as tk
from timer import Timer
import time

class MessageModal(Toplevel):
    is_already_open = False

    def __init__(self, root, time_label_var, modal_should_close):
        super().__init__(root, bg="white")
        if MessageModal.is_already_open:
            self.destroy()
            return
        MessageModal.is_already_open = True
        self.__is_open = True
        self.modal_should_close = modal_should_close
        self.set_up_modal_attributes()
        self.create_widgets(time_label_var)
        self.bind_hide_events()
        self.hide()

    def set_up_modal_attributes(self):
        # settup the semitransparent background
        self.wm_attributes("-alpha", 0.3)
        self.wm_attributes("-fullscreen", True)
        self.wm_overrideredirect(True) # hide from taskbar
        # setting up the top layer in front of the background
        self.container = Toplevel(self, bg='magenta')
        self.container.attributes("-fullscreen", True)
        self.container.wm_attributes("-alpha", 0.85)
        self.container.wm_attributes("-transparentcolor", 'magenta')
        self.container.overrideredirect(True) # hide from taskbar

    def create_widgets(self, time_label_var):
        self.frame = Frame(self.container,  bg="#111")
        self.frame.place(relx=.5, rely=.5, anchor="center", width=440, height=210)
        self.time_label = Label(self.frame, textvariable=time_label_var, bg="#111", foreground="white", font=("Cookie", 75))
        self.time_label.place(relx=.5, rely=.43, anchor="center")
        caption = Label(self.frame, text="Time to take a break.", bg="#111", foreground="white", font=("Century Gothic", 13))
        caption.place(relx=.5, rely=.7, anchor="center")

    def bind_hide_events(self):
        hide = lambda _ : self.hide()
        self.bind("<Escape>", hide)
        self.bind("<space>", hide)
        self.container.bind("<Escape>", hide)
        self.container.bind("<space>", hide)
    
    def show(self):
        self.focus_set()
        self.deiconify()
        self.container.deiconify()
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        self.container.attributes("-topmost", True)

    def hide(self):
        self.withdraw()
        self.container.withdraw()
