import tkinter as tk
import numpy as np
import cv2 as cv
import mss
from PIL import Image,ImageTk


class LeagueFrame(tk.Frame):
    IMAGE_PATH = "imgs/"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.monitor = {"top": 0, "left": 1855, "width": 65, "height": 31}

        self.width = 41
        self.height = 14

        self.x_off = 5
        self.y_off = 8

        self.top = self.monitor["top"] + self.y_off
        self.left = self.monitor["left"] + self.x_off

        self.mask = cv.imread(f'{self.IMAGE_PATH}1080p_mask_small.jpg',0)
        self.char_images = []
        for image in range(10):
            self.char_images.append(Image.open(f"{self.IMAGE_PATH}{image}.png"))
        self.char_images.append(Image.open(f"{self.IMAGE_PATH}colon.png"))

        self.old_time = 0


        self.configure(height = self.height, width = self.width)
        self.place(x=0, y=0)
        
        self.canvas = tk.Canvas(self, height = self.height, width = self.width,highlightthickness=0, borderwidth = 0, background="red")
        self.canvas.place(x=0,y=0)

        # self.get_clock_window()


        # The image for the ingame timer is updated
        # in set_time()
        self.img = self.get_image()


    def get_draggables(self):
        return [self.canvas]

    def set_time(self, new_time):
        # Time is in 00:00.00 format
        # This turns it into 00:00
        new_time = new_time[0:5]
        if new_time != self.old_time:
            temp = self.img

            x = 0
            for char in new_time:
                if char != ':':
                    img = self.char_images[int(char)]
                    temp.paste(img, (x,0), img)
                    x += 9
                else:
                    temp.paste(self.char_images[10], (x,0), self.char_images[10])
                    x += 4
            self.temp = ImageTk.PhotoImage(temp)
            self.canvas.delete('all')
            self.canvas.create_image(0,0,image=self.temp, anchor="nw")
            self.old_time = new_time



    def update_image(self):
        self.img = self.get_image()

        self.after(100, self.update_image)

    def get_image(self):
        with mss.mss() as sct:
            img = np.array(sct.grab(self.monitor))

            # Removes the alpha value from every pixel
            img = img[...,0:3]
            output = cv.inpaint(img,self.mask,6,cv.INPAINT_TELEA)

            output = cv.cvtColor(output, cv.COLOR_RGB2BGR)

            output = output[self.y_off:self.y_off+self.height, 
                            self.x_off:self.x_off+self.width]
            
            output = Image.fromarray(output)

            return output