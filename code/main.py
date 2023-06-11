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
password_list = []
sites_list = []


####################################
#          Json functions
####################################

def load_json():
    if os.path.isfile('passwords.json'):
        with open('passwords.json') as x:
            data = json.load(x)['passwords']
            for x in data:
                password_list.append(Password(x['site'],x['pass']))
                sites_list.append(x['site'])
        return
    
    events = {}
    events['passwords'] = []
    with open("passwords.json","w") as f:
        json.dump(events,f)

def save_json():
    to_save = {}
    to_save['passwords']=[]
    for x in password_list:
        to_save['passwords'].append({'site' : x.get_site(), 'pass' : x.get_pass()})

    with open("passwords.json","w") as f:
        json.dump(to_save, f)

####################################
# Encrypyon and decrypyion functions
####################################

def gen_fernet_key(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def decrypt_pass(password, master_key):
    key = gen_fernet_key(bytes(master_key,'utf-8'))
    fernet = Fernet(key)
    return fernet.decrypt(bytes(password,'utf-8'))

def cypher_pass(master_key,password):
    key = gen_fernet_key(master_key.encode('utf-8'))
    fernet = Fernet(key)
    return fernet.encrypt(password.encode('utf-8'))


####################################
#           GUI functions
####################################
def obtain_password():

    if is_site(site_entry.get()):
        CTkMessagebox(title="Warning", message="Site not found")
        return
    
    if master_key_selector.get() == "" or site_selector.get() == "":
        CTkMessagebox(title="Warning", message="One or more fields are empty")
        return

    password = get_site_pass(site_selector.get())
    
    clear_password = decrypt_pass(password, master_key_selector.get())

    app.clipboard_clear()
    app.clipboard_append(clear_password)
    CTkMessagebox(title="Info", message="Password copied to clipboard")
    

def get_site_pass(site):
    for x in password_list:
        if x.get_site() == site:
            return x.get_pass()

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
    
    cypher_password = cypher_pass(master_key_entry.get(),password_entry.get())

    password_list.append(Password(site_entry.get(), cypher_password.decode("utf-8") ))
    sites_list.append(site_entry.get())
    
    save_json()
    

if __name__ == "__main__":
    load_json()

####################################
#               GUI
####################################
app = ctk.CTk()
app.title('Password manager')
app.geometry('400x350')

options_tab = ctk.CTkTabview(app)
options_tab.pack(fill="x", pady=10)

options_tab.add(add_pass)
options_tab.add(obtain_pass)

# Options tab
master_key_entry = ctk.CTkEntry(options_tab.tab(add_pass),placeholder_text="Master key")
master_key_entry.configure(show="*")
site_entry = ctk.CTkEntry(options_tab.tab(add_pass),placeholder_text="Site")
password_entry = ctk.CTkEntry(options_tab.tab(add_pass),placeholder_text="Password")
password_entry.configure(show="*")
save_button = ctk.CTkButton(options_tab.tab(add_pass),text="Save", command=save_password)

master_key_entry.pack(pady=10)
site_entry.pack(pady=10)
password_entry.pack(pady=10)
save_button.pack(pady=10)

# Obtain password tab
site_selector = ctk.CTkOptionMenu(options_tab.tab(obtain_pass),values=sites_list)
master_key_selector = ctk.CTkEntry(options_tab.tab(obtain_pass),placeholder_text="Master key")
master_key_selector.configure(show="*")
obtain_button = ctk.CTkButton(options_tab.tab(obtain_pass),text="Obtain", command=obtain_password)

site_selector.pack(pady=10)
master_key_selector.pack(pady=10)
obtain_button.pack(pady=10)


app.mainloop()
