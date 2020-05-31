from tkinter import Toplevel, Label, StringVar, Frame
from timer import Timer
import time

class MessageModal(Toplevel):
    def __init__(self, life_time, timer):
        super().__init__(bg="black")
        # change opacity
        self.wm_attributes("-alpha", 0.9)
        self.wm_attributes("-transparentcolor", 'black')
        # bring to top
        self.attributes("-topmost", 1)
        self.attributes("-topmost", 0)
        # set fullscreen
        self.attributes("-fullscreen", True)
        self.focus_set()
        # add msg
        self.__is_open = True
        self.timer = timer
        self.create_widgets()
        # add event listeners for closing
        self.bind("<Escape>", lambda event: self.close())
        self.bind("<Motion>", lambda event: self.close())
        self.update()

    def create_widgets(self):
        self.frame = Frame(self,  bg="#111")
        self.frame.place(relx=.5, rely=.5, anchor="center", width=440, height=210)
        self.time_label_var = StringVar(self.frame)
        self.time_label = Label(self.frame, textvariable=self.time_label_var, bg="#111", foreground="white", font=("Cookie", 75))
        self.time_label.place(relx=.5, rely=.45, anchor="center")
        caption = Label(self.frame, text="Time to take a break.", bg="#111", foreground="white", font=("Century Gothic", 14))
        caption.place(relx=.5, y=145, anchor="center")
    
    def update(self):
        if self.__is_open and not self.timer.is_running():
            self.close()
        if self.__is_open:
            time_left = self.timer.get_time_left()
            self.time_label_var.set( Timer.format_time( time_left ) )
            if self.timer.get_mode() == Timer.POMODORO:
                self.close()
            else:
                self.after(100, self.update)

    def close(self):
        if self.__is_open:
            self.__is_open = False
            self.unbind("<Escape>")
            self.unbind("<Motion>")
            self.destroy()
