import tkinter as tk
import glob
import json
import os
import hashlib
from tkinter import filedialog
from tkinter import messagebox

BUFFER_SIZE = 8192

def read_secured_paths_file():
    file_path = os.path.join(os.path.dirname(__file__), "secured_files.txt")
    try:
        with open(file_path, 'r') as f:
            folders  =[line.strip() for line in f.readlines()]
        return folders
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
        return []


def obtain_path_files(path, visited_directories=None):
    '''
    Obtiene todos los archivos de un directorio y sus subdirectorios recursivamente
    '''
    if visited_directories is None:
        visited_directories = set()

    path = os.path.join(path, "**")
    files = []

    for file in glob.glob(path, recursive=True):
        if os.path.isfile(file):
            files.append(os.path.abspath(file))
        elif os.path.isdir(file) and file not in visited_directories:
            visited_directories.add(file)
            files += obtain_path_files(file, visited_directories)

    return files


def calculate_hash(file, hash_function):
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
    good_files_number = 0 
    bad_files = []
    no_matches_files = []
    original_hashes_dictionary = load_hash_dictionary()
    current_hashes_dictionary = {}
    return None


def send_warning_message():
    # Mandar un correo al cliente de que hay un problema de integridad
    return None


if __name__ == '__main__':
    files = obtain_path_files("../../Downloads/rl_mario", None)
    for file in files:
        print("Hash de ", file, ":", calculate_hash(file, None))
