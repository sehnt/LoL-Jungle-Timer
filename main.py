import app
import keyboard


app = app.App()
listener = keyboard.hook(app.on_key)