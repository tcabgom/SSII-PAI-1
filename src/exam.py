import tkinter as tk
import glob
import json
import os
import hashlib
import time


BUFFER_SIZE = 8192
base_paths = "base_paths.json"
rel_paths = "rel_paths.json"
HASHES_PATH = "paths.json"

def load_files_dict(base_paths_file="base_paths.json", rel_paths_file="rel_paths.json"):
    try:
        with open(base_paths_file, 'r') as f:
            base_paths_dict = json.load(f)
        with open(rel_paths_file, 'r') as f:
            rel_paths_dict = json.load(f)

        file_dict = {}

        for key, relative_path in rel_paths_dict.items():
            if key in base_paths_dict:
                base_path = base_paths_dict[key]
                for r in relative_path:
                    joined_path = os.path.join(base_path, r[0])
                    file_dict[joined_path] = r[1]

        return file_dict

    except FileNotFoundError:
        print("One or both of the files not found.")
        return []

def calculate_hash(file):
    '''
    Devuelve el hash de un archivo
    '''
    file_bytes = read_file(file)
    return hashlib.sha256(file_bytes).hexdigest()


def read_file(file):
    '''
    Lee un archivo y lo devuelve en bytes
    '''
    file_bytes = b""
    with open(file, "rb") as f:
        while True:
            file_content = f.read(BUFFER_SIZE)
            if file_content == b"":
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
    files_dict = load_files_dict()
    good_files = []
    bad_files = []
    for file in files_dict.keys():
        hash = calculate_hash(file)
        if hash == files_dict[file]:
            print("Good file")
            good_files.append(file)
        else:
            print("Bad file")
            bad_files.append(file)
            send_warning_message()

def send_warning_message():
    # Mandar un correo al cliente de que hay un problema de integridad
    return None

def integrity_update(dict):
    with open(HASHES_PATH, 'w') as f:
        json.dump(dict, f, indent=2)



'''
def send_warning_message(receiver_email):
    
    # Configuración de la API de SendGrid
    sg_api_key = 'tu_clave_de_api'  # Reemplaza con tu clave de API de SendGrid

    message = Mail(
        from_email='tu_correo_electronico',  # Reemplaza con tu dirección de correo
        to_emails=receiver_email,
        subject='Advertencia: Problema de Integridad',
        plain_text_content='¡Advertencia! Se detectó un problema de integridad en el sistema.'
    )

    try:
        sg = SendGridAPIClient(sg_api_key)
        response = sg.send(message)
        print(f"Correo electrónico de advertencia enviado con éxito. Código de respuesta: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {e}")

    print("¡Advertencia! Se detectó un problema de integridad.")
'''
