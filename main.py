import tkinter as tk
import tkinter.messagebox
import threading

# Import from custom modules
from ui import MainView
from corelib import (
    authenticate_google_calender, get_audio, speak, note,
    get_date, get_events
)

root = tk.Tk()
    
# Creating a basic window
root.geometry("420x400")
root.title("Virtual Assistant")
root.iconbitmap("avatar.ico")

class Worker(threading.Thread):
    def run(self):
        # long process goes here
        self.assistant_loop()

    def assistant_loop(self, awake="hello assistant"):
        SERVICE = authenticate_google_calender()
        calendar_strings = []
        note_strings = []

        with open("calendar_strings.txt", "r") as file:
            calendar_strings = file.read().split(";")
        with open("note_strings.txt", "r") as file:
            note_strings = file.read().split(";")

        while True:
            try:
                print("Say '" + awake + "' for response")
                if get_audio().lower().count(awake) > 0:
                    speak("Hello, I am your assistant. How can I help you?")
                    text = get_audio().lower()

                    for phrase in calendar_strings:
                        if phrase in text:
                            date = get_date(text)
                            if date:
                                get_events(date, SERVICE)
                                break
                            else:
                                speak("I can't help you, without mentioning a day, please try again, with mention a day.")
                                break
                    else:
                        for phrase in note_strings:
                            if phrase in text:
                                speak("What would you like to me write down?")
                                note_text = get_audio()
                                note(note_text)
                                speak("I have made a note of that")
                                break      
                        else:
                            speak("Sorry, I can't understan, please try again")
            except:
                pass


if __name__ == "__main__":
    main_view = MainView(root)
    main_view.pack(side="top", fill="both", expand=True)

    # Add menus
    menu = tk.Menu(root)
    root.config(menu=menu)

    file_menu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.destroy)
    edit_menu = tk.Menu(menu)
    menu.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Settings", command=main_view.p2.show)

    # Add status bar
    status_bar= tk.Label(main_view.bottom_frame, text="Status", bd=1, relief="sunken", anchor="w")
    status_bar.pack(side="bottom", fill="x")

    root.mainloop()

    # w = Worker()
    # w.start()
    # tkinter.messagebox.showinfo("Work Started", "OK started working")
    # root.update()
    # w.join()
    # tkinter.messagebox.showinfo("Work Complete", "OK Done")
    

    