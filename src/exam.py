import tkinter as tk
import glob
import json
import os
import hashlib


BUFFER_SIZE = 8192
base_paths = "base_paths.json"
rel_paths = "rel_paths.json"
HASHES_PATH = "paths.json"

def load_files(base_paths_file="base_paths.json", rel_paths_file="rel_paths.json"):
    try:
        with open(base_paths_file, 'r') as f:
            base_paths_dict = json.load(f)
        with open(rel_paths_file, 'r') as f:
            rel_paths_dict = json.load(f)

        file_list = []

        for key, relative_path in rel_paths_dict.items():
            if key in base_paths_dict:
                base_path = base_paths_dict[key]
                print(base_path, "\n", relative_path)
                for r in relative_path:
                    joined_path = os.path.join(base_path, r)
                    file_list.append(joined_path)

        return file_list

    except FileNotFoundError:
        print("One or both of the files not found.")
        return []

def calculate_hash(file):
    '''
    Devuelve el hash de un archivo
    '''
    # TODO Quizas deba admitir distintos tipos de funciones hash
    file_bytes = read_file(file)
    return hashlib.sha256(file_bytes).hexdigest()


def read_file(file):
    '''
    Lee un archivo y lo devuelve en bytes
    '''
    # TODO Considerar añadirle id de usuario y/o un token para mayor seguridad
    file_bytes = b""
    with open(file, "rb") as f:
        while True:
            file_content = f.read(BUFFER_SIZE)
            if not file_content:
                break
            file_bytes += file_content

    return file_bytes


def load_hash_dictionary(file_path="hashes.json"):
    try:
        with open(file_path, "r") as f:
            hash_dict = json.load(f)
            return hash_dict.get("hashes", {})
    except FileNotFoundError:
        with open(file_path, "w") as f:
            json.dump({"hashes": {}}, f)
        return {}


def check_integrity():
    '''
    Examina la integridad de los archivos
    '''
    integrity_dict = load_hash_dictionary()
    files = load_files()
    good_files = []
    bad_files = []
    new_files_tracked = []
    for file in files:
        hash = calculate_hash(file)
        print(hash)
        if file in integrity_dict:
            if hash == integrity_dict[file]:
                good_files.append(file)
            else:
                bad_files.append(file)
                send_warning_message()
        else:
            new_files_tracked.append(file)
            integrity_dict[file] = hash
    if len(new_files_tracked) != 0:
        integrity_update(integrity_dict)

def send_warning_message():
    # Mandar un correo al cliente de que hay un problema de integridad
    return None

def integrity_update(dict):
    with open(HASHES_PATH, 'w') as f:
        json.dump(dict, f, indent=2)

if __name__ == '__main__':
    for f in load_files():
        print(f)
