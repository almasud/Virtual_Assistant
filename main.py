import tkinter as tk
import tkinter.messagebox
import threading
from ui import MainView

root = tk.Tk()
    
# Creating a basic window
root.geometry("470x400")
root.title("Virtual Assistant")
root.iconbitmap("avatar.ico")


if __name__ == "__main__":
    main_view = MainView(root)
    main_view.pack(side="top", fill="both", expand=True)

    root.mainloop()

    

    