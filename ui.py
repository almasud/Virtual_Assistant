import tkinter as tk
import tkinter.messagebox
import re
import configparser
import threading
import datetime
from PIL import ImageTk, Image
from functions import (
    authenticate_google_calender, get_audio, speak, make_note, get_date, 
    get_events, is_internet, play_from_online, query_from_online
)

EVENTS_REMINDER_SERVICE = False
NOTE_MAKING_SERVICE = False
MUSIC_PLAYING_SERVICE = False
QUERY_SERVICE = False

# For displaying a popup window that contains an error message
def show_error_message(title, message):
    tkinter.messagebox.showerror(title, message)


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def show(self):
        # lift a particular window above the others
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events_reminder_service_var = tk.IntVar()
        self.note_making_service_var = tk.IntVar()
        self.music_playing_service_var = tk.IntVar()
        self.query_service_var = tk.IntVar()
        self.chk_img = ImageTk.PhotoImage(
            Image.open(r"checkbox.png").resize((20, 20), Image.ANTIALIAS)
            )
        self.unchk_img = ImageTk.PhotoImage(
            Image.open(r"uncheckbox.png").resize((20, 20), Image.ANTIALIAS)
            )

        service_label = tk.Label(self, text="Active Services", font=(16))
        services_frame = tk.Frame(self)
        self.events_reminder_service_checkbox = tk.Checkbutton(services_frame, 
            variable=self.events_reminder_service_var, command=self.active_service, 
            text="Events Reminder", indicatoron=False, bd=0, image=self.unchk_img,
            selectimage=self.chk_img, compound="left", selectcolor="#F0F0F0")
        self.note_making_service_checkbox = tk.Checkbutton(services_frame,  
            variable=self.note_making_service_var, command=self.active_service,  
            text="Note Making", indicatoron=False, bd=0, image=self.unchk_img,
            selectimage=self.chk_img, compound="left", selectcolor="#F0F0F0")
        self.music_playing_service_checkbox = tk.Checkbutton(services_frame,  
            variable=self.music_playing_service_var, command=self.active_service,  
            text="Music Playing", indicatoron=False, bd=0, image=self.unchk_img,
            selectimage=self.chk_img, compound="left", selectcolor="#F0F0F0")
        self.query_service_checkbox = tk.Checkbutton(services_frame, 
            variable=self.query_service_var, command=self.active_service, 
            text="Query Service", indicatoron=False, bd=0, image=self.unchk_img,
            selectimage=self.chk_img, compound="left", selectcolor="#F0F0F0")

        # Displaying the views
        service_label.pack(side="top", pady=5)
        services_frame.pack(side="top")
        self.events_reminder_service_checkbox.pack(side="left")
        self.note_making_service_checkbox.pack(side="left")
        self.music_playing_service_checkbox.pack(side="left")
        self.query_service_checkbox.pack(side="left")

        self.initiate_service()

    def initiate_service(self):
        global EVENTS_REMINDER_SERVICE
        global NOTE_MAKING_SERVICE
        global MUSIC_PLAYING_SERVICE
        global QUERY_SERVICE
        config = configparser.ConfigParser()
        
        # Get data from files
        if bool(config.read("config.ini")):
            if bool(int(config.get("DEFAULT", "events_reminder_service"))):
                self.events_reminder_service_var.set(1)
                EVENTS_REMINDER_SERVICE = True
            else:
                self.events_reminder_service_var.set(0)

            if bool(int(config.get("DEFAULT", "note_making_service"))):
                self.note_making_service_var.set(1)
                NOTE_MAKING_SERVICE = True
            else:
                self.note_making_service_var.set(0)

            if bool(int(config.get("DEFAULT", "music_playing_service"))):
                self.music_playing_service_var.set(1)
                MUSIC_PLAYING_SERVICE = True
            else:
                self.music_playing_service_var.set(0)
            
            if bool(int(config.get("DEFAULT", "query_service"))):
                self.query_service_var.set(1)
                QUERY_SERVICE = True
            else:
                self.query_service_var.set(0)
        else:
            config['DEFAULT'] = {
                'events_reminder_service': "1", 
                'note_making_service': "1", 
                'music_playing_service': "1",
                'query_service': "1"
            }
            # Write into config file        
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
    
    def active_service(self):
        global EVENTS_REMINDER_SERVICE
        global NOTE_MAKING_SERVICE
        global MUSIC_PLAYING_SERVICE
        global QUERY_SERVICE
        config = configparser.ConfigParser()
        config.read("config.ini")

        if self.events_reminder_service_var.get():
            config["DEFAULT"]["events_reminder_service"] = "1"
            EVENTS_REMINDER_SERVICE = True
        else:
            config["DEFAULT"]["events_reminder_service"] = "0"
            EVENTS_REMINDER_SERVICE = False

        if self.note_making_service_var.get():
            config["DEFAULT"]["note_making_service"] = "1"
            NOTE_MAKING_SERVICE = True
        else:
            config["DEFAULT"]["note_making_service"] = "0"
            NOTE_MAKING_SERVICE = False
        
        if self.music_playing_service_var.get():
            config["DEFAULT"]["music_playing_service"] = "1"
            MUSIC_PLAYING_SERVICE = True
        else:
            config["DEFAULT"]["music_playing_service"] = "0"
            MUSIC_PLAYING_SERVICE = False

        if self.query_service_var.get():
            config["DEFAULT"]["query_service"] = "1"
            QUERY_SERVICE = True
        else:
            config["DEFAULT"]["query_service"] = "0"
            QUERY_SERVICE = False

        # Write into config file        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assistant_strings_var = tk.StringVar()
        self.events_reminder_strings_var = tk.StringVar()
        self.note_making_strings_var = tk.StringVar()
        self.music_playing_strings_var = tk.StringVar()
        self.query_service_strings_var = tk.StringVar()
        # Call the response_strings_form when Page2 initialized
        self.response_strings_form()
        
    def response_strings_form(self):
        assistant_strings_file = ""
        events_reminder_strings_file = ""
        note_making_strings_file = ""
        music_playing_strings_file = ""
        query_service_strings_file = ""

        # Get data from files
        try:
            with open("assistant_strings.txt", "r") as file:
                assistant_strings_file = file.read()

            with open("events_reminder_strings.txt", "r") as file:
                events_reminder_strings_file = file.read()

            with open("note_making_strings.txt", "r") as file:
                note_making_strings_file = file.read()

            with open("music_playing_strings.txt", "r") as file:
                music_playing_strings_file = file.read()

            with open("query_service_strings.txt", "r") as file:
                query_service_strings_file = file.read()
        except:
            pass

        # Set initial value
        if len(assistant_strings_file) == 0:
            with open("assistant_strings.txt", "w") as file:
                file.write("hello assistant")
        self.assistant_strings_var.set(assistant_strings_file)

        if len(events_reminder_strings_file) == 0:
            with open("events_reminder_strings.txt", "w") as file:
                file.write("what i have;have plans;any plan;am i busy;mi busy")
        self.events_reminder_strings_var.set(events_reminder_strings_file)

        if len(note_making_strings_file) == 0:
            with open("note_making_strings.txt", "w") as file:
                file.write("make a note;write this down;remember this")
        self.note_making_strings_var.set(note_making_strings_file)

        if len(music_playing_strings_file) == 0:
            with open("music_playing_strings.txt", "w") as file:
                file.write("play a music;play a song;play music;play song;music play;song play")
        self.music_playing_strings_var.set(music_playing_strings_file)

        if len(query_service_strings_file) == 0:
            with open("query_service_strings.txt", "w") as file:
                file.write("tell me;tell something;query something;want to know")
        self.query_service_strings_var.set(query_service_strings_file)
        
        # Response strings for Services
        response_str_label = tk.Label(self, text="Response strings of Services", 
            font=("arial", 12), fg="#2280C6")
        response_str_label.grid(row=1, columnspan=2, pady=5)

        #  Assistant service response strings
        assistant_str_label = tk.Label(self, text="Assistant", 
            font=("arial", 10, "bold"), fg="#2280C6")
        assistant_str_label.grid(row=2, sticky="W", padx=5)
        assistant_str_entry = tk.Entry(self, width=35, font=("arial", 12), 
            textvariable=self.assistant_strings_var, fg="#444", bd=1, bg="#fff")
        assistant_str_entry.grid(row=2, column=1, ipady=5, pady=5)

        # Events reminder service response strings
        events_reminder_str_label = tk.Label(self, text="Events Reminder", 
            font=("arial", 10, "bold"), fg="#2280C6")
        events_reminder_str_label.grid(row=3, sticky="W", padx=5)
        events_reminder_str_entry = tk.Entry(self, width=35, font=("arial", 12), 
            textvariable=self.events_reminder_strings_var, fg="#444", bd=1, bg="#fff")
        events_reminder_str_entry.grid(row=3, column=1, ipady=5, pady=5)

        # Note Making service response strings
        note_str_label = tk.Label(self, text="Note Making", 
            font=("arial", 10, "bold"), fg="#2280C6")
        note_str_label.grid(row=4, sticky="W", padx=5)
        note_str_entry = tk.Entry(self, width=35, font=("arial", 12), 
            textvariable=self.note_making_strings_var, fg="#444", bd=1, bg="#fff")
        note_str_entry.grid(row=4, column=1, ipady=5, pady=5)
        
        # Music Playing service response strings
        music_str_label = tk.Label(self, text="Music Playing", 
            font=("arial", 10, "bold"), fg="#2280C6")
        music_str_label.grid(row=5, sticky="W", padx=5)
        music_str_entry = tk.Entry(self, width=35, font=("arial", 12), 
            textvariable=self.music_playing_strings_var, fg="#444", bd=1, bg="#fff")
        music_str_entry.grid(row=5, column=1, ipady=5, pady=5)

        #  Query service response strings
        query_service_str_label = tk.Label(self, text="Query Service", 
            font=("arial", 10, "bold"), fg="#2280C6")
        query_service_str_label.grid(row=6, sticky="W", padx=5)
        query_service_str_entry = tk.Entry(self, width=35, font=("arial", 12), 
            textvariable=self.query_service_strings_var, fg="#444", bd=1, bg="#fff")
        query_service_str_entry.grid(row=6, column=1, ipady=5, pady=5)
        
        # Save Button
        save_btn = tk.Button(self, text="Save", font=("arial", 12), 
            bg="#066DBA", fg="#fff", command=self.save_strings, cursor="hand2")
        save_btn.grid(row=7, columnspan=2)

    def save_strings(self):
        assist_str = self.assistant_strings_var.get()
        cal_str = self.events_reminder_strings_var.get()
        note_str = self.note_making_strings_var.get()
        music_str = self.music_playing_strings_var.get()
        query_str = self.query_service_strings_var.get()

        if (assist_str == ""
            or cal_str == "" 
            or note_str == "" 
            or music_str == ""
            or query_str == "" 
        ):
            show_error_message("Invalid", "Field cannot be empty.")
        else:
            # Validate all fields except Assistant String
            pattern = r"^[a-zA-Z][a-zA-Z\s;]*[a-zA-Z]$"
            if (re.match(pattern, cal_str) 
                and re.match(pattern, note_str) 
                and re.match(pattern, music_str)
                and re.match(pattern, query_str)
            ):
                with open("assistant_strings.txt", "w") as file:
                    file.write(assist_str)
                with open("events_reminder_strings.txt", "w") as file:
                    file.write(cal_str)
                with open("note_making_strings.txt", "w") as file:
                    file.write(note_str)
                with open("music_playing_strings.txt", "w") as file:
                    file.write(music_str)
                with open("query_service_strings.txt", "w") as file:
                    file.write(query_str)
                tkinter.messagebox.showinfo("Success", "Records are successfully saved.")
            else:
                show_error_message("Invalid", "Only letter(start and end with), whitespace and semicolon (; as separator) are allowed.")
        
       
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
        label = tk.Label(self.top_frame, text="Virtual Assistant", fg="#066DBA", font=("tahoma", 16, "bold", "italic"))
        label.pack(side="top")

        # Code for container Frame
        # Button for back to Page 1 from Page 2
        back_btn = tk.Button(self.p2, text="<= Back", fg="#fff", bg="#066DBA",
            command=self.p1.show, font=("arial", 10, "bold"), cursor="hand2")
        back_btn.grid(row=0)
        # Show page1 as default page
        self.p1.show()

        # Add status bar
        self.status_bar= tk.Label(self.bottom_frame, text="Status", bd=1, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x", ipady=5)

        # Service start button
        self.service_start_btn_var = tk.StringVar()
        self.service_start_btn_var.set("Start Service")
        service_start_btn = tk.Button(self.p1, textvariable=self.service_start_btn_var, 
            font=("arial", 12), bg="#066DBA", fg="#fff", cursor="hand2", command=self.service_listener)
        service_start_btn.pack(side="top", pady=25)

        # Assistant respone text lable
        response_text = ""
        with open("assistant_strings.txt", "r") as file:
            response_text = file.read()
        assistant_response_var = tk.StringVar()
        assistant_response_var.set("Say, \"" + response_text + "\" for response.")
        self.assistant_response_label = tk.Label(self.p1, textvariable=assistant_response_var, font=("arial", 12), fg="#444444")

    def service_listener(self):
        if (EVENTS_REMINDER_SERVICE 
            or NOTE_MAKING_SERVICE 
            or MUSIC_PLAYING_SERVICE
            or QUERY_SERVICE
        ):
            self.service_start_btn_var.set("Running Service...")
            self.assistant_response_label.pack(side="top", pady=26)
            # Start services in background thread to free UI thread
            assitant_thread = threading.Thread(target = self.get_assistant)
            assitant_thread.start()
            
        else:
            show_error_message("Invalid operation", "Sorry, You have no any active service.\nPlease active at least one service.")
            self.status_bar["text"] = "Sorry, You have no any active service, Please active at least one service."

    def get_assistant(self):
        global EVENTS_REMINDER_SERVICE
        global NOTE_MAKING_SERVICE
        global MUSIC_PLAYING_SERVICE
        global QUERY_SERVICE
        awake = ""
        events_reminder_strings = []
        note_making_strings = []
        music_playing_strings = []
        query_service_strings = []
        
        if (not is_internet() 
            and (EVENTS_REMINDER_SERVICE 
                    or NOTE_MAKING_SERVICE 
                    or MUSIC_PLAYING_SERVICE
                    or QUERY_SERVICE
                )
            ):
            show_error_message(title="Connection error", message="Services are activated that required an internet connection.")
            self.status_bar["text"] = "Sorry, Services are activated that required an internet connection."
            # Disable all activated services.
            config = configparser.ConfigParser()
            config.read("config.ini")
            if self.p1.events_reminder_service_var.get():
                self.p1.events_reminder_service_var.set(False)
                EVENTS_REMINDER_SERVICE = False
                config["DEFAULT"]["events_reminder_service"] = "0"
            if self.p1.note_making_service_var.get():
                self.p1.note_making_service_var.set(False)
                NOTE_MAKING_SERVICE = False
                config["DEFAULT"]["note_making_service"] = "0"
            if self.p1.music_playing_service_var.get():
                self.p1.music_playing_service_var.set(False)
                MUSIC_PLAYING_SERVICE = False
                config["DEFAULT"]["music_playing_service"] = "0"
            if self.p1.query_service_var.get():
                self.p1.query_service_var.set(False)
                QUERY_SERVICE = False
                config["DEFAULT"]["query_service"] = "0"
            # Write into config file        
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        else:
            with open("events_reminder_strings.txt", "r") as file:
                events_reminder_strings = file.read().split(";")
            with open("note_making_strings.txt", "r") as file:
                note_making_strings = file.read().split(";")
            with open("music_playing_strings.txt", "r") as file:
                music_playing_strings = file.read().split(";")
            with open("query_service_strings.txt", "r") as file:
                query_service_strings = file.read().split(";")
            with open("assistant_strings.txt", "r") as file:
                awake = file.read()

            try:
                print("Say '" + awake + "' for response")
                self.status_bar["text"] = "Say '" + awake + "' for response"
                if get_audio(status_bar=self.status_bar).lower().count(awake) > 0:
                    speak("Hello, I am your assistant. How can I help you?")
                    text = get_audio(status_bar=self.status_bar).lower()
                    recognize = False
                    today = datetime.date.today()

                    if EVENTS_REMINDER_SERVICE:
                        for phrase in events_reminder_strings:
                            if phrase in text:
                                recognize = True
                                try:
                                    date = get_date(text)
                                except ValueError:
                                    speak("Sorry, It's not a valid date, Please try again with a valid date.")
                                    self.status_bar["text"] = "Sorry, It's not a valid date! Please try again with a valid date."
                                    break
                                if date:
                                    if date < today:
                                        speak("Sorry, you have mentioned a past day, Please mention an upcoming day.")
                                        self.status_bar["text"] = "Sorry, you have mentioned a past day! Please mention an upcoming day."
                                        break
                                    SERVICE = authenticate_google_calender(message_box=tkinter.messagebox)
                                    if SERVICE:
                                        get_events(date, SERVICE, status_bar=self.status_bar)
                                    else:
                                        speak("Sorry, I can not read your calendar, Please give the permission first.")
                                        self.status_bar["text"] += ", Sorry, I can't read your Calendar! Please give the permission first."
                                    break
                                else:
                                    speak("I can't help you, without mentioning a day, please try again, with mention a day.")
                                    self.status_bar["text"] += ", Please mention with a day of week."
                                    break
                    
                    if NOTE_MAKING_SERVICE:
                        for phrase in note_making_strings:
                            if phrase in text:
                                recognize = True
                                speak("What would you, like to write?")
                                note_text = get_audio(status_bar=self.status_bar)
                                make_note(note_text)
                                speak("I have made a note of that")
                                break

                    if MUSIC_PLAYING_SERVICE:
                        for phrase in music_playing_strings:
                            if phrase in text:
                                recognize = True
                                speak("What would you, like to play?")
                                music_text = get_audio(status_bar=self.status_bar)
                                play_from_online(music_text, status_bar=self.status_bar)
                                break

                    if QUERY_SERVICE:
                        for phrase in query_service_strings:
                            if phrase in text:
                                recognize = True
                                speak("What would you, like to know?")
                                query_text = get_audio(status_bar=self.status_bar)
                                query_from_online(query_text, status_bar=self.status_bar)
                                break       
                            
                    if not recognize:
                        speak("Sorry, I can't understan, Please try again")
                        self.status_bar["text"] += ", Couldn't understant! Please try again"        
            except:
                pass
        
        self.service_start_btn_var.set("Start Service")


