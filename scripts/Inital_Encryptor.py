import os
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from cryptography.fernet import Fernet

key = r'----#path to key on USB example: r'D:\key.txt'----'
directory = r'#path to vault'

def load_key(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def encrypt_directory(directory, key, progress_bar, progress_label):
    fernet = Fernet(key)
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    progress_bar['maximum'] = len(file_list)
    for i, file_path in enumerate(file_list, 1):
        with open(file_path, 'rb') as original_file:
            data = original_file.read()
        encrypted_data = fernet.encrypt(data)
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
        progress_bar['value'] = i
        progress_label.config(text=f"Encrypting... ({i}/{len(file_list)})")
        window.update_idletasks()
    progress_label.config(text="Encrypted")
    collapse_button.pack()

def select_and_encrypt():
    global key
    key = load_key(key)
    if not key:
        messagebox.showerror("Error", "Failed to load encryption key.")
        return
    encrypt_button.config(state=tk.DISABLED)
    encrypt_directory(directory, key, progress_bar, progress_label)

def collapse_window():
    window.destroy()

window = tk.Tk()
window.title("Encryption Progress")
window.geometry("400x200")

progress_label = tk.Label(window, text="Ready to Encrypt", font=("Arial", 12))
progress_label.pack(pady=10)

progress_bar = Progressbar(window, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=10)

encrypt_button = tk.Button(window, text="Start Encryption", command=select_and_encrypt)
encrypt_button.pack(pady=5)

collapse_button = tk.Button(window, text="Collapse", command=collapse_window)

window.mainloop()
