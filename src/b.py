import tkinter as tk
import hashlib
import os
import json
from tkinter import filedialog
from tkinter import messagebox

def calculate_hash(file_path):
    '''
    Calcula el hash SHA-256 de un archivo dividido en bloques de 8192 bytes
    '''
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def hash_directory(directory_path, hash_file="hashes.json"):
    '''
    Calcula el hash de todos los archivos y directorios de un directorio y sus subdirectorios
    '''
    hashes = {}

    for root, dirs, files in os.walk(directory_path):

        for file_name in files:
            file_path = os.path.join(root, file_name).replace("\\", "/")
            if os.path.isfile(file_path):  # Verifica si es un archivo
                file_hash = calculate_hash(file_path)
                hashes[file_path] = file_hash

    with open(hash_file, 'w') as f:
        json.dump(hashes, f, indent=2)

def load_saved_hashes(hash_file):
    try:
        with open(hash_file, 'r') as f:
            data = f.read()
            if data:
                return json.loads(data)
            else:
                return {}
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        messagebox.showerror("Error", f"El archivo {hash_file} no es un archivo JSON válido.")
        return {}


def save_paths_to_file(paths, file_path):
    with open(file_path, 'w') as f:
        json.dump(paths, f, indent=2)

def add_path_to_list(path, file_path):
    paths = load_saved_hashes(file_path)
    if not paths:
        paths = []
    paths.append(path.replace("\\", "/"))
    save_paths_to_file(paths, file_path)


def check_directory_integrity(directory_path, saved_hashes):
    for root, dirs, files in os.walk(directory_path):


        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):  # Verifica si es un archivo
                check_item_integrity(file_path, saved_hashes)

def check_item_integrity(item_path, saved_hashes):
    if item_path in saved_hashes:
        saved_hash = saved_hashes[item_path]
        current_hash = calculate_hash(item_path)

        if current_hash != saved_hash:
            messagebox.showwarning("Advertencia", f"Advertencia: La integridad de {item_path} ha cambiado.")
            raise IntegrityError()
    else:
        messagebox.showwarning("Advertencia", f"Advertencia: {item_path} no estaba presente en el conjunto original.")
        raise IntegrityError()

def check_integrity(directory_path, hash_file="hashes.json"):
    print("Checking integrity for", directory_path)
    saved_hashes = load_saved_hashes(hash_file)

    if saved_hashes:
        try:
            check_directory_integrity(directory_path, saved_hashes)
            messagebox.showinfo("Integridad", f"La integridad del directorio {directory_path} es válida.")
            return True
        except IntegrityError:
            return False

class IntegrityError(Exception):
    pass

def begin_exam():
    directory_path = filedialog.askdirectory(title="Seleccionar directorio para verificar integridad")
    if directory_path:
        add_path_to_list(directory_path, "paths.json")

def start_exam():
    paths = load_saved_hashes("paths.json")
    for path in paths:
        hash_directory(path)
        check_integrity(path)

def application_screen():
    window = tk.Tk()

    color_background =     "#28393b"
    color_text =           "#ffffff"
    color_button =         "#4caf50"
    color_button_pressed = "#388e3c"

    window.geometry("960x640")
    window.title("Sistema de Detección de Intrusos")
    window.configure(bg=color_background)

    test_text = tk.Label(window, text="Welcome", fg=color_text, bg=color_background)
    new_element_button = tk.Button(window, text="Add Element", bg=color_button, activebackground=color_button_pressed, command=begin_exam)
    log_file_button = tk.Button(window, text="Open Log File", bg=color_button, activebackground=color_button_pressed)
    start_button = tk.Button(window, text="Start Exam", bg=color_button, activebackground=color_button_pressed, command=start_exam)
    exit_button = tk.Button(window, text="Close Program", bg=color_button, activebackground=color_button_pressed, command=window.destroy)

    test_text.pack(pady=10)
    new_element_button.pack(pady=5)
    log_file_button.pack(pady=5)
    start_button.pack(pady=5)
    exit_button.pack(pady=5)
    window.mainloop()


if __name__ == '__main__':
    application_screen()