import xml.etree.ElementTree as ET
import os
import shutil
from proyecto.move_file import moveToPath
from proyecto.facturaSII import sii_insert
from proyecto.factura_normal import normal_insert

ruta_origen = 'facturas/'
ruta_destino = 'data/'
ruta_error = 'Error/'
def main():
    factura = str('data/data.xml')

    moveToPath()
    tree = ET.parse(factura)
    root = tree.getroot()
    root2 = str(root)
    texto = '{http://www.sii.cl/SiiDte}DTE'

    if texto in root2:
        print('Factura SII')
        try:
            sii_insert()
        except Exception as e:
            file_count = len(os.listdir(ruta_error))
            nuevo_nombre = f'error_factura_{file_count}.xml'
            shutil.move(ruta_destino+'data.xml', os.path.join(ruta_error, nuevo_nombre))
    else:
        print('Factura Normal')
        try:
            normal_insert()
        except Exception as e:
            file_count = len(os.listdir(ruta_error))
            nuevo_nombre = f'error_factura_{file_count}.xml'
            shutil.move(ruta_destino+'data.xml', os.path.join(ruta_error, nuevo_nombre))

num_files = len([f for f in os.listdir(ruta_origen) if os.path.isfile(os.path.join(ruta_origen, f))])
print('Total de Archivos a Cargar a SQL : '+ str(num_files))

for i in range(num_files):
    main()
