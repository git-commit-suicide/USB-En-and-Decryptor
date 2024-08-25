import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
from cryptography.fernet import Fernet

key = r'----#path to key on USB example: r'D:\key.txt'----'
directory = r'#path to vault'
loaded_key = None


def load_key(key):
    with open(key, 'rb') as file:
        return file.read()

def decrypt_directory(directory, key, progress_bar, progress_label):
    fernet = Fernet(key)
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    progress_bar['maximum'] = len(file_list)
    for i, file_path in enumerate(file_list, 1):
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        progress_bar['value'] = i
        progress_label.config(text=f"Decrypting... ({i}/{len(file_list)})")
        window.update_idletasks()
    progress_label.config(text="Decrypted")
    reencrypt_button.pack()

def reencrypt_directory(directory, key, progress_bar, progress_label):
    fernet = Fernet(key)
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    progress_bar['value'] = 0
    progress_bar['maximum'] = len(file_list)
    for i, file_path in enumerate(file_list, 1):
        with open(file_path, 'rb') as original_file:
            data = original_file.read()
        encrypted_data = fernet.encrypt(data)
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        progress_bar['value'] = i
        progress_label.config(text=f"Re-encrypting... ({i}/{len(file_list)})")
        window.update_idletasks()
    progress_label.config(text="Re-encrypted")
    reencrypt_button.pack_forget()
    collapse_button.pack()

def start_decryption():
    global loaded_key
    global directory
    if not loaded_key:
        loaded_key = load_key(key)
    if not loaded_key:
        messagebox.showerror("Error", "Failed to load decryption key")
        return

    decrypt_button.config(state=tk.DISABLED)
    manual_select_button.config(state=tk.DISABLED)
    
    decrypt_directory(directory, loaded_key, progress_bar, progress_label)

def select_key():
    global loaded_key
    key_file = filedialog.askopenfilename(title="Select Decryption Key txt", filetypes=[("Text Files", "*.txt")])
    if key_file:
        loaded_key = load_key(key_file)
        return loaded_key
    else:
        return None

def collapse_window():
    window.destroy()

window = tk.Tk()
window.title("Decryption Progress")
window.geometry("400x200")

progress_label = tk.Label(window, text="Decrypting...", font=("Arial", 12))
progress_label.pack(pady=10)

progress_bar = Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=10)

decrypt_button = tk.Button(window, text="Start Decryption", command=start_decryption)
decrypt_button.pack(pady=5)

manual_select_button = tk.Button(window, text="Select Decryption Key Manually", command=select_key)
manual_select_button.pack(pady=5)

reencrypt_button = tk.Button(window, text="Re-encrypt", command=lambda: reencrypt_directory(directory, loaded_key, progress_bar, progress_label))

collapse_button = tk.Button(window, text="Collapse", command=collapse_window)

window.mainloop()

