from tkinter import *
from PIL import ImageTk, Image
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# initialize and configure window
window = Tk()
window.geometry = ("1280x815")
window.attributes('-fullscreen', True)
window.configure(bg = "black")

# initialize frame
frame = Frame(window, bg = "black")
frame.pack()
frame.place(anchor = 'center', relx = 0.5, rely = 0.5)

# load splash screen image
origImg = Image.open("photon.jpg")
resizeImg = origImg.resize((window.winfo_screenwidth(), window.winfo_screenheight()))
img = ImageTk.PhotoImage(resizeImg)

# initialize label to hold frame and image
label = Label(frame, image = img, borderwidth = 0)
label.pack(fill = BOTH, expand = YES)

# display window for 3 seconds, then close it
window.after(3000, lambda:window.destroy())
window.mainloop()