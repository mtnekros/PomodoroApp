from tkinter import Toplevel, Label, StringVar, Frame
from timer import Timer
import time

class MessageModal(Toplevel):
    is_already_open = False

    def __init__(self, timer):
        super().__init__(bg="black")
        # add msg
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
        self.bind("<Motion>", lambda event: self.close())
        self.update()

    def set_up_modal_attributes(self):
        # change opacity
        self.wm_attributes("-alpha", 0.9)
        self.wm_attributes("-transparentcolor", 'black')
        # bring to top
        self.attributes("-topmost", True)
        # self.attributes("-topmost", False)
        # set fullscreen
        self.attributes("-fullscreen", True)
        self.focus_set()

    def create_widgets(self):
        self.frame = Frame(self,  bg="#111")
        self.frame.place(relx=.5, rely=.5, anchor="center", width=440, height=210)
        self.time_label_var = StringVar(self.frame)
        self.time_label = Label(self.frame, textvariable=self.time_label_var, bg="#111", foreground="white", font=("Cookie", 75))
        self.time_label.place(relx=.5, rely=.45, anchor="center")
        caption = Label(self.frame, text="Time to take a break.", bg="#111", foreground="white", font=("Century Gothic", 14))
        caption.place(relx=.5, y=145, anchor="center")
    
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
