import tkinter as tk
import glob
import json
import os
import hashlib


BUFFER_SIZE = 8192
paths = "src/secured_files.txt"
HASHES_PATH = "paths.json"

def load_files(paths = paths):
    try:
        with open(paths, 'r') as archivo:
            paths = archivo.read().splitlines()
        return paths
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{paths}'.")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

class Hash_Type(Enum):
    SHA256 = "SHA256"

def calculate_hash(file, hash_function = Hash_Type.SHA256):
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


def load_hash_dictionary():
    with open("hashes.json", "r") as f:
        hash_dict = json.load(f)
        return hash_dict["hashes"]


def check_integrity():
    integrity_dict = load_hash_dictionary()
    files = load_files()
    good_files = []
    bad_files = []
    new_files_tracked = []
    for file in files:
        hash = calculate_hash(file)
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
    return None

def send_warning_message():
    # Mandar un correo al cliente de que hay un problema de integridad
    return None

def integrity_update(dict):
    with open(HASHES_PATH, 'w') as f:
        json.dump(dict, f, indent=2)

