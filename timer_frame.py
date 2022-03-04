import tkinter as tk
from tkinter import ttk

class TimerFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.height = self.parent.winfo_height()
        self.width = self.parent.winfo_width()

        self.configure(height = self.height, width = self.width, background = "#474747")
        self.place(x=0,y=0)

        clock_font_size = int(min(70.0/200*self.height, 33/200*self.width))

        self.clock_label = ttk.Label(self, anchor= "center", text = "00:00.01",foreground = "white",
            background = "#474747", font = ("RopaSans-Regular", clock_font_size),
            width = 3/4*self.width)

        self.clock_label.place(
            x=100/200*self.width - 2.60*clock_font_size, y=1/3*self.height - 0.7*clock_font_size)

        self.switch_view_button = tk.Button(
            self,
            bg = self.controller.button_bg,
            text = "Set Hotkeys",
            font = ("RopaSans-Regular", int(min(15.0/200*self.height, 13/200*self.width))),
            fg = self.controller.button_fg,
            command=lambda:self.controller.switch(self.controller.HOTKEYS_FRAME),
            relief = "flat")

        self.switch_view_button.place(
            x = 45/200*self.width, y = 90/125*self.height,
            width = 110/200*self.width,
            height = 22/125*self.height)

    def set_time(self, new_time):
        self.clock_label.configure(text = new_time)

    def get_draggables(self):
        return [self, self.clock_label]

    def resize(self):
        self.width = self.parent.winfo_width()
        self.height = self.parent.winfo_height()
        self.configure(width = self.width, height = self.height)
        self.place(x=0,y=0)


        clock_font_size = int(min(70.0/200*self.height, 33/200*self.width))
        self.clock_label.configure(font = ("RopaSans-Regular", clock_font_size))
        
        self.clock_label.place(
            x=100/200*self.width - 2.60*clock_font_size, y=1/3*self.height - 0.7*clock_font_size)

        self.switch_view_button.configure(font = ("RopaSans-Regular", int(min(15.0/200*self.height, 13/200*self.width))))
        self.switch_view_button.place(
            x = 45/200*self.width, y = 90/125*self.height,
            width = 110/200*self.width,
            height = 22/125*self.height)