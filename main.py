import tkinter as tk
import tkinter.messagebox
import threading
from ui import MainView

root = tk.Tk() # create a Tk root window

w = 460 # width for the Tk root
h = 400 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# Set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.title("Virtual Assistant")
root.iconbitmap("avatar.ico")

if __name__ == "__main__":
    main_view = MainView(root)
    main_view.pack(side="top", fill="both", expand=True)

    root.mainloop() # starts the mainloop


    