import tkinter as tk
from tkinter import ttk
from threading import Thread
import winsound
import os
from aggdraw import Pen, Brush, Dib

from animated_shapes import CountDownRing
from galaxy import Galaxy, DestructionCirle
from helpers import from_rgb, widget_bounds
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
        self.minsize(320, 410)
        self.create_pages()
        self.show_page(Page.HOME)

    def create_pages(self):
        cx,cy = int(425/2), 300
        self.pages = {
            Page.HOME: StartFrame(self),
            Page.TIMER: TimerFrame(self),
        }
        for page in self.pages.values():
            page.place(relwidth=1, relheight=1)

    def go_to_timer_page(self):
        self.pages[Page.TIMER].start_timer()
        self.show_page(Page.TIMER)

    def bring_to_front(self):
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-topmost", False)
        
    def show_page(self, in_page):
        for page in self.pages.values():
            page.set_active(False)
        self.pages[in_page].tkraise()
        self.pages[in_page].set_active(True)


class StartFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.is_active = False
        # add start button
        self.controller = root
        ttk.Button(self, text="Start Timer", command=self.controller.go_to_timer_page).place(relx=0.5, rely=0.5, anchor="center", width=100, height=30)
    
    def set_active(self, active: bool):
        self.is_active = active
        

class TimerFrame(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(root, bg="", **kw)
        self.controller = root
        self.is_active = False
        self.bg_color = (30,30,30)
        self.timer = Timer()
        self.configure_styling()
        self.set_up_animations()
        self.create_widgets()
        self.animate()
    
    @property
    def restriction_bounds_list(self):
        widgets = [(self.play_pause_btn, 10), (self.stop_btn, 10), (self.time_label, 35)]
        return [widget_bounds(widget, offset) for widget,offset in widgets]

    @property
    def bounds(self):
        return widget_bounds(self, offset=0)

    def set_active(self, active: bool):
        self.is_active = active
    
    def configure_styling(self):
        style = ttk.Style(self)
        style.configure("TLabel", background=from_rgb(*self.bg_color), foreground="white")
        style.configure("Time.TLabel", font=("Cookie", 55))

    def set_up_animations(self):
        self.dib = Dib("RGB", (self.winfo_screenwidth(), self.winfo_screenheight()))
        self.time_ring = CountDownRing(*self.get_ring_center(),150,7,"white")
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
        self.play_pause_var = tk.StringVar(self, "Pause")
        self.play_pause_btn = ttk.Button(self, textvariable=self.play_pause_var, command=self.toggle_play)
        self.stop_btn = ttk.Button(self, text="Stop", command=self.stop_timer)
        self.play_pause_btn.place(relx=0.4, rely=0.8, x=-30, anchor="n", height=32, width=110)
        self.stop_btn.place(relx=0.6, rely=0.8, x= +30, anchor="n", height=32, width=110)
        # creating mode option menu
        self.mode_var = tk.StringVar(self)
        self.mode_selection = ttk.OptionMenu(self, self.mode_var, self.timer.get_mode(), *Timer.get_all_modes(), command=self.change_mode)
        self.mode_selection.place(relx=0.5, rely=0.4, y=-60, anchor="center")
        # message modal
        modal_should_close = lambda: not self.is_active or self.timer.get_mode() == Timer.POMODORO
        self.message_modal = MessageModal(self, self.time_label_var, modal_should_close)
    
    def change_mode(self, selected_mode):
        self.timer.set_mode(selected_mode)
        self.start_timer()

    def toggle_play(self):
        if self.timer.is_running():
            self.timer.pause()
        else:
            self.timer.resume()
        self.update_play_pause_var()

    def update_play_pause_var(self):
        self.play_pause_var.set( "Pause" if self.timer.is_running() else "Resume" )

    def start_timer(self):
        winsound.PlaySound(SOUND_FILE, winsound.SND_ASYNC)
        self.timer.reset()
        self.update_play_pause_var()
        self.galaxy.explode_all_stars()
        if self.timer.get_mode() != Timer.POMODORO:
            self.message_modal.show()
        else:
            self.message_modal.hide()

    def stop_timer(self):
        self.timer.set_mode(Timer.POMODORO)
        self.mode_var.set(Timer.POMODORO)
        self.timer.stop()
        self.galaxy.reset()
        self.controller.show_page(Page.HOME)

    def handle_time_up(self):
        self.timer.update_count()
        next_mode = self.timer.set_next_mode()
        self.mode_var.set(next_mode)
        self.controller.bring_to_front()
        self.start_timer()

    def get_ring_center(self):
        return self.winfo_width()/2,  self.winfo_height() * 4/10

    def update(self):
        cx, cy = self.get_ring_center()
        self.galaxy.update(self.bounds, self.restriction_bounds_list)
        if self.timer.is_running():
            time_left = self.timer.get_time_left()
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
        if self.is_active:
            self.update()
            self.draw()
        self.after(dt, func=lambda: self.animate())

app = PomodoroApp()
app.mainloop()