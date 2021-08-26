# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 23:05:33 2020

@author: fromero
"""

# módulo para establecer la conexión a SQL Server

# importar librerías
import pyodbc
import configparser as cp

# función para establecer la conexión a la red social twitter
def api_sql_server():
    # leer el archivo de configuración
    config = cp.RawConfigParser()
    config.read('setup.properties')
    # obtener las credenciales de acceso del archivo de configuración
    server    = config.get('database', 'server')
    database  = config.get('database', 'dbname')
    username  = config.get('database', 'username')
    password  = config.get('database', 'password')
    # retornar el punto de ocnexión a la red social
    # return pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
