# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 18:36:26 2021

@author: fromero
"""

# Recomendaciones
# 1. Instalar python 3.6.1 https://www.python.org/downloads/release/python-361/
# 2. Instalar la librería leila -> pip install leila

# 3. Importar las librerías requeridas
import pandas as pd
from leila.reporte import generar_reporte

# 4. Importar librería para conectar a sql server
from conectar_a_sql_server import api_sql_server 

# 5. Definir sentencias SQL de consulta
query_5311A = "select * from T_T_CALIDAD_DATOS_5311A"
query_5433B = "select * from T_T_CALIDAD_DATOS_5433B"

# 6. Crear objetos sql y conectarlos al driver de sql server
cursor_5311A = api_sql_server()
cursor_5433B = api_sql_server()

# 7. Ejecutar consultas y convertirlas a DataFrame para Leila
df_5311A = pd.read_sql(query_5311A, cursor_5311A)
df_5433B = pd.read_sql(query_5433B, cursor_5433B)

# 8. Generar reportes
generar_reporte(df_5311A, titulo = "Reporte T_T_CALIDAD_DATOS_5311A", archivo = "reportes/T_T_CALIDAD_DATOS_5311A/T_T_CALIDAD_DATOS_5311A.html")
generar_reporte(df_5433B, titulo = "Reporte T_T_CALIDAD_DATOS_5433B", archivo = "reportes/T_T_CALIDAD_DATOS_5433B/T_T_CALIDAD_DATOS_5433B.html")


# el nombre del archivo debe llevar al final, el periodo al que corresponde...



# 3. cargar el archivo que contiene los datos
datos = pd.read_excel("datos/T_T_CALIDAD_DATOS_5433B.xls")
   
# 4. generar el reporte utilizando la librería leila
generar_reporte(datos, titulo = "Reporte T_T_CALIDAD_DATOS_5433B", archivo = "reportes/T_T_CALIDAD_DATOS_5433B/T_T_CALIDAD_DATOS_5433B.html")

