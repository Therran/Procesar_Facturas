import xml.etree.ElementTree as ET
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


def insert_normal():
    ruta_destino = 'data/'
    factura = str('data/data.xml')

    ##Connect to Mysql
    mydbFacturas = create_engine(
        f'mysql+mysqlconnector://{"tu_usuario"}:{"tu_contraseña"}@{"tu_host"}:{tu_puerto}/{"tu_BBDD"}',
        poolclass=NullPool)

    ## Open, Read amd Modify XML
    tree = ET.parse(factura)
    root = tree.getroot()
    df = pd.read_xml(ET.tostring(root.find('Documento/')), encoding="ISO-8859-1")
    df.fillna(method='ffill', axis=0, inplace=True)
    n = df.shape[0]
    x = int(n - 1)
    df.fillna(method='ffill', axis=0, inplace=True)
    df_idem = df.iloc[[x]]
    print('Detalle Encabezado Normal')
    print(df_idem)

    ## Insert to Header Table
    df_idem.to_sql('tu_tabla', con=mydbFacturas, if_exists='append', index=False)
    mydbFacturas.dispose()

    ## Open, Read amd Modify XML "Cargos"
    folio = df['Folio'].astype(int)
    detalles = root.findall('.//Detalle')
    df_detalleCargo = pd.DataFrame()

    for detalle in detalles:
        data = {}
        for child in detalle:
            tag = ET.QName(child.tag).text
            data[tag] = child.text
        df_detalleCargo = pd.concat([df_detalleCargo, pd.DataFrame(data, index=[0])])
    df_detalleCargo['Folio'] = folio[0]
    print('Detalle Cargos Normal')
    print(df_detalleCargo)

    ## Insert to Cargos Table
    df_detalleCargo.to_sql('tu_tabla2', con=mydbFacturas, if_exists='append', index=False)
    mydbFacturas.dispose()

    ##Erase Temporal File
    archivos = os.listdir(ruta_destino)
    for archivo in archivos:
        ruta_archivo = os.path.join(ruta_destino, archivo)
        os.remove(ruta_archivo)

insert_normal()