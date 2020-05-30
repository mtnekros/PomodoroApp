from tkinter import Toplevel, Label
import time

class MessageModal(Toplevel):
    def __init__(self, title, msg, life_time):
        super().__init__()
        self.title(title)
        self.__is_open = True
        # add msg
        self.msg = Label(self, text=msg, bg="#999", foreground="#000", font=("Arial Rounded MT", 22))
        self.msg.place(relx=.5, rely=.5, anchor="center", relheight=1, relwidth=1)
        # change opacity
        self.wm_attributes("-alpha", 0.6)
        # bring to top
        self.attributes("-topmost", 1)
        self.attributes("-topmost", 0)
        # set fullscreen
        self.attributes("-fullscreen", True)
        # add event listeners for closing
        self.focus_set()
        self.after(life_time, self.close)
        time.sleep(3)
        self.bind("<Escape>", lambda event: self.close())
        self.bind("<Motion>", lambda event: self.close())

    def close(self):
        if self.__is_open:
            self.__is_open = False
            self.destroy()
        