import keyboard
import mouse
import time
import threading


class Timer(threading.Thread):
    NUM_HOTKEYS = 4
    PAUSE = 0
    RESET = 1
    SKIP  = 2
    RIGHT = 3
    HOTKEYS_FILE = "hotkeys.txt"

    PAUSE_ON_RESET = 0
    SHOW_INGAME = 1
    NUM_SWITCHES = 2

    DEFAULT_HOTKEYS = ["None", "ctrl+shift+p", "ctrl+shift+o", "None"]

    def __init__(self):
        self.is_paused = False
        self.timer = 0
        self.skip_start = -30
        self.last = time.perf_counter()
        self.hotkeys = self.DEFAULT_HOTKEYS
        self.switches = [False]*self.NUM_SWITCHES

        self.load_settings()

        threading.Thread.__init__(self, daemon=True)
        self.start()

    def toggle_switch(self, switch, is_pressed):
        self.switches[switch] = is_pressed
        self.save_hotkeys()

    def cycle_pause(self):
        self.is_paused = not self.is_paused
        self.skip_start = -30

    def start_timer(self):
        self.is_paused = False

    def reset_timer(self):
        if self.switches[self.PAUSE_ON_RESET]:
            self.timer = 90
            self.skip_start = -30
            self.is_paused = True
        else:
            self.timer = 0
            self.skip_start = -30

    def skip_30(self):
        if self.is_paused:
            self.timer += 30
        elif self.skip_start < self.timer - 29.6:
            self.skip_start = self.timer
            self.timer += 27.9

    # bound to Right Click
    def wait_for_right(self):
        mouse.on_right_click(self.on_right)

    def on_right(self):
        mouse.unhook_all()
        self.start_timer()

    def update_hotkeys(self, hotkeys):
        keyboard.unhook_all_hotkeys()
        self.set_hotkeys(hotkeys)
        self.save_hotkeys()

    def set_hotkeys(self, hotkeys):
        if hotkeys[self.PAUSE] != "None":
            keyboard.add_hotkey(hotkeys[self.PAUSE], self.cycle_pause)
        if hotkeys[self.RESET] != "None":
            keyboard.add_hotkey(hotkeys[self.RESET], self.reset_timer)
        if hotkeys[self.SKIP] != "None":
            keyboard.add_hotkey(hotkeys[self.SKIP], self.skip_30)
        if hotkeys[self.RIGHT] != "None":
            keyboard.add_hotkey(hotkeys[self.RIGHT], self.wait_for_right)

        self.hotkeys = hotkeys

    def load_settings(self):
        hotkeys = self.DEFAULT_HOTKEYS
        switches = [False] * self.NUM_SWITCHES

        try:
            with open(self.HOTKEYS_FILE, 'r') as file:
                lines = file.readlines()
                if len(lines) != len(hotkeys) + len(switches):
                    pass
                else:
                    data = []
                    for line in lines:
                        data.append(line.strip())
                    
                    hotkeys = data[0:self.NUM_HOTKEYS]
                    # switches = data[self.NUM_HOTKEYS:]
                    switches = [eval(switch) for switch in data[self.NUM_HOTKEYS:]]
        except FileNotFoundError:
            pass
        
        self.set_hotkeys(hotkeys)

        for switch in range(self.NUM_SWITCHES):
            if switches[switch] == True:
                self.toggle_switch(switch, switches[switch])
        

    def save_hotkeys(self):
        with open(self.HOTKEYS_FILE, 'w') as file:
            for hotkey in self.hotkeys:
                file.write(hotkey + "\n")
            for switch in self.switches:
                file.write(str(switch) + "\n")

    def sec_to_min(self, input):
        minutes = int(input/60)
        seconds = int(input%60)
        decimal = round(input - minutes*60 - seconds, 2) # rounds to second decimal

        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"
        
        if decimal == 0:
            decimal = "00"
        else:
            decimal = f"{decimal}"[2:]

        if len(decimal) == 1:
            decimal += "0"

        return f"{minutes}:{seconds}.{decimal}"

    def get_time(self):
        return self.sec_to_min(self.timer)

    def run(self):
        while True:
            current = time.perf_counter()
            if not self.is_paused:
                self.timer += current - self.last
            self.last = current

            time.sleep(0.01)

