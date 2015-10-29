from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
root = Tk()
myimg = ImageTk.PhotoImage(Image.open('a.jpg'))
l =ttk.Label(root, text="Starting...")
l['image'] = myimg
l.grid()

text=Text(l)
text.grid()
root.mainloop()