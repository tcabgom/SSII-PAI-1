import tkinter as tk
import glob
import json
import os

BUFFER_SIZE = 8192
'''
import hashlib
import os

def calcular_hash(file_path):
    # Calcula el hash de un archivo dado
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()
'''


def calculate_hash():
    # Función para calcular hash de binario/imagen/directorio
    return None


'''
def check_integrity(file_path, hash_file="hash_guardado.txt"):
    # Comprueba que el hash de un fichero coincide con el guardado
    try:
        with open(hash_file, 'r') as f:
            hash_guardado = f.read().strip()
    except FileNotFoundError:
        print("No se encontró un hash guardado. Por favor, guarda el hash antes de verificar la integridad.")
        return False

    if os.path.isfile(file_path):
        current_hash = calcular_hash(file_path)
        if current_hash == hash_guardado:
            print(f"La integridad del archivo {file_path} es válida.")
            return True
        else:
            print(f"Advertencia: La integridad del archivo {file_path} no es válida.")
            return False

    elif os.path.isdir(file_path):
        # Verificar integridad de un directorio
        for root, dirs, files in os.walk(file_path):
            for file_name in files:
                current_file_path = os.path.join(root, file_name)
                current_hash = calcular_hash(current_file_path)
                if current_hash != hash_guardado:
                    print(f"Advertencia: La integridad del archivo {current_file_path} no es válida.")
                    return False

        print(f"La integridad del directorio {file_path} es válida.")
        return True

    else:
        print(f"Error: La ruta {file_path} no es un archivo ni un directorio válido.")
        return False

# Uso de la función
archivo_o_directorio_a_verificar = "ruta/del/archivo_o_directorio"
hash_calculado = calcular_hash(archivo_o_directorio_a_verificar)
guardar_hash(hash_calculado, hash_file="hash_guardado.txt")
check_integrity(archivo_o_directorio_a_verificar)

'''

def obtain_path_files(path, hashfuction):
    path = path + "/**"
    files = []
    for file in glob.glob(path, recursive=True):
        if os.path.isfile(file):
            files.append(os.path.abspath(file))
    return files


def calculate_hash(file, hash_function):
    file_bytes = read_file(file)
    case default:
        return hashlib.sha256(file_bytes).hexdigest()


def read_file(file):
    file_bytes = b""
    with open(file, "rb") as f:
        while True:
            file_content = f.read(BUFFER_SIZE)
            if not file_content:
                break
            b += file_content
    return file_bytes



def hash_files(files):
    # Calcula el hash de un archivo
    return None 

def load_hash_dictionary():
    with open("hashes.json", "r") as f:
        hash_dict = json.load(f)
        return hash_dict["hashes"]


def check_integrity():
    # Comprueba que el hash de un fichero coincide con el guardado
    return None


def begin_exam():
    # Verificar integridad de ficheros marcados
    return None


def send_warning_message():
    # Mandar un correo al cliente de que hay un problema de integridad
    return None


if __name__ == '__main__':
    print("Hello World")


'''

import tkinter as tk
import hashlib
import os
from tkinter import filedialog
from tkinter import messagebox

def calculate_hash(file_path):
    # Calcula el hash de un archivo dado
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def hash_directory(directory_path, hash_file="hash_guardado_directorio.txt"):
    # Hashea todos los archivos de un directorio y guarda los hashes en un archivo
    hashes = {}

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_hash(file_path)
            hashes[file_path] = file_hash

    with open(hash_file, 'w') as f:
        for file_path, file_hash in hashes.items():
            f.write(f"{file_path}:{file_hash}\n")

def check_integrity(directory_path, hash_file="hash_guardado_directorio.txt"):
    # Compara los hashes guardados con los hashes actuales de un directorio
    try:
        with open(hash_file, 'r') as f:
            saved_hashes = {line.split(':')[0]: line.split(':')[1].strip() for line in f.readlines()}
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró un archivo de hashes guardados. Debes generar los hashes antes de verificar la integridad.")
        return False

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            current_hash = calculate_hash(file_path)

            if file_path in saved_hashes:
                saved_hash = saved_hashes[file_path]

                if current_hash != saved_hash:
                    messagebox.showwarning("Advertencia", f"Advertencia: La integridad del archivo {file_path} ha cambiado.")
                    return False
            else:
                messagebox.showwarning("Advertencia", f"Advertencia: El archivo {file_path} no estaba presente en el conjunto original.")
                return False

    messagebox.showinfo("Integridad", f"La integridad del directorio {directory_path} es válida.")
    return True

def begin_exam():
    # Verificar integridad de ficheros marcados
    directory_path = filedialog.askdirectory(title="Seleccionar directorio para verificar integridad")
    if directory_path:
        hash_directory(directory_path)
        check_integrity(directory_path)

def send_warning_message(receiver_email):
    # Puedes implementar aquí la función para enviar un correo electrónico si lo deseas
    print("¡Advertencia! Se detectó un problema de integridad.")

def application_screen():
    # Pantalla de la aplicación
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
    start_button = tk.Button(window, text="Start Exam", bg=color_button, activebackground=color_button_pressed)
    exit_button = tk.Button(window, text="Close Program", bg=color_button, activebackground=color_button_pressed, command=window.destroy)

    test_text.pack(pady=10)
    new_element_button.pack(pady=5)
    log_file_button.pack(pady=5)
    start_button.pack(pady=5)
    exit_button.pack(pady=5)
    window.mainloop()

if __name__ == '__main__':
    application_screen()

'''