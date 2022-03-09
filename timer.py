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

    DEFAULT_HOTKEYS = ["None", "ctrl+shift+p", "ctrl+shift+o", "None"]

    def __init__(self):
        self.is_paused = False
        self.timer = 0
        self.last = time.perf_counter()
        self.hotkeys = self.DEFAULT_HOTKEYS

        self.load_hotkeys()

        threading.Thread.__init__(self)
        self.start()

    def cycle_pause(self):
        self.is_paused = not self.is_paused

    def start_timer(self):
        self.is_paused = False

    def reset_timer(self):
        self.timer = 0

    def skip_30(self):
        self.timer += 27.741

    # bound to Right Click
    def wait_for_right(self):
        mouse.on_right_click(self.on_right)

    def on_right(self):
        mouse.unhook_all()
        self.start_timer()

    def update_hotkeys(self, hotkeys):
        keyboard.unhook_all_hotkeys()
        self.set_hotkeys(hotkeys)
        self.save_hotkeys(hotkeys)

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

    def load_hotkeys(self):
        hotkeys = self.DEFAULT_HOTKEYS
        try:
            with open(self.HOTKEYS_FILE, 'r') as file:
                for idx, line in enumerate(file.readlines()):
                    line = line.strip()
                    hotkeys[idx] = line
        except FileNotFoundError:
            pass
        
        self.set_hotkeys(hotkeys)

    def save_hotkeys(self, hotkeys):
        with open(self.HOTKEYS_FILE, 'w') as file:
            for hotkey in hotkeys:
                file.write(hotkey + "\n")

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

