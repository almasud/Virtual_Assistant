import tkinter as tk
# Import from custom modules
from ui import MainView
from corelib import (
    authenticate_google_calender, get_audio, speak, note,
    get_date, get_events
)

root = tk.Tk()

# Creating a basic window
root.geometry("400x400")
root.title("Virtual Assistant")
root.iconbitmap("avatar.ico")


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

    root.mainloop()

    SERVICE = authenticate_google_calender()
    CALENDAR_STRINGS = ""
    NOTE_STRINGS = ""

    with open("calendar_strings.txt", "r") as file:
        CALENDAR_STRINGS = file.read().split(";")

    with open("calendar_strings.txt", "r") as file:
        NOTE_STRINGS = file.read().split(";")
    
    AWAKE = "hello assistant"

    while True:
        try:
            print("Say '" + AWAKE + "' for response")
            if get_audio().lower().count(AWAKE) > 0:
                speak("Hello, I am your assistant. How can I help you?")
                text = get_audio().lower()

                for phrase in CALENDAR_STRINGS:
                    if phrase in text:
                        date = get_date(text)
                        if date:
                            get_events(date, SERVICE)
                            break
                        else:
                            speak("I can't help you, without mentioning a day, please try again, with mention a day.")
                            break
                else:
                    for phrase in NOTE_STRINGS:
                        if phrase in text:
                            speak("What would you like to me write down?")
                            note_text = get_audio()
                            note(note_text)
                            speak("I have made a note of that")
                            break      
                    else:
                        speak("Sorry, I can't understan, please try again")
        except Exception as e:
            pass

 