import glob
import json
import os
from tkinter import filedialog, messagebox

base_paths = "base_paths.json"
rel_paths = "rel_paths.json"

def load_base_paths():
    with open(base_paths, 'r', encoding='utf-8') as f:
        pass
    pass

def add_new_file():
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
        print(p)
    
    with open(rel_paths, 'w', encoding='utf-8') as f:
        json.dump(rel_paths_dict, f)

def obtain_path_files(path, id, base_path, visited_directories=None):
    '''
    Obtiene todos los archivos de un directorio y sus subdirectorios recursivamente
    '''
    if visited_directories is None:
        visited_directories = set()

    path = os.path.join(path, "**")
    files = set()

    for file in glob.glob(path, recursive=True):
        if os.path.isfile(file):
            files.add(parse_file_path(file, id, base_path))
        elif os.path.isdir(file) and file not in visited_directories:
            visited_directories.add(file)
            files.update(obtain_path_files(file, id, base_path, visited_directories))

    return files

def parse_file_path(file, id, base_path):
    '''
    Devuelve la ruta relativa de un archivo con respecto a un directorio base
    '''
    relative_path = os.path.relpath(file, base_path)
    return relative_path


'''

def add_new_file():

    directory_path = filedialog.askdirectory(title="Seleccionar directorio para verificar integridad")

    if os.path.exists(rel_paths):
        with open(rel_paths, 'r', encoding='utf-8') as file:
            rel_paths_dict = json.load(file)
    else:
        rel_paths_dict = {}

    if directory_path:
        if not os.path.exists(base_paths):
            with open(base_paths, 'w', encoding='utf-8') as create_file:
                pass
        with open(base_paths, 'r+', encoding='utf-8') as f:
            f.write(directory_path + '\n')
            id = len(f.readlines())
            for p in obtain_path_files(directory_path, id, directory_path):
                if id not in rel_paths_dict:
                    rel_paths_dict[id] = [p]
                else:
                    rel_paths_dict[id].append(p)
                print(p)
        
        with open(rel_paths, 'w', encoding='utf-8') as f:
            json.dump(rel_paths_dict, f)





            

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

'''
