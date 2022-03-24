import tkinter as tk

class ToggleSwitch(tk.Button):
    def __init__(self, parent, idx):
        self.parent = parent

        self.fg = self.parent.controller.button_fg
        self.bg = self.parent.controller.button_bg

        tk.Button.__init__(self, parent,
                fg = self.fg,
                bg = self.bg,
                activebackground= self.fg,
                activeforeground= self.bg,
                borderwidth = 1,
                command = self.press,

                relief = "raised")


        self.is_pressed = False
        

        self.idx = idx
    
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.update_font()
        self.update_placement()

    def update_font(self):
        self.configure(font = ("Arial", int(min(0.05*self.height, 0.03*self.width))))

    def update_placement(self):
        self.place(
            x = (.475*self.idx + 0.05)*self.width, 
            y = (70)/125*self.height,
            width = 0.425*self.width,
            height = 0.1*self.height)

    def press(self):
        if self.is_pressed:
            self.configure(bg = self.bg, fg = self.fg)
            self.configure(text = self['text'][:-1] + "X")
            self.is_pressed = False
        else:
            self.configure(bg = "white", fg = "black")
            self.configure(text = self['text'][:-1] + "✓")
            self.is_pressed = True

        self.parent.controller.toggle_switch(self.idx, self.is_pressed)
        
    # def release(self):
    #     self.configure(bg = self.bg, fg = self.fg)
    #     self.parent.controller.toggle_switch(self, False)