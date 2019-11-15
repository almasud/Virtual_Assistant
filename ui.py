import tkinter as tk
import tkinter.messagebox
import re
import configparser
import threading
from functions import (
    authenticate_google_calender, get_audio, speak, note,
    get_date, get_events
)

EVENTS_REMINDER_ACTIVE = False
NOTE_MAKING_SERVICE = False

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events_reminder_active_var = tk.IntVar()
        self.note_active_var = tk.IntVar()

        service_label = tk.Label(self, text="Active Services", font=(16))
        services_frame = tk.Frame(self)
        self.events_reminder_active_btn = tk.Checkbutton(services_frame, 
            variable=self.events_reminder_active_var, command=self.active_service, 
            text="Events Reminder")
        self.note_active_btn = tk.Checkbutton(services_frame,  
            variable=self.note_active_var, command=self.active_service,  
            text="Note Making")

        # Displaying the views
        service_label.pack(side="top", pady=5)
        services_frame.pack(side="top")
        self.events_reminder_active_btn.pack(side="left")
        self.note_active_btn.pack(side="left")

        self.initiate_service()

    def initiate_service(self):
        global EVENTS_REMINDER_ACTIVE
        global NOTE_MAKING_SERVICE
        config = configparser.ConfigParser()
        
        # Get data from files
        if bool(config.read("config.ini")):
            if bool(int(config.get("DEFAULT", "events_reminder_service"))):
                self.events_reminder_active_var.set(True)
                EVENTS_REMINDER_ACTIVE = True
            else:
                self.events_reminder_active_var.set(False)

            if bool(int(config.get("DEFAULT", "note_making_service"))):
                self.note_active_var.set(True)
                NOTE_MAKING_SERVICE = True
            else:
                self.note_active_var.set(False)
        else:
            config['DEFAULT'] = {'events_reminder_service': "1", 
                'note_making_service': "1"}
            # Write into config file        
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
    
    def active_service(self):
        global EVENTS_REMINDER_ACTIVE
        global NOTE_MAKING_SERVICE
        config = configparser.ConfigParser()
        config.read("config.ini")

        if self.events_reminder_active_var.get():
            config["DEFAULT"]["events_reminder_service"] = "1"
            EVENTS_REMINDER_ACTIVE = True
        else:
            config["DEFAULT"]["events_reminder_service"] = "0"
            EVENTS_REMINDER_ACTIVE = False

        if self.note_active_var.get():
            config["DEFAULT"]["note_making_service"] = "1"
            NOTE_MAKING_SERVICE = True
        else:
            config["DEFAULT"]["note_making_service"] = "0"
            NOTE_MAKING_SERVICE = False

        # Write into config file        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events_reminder_strings_var = tk.StringVar()
        self.note_making_strings_var = tk.StringVar()
        self.assistant_strings_var = tk.StringVar()
        self.response_strings_form()
        
    def response_strings_form(self):
        assistant_strings_file = ""
        events_reminder_strings_file = ""
        note_making_strings_file = ""

        # Get data from files
        try:
            with open("assistant_strings.txt", "r") as file:
                assistant_strings_file = file.read()

            with open("events_reminder_strings.txt", "r") as file:
                events_reminder_strings_file = file.read()

            with open("note_making_strings.txt", "r") as file:
                note_making_strings_file = file.read()
        except:
            pass

        # Set initial value
        if len(assistant_strings_file) == 0:
            with open("assistant_strings.txt", "w") as file:
                file.write("hello assistant")
        self.assistant_strings_var.set(assistant_strings_file)

        if len(events_reminder_strings_file) == 0:
            with open("events_reminder_strings.txt", "w") as file:
                file.write("what i have;do i have plans;do i have any plan;am i busy;mi busy")
        self.events_reminder_strings_var.set(events_reminder_strings_file)

        if len(note_making_strings_file) == 0:
            with open("note_making_strings.txt", "w") as file:
                file.write("make a note;write this down;remember this")
        self.note_making_strings_var.set(note_making_strings_file)
        
        # Response strings for assistant service
        assistant_str_label = tk.Label(self, text="Assistant Response", 
            font=("arial", 10, "bold"), fg="blue")
        assistant_str_label.grid(row=1, sticky="E")
        assistant_str_entry = tk.Entry(self, width=30, font=("arial", 12), 
            textvariable=self.assistant_strings_var, fg="#fff", bd=1, bg="#444")
        assistant_str_entry.grid(row=1, column=1, ipady=5, pady=5)

        # Response strings for events reminder service
        events_reminder_str_label = tk.Label(self, text="Events Reminder Response", 
            font=("arial", 10, "bold"), fg="blue")
        events_reminder_str_label.grid(row=2, sticky="E")
        events_reminder_str_entry = tk.Entry(self, width=30, font=("arial", 12), 
            textvariable=self.events_reminder_strings_var, fg="#fff", bd=1, bg="#444")
        events_reminder_str_entry.grid(row=2, column=1, ipady=5, pady=5)

        # Response strings for Note Making service
        note_str_label = tk.Label(self, text="Note Making Response", 
            font=("arial", 10, "bold"), fg="blue")
        note_str_label.grid(row=3, sticky="E")
        note_str_entry = tk.Entry(self, width=30, font=("arial", 12), 
            textvariable=self.note_making_strings_var, fg="#fff", bd=1, bg="#444")
        note_str_entry.grid(row=3, column=1, ipady=5, pady=5)
        
        # Save Button
        save_btn = tk.Button(self, text="Save", font=("arial", 12), 
            bg="#444", fg="#fff", command=self.save_strings, cursor="hand2")
        save_btn.grid(row=4, columnspan=2)

    def save_strings(self):
        assist_str = self.assistant_strings_var.get()
        cal_str = self.events_reminder_strings_var.get()
        note_str = self.note_making_strings_var.get()

        if assist_str == "" or cal_str == "" or note_str == "":
            tkinter.messagebox.showinfo("Invalid", "Field cannot be empty.")
        else:
            pattern = r"^[a-zA-Z]+[0-9;\s]*"
            if re.match(pattern, cal_str) and re.match(pattern, note_str):
                with open("assistant_strings.txt", "w") as file:
                    file.write(assist_str)
                with open("events_reminder_strings.txt", "w") as file:
                    file.write(cal_str)
                with open("note_making_strings.txt", "w") as file:
                    file.write(note_str)
                tkinter.messagebox.showinfo("Success", "Records are successfully saved.")
            else:
                tkinter.messagebox.showinfo("Invalid", "Only Charater, Number and ; (semicolon)  are allowed.")
        
       
