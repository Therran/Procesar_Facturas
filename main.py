import xml.etree.ElementTree as ET
from proyecto.factura_SII import *
from proyecto.factura_normal import *
from proyecto.move_file import *



def mi_funcion():
    ruta_destino = 'data/'
    factura = str('data/data.xml')

    tree = ET.parse(factura)
    root = tree.getroot()

    root2 = str(root)
    texto = '{http://www.sii.cl/SiiDte}DTE'

    print(root2)



    if texto in root2:
        print("SII")
        sii_insert()
        return()
    else:
        print("Normal")
        insert_normal()

mi_funcion()