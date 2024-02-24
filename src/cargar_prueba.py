import os
import random

def generar_frase(i):
    
    frase = f"Archivo generado {i}"
    return frase

def crear_archivos(num_archivos, carpeta, extensiones):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    for i in range(1, num_archivos + 1):
        nombre_archivo = f"archivo_{i}{random.choice(extensiones)}"
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        with open(ruta_archivo, 'w') as archivo:
            archivo.write(generar_frase(i))


carpeta_elegida = "../pruebas"  

extensiones = ['.txt', '.csv', '.json', '.xml', '.html', '.pdf']

num_archivos = 1000

crear_archivos(num_archivos, carpeta_elegida, extensiones)

print(f"Se han creado exitosamente {num_archivos} archivos en la carpeta {carpeta_elegida}.")
