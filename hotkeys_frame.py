import tkinter as tk
from tkinter import ttk

import timer

class HotkeysFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.height = self.parent.winfo_height()
        self.width = self.parent.winfo_width()

        self.hotkey_buttons = [None] * timer.Timer.NUM_HOTKEYS
        self.hotkey_text = [None] * timer.Timer.NUM_HOTKEYS

        self.configure(width = self.width, height = self.height, background="#474747")
        self.place(x=0,y=0)


        self.view_clock_butt = tk.Button(self,text = "View Clock", 
            bg = self.controller.button_bg,
            fg = self.controller.button_fg,
            command=lambda:self.controller.switch(self.controller.TIMER_FRAME), 
            relief = "flat")


        for hotkey_button in range(len(self.hotkey_buttons)):
            self.hotkey_buttons[hotkey_button] = tk.Button(self,
                text = "None",
                fg = self.controller.button_fg,
                bg = self.controller.button_bg,
                activebackground= self.controller.button_fg,
                activeforeground= self.controller.button_bg,
                borderwidth = 1,
                command = (lambda num=hotkey_button:self.controller.toggle_hotkey(self.hotkey_buttons[num])),
                relief = "raised")

            self.hotkey_text[hotkey_button] = ttk.Label(self,
                foreground= "#ffffff",
                background= "#474747")



        self.hotkey_text[timer.Timer.PAUSE].configure(text = "Pause / Unpause") 
        self.hotkey_text[timer.Timer.RESET].configure(text = "Reset Practice Tool")
        self.hotkey_text[timer.Timer.SKIP].configure(text = "Skip 30 Seconds")

        # Sets the size and location of all widgets for the first time
        self.resize()

    # Returns all elements that must be bound to allow
    # the application to be moved by dragging
    def get_draggables(self):
        ret = [self]

        for hotkey in self.hotkey_text:
            ret.append(hotkey)

        return ret

    def resize(self):
        self.width = self.parent.winfo_width()
        self.height = self.parent.winfo_height()

        self.configure(width = self.width, height = self.height)
        self.place(x=0,y=0)

        self.view_clock_butt.configure(font = ("RopaSans-Regular", int(min(15.0/200*self.height, 13/200*self.width))))

        self.view_clock_butt.place(x = 45/200*self.width, y = 90/125*self.height, 
            width = 110/200*self.width, height = 22/125*self.height)

        hotkey_font_size = int(min(12.0/125*self.height, 8/200*self.width))

        for hotkey_button in range(len(self.hotkey_buttons)):
            self.hotkey_buttons[hotkey_button].configure(font = ("RopaSans-Regular", int(min(12.0/200*self.height, 9/200*self.width))))
            self.hotkey_text[hotkey_button].configure(font = ("RopaSans-Regular", hotkey_font_size))

        
        for idx, hotkey in enumerate(self.hotkey_text):
            hotkey.place(
                x=35/200*self.width - 3*hotkey_font_size, y=(19.5/125 + 25/125*idx)*self.height - 0.7*hotkey_font_size)

        self.hotkey_buttons[0].place(
            x = 116/200*self.width, y = 12/125*self.height,
            width = 80/200*self.width,
            height = 15/125*self.height)

        self.hotkey_buttons[1].place(
            x = 116/200*self.width, y = 37/125*self.height,
            width = 80/200*self.width,
            height = 15/125*self.height)

        self.hotkey_buttons[2].place(
            x = 116/200*self.width, y = 63/125*self.height,
            width = 80/200*self.width,
            height = 15/125*self.height)