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
     tree = ET.parse(factura)
     root = tree.getroot()
     df = pd.read_xml(ET.tostring(root.find('{http://www.sii.cl/SiiDte}Documento/')), encoding="ISO-8859-1")
     df.fillna(method='ffill', axis=0, inplace=True)
     n = df.shape[0]
     x = int(n - 1)
     df_idem = df.iloc[[x]]
     print('Detalle Encabezado')
     print(df_idem)

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
