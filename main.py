import tkinter as tk
from tkinter import ttk
from threading import Thread
import os
from aggdraw import Pen, Brush, Dib
from pygame import mixer

from pages.timer import Timer
from pages import PAGE, StartFrame, TimerFrame

PRIMARY_COLOR = '#fff'
SECONDARY_COLOR = '#FA690E'
BG_COLOR = '#F35D00'

class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.geometry(f"{425}x{600}")
        self.minsize(320, 410)
        self.create_pages()
        self.create_app_btns()
        self.show_page(PAGE.HOME)

    def create_pages(self):
        self.pages = {
            PAGE.HOME: StartFrame(self),
            PAGE.TIMER: TimerFrame(self),
        }
        for page in self.pages.values():
            page.place(relwidth=1, relheight=1)
        
    def create_app_btns(self):
        self.music_btn = ttk.Button(self, text="Music", command=self.toggle_music)
        self.music_btn.place(relx=1, x=-50, y=20, anchor="ne")
        mixer.init()
        mixer.music.set_volume(0.2)
        mixer.music.load("./sounds/bg.mp3")

    def toggle_music(self):
        if mixer.music.get_busy():
            mixer.music.fadeout(1500)
        else:
            mixer.music.play(-1, start=4.5)

    def go_to_timer_page(self):
        self.pages[PAGE.TIMER].start_timer()
        self.show_page(PAGE.TIMER)

    def bring_to_front(self):
        self.wm_attributes("-topmost", True, "-topmost", False)
        
    def show_page(self, in_page):
        for page in self.pages.values():
            page.set_active(False)
        curr_page = self.pages[in_page]
        curr_page.tkraise()
        curr_page.set_active(True)
        self.music_btn.tkraise()     

app = PomodoroApp()
app.mainloop()