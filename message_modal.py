from tkinter import Toplevel, Label, StringVar, Frame
import tkinter as tk
from timer import Timer
import time

class MessageModal(Toplevel):
    is_already_open = False

    def __init__(self, timer):
        super().__init__( bg="white")
        self.set_up_modal_attributes()
        if MessageModal.is_already_open:
            self.destroy()
            return
        MessageModal.is_already_open = True
        self.__is_open = True
        self.timer = timer
        self.timer_mode = timer.get_mode()
        self.create_widgets()
        # add event listeners for closing
        self.bind("<Escape>", lambda event: self.close())
        self.bind("<space>", lambda event: self.close())
        self.update()

    def set_up_modal_attributes(self):
        # settup the semitransparent background
        self.wm_attributes("-alpha", 0.3)
        self.wm_attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        self.wm_overrideredirect(True) # hide from taskbar
        self.focus_set()
        # setting up the top layer in front of the background
        self.container = Toplevel(self, bg='magenta')
        self.container.attributes("-fullscreen", True)
        self.container.wm_attributes("-alpha", 0.85)
        self.container.wm_attributes("-transparentcolor", 'magenta')
        self.container.attributes("-topmost", True)
        self.container.overrideredirect(True) # hide from taskbar

    def create_widgets(self):
        self.frame = Frame(self.container,  bg="#111")
        self.frame.place(relx=.5, rely=.5, anchor="center", width=440, height=210)
        self.time_label_var = StringVar(self.frame)
        self.time_label = Label(self.frame, textvariable=self.time_label_var, bg="#111", foreground="white", font=("Cookie", 75))
        self.time_label.place(relx=.5, rely=.43, anchor="center")
        caption = Label(self.frame, text="Time to take a break.", bg="#111", foreground="white", font=("Century Gothic", 13))
        caption.place(relx=.5, rely=.7, anchor="center")
    
    def update(self):
        if not self.timer.is_running():
            self.close()
        if self.__is_open:
            time_left = self.timer.get_time_left()
            self.time_label_var.set( Timer.format_time( time_left ) )
            if self.timer.get_mode() != self.timer_mode:
                self.close()
            else:
                self.after(10, self.update)

    def close(self):
        if self.__is_open:
            self.__is_open = False
            self.unbind("<Escape>")
            self.unbind("<Motion>")
            MessageModal.is_already_open = False
            self.destroy()
