import tkinter as tk


class ToggleBtn(tk.Label):
    def __init__(self, root, on_img, off_img, cmd, **kwargs):
        super().__init__(root,**kwargs)
        self.on_img = tk.PhotoImage(file=on_img)
        self.off_img = tk.PhotoImage(file=off_img)
        self.cmd = cmd
        self.is_on = False
        self.config(image=self.off_img)
        self.bind("<Button-1>", self.toggle)

    def toggle(self, event):
        self.is_on = not self.is_on
        if self.is_on:
            self.config(image=self.on_img)
        else:
            self.config(image=self.off_img)
        self.cmd(self.is_on)

root = tk.Tk()
root.geometry("1000x600")
root.config(bg="red")
def toggleMusic(is_on):
    if is_on:
        print ("Play Music")
    else:
        print("Pause Music")
ToggleBtn(root, "./imgs/enable-sound.png", "./imgs/sound-disabled.png", cmd=toggleMusic, width=600, height=600, bg="red").pack()
root.mainloop()