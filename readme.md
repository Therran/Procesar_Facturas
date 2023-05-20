# Procesar facturas de Compañias Electricas  en .xml con python, pandas y mysql

Este markdown muestra cómo usar python para leer facturas en formato xml, transformarlas a dataframe con pandas y cargarlas a una base de datos mysql.

![code.png](img%2Fcode.png)

### Este codigo te permite saber que formato de estructura tiene el Documento XML y aplicar el procesos e trasformacion y carga a base de datos segun sea el Emisor.
### Nos permite en caso de Error en la Lectura, Transformacion o Carga Mover esta Factura a una carpeta de error para posteriornete identificar el error en formato. De esta manera no se produsca un "Break" del proceso en cargas masivas de documentacion.
### * Se recomienda tener creada la tabla en la base de datos, si la tabla no exista en nuestra BBDD el script la creara automaticamente


### Detalles:

Debido a composision de los formatos de la factura en CL se deben considerar lo siguiente:


    * Facturas correspoden a formato XML correpondiente a Servicios Electricos (CL)
        - En Chile existen 2 tipos de emision de facturas:
            1.- Facturas emitidas directamente por la compañia
            2.- Factura emitidas a travez de Servicio de Impuestos Internos desde ahora "SII"

    * Segun el emisor el tratamiento de los datos cambia.


### requirements
````requirements.txt
Pandas == 2.0.1
SQLAlchemy == 2.0.15
mysql-connector-python == 8.0.33
mysql-connector == 2.2.9
xml == integado
os == integado
````
### 




### Factura Emisor "Compañia".

Este tipo de Documento XML es sencillo de procesar debido a que su estructura XML de arbol de datos: `Padre` - `Hijo` sigue el formato estandar como el siguiente ejemplo:
````html
Schema for XML Signatures
    http://www.w3.org/2000/09/xmldsig#
````
En estos casos se debe ingresar con libreria `Pandas` y recorrer la estructura de datos hasta llegar al `Hijo` un pequeño ejemplo de codigo:
```` python
import pandas as pd
Factura = "ubicacion/tu/archivo.xml"

#Creamos Dataframe
df = pd.read_xml(Factura, xpath="//Detalle",encoding="ISO-8859-1") 
print(df)
````
Con este simple codigo leemos el archvio de la variable "Factura" y navegamos a travez de la estrutura XML hasta el hijo con una referencia a xpath `"//Detalle"` obteniendo un dataframe con los datos ubicados dentro la estructura.

### Factura Emisor "SII".

Este tipo de Documento XML sigue estructura XMLNS arbol de datos: `Padre` - `Hijo` conservando el formato estandar sin embargo la estructura de `Hijos` se encuentran dentro del mismo nivel.

En estos casos se debe ingresar con libreria `xml` y encontrar a `Hijo` un pequeño ejemplo de codigo:
```` python
import xml.etree.ElementTree as ET
import pandas as pd
Factura = "ubicacion/tu/archivo.xml"

#Abrimos y parcemos el archivo.
tree = ET.parse(factura)
#Ubicamos la "Raiz" o "Root" del la estructura XMLNS
root = tree.getroot()
#creamos un DataFrame con Pandas pasando los argumentos "ET.tostring" dentro de este argumento buscamos dentro de variable "Root" el "Hijo" en este ejemplo "Documentos".
df = pd.read_xml(ET.tostring(root.find('{http://www.sii.cl/SiiDte}Documento/')), encoding="ISO-8859-1")
print(df)
````
### Proceso de carga a BBDD MySQL
ya obteniendo los datos necesario de la factura, procedemos a realizar la carga de estos DataFrame a la base de datos
#### Primero creamos la conexon al servidor de Bases de Datos:
```` python
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

#Conectamos a base de datos
mydbFacturas = create_engine(f'mysql+mysqlconnector://{"tu_usuario"}:{"Tu_contraseña"}@{"tu_host"}:{tu_puerto}/{"tu_BBDD"}')
#Insertamos tabla a base de datos
df.to_sql('tu_tabla', con=mydbFacturas, if_exists='append', index=False)
#Finalizamos conexion
mydbFacturas.dispose()
```` 