import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import requests
from datetime import datetime
import json
import winsound
import os

from canvas import AppCanvas
from animated_shapes import CountDownRing, Ripples
from message_modal import MessageModal
from timer import Timer

PRIMARY_COLOR = '#fff'
SECONDARY_COLOR = '#FA690E'
BG_COLOR = '#F35D00'
SOUND_FILE = f"{os.getcwd()}/sounds/bell.wav"


def quote_of_the_day():
    try:
        with open("quote-of-the-day.json", "r") as in_file:
            quote = json.loads(in_file.read())

        if quote["date"] != datetime.today().strftime("%Y-%m-%d"):
            response = requests.get("https://quotes.rest/qod?language=en")
            quote = response.json()["contents"]["quotes"][0]
            with open("quote-of-the-day.json", "w") as out_file:
                out_file.write(json.dumps(quote))
        
        return f"{quote['quote']}\n- {quote['author']}"
    except :
        return f"You can't always have quotes.\n- Pomodoro App"

class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.geometry(f"{425}x{600}")
        self.stage_radius = 168
        self.timer = Timer()
        self.set_up_canvas()
        self.create_widgets()
        self.stop_timer()
        self.animate()

    def set_up_canvas(self):
        width,height = 425, 600
        min_r, max_r = self.stage_radius - 10, self.stage_radius + 80
        self.canvas = AppCanvas(root=self, bg=BG_COLOR)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        # geometries
        self.ripples = Ripples(self.canvas, 0, 0, min_r, max_r, color=SECONDARY_COLOR, nRipples=2)
        self.stage = self.canvas.create_circle(0, 0, self.stage_radius, outline=SECONDARY_COLOR, fill=SECONDARY_COLOR)
        self.timer_ring = CountDownRing(self.canvas, 0, 0, min_r, 8, PRIMARY_COLOR)
        # text
        self.time_text = self.canvas.create_text(0, 0, text="", font=("Helvetica", 54), fill=PRIMARY_COLOR)
        self.quote = self.canvas.create_text(0, 0, anchor="s", text=quote_of_the_day(), justify="center", font=("Century Gothic", 10), fill="#FFF")

        self.canvas.bind("<Configure>", lambda event: self.place_all_widgets())

    def get_center(self):
        return self.winfo_width()/2, self.winfo_height()/2 - 40;

    def create_widgets(self):
        self.start_btn = ttk.Button(self, text="START", command=self.handle_timer_start)
        self.stop_btn = ttk.Button(self, text="STOP", command=self.stop_timer)
        
        # style.configure("TMenubutton", foreground=BG_COLOR, relief="flat", background=PRIMARY_COLOR )
        self.mode_select_var = tk.StringVar(self)
        self.mode_select = ttk.OptionMenu(self, self.mode_select_var, self.timer.get_mode(), *Timer.get_all_modes(), command=self.change_mode)

    def change_mode(self, value):
        self.timer.set_mode(value)
        if self.timer.is_running():
            self.handle_timer_start()

    def handle_timer_start(self):
        self.timer.start()
        self.place_all_widgets()
        self.canvas.itemconfig(self.time_text, state="normal")
        self.ripples.set_visible(True)
        self.start_btn.place_forget()
        winsound.PlaySound(SOUND_FILE, winsound.SND_ASYNC)

    def place_all_widgets(self):
        cx, cy = self.get_center()
        self.timer_ring.translate(cx, cy)
        self.canvas.coords(self.stage, self.canvas.get_bounds(cx, cy, self.stage_radius))
        self.canvas.coords(self.time_text, cx, cy)
        self.canvas.coords(self.quote, cx, self.winfo_height()-10)
        self.canvas.itemconfig(self.quote, width=self.winfo_width()-20)
        self.mode_select.place(x=cx, y=cy-70, anchor="center")
        self.ripples.translate(cx, cy)
        if self.timer.is_running():
            self.stop_btn.place(x=cx, y=cy + self.stage_radius + 80, anchor="center")
        else:
            self.start_btn.place(x=cx, y=cy, anchor="center",width=145, height=35)
            
    def stop_timer(self):
        cx, cy = self.get_center()
        self.timer.stop()
        self.timer_ring.reset()
        self.place_all_widgets()
        self.canvas.itemconfig(self.time_text, state="hidden")
        self.ripples.set_visible(False)
        self.stop_btn.place_forget()

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