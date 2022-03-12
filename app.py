import tkinter as tk
from tkinter import ttk
import threading
import keyboard
import mouse
import timer

import timer_frame
import hotkeys_frame
import league_frame

class App(threading.Thread):

    TIMER_FRAME = 0
    HOTKEYS_FRAME = 1
    LEAGUE_CLOCK_FRAME = 2
    FRAME_COUNT = 3

    RESIZE_FREQ = 20
    CLOCK_FREQ = 20

    MIN_WIDTH = 70
    MIN_HEIGHT = 50

    IMAGE_PATH = "imgs/"

    def __init__(self):
        self.hotkey_binds = ["None", "ctrl+shift+p", "ctrl+shift+o"]
        self.active_button = None # the current hotkey being changed
        self.active_recording = set()

        self.button_bg = "#343030"
        self.button_fg = "#ffffff"

        self.timer = timer.Timer()

        self.width = 400
        self.height = 250

        self.current_frame = self.TIMER_FRAME

        threading.Thread.__init__(self)
        self.start()

    def get_button_idx(self, button):
        return self.hotkeys_frame.hotkey_buttons.index(button)

    def on_key(self, key):
        if key.event_type == keyboard.KEY_DOWN:
            if self.active_button is not None:
                
                self.active_recording.add(key.name)

        elif key.event_type == keyboard.KEY_UP:
            if self.active_button is not None:

                self.set_keybind()

                self.reset_active()

    def initialize_keybinds(self, keybinds):
        self.hotkey_binds = keybinds

        for idx, keybind in enumerate(self.hotkey_binds):
            self.hotkeys_frame.hotkey_buttons[idx].configure(text = keybind)

    def set_keybind(self):

        if len(self.active_recording) == 0:
            new_text = "None"
        else:
            new_text = ""
            for key in self.active_recording:
                new_text += key.lower() + "+"
            
            new_text = new_text[0:-1]
        
        self.hotkey_binds[self.get_button_idx(self.active_button)] = new_text

        self.active_button.configure(text = new_text)

        self.timer.update_hotkeys(self.hotkey_binds)

    def get_hotkey_binds(self):
        return self.hotkey_binds

    def callback(self):
        self.root.quit()

    def switch(self, frame):
        self.reset_active()
        self.frames[frame].tkraise()
        self.current_frame = frame

        if self.current_frame != self.LEAGUE_CLOCK_FRAME:
            self.frames[self.current_frame].resize()

    def toggle_hotkey(self, button):
        if self.active_button == button:
            self.set_keybind()
            self.reset_active()
        else:
            self.reset_active()

            self.active_button = button


    def reset_active(self):
        if self.active_button != None:
            self.active_button.release()
            self.active_button = None
            self.active_recording = set()

    def update_clock(self):
        current = self.timer.get_time()

        self.timer_frame.set_time(current)
        self.league_frame.set_time(current)
            
        self.root.after(self.CLOCK_FREQ, self.update_clock)

    # bound to <B1-Motion>
    def move_window(self,event):
        self.root.geometry('+{0}+{1}'.format(self.root.winfo_x() + event.x_root - self.mouse_x, self.root.winfo_y() + event.y_root - self.mouse_y))
        self.mouse_x, self.mouse_y = event.x_root, event.y_root

    # bound to <Button-1>
    def track_mouse(self, event):
        self.mouse_x, self.mouse_y = event.x_root, event.y_root

    def switch_clock(self, event):
        if self.current_frame == self.LEAGUE_CLOCK_FRAME:
            self.root.overrideredirect(False)
            self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
            self.root.minsize(width=self.MIN_WIDTH,height=self.MIN_HEIGHT)
            self.switch(self.TIMER_FRAME)
            
        else:
            self.root.overrideredirect(True)
            self.root.minsize(width=0,height=0)
            self.root.geometry(f"{self.league_frame.width}x{self.league_frame.height}")
            self.root.geometry(f"+{self.league_frame.left}+{self.league_frame.top}")
            self.switch(self.LEAGUE_CLOCK_FRAME)


    def resize(self, e):
        # Only update the window size when not displaying the ingame clock
        if self.current_frame != self.LEAGUE_CLOCK_FRAME:
            self.width = max(self.MIN_WIDTH, self.root.winfo_width())
            self.height = max(self.MIN_HEIGHT, self.root.winfo_height())
            self.x = self.root.winfo_x()
            self.y = self.root.winfo_y()

            self.frames[self.current_frame].resize()


    def run(self):


        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry(f"{self.width}x{self.height}")
        self.x = self.root.winfo_x()
        self.y = self.root.winfo_y()

        self.root.resizable(True, True)
        # self.root.overrideredirect(True)
        # self.root.wm_attributes('-fullscreen', 'True')

        self.root.attributes('-topmost',True)

        self.root.title("Jungle Clear Timer")
        self.root.iconbitmap(f'{self.IMAGE_PATH}icon.ico')
        self.root.option_add("*tearOff", False)

        self.root.minsize(width=self.MIN_WIDTH, height=self.MIN_HEIGHT)

        self.timer_frame = timer_frame.TimerFrame(self.root, self)
        self.hotkeys_frame = hotkeys_frame.HotkeysFrame(self.root, self)
        self.league_frame = league_frame.LeagueFrame(self.root, self)
        
        self.frames = [None] * self.FRAME_COUNT
        self.frames[0] = self.timer_frame
        self.frames[1] = self.hotkeys_frame
        self.frames[2] = self.league_frame

        self.current_frame = self.TIMER_FRAME
        self.frames[self.TIMER_FRAME].tkraise()
        

        for frame in self.frames:
            if frame is not None:
                for widget in frame.get_draggables():
                    widget.bind('<Button-1>', self.track_mouse)
                    widget.bind('<B1-Motion>', self.move_window)
                    widget.bind('<Double-Button-1>', self.switch_clock)
                

        self.initialize_keybinds(self.timer.hotkeys)

        # self.root.after(self.RESIZE_FREQ, self.resize)
        self.root.bind('<Configure>', self.resize)
        self.root.after(100, self.league_frame.update_image)
        self.root.after(self.CLOCK_FREQ, self.update_clock)
        self.root.mainloop()