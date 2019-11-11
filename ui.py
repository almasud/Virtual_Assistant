import tkinter as tk
import tkinter.messagebox
import re

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="This is page 1")
        label.pack(side="top", fill="both", expand=True)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.strings_form()
        
    def strings_form(self):
        self.calendar_strings = tk.StringVar()
        self.note_strings = tk.StringVar()
        # Set initial value
        self.calendar_strings.set("what i have;do i have plans;do i have any plan;am i busy;mi busy")
        self.note_strings.set("make a note;write this down;remember this")
        
        # For Calendar Command Strings
        calendar_str_label = tk.Label(self, text="Calendar Strings", font=("arial", 10, "bold"))
        calendar_str_label.grid(row=1, sticky="E")
        calendar_str_entry = tk.Entry(self, width=30, font=("arial", 12), 
            textvariable=self.calendar_strings, fg="blue")
        calendar_str_entry.grid(row=1, column=1, ipady=5, pady=5)
        # For Note Command Strings
        note_str_label = tk.Label(self, text="Note Strings", font=("arial", 10, "bold"))
        note_str_label.grid(row=2, sticky="E")
        note_str_entry = tk.Entry(self, width=30, font=("arial", 12), 
            textvariable=self.note_strings, fg="blue")
        note_str_entry.grid(row=2, column=1, ipady=5, pady=5)
        # Save Button
        save_btn = tk.Button(self, text="Save", font=("arial", 12), command=self.save_strings)
        save_btn.grid(row=3, columnspan=2)

    def save_strings(self):
        cal_str = self.calendar_strings.get()
        note_str = self.note_strings.get()

        if cal_str == "" or note_str == "":
            tkinter.messagebox.showinfo("Invalid", "Field cannot be empty.")
        else:
            pattern = r"^[a-zA-Z]+[0-9;\s]*"
            if re.match(pattern, cal_str) and re.match(pattern, note_str):
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

        top_frame = tk.Frame(self )
        container = tk.Frame(self)
        top_frame.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        #Code for top frame
        label = tk.Label(top_frame, text="Welcome to Virtual Assistant", fg="#444", font=("tahoma", 16, "bold", "italic"))
        label.pack(side="top")

        # Code for container
         # Back button for Page 1 in Page 2
        back_btn = tk.Button(self.p2, text="Back", fg="#444", command=self.p1.show)
        back_btn.grid(row=0)
        # Show page1 as default page
        self.p1.show()
