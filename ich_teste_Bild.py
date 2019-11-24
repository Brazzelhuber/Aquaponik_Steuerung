from tkinter import *
import PIL
from PIL import Image, ImageTk

canvas_width = 570
canvas_height =300

canvas = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
canvas.grid()
mysize =(570,300)
img = Image.open("tilapia.png")
img = img.resize(mysize, PIL.Image.ANTIALIAS)
canvas.image = ImageTk.PhotoImage(img)
canvas.create_image(0,0, anchor=NW, image=canvas.image)


mainloop()
