# [**Download Here**](https://github.com/sehnt/LoL-Jungle-Timer/releases)


# LoL-Jungle-Timer
Custom Python Application for a more convenient way of timing jungle clears.

**DISCLAIMER: Only works with 1080p at 100% Scaling. Also has not been tested on MacOS**

# Main Features:
 - Double click to open an overlay that replicates the ingame timer
 - Hotkeys to mimic Practice Tool time controls

[![Image from Gyazo](https://i.gyazo.com/2f251da0d9d5fd371a774dc9895f2477.gif)](https://gyazo.com/2f251da0d9d5fd371a774dc9895f2477)


# Ingame Timer:

The Ingame Timer page is meant to cover up the actual League of Legends timer with this application's timer.
 - You can access this page by double clicking anywhere on the application (except a button). 
 - To exit the Ingame Timer, double click on the application once again.
 - The application will shrink and automatically move to the correct position for a 1080p monitor on 100% scaling.

High Contrast Examples:

![image](https://user-images.githubusercontent.com/78941433/156722740-270d98ef-297e-4976-a267-92eb24768c83.png)
![image](https://user-images.githubusercontent.com/78941433/156722752-ce31a659-cefa-47c7-9c0c-2267e3e231d6.png)


# Main Timer:

The Main Timer page displays the timer and has a button to move to the Hotkey page:
![image](https://user-images.githubusercontent.com/78941433/156722155-a13a47b6-d0f7-4546-a8b5-64bd2dd96b31.png)

# Hotkeys:

The Hotkey page allows you set four hotkeys:
 - Pause / Unpause the timer
 - Reset the timer
 - Skip 30 seconds (Actually skips ~27.7 seconds to mimic practice tool)
 - Start on Right Click
   - After you press this hotkey, the timer will start on your next right click

![image](https://user-images.githubusercontent.com/78941433/157542639-a64c9214-8c59-416a-a8b3-b314405d1739.png)


# **Compilation Instructions:**
If you want to compile the code for yourself, here's how to do so.
If you don't what you're doing, I would strongly recommend just downloading
a precompiled .exe from the releases page. It's much easier

1. Install Python: https://www.python.org/downloads/
2. Open up the Windows Terminal
3. Type: pip install pyinstaller
4. Navigate to this project's folder
5. Run the following
 - pip install pillow
 - pip install mss
 - pip install opencv-python
 - pip install numpy
 - pip install keyboard
 - pip install mouse
 - pyinstaller main.py --exclude-module \_bootlocale --add-data imgs;imgs --noconsole --icon=imgs/icon.ico --clean --name Jungle-Timer

6. Navigate to dist/Jungle-Timer
7. Run Jungle-Timer.exe
