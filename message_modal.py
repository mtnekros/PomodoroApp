from tkinter import Toplevel, Label

class MessageModal(Toplevel):
    def __init__(self, title, msg, life_time):
        super().__init__()
        self.title(title)
        self.is_open = True
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
        self.bind("<Escape>", lambda event: self.close())
        # self.bind("<Motion>", lambda event: self.close())
        self.after(life_time, self.close)

    def close(self):
        if self.is_open:
            self.is_open = False
            self.destroy()
        