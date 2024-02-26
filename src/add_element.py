import glob
import json
import os
import shutil
import exam
from tkinter import filedialog, messagebox

base_paths = "base_paths.json"
rel_paths = "rel_paths.json"
recovery_directory = "/recovery"


def add_new_dir():
    '''
    Añade un nuevo directorio a la lista de archivos a verificar
    '''
    directory_path = filedialog.askdirectory(title="Seleccionar directorio para verificar integridad")

    if directory_path:
        id,duplicated = add_base_path(directory_path)
        if duplicated:
            messagebox.showerror("Error", "El directorio seleccionado ya se encuentra en la lista")
            return
        add_rel_path(directory_path, id)
        
    print(f"Añadido directorio {directory_path} correctamente ")

def add_new_file():
    file_path = filedialog.askopenfilename(title="Seleccionar archivo para verificar integridad")
    if file_path:
        duplicated = add_filepath(file_path)
        if duplicated:
            messagebox.showerror("Error", "El archivo seleccionado ya se encuentra en la lista")
            return
        
    print(f"Añadido archivo {file_path} correctamente")
    
def add_filepath(file_path):
    base, rel = split_string_in_half(file_path) 
    id, duplicated = add_base_path(base)
    if duplicated:
        return duplicated
    if os.path.exists(rel_paths):
        with open(rel_paths, 'r', encoding='utf-8') as file:
            rel_paths_dict = json.load(file)
    else:
        rel_paths_dict = {}  
    
    rel_path = get_relpath(file_path, base)
    rel_paths_dict[id] = [rel_path]
    
    with open(rel_paths, 'w', encoding='utf-8') as f:
        json.dump(rel_paths_dict, f)


def split_string_in_half(input_string):
    length = len(input_string)
    middle = length // 2

    first_half = input_string[:middle]
    second_half = input_string[middle:]

    return first_half, second_half

def add_base_path(directory_path):
    id = 0
    duplicated = False
    if os.path.exists(base_paths):
        with open(base_paths, 'r', encoding='utf-8') as file:
            base_paths_dict = json.load(file)
        if directory_path in base_paths_dict.values():
            duplicated = True
            return None, duplicated
        id = len(base_paths_dict.keys())
        base_paths_dict[id] = directory_path
    else:
        base_paths_dict = {}
        base_paths_dict[id] = directory_path

    with open(base_paths, 'w', encoding='utf-8') as f:
        json.dump(base_paths_dict, f)
    return id, duplicated

def add_rel_path(directory_path, id):
    if os.path.exists(rel_paths):
        with open(rel_paths, 'r', encoding='utf-8') as file:
            rel_paths_dict = json.load(file)
    else:
        rel_paths_dict = {}
    for p in obtain_path_files(directory_path, id, directory_path):
        if id not in rel_paths_dict:
            rel_paths_dict[id] = [p]
        else:
            rel_paths_dict[id].append(p)

    
    with open(rel_paths, 'w', encoding='utf-8') as f:
        json.dump(rel_paths_dict, f)

def update_rel_paths():
    if os.path.exists(base_paths):
        with open(base_paths, 'r', encoding='utf-8') as file:
            base_paths_dict = json.load(file)
    else:
        return

    if os.path.exists(rel_paths):
        with open(rel_paths, 'r', encoding='utf-8') as file:
            rel_paths_dict = json.load(file)
    else:
        rel_paths_dict = {}

    for id, base_path in base_paths_dict.items():
        paths = obtain_path_files(base_path, id, base_path)
        
        if id not in rel_paths_dict:
            rel_paths_dict[id] = paths
        else:
            rel_paths_dict[id].extend(paths)

    with open(rel_paths, 'w', encoding='utf-8') as f:
        json.dump(rel_paths_dict, f, indent=2) 

def obtain_path_files(path, id, base_path, visited_directories=None):
    '''
    Obtiene todos los archivos de un directorio y sus subdirectorios recursivamente
    '''
    if visited_directories is None:
        visited_directories = set()

    path = os.path.join(path, "**")
    files = set()
    if not os.path.exists(recovery_directory):
        os.makedirs(recovery_directory)
    for file in glob.glob(path, recursive=True):
        if os.path.isfile(file):
            rel_path = get_relpath(file, base_path)
            hash_value = rel_path[1]  
            copy_to_recovery_directory(file, hash_value)
            files.add(rel_path)
        elif os.path.isdir(file) and file not in visited_directories:
            visited_directories.add(file)
            files.update(obtain_path_files(file, id, base_path, visited_directories))

    return files

def get_relpath(file, base_path):
    '''
    Devuelve la ruta relativa de un archivo con respecto a un directorio base
    '''
    hash = exam.calculate_hash(file)
    relative_path = os.path.relpath(file, base_path)
    return (relative_path,hash)

def copy_to_recovery_directory(file, hash_value):
    """
    Copia el archivo al directorio de recuperación con el nombre del hash.
    """
    recovery_path = os.path.join(recovery_directory, hash_value)

    try:
        shutil.copy2(file, recovery_path)
        print("Archivo copiado correctamente al directorio de recuperación")
    except Exception as e:
        print(f"Error al copiar el archivo: {e}")

