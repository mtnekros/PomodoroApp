import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import winsound
import os

from canvas import AppCanvas
from animated_shapes import CountDownRing, Ripples
from message_modal import MessageModal
from timer import Timer

WIDTH = 380
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2 - 38
MIN_RADIUS = 120
MAX_RADIUS = 190
PRIMARY_COLOR = '#fff'
SECONDARY_COLOR = '#FA690E'
BG_COLOR = '#F35D00'
SOUND_FILE = f"{os.getcwd()}/sounds/bell.wav"

start_btn_style = {
    "font"             : ('Cabin Sketch', 22),
    "foreground"       : SECONDARY_COLOR,
    "activeforeground" : BG_COLOR,
    "bg"               : PRIMARY_COLOR,
    "activebackground" : "#F0E0D0",
    "relief"           : "flat",
    "borderwidth"      : 0,
}
stop_btn_style = {
    "font"             :  ('Arial', 14, 'normal'),
    "foreground"       : PRIMARY_COLOR,
    "activeforeground" : PRIMARY_COLOR,
    "bg"               : "#FD8234",
    "activebackground" : SECONDARY_COLOR,
    "relief"           : "flat",
    "borderwidth"      : 0,
}

class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        # self.wm_attributes('-alpha', 0.9)
        self.timer = Timer()
        self.set_up_canvas()
        self.create_widgets()
        self.stop_timer()
        self.animate()

    def set_up_canvas(self):
        cx, cy, min_r, max_r = CENTER_X, CENTER_Y, MIN_RADIUS, MAX_RADIUS
        self.canvas = AppCanvas(root=self, bg=BG_COLOR)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        # geometries
        self.ripples = Ripples(self.canvas, cx, cy, min_r, max_r, color=SECONDARY_COLOR, nRipples=2)
        self.stage = self.canvas.create_circle(cx, cy, min_r+8, outline=SECONDARY_COLOR, fill=SECONDARY_COLOR)
        self.timer_ring = CountDownRing(self.canvas, cx, cy, min_r, 8, PRIMARY_COLOR)
        # text
        self.time_text = self.canvas.create_text(cx, cy, text="", font=("Helvetica", 45), fill=PRIMARY_COLOR)

    def create_widgets(self):
        self.start_btn = tk.Button(self, text="START", command=self.handle_timer_start, **start_btn_style)
        self.stop_btn = tk.Button(self, text="STOP", command=self.stop_timer, **stop_btn_style)

        style = ttk.Style(self)
        
        style.configure("TMenubutton", foreground=BG_COLOR, background=PRIMARY_COLOR )
        self.mode_select_var = tk.StringVar(self)
        options = [Timer.POMODORO, Timer.SHORT_BREAK, Timer.LONG_BREAK]
        self.mode_select = ttk.OptionMenu(self, self.mode_select_var, self.timer.get_mode(), *options, command=self.change_mode)
        self.mode_select.place(x=CENTER_X, y=CENTER_Y-45, anchor="center")

    def change_mode(self, value):
        self.timer.set_mode(value)
        if self.timer.is_running():
            self.handle_timer_start()

    def handle_timer_start(self):
        self.timer.start()
        self.start_btn.place_forget()
        self.canvas.itemconfig(self.time_text, state="normal")
        self.ripples.set_visible(True)
        self.stop_btn.place(x=CENTER_X,y=HEIGHT-100, anchor='center', width=100, height=30)
        winsound.PlaySound(SOUND_FILE, winsound.SND_ASYNC)

    def stop_timer(self):
        self.timer.stop()
        self.timer_ring.reset()
        self.canvas.itemconfig(self.time_text, state="hidden")
        self.ripples.set_visible(False)
        self.stop_btn.place_forget()
        self.start_btn.place(x=CENTER_X, y=CENTER_Y, anchor='center', width=145, height=35)

    def handle_time_up(self):
        self.timer_ring.reset()
        self.timer.handle_timer_completed()
        next_mode = self.timer.get_mode()
        self.mode_select_var.set( next_mode )
        winsound.PlaySound(SOUND_FILE, winsound.SND_ASYNC)
        self.show_timer_complete_msg(next_mode)

    def show_timer_complete_msg(self, next_mode):
        if next_mode == Timer.POMODORO:
            title = "Focus"
            msg = f"Focus on your task for the next 25 minutes.\nPomodoro No: {self.timer.getNPomodoros() + 1}"
            duration = 5000 # ms
        else:
            title = "Break"
            msg = f"Time to take a break."
            duration = self.timer.get_duration() * 1000 # converting to miliseconds
        Thread(target= lambda: MessageModal(title, msg, duration)).start()

    def animate(self):
        dt = 10 # 10 ms
        if self.timer.is_running():
            time_left = self.timer.get_time_left()
            self.timer_ring.update(time_left, self.timer.get_duration())
            self.canvas.itemconfig(self.time_text, text=Timer.format_time( time_left ))
            self.ripples.update(dt/1000)
            if time_left < 0:
                self.handle_time_up()
        self.after(dt, func=lambda: self.animate())

PomodoroApp().mainloop()