import os
import random

ruta_origen = 'facturas/'
ruta_destino = 'data/'

def moveToPath():
    archivos = os.listdir(ruta_origen)
    archivo_aleatorio = random.choice(archivos)

    ruta_archivo_aleatorio = os.path.join(ruta_origen, archivo_aleatorio)

    nuevo_nombre = 'data.xml'
    ruta_nuevo_archivo = os.path.join(ruta_destino, nuevo_nombre)

    os.rename(ruta_archivo_aleatorio, ruta_nuevo_archivo)

moveToPath()