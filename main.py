import tkinter as tk
from tkinter import ttk
from threading import Thread
import winsound
import os
from aggdraw import Pen, Brush, Dib

from animated_shapes import CountDownRing
from galaxy import Galaxy, DestructionCirle
from helpers import from_rgb
from message_modal import MessageModal
from timer import Timer

PRIMARY_COLOR = '#fff'
SECONDARY_COLOR = '#FA690E'
BG_COLOR = '#F35D00'
SOUND_FILE = f"{os.getcwd()}/sounds/bell.wav"

class Page:
    HOME = "Home Page"
    TIMER = "Timer Page"
    SETTINGS = "Settings Page"

class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.geometry(f"{425}x{600}")
        self.create_pages()
        self.wm_attributes("-transparentcolor", "magenta")

    def create_pages(self):
        cx,cy = int(425/2), 300
        self.pages = {
            Page.TIMER: TimerFrame(self),
            Page.HOME: tk.Frame(self),
        }
        for page in self.pages.values():
            page.place(relwidth=1, relheight=1)

        ttk.Button(self.pages[Page.HOME], text="Start Timer", command=self.start_timer).place(relx=0.5, rely=0.5, anchor="center")

    def start_timer(self):
        self.pages[Page.TIMER].start_timer()
        self.show_page(Page.TIMER)
        
    def show_page(self, page):
        self.pages[page].tkraise()

class TimerFrame(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(root, bg="", **kw)
        self.controller = root
        self.bg_color = (30,30,30)
        self.timer = Timer()
        self.configure_styling()
        self.set_up_animations()
        self.create_widgets()
        self.animate()
    
    def configure_styling(self):
        style = ttk.Style(self)
        style.configure("TLabel", background=from_rgb(*self.bg_color), foreground="white")
        style.configure("Time.TLabel", font=("Cookie", 50))

    def set_up_animations(self):
        self.dib = Dib("RGB", (self.winfo_screenwidth(), self.winfo_screenheight()))
        self.time_ring = CountDownRing(*self.get_ring_center(),150,7,"white",(50,50,50))
        self.galaxy = Galaxy()
        self.death_circle = DestructionCirle()
        self.bind("<Button-1>", lambda event: self.death_circle.activate(event.x, event.y))
        self.bind("<ButtonRelease-1>", lambda _: self.death_circle.execute_destruction(self.galaxy))

    def create_widgets(self):
        # creating time label
        self.time_label_var = tk.StringVar(self,Timer.format_time(self.timer.get_duration()))
        self.time_label = ttk.Label(self, textvariable=self.time_label_var,style="Time.TLabel")
        self.time_label.place(relx=0.5, rely=0.4, anchor="center")
        # creating start and stop btns
        self.start_btn = ttk.Button(self, text="Reset", command=self.start_timer)
        self.stop_btn = ttk.Button(self, text="Stop", command=self.stop_timer)
        self.start_btn.place(relx=0.4, rely=0.8, x=-20, anchor="n", height=40, width=100)
        self.stop_btn.place(relx=0.6, rely=0.8, x= +20, anchor="n", height=40, width=100)
        # creating mode option menu
        self.mode_var = tk.StringVar(self)
        self.mode_selection = ttk.OptionMenu(self, self.mode_var, self.timer.get_mode(), *Timer.get_all_modes(), command=self.change_mode)
        self.mode_selection.place(relx=0.5, rely=0.4, y=-60, anchor="center")
    
    def change_mode(self, selected_mode):
        self.timer.set_mode(selected_mode)
        self.start_timer()

    def start_timer(self):
        self.timer.start()
        self.galaxy.explode_all_stars()
        if self.timer.get_mode() != Timer.POMODORO:
            self.show_break_msg()

    def stop_timer(self):
        self.timer.stop()
        self.galaxy.reset()
        self.controller.show_page(Page.HOME)

    def handle_time_up(self):
        winsound.PlaySound(SOUND_FILE, winsound.SND_ASYNC)
        self.timer.update_count()
        next_mode = self.timer.set_next_mode()
        self.mode_var.set(next_mode)
        self.start_timer()

    def show_break_msg(self):
        Thread(target=lambda: MessageModal(self.timer.get_duration(), self.timer)).start()

    def get_ring_center(self):
        return self.winfo_width()/2,  self.winfo_height() * 4/10

    def update(self):
        cx, cy = self.get_ring_center()
        if self.timer.is_running():
            time_left = self.timer.get_time_left()
            self.galaxy.update(self.winfo_width(), self.winfo_height())
            self.time_ring.update(time_left, self.timer.get_duration())
            self.time_label_var.set( Timer.format_time(time_left) )
            if time_left < 0:
                self.handle_time_up()
        self.time_ring.translate(cx, cy)

    def draw(self):
        self.dib.rectangle((0,0,self.winfo_width(), self.winfo_height()), Pen(self.bg_color), Brush(self.bg_color))
        self.galaxy.draw(self.dib)
        self.death_circle.draw(self.dib)
        self.time_ring.draw(self.dib)
        self.dib.expose(hwnd=self.winfo_id())
        self.death_circle.update()

    def animate(self):
        dt = 10
        self.update()
        self.draw()
        self.after(dt, func=lambda: self.animate())

app = PomodoroApp()
app.mainloop()