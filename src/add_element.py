import json
import os
from tkinter import filedialog, messagebox


def add_new_file():
    directory_path = filedialog.askdirectory(title="Seleccionar directorio para verificar integridad")
    if directory_path:
        add_path_and_subpaths_to_list(directory_path, "paths.txt")

def add_path_and_subpaths_to_list(path, file_path):
    paths = load_saved_paths(file_path)
    if not paths:
        paths = []
    paths.extend(get_all_subpaths(path))

    unique_paths = set(paths)  # Eliminar duplicados
    unique_paths = list(unique_paths)  # Convertir de nuevo a lista

    save_paths_to_file(unique_paths, file_path)

def get_all_subpaths(path):
    subpaths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            subpaths.append(os.path.join(root, file).replace("\\", "/"))
    return subpaths

def save_paths_to_file(paths, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for path in paths:
            f.write(path + '\n')

def load_saved_paths(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar el archivo {file_path}: {str(e)}")
        return []