class MainView(Page):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p1 = Page1(self)
        self.p2 = Page2(self)
        self.top_frame = tk.Frame(self)
        self.container = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)

        self.top_frame.pack(side="top", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)
        self.bottom_frame.pack(side="bottom", fill="x", expand=False)
        self.p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        # Add menus
        menu = tk.Menu(root)
        root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=root.destroy)
        edit_menu = tk.Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Settings", command=self.p2.show)

        #Code for top frame
        label = tk.Label(self.top_frame, text="Virtual Assistant", fg="green", font=("tahoma", 16, "bold", "italic"))
        label.pack(side="top")

        # Code for container Frame
        # Back button for Page 1 in Page 2
        back_btn = tk.Button(self.p2, text="<= Back", fg="#fff", bg="#444",
            command=self.p1.show, font=("arial", 10, "bold"), cursor="hand2")
        back_btn.grid(row=0)
        # Show page1 as default page
        self.p1.show()

        # Add status bar
        self.status_bar= tk.Label(self.bottom_frame, text="Status", bd=1, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", ipady=5)

        # Service start button
        service_start_btn_var = tk.StringVar()
        service_start_btn_var.set("Start Service")
        service_start_btn = tk.Button(self.p1, textvariable=service_start_btn_var, 
            font=("arial", 12), bg="#444", fg="#fff", cursor="hand2", command=self.service_listener)
        service_start_btn.pack(side="top", pady=25)

    
    def service_listener(self):
        assitant_thread = threading.Thread(target = self.get_assistant)
        assitant_thread.start()

    def get_assistant(self):
        global EVENTS_REMINDER_ACTIVE
        global NOTE_MAKING_SERVICE
        events_reminder_strings = []
        note_making_strings = []
        awake = ""
        
        if EVENTS_REMINDER_ACTIVE:
            SERVICE = authenticate_google_calender(message_box=tkinter.messagebox)
            if not SERVICE:
                config = configparser.ConfigParser()
                config.read("config.ini")
                if self.p1.events_reminder_active_var.get():
                    self.p1.events_reminder_active_var.set(False)
                    EVENTS_REMINDER_ACTIVE = False
                    config["DEFAULT"]["events_reminder_service"] = "0"
                    # Write into config file        
                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)

        with open("events_reminder_strings.txt", "r") as file:
            events_reminder_strings = file.read().split(";")
        with open("note_making_strings.txt", "r") as file:
            note_making_strings = file.read().split(";")
        with open("assistant_strings.txt", "r") as file:
            awake = file.read()

        try:
            print("Say '" + awake + "' for response")
            self.status_bar["text"] = "Say '" + awake + "' for response"
            if get_audio().lower().count(awake) > 0:
                speak("Hello, I am your assistant. How can I help you?")
                text = get_audio(status_bar=self.status_bar).lower()
                recognize = False

                if EVENTS_REMINDER_ACTIVE or NOTE_MAKING_SERVICE:
                    if EVENTS_REMINDER_ACTIVE:
                        for phrase in events_reminder_strings:
                            if phrase in text:
                                recognize = True
                                date = get_date(text)
                                if date:
                                    get_events(date, SERVICE)
                                    break
                                else:
                                    speak("I can't help you, without mentioning a day, please try again, with mention a day.")
                                    self.status_bar["text"] += ", Please mention with a day of week."
                                    break
                    
                    if NOTE_MAKING_SERVICE:
                        for phrase in note_making_strings:
                            if phrase in text:
                                recognize = True
                                speak("What would you like to me write down?")
                                note_text = get_audio(status_bar=self.status_bar)
                                note(note_text)
                                speak("I have made a note of that")
                                break      
                            
                    if not recognize:
                        speak("Sorry, I can't understan, Please try again")
                        self.status_bar["text"] += ", Couldn't understant! Please try again"
                
                else:
                    speak("Sorry, You have no any active service, Please active at least one service")
                    self.status_bar["text"] = "Sorry, You have no any active service, Please active at least one service"
                
        except:
            pass


