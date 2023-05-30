import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

def normal_insert():
    ruta_destino = 'data/'
    factura = str('data/data.xml')

    ##Connect to Mysql
    mydbFacturas = create_engine(
        f'mysql+mysqlconnector://{"ru_usuario"}:{"tu_contraseña"}@{"tu_host"}:{tu_puerto}/{"tu_BBDD"}',
        poolclass=NullPool)

    ## Open, Read amd Modify XML
    df_idDoc = pd.read_xml(factura, xpath='//IdDoc', encoding='ISO-8859-1')
    df_Emisor = pd.read_xml(factura, xpath='//Emisor', encoding='ISO-8859-1')
    df_Receptor = pd.read_xml(factura, xpath='//Receptor', encoding='ISO-8859-1')
    df_Totales = pd.read_xml(factura, xpath='//Totales', encoding='ISO-8859-1')
    df_Encabezado = pd.concat([df_idDoc, df_Emisor, df_Receptor, df_Totales], axis=1)
    df_Encabezado
    print('Detalle Encabezado')
    print(df_Encabezado)

    ## Insert to Header Table
    df_Encabezado.to_sql('tu_tabla', con=mydbFacturas, if_exists='append', index=False)
    mydbFacturas.dispose()

    ## Open, Read amd Modify XML "Cargos"
    df_detalleCargo = pd.read_xml('facturas/data.xml', xpath='//Detalle', encoding='ISO-8859-1')
    folio = df_idDoc['Folio']
    df_detalleCargo['Folio'] = folio[0]
    print('Detalle Cargos')
    print(df_detalleCargo)

    ## Insert to Cargos Table
    df_detalleCargo.to_sql('cargos', con=mydbFacturas, if_exists='append', index=False)
    mydbFacturas.dispose()

    ##Erase Temporal File
    archivos = os.listdir(ruta_destino)
    for archivo in archivos:
        ruta_archivo = os.path.join(ruta_destino, archivo)
        os.remove(ruta_archivo)
