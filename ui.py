import tkinter as tk
import tkinter.messagebox
import re
import configparser

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calendar_active_var = tk.IntVar()
        self.note_active_var = tk.IntVar()

        service_label = tk.Label(self, text="Active Services", font=(16))
        services_frame = tk.Frame(self)
        self.caledar_active_btn = tk.Checkbutton(services_frame, 
            variable=self.calendar_active_var, command=self.active_service, 
            text="Calendar Service")
        self.note_active_btn = tk.Checkbutton(services_frame,  
            variable=self.note_active_var, command=self.active_service,  
            text="Note Service")

        # Service start and stop buttons
        self.start_stop_service_btn = tk.Button(self, text="Start Service", 
            font=("arial", 12), bg="#444", fg="#fff", cursor="hand2")

        # Displaying the views
        service_label.pack(side="top", pady=5)
        services_frame.pack(side="top")
        self.caledar_active_btn.pack(side="left")
        self.note_active_btn.pack(side="left")
        self.start_stop_service_btn.pack(side="top", pady=25)

        self.initiate_service()

    def initiate_service(self):
        config = configparser.ConfigParser()
        
        # Get data from files
        if bool(config.read("config.ini")):
            if bool(int(config.get("DEFAULT", "calendar_service"))):
                self.calendar_active_var.set(True)
            else:
                self.calendar_active_var.set(False)

            if bool(int(config.get("DEFAULT", "note_service"))):
                self.note_active_var.set(True)
            else:
                self.note_active_var.set(False)
        else:
            config['DEFAULT'] = {'calendar_service': "1", 
                'note_service': "1"}
            # Write into config file        
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
    
    def active_service(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        if self.calendar_active_var.get():
            config["DEFAULT"]["calendar_service"] = "1"
        else:
            config["DEFAULT"]["calendar_service"] = "0"

        if self.note_active_var.get():
            config["DEFAULT"]["note_service"] = "1"
        else:
            config["DEFAULT"]["note_service"] = "0"

        # Write into config file        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calendar_strings_var = tk.StringVar()
        self.note_strings_var = tk.StringVar()
        self.assistant_strings_var = tk.StringVar()
        self.response_strings_form()
        
    def response_strings_form(self):
        assistant_strings_file = ""
        calendar_strings_file = ""
        note_strings_file = ""

        # Get data from files
        try:
            with open("assistant_strings.txt", "r") as file:
                assistant_strings_file = file.read()

            with open("calendar_strings.txt", "r") as file:
                calendar_strings_file = file.read()

            with open("note_strings.txt", "r") as file:
                note_strings_file = file.read()
        except:
            pass

        # Set initial value
        if len(assistant_strings_file) == 0:
            with open("assistant_strings.txt", "w") as file:
                file.write("hello assistant")
        self.assistant_strings_var.set(assistant_strings_file)

        if len(calendar_strings_file) == 0:
            with open("calendar_strings.txt", "w") as file:
                file.write("what i have;do i have plans;do i have any plan;am i busy;mi busy")
        self.calendar_strings_var.set(calendar_strings_file)

        if len(note_strings_file) == 0:
            with open("note_strings.txt", "w") as file:
                file.write("make a note;write this down;remember this")
        self.note_strings_var.set(note_strings_file)
        
        # Response strings for assistant service
        assistant_str_label = tk.Label(self, text="Assistant Response", 
            font=("arial", 10, "bold"), fg="blue")
        assistant_str_label.grid(row=1, sticky="E")
        assistant_str_entry = tk.Entry(self, width=30, font=("arial", 12), 
            textvariable=self.assistant_strings_var, fg="#fff", bd=1, bg="#444")
        assistant_str_entry.grid(row=1, column=1, ipady=5, pady=5)

        # Response strings for Calendar service
        calendar_str_label = tk.Label(self, text="Calendar Response", 
            font=("arial", 10, "bold"), fg="blue")
        calendar_str_label.grid(row=2, sticky="E")
        calendar_str_entry = tk.Entry(self, width=30, font=("arial", 12), 
            textvariable=self.calendar_strings_var, fg="#fff", bd=1, bg="#444")
        calendar_str_entry.grid(row=2, column=1, ipady=5, pady=5)

        # Response strings for Note service
        note_str_label = tk.Label(self, text="Note Response", 
            font=("arial", 10, "bold"), fg="blue")
        note_str_label.grid(row=3, sticky="E")
        note_str_entry = tk.Entry(self, width=30, font=("arial", 12), 
            textvariable=self.note_strings_var, fg="#fff", bd=1, bg="#444")
        note_str_entry.grid(row=3, column=1, ipady=5, pady=5)
        
        # Save Button
        save_btn = tk.Button(self, text="Save", font=("arial", 12), 
            bg="#444", fg="#fff", command=self.save_strings, cursor="hand2")
        save_btn.grid(row=4, columnspan=2)

    def save_strings(self):
        assist_str = self.assistant_strings_var.get()
        cal_str = self.calendar_strings_var.get()
        note_str = self.note_strings_var.get()

        if assist_str == "" or cal_str == "" or note_str == "":
            tkinter.messagebox.showinfo("Invalid", "Field cannot be empty.")
        else:
            pattern = r"^[a-zA-Z]+[0-9;\s]*"
            if re.match(pattern, cal_str) and re.match(pattern, note_str):
                with open("assistant_strings.txt", "w") as file:
                    file.write(assist_str)
                with open("calendar_strings.txt", "w") as file:
                    file.write(cal_str)
                with open("Note_strings.txt", "w") as file:
                    file.write(note_str)
            else:
                tkinter.messagebox.showinfo("Invalid", "Only Charater, Number and ; (semicolon)  are allowed.")

        
class MainView(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
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

        #Code for top frame
        label = tk.Label(self.top_frame, text="Welcome to Virtual Assistant", fg="green", font=("tahoma", 16, "bold", "italic"))
        label.pack(side="top")

        # Code for container Frame
        # Back button for Page 1 in Page 2
        back_btn = tk.Button(self.p2, text="<- Back", width=10, fg="#444", command=self.p1.show)
        back_btn.grid(row=0)
        # Show page1 as default page
        self.p1.show()
