import tkinter as tk

class HotkeyButton(tk.Button):
    def __init__(self, parent, idx):
        self.parent = parent

        self.button_fg = self.parent.controller.button_fg
        self.button_bg = self.parent.controller.button_bg

        tk.Button.__init__(self, parent,
                text = "None",
                fg = self.button_fg,
                bg = self.button_bg,
                activebackground= self.parent.controller.button_fg,
                activeforeground= self.parent.controller.button_bg,
                borderwidth = 1,
                command = self.press,
                # command = (lambda num=idx:self.parent.controller.toggle_hotkey(self.hotkey_buttons[num])),
                relief = "raised")

        

        self.idx = idx
    
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.update_font()
        self.update_placement()

    def update_font(self):
        self.configure(font = ("RopaSans-Regular", int(min(0.06*self.height, 0.05*self.width))))

    def update_placement(self):
        self.place(
            x = 0.58*self.width, 
            y = (6 + 15*self.idx)/125*self.height,
            width = 0.4*self.width,
            height = 0.1*self.height)

    def press(self):
        self.configure(bg = "white", fg = "black")
        self.parent.controller.toggle_hotkey(self)
        
        

    def release(self):
        self.configure(bg = self.button_bg, fg = self.button_fg)