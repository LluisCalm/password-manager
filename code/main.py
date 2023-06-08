import customtkinter as ctk
from password import Password
from CTkMessagebox import CTkMessagebox
import os
import json
import base64
import os
from cryptography.fernet import Fernet
import base64, hashlib

add_pass = "Save new password"
obtain_pass = "Obtain password"
change_pass = "Change password"
password_list = []
sites_list = []

def gen_fernet_key(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def verify_json():
    if os.path.isfile('passwords.json'):
        return
    
    events = {}
    events['passwords'] = []
    with open("passwords.json","w") as f:
        json.dump(events,f)


def obtain_passwords():
    with open('passwords.json') as x:
        data = json.load(x)['passwords']
    
    for x in data:
        password_list.append(Password(x['site'],x['pass']))
        sites_list.append(x['site'])
    

def is_site(site):
    for x in password_list:
        if x.get_site() == site:
            return True
    return False

def save_password():

    if master_key_entry.get() == "" or site_entry.get() == "" or password_entry.get() == "":
        CTkMessagebox(title="Warning", message="One or more fields are empty")
        return
    
    if is_site(site_entry.get()):
        CTkMessagebox(title="Warning", message="This site has alredy a password saved")
        return
    
    key = gen_fernet_key(master_key_entry.get().encode('utf-8'))
    fernet = Fernet(key)
    cypher_password = fernet.encrypt(password_entry.get().encode('utf-8'))
    password_list.append(Password(site_entry.get(), cypher_password.decode("utf-8") ))
    sites_list.append(site_entry.get())
    
    save_json()
    
    

def change_password():
    print("a")


def save_json():
    to_save = {}
    to_save['passwords']=[]
    for x in password_list:
        to_save['passwords'].append({'site' : x.get_site(), 'pass' : x.get_pass()})

    with open("passwords.json","w") as f:
        json.dump(to_save, f)


# First actions:
verify_json()
obtain_passwords()


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
site_selector = ctk.CTkOptionMenu(options_tab.tab(obtain_pass),values=sites_list)
obtain_button = ctk.CTkButton(options_tab.tab(obtain_pass),text="Obtain", command=obtain_passwords)

site_selector.pack(pady=10)
obtain_button.pack(pady=10)

# Change password tab
site_selector = ctk.CTkOptionMenu(options_tab.tab(change_pass),values=sites_list)
master_key_entry_ch = ctk.CTkEntry(options_tab.tab(change_pass),placeholder_text="Master key")
current_password_entry = ctk.CTkEntry(options_tab.tab(change_pass),placeholder_text="Current password")
new_password_entry = ctk.CTkEntry(options_tab.tab(change_pass),placeholder_text="New password")
obtain_button = ctk.CTkButton(options_tab.tab(change_pass),text="Change", command=change_password)

site_selector.pack(pady=10)
master_key_entry_ch.pack(pady=10)
current_password_entry.pack(pady=10)
new_password_entry.pack(pady=10)
obtain_button.pack(pady=10)


app.mainloop()