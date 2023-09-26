from tkinter import *
from PIL import ImageTk, Image

# initialize and configure window
window = Tk()
window.geometry = ("1280x815")
window.attributes('-fullscreen', True)
window.configure(bg = "black")

# initialize frame
frame = Frame(window, width = 1280, height = 815, bg = "black")
frame.pack()
frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

# load splash screen image
img = ImageTk.PhotoImage(Image.open("photon.jpg"))

# initialize label to hold frame and image
label = Label(frame, image = img, borderwidth = 0)
label.pack(fill = BOTH, expand = YES)

# display window for 3 seconds, then close it
window.after(3000, lambda:window.destroy())
window.mainloop()