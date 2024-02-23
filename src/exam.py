import datetime
import tkinter as tk
import glob
import json
import os
import hashlib
import time
import add_element


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
    start_time = time.time()
    files_dict = load_files_dict()
    good_files = 0
    bad_files = []
    deleted_files = []
    for file in files_dict.keys():
        if os.path.exists(file):
            hash = calculate_hash(file)
            if hash == files_dict[file]:
                good_files += 1
            else:
                bad_files.append(file)
                send_warning_message()
        else:
            deleted_files.append(file)

    log_filename = f"logs/integrity_log_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

    with open(log_filename, 'w') as log_file:

        log_file.write("\n########### Summary ###########\n")
        log_file.write(f"Total Good Files: {good_files}\n")
        log_file.write(f"Total Bad Files: {len(bad_files)}\n")
        log_file.write(f"Total Deleted Files: {len(deleted_files)}\n")
        log_file.write(f"Time taken: {time.time() - start_time:.2f} seconds\n\n")
        log_file.write("List of Bad Files:\n")
        log_file.write("\n".join(bad_files) + "\n")
        log_file.write("\nList of Deleted Files:\n")
        log_file.write("\n".join(deleted_files) + "\n")


def send_warning_message():
    destinatario = "alex.0002002@gmail.com"
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    remitente = 'tu_correo@gmail.com'
    contraseña = 'tu_contraseña'
    

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
