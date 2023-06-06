import customtkinter as ctk
from password import Password
from CTkMessagebox import CTkMessagebox
import os
import json

add_pass = "Save new password"
obtain_pass = "Obtain password"
change_pass = "Change password"

# Search the events.json or creates it 
def verify_json():
    if os.path.isfile('events.json'):
        return
    
    events = {}
    events['events'] = []
    with open("events.json","w") as f:
        json.dump(events,f)

def is_site(site):
    return False

def obtain_password():
    print(site_selector.get)

def save_password():
    if master_key_entry.get() == "" or site_entry.get() == "" or password_entry.get() == "":
        CTkMessagebox(title="Warning", message="One or more fields are empty")
    
    if is_site(site_entry.get()):
        CTkMessagebox(title="Warning", message="This site has alredy a password saved")
    print("a")


###########
#   GUI
###########
app = ctk.CTk()
app.title('Password manager')
app.geometry('400x350')

options_tab = ctk.CTkTabview(app)
options_tab.pack(fill="x", pady=10)

options_tab.add(add_pass)
options_tab.add(obtain_pass)
options_tab.add(change_pass)

# Options tab
master_key_entry = ctk.CTkEntry(options_tab.tab(add_pass),placeholder_text="Master key")
site_entry = ctk.CTkEntry(options_tab.tab(add_pass),placeholder_text="Site")
password_entry = ctk.CTkEntry(options_tab.tab(add_pass),placeholder_text="Password")
save_button = ctk.CTkButton(options_tab.tab(add_pass),text="Save", command=save_password)

master_key_entry.pack(pady=10)
site_entry.pack(pady=10)
password_entry.pack(pady=10)
save_button.pack(pady=10)

# Obtain password tab
site_selector = ctk.CTkOptionMenu(options_tab.tab(obtain_pass),values=["option 1", "option 2"]) # En un futuro aqui poner el string
obtain_button = ctk.CTkButton(options_tab.tab(obtain_pass),text="Obtain", command=obtain_password)

site_selector.pack(pady=10)
obtain_button.pack(pady=10)

# Change password tab
site_selector = ctk.CTkOptionMenu(options_tab.tab(change_pass),values=["option 1", "option 2"]) # En un futuro aqui poner el string
master_key_entry_ch = ctk.CTkEntry(options_tab.tab(change_pass),placeholder_text="Master key")
current_password_entry = ctk.CTkEntry(options_tab.tab(change_pass),placeholder_text="Current password")
new_password_entry = ctk.CTkEntry(options_tab.tab(change_pass),placeholder_text="New password")
obtain_button = ctk.CTkButton(options_tab.tab(change_pass),text="Change", command=obtain_password)

site_selector.pack(pady=10)
master_key_entry_ch.pack(pady=10)
current_password_entry.pack(pady=10)
new_password_entry.pack(pady=10)
obtain_button.pack(pady=10)


app.mainloop()