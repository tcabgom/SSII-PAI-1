from datetime import datetime
import shutil
import json
import os
import hashlib
import time
from notification import mostrar_notificacion


BUFFER_SIZE = 8192
base_paths = "base_paths.json"
rel_paths = "rel_paths.json"
recovery_directory = "recovery"
deleted_files_directory = "deleted_files"

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
    
    mostrar_notificacion("Realizando chequeo de integridad", f"Realizando chequeo de integridad el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")
    
    start_time = time.time()
    files_dict = load_files_dict()
    good_files = 0
    bad_files = []
    deleted_files = []
    restored_files = []
    for file in files_dict.keys():
        if os.path.exists(file):
            hash = calculate_hash(file)
            if hash == files_dict[file]:
                good_files += 1
            else:
                bad_files.append(file)
                deleted_file_copy = copy_to_deleted_files(file)
                if deleted_file_copy:
                    deleted_files.append(deleted_file_copy)
                    
                restored_file = restore_from_recovery(file, files_dict[file])
                if restored_file:
                    restored_files.append(restored_file)
                    
        else:
            deleted_files.append(file)

    create_integrity_log(good_files, bad_files, deleted_files, restored_files, start_time)
        



def create_integrity_log(good_files, bad_files, deleted_files, restored_files, start_time):
    '''
    Crea un archivo de log con el resultado del chequeo de integridad y muestra una notificación.
    '''
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_filename = f"logs/integrity_log_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"

    with open(log_filename, 'w') as log_file:
        log_file.write("\n########### Summary ###########\n")
        log_file.write(f"Archivos integros: {good_files}\n")
        log_file.write(f"Archivos modificados: {len(bad_files)}\n")
        log_file.write(f"Archivos borrados: {len(deleted_files)}\n")
        log_file.write(f"Archivos restaurados: {len(restored_files)}\n")
        log_file.write(f"Tiempo: {time.time() - start_time:.2f} segundos\n\n")
        log_file.write("Lista de archivos modificados:\n")
        log_file.write("\n".join(bad_files) + "\n")
        log_file.write("\nLista de archivos borrados:\n")
        log_file.write("\n".join(deleted_files) + "\n")
        log_file.write("\nLista de archivos restaurados:\n")
        log_file.write("\n".join(restored_files) + "\n")

    log_notification_message = (f"Chequeo de integridad realizado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                                f"Información guardada dentro de la carpeta de esta aplicación en {log_filename}")
    mostrar_notificacion("Chequeo de integridad finalizado", log_notification_message)




def generar_informe():
    # Recopilar todos los archivos de logs en la carpeta "logs"
    archivos_logs = [archivo for archivo in os.listdir("logs") if archivo.startswith("integrity_log")]

    # Crear una carpeta para almacenar los logs probados
    if not os.path.exists("logs_procesados"):
        os.makedirs("logs_procesados")

    # Mover los archivos de logs a la carpeta de logs probados
    for archivo_log in archivos_logs:
        ruta_origen = os.path.join("logs", archivo_log)
        ruta_destino = os.path.join("logs_procesados", archivo_log)
        os.rename(ruta_origen, ruta_destino)

    # Procesar los archivos de logs
    contenido_logs = []
    for archivo_log in archivos_logs:
        with open(os.path.join("logs_procesados", archivo_log), 'r') as log_file:
            contenido_logs.append(log_file.read())

    # Crear un informe combinando todos los logs
    if not os.path.exists("informes"):
        os.makedirs("informes")
    informe_filename = f"informes/informe_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(informe_filename, 'w') as informe_file:
        informe_file.write("\n\n".join(contenido_logs))


    # Mostrar una notificación indicando la generación del informe
    mostrar_notificacion("Generación de informe", f"Se ha generado un informe con los logs acumulados: {informe_filename}")

def restore_from_recovery(file, original_hash):
    """
    Restaura el archivo desde el directorio de recuperación si es posible.
    Retorna la ruta del archivo restaurado o None si no se pudo restaurar.
    """
    recovery_path = os.path.join(recovery_directory, original_hash)
    
    try:
        shutil.copy2(recovery_path, file)
        return file
    except Exception as e:
        print(f"Error al restaurar el archivo desde el directorio de recuperación: {e}")
        return None


def copy_to_deleted_files(file, deleted_files_directory):
    """
    Copia el archivo al directorio de archivos eliminados.
    """
    if not os.path.exists(deleted_files_directory):
        os.makedirs(deleted_files_directory)

    deleted_file_copy = os.path.join(deleted_files_directory, os.path.basename(file))
    shutil.copy2(file, deleted_file_copy)
    print(f"Copiado el archivo original a {deleted_file_copy}")
