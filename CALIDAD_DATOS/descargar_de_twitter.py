# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 10:33:27 2020

@author: fromero
"""

#módulo para descargar mensajes de la red social twitter

#importar librerías
from conectar_a_twitter import api_twitter #importar librería para conectar a twitter     
from conectar_a_sql_server import api_sql_server #importar librería para conectar a sql server
import re #para manejo de cadenas
from datetime import date, timedelta #para manejo de fechas (ayer y hoy)

#obtener fechas de ayer y hoy
ayer = date.today() + timedelta(days=-1)
hoy = date.today()

#definir scripts de sql
sql_entidad = "select cuenta_twitter from dbo.entidad"
sql_tweet = "insert into tmp_tweet (id_tweet, fecha, texto, texto_procesado, cantidad_favoritos, cantidad_retweets, lista_hashtags, lista_usuarios, autor_tweet, autor_cantidad_seguidores, autor_cantidad_seguidos,val_positiva, val_negativa, val_alegria, val_tristeza, val_confianza, val_aversion, val_miedo, val_ira, val_sorpresa, val_anticipacion, val_neutral) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"

#crear objeto twitter y conectarlo a la api de twitter
twitter = api_twitter()

#crear objetos sql y concetarlos al driver de sql server
sql1 = api_sql_server()
sql2 = api_sql_server()
sql3 = api_sql_server()

#crear cursores de conexión a sql server
cursor_entidad = sql1.cursor()
cursor_tweet   = sql2.cursor()
cursor_procs   = sql3.cursor()
#obtener de la tabla entidad, los criterios de consulta
with cursor_entidad.execute(sql_entidad):
    cuenta_entidad = cursor_entidad.fetchone()
    while cuenta_entidad:  #mientras hayan cuentas de twitter
        #obtener tweets para la cuenta de twitter activa
        #new_tweets = twitter.search(q=str(cuenta_entidad[0]), tweet_mode='extended', since=ayer, until=hoy, count=5000)
        new_tweets = twitter.search(q=str(cuenta_entidad[0]), tweet_mode='extended', since='2021-07-15', until='2021-07-16', count=5000)
        print (str(cuenta_entidad[0]) + ' --> ' + str(len(new_tweets)))
        for tweet in new_tweets:
            #para cada  tweet obtener la lista de hastags
            lista_hastags  = ''
            for hashtag in tweet.entities['hashtags']:
                lista_hastags = lista_hastags + '#' + hashtag['text'] + ','
            lista_hastags = lista_hastags[:-1]    
            #para cada  tweet obtener la lista de usuarios
            lista_usuarios = ''
            for user in tweet.entities['user_mentions']:
                lista_usuarios = lista_usuarios + '@' + user['screen_name'] + ','
            lista_usuarios = lista_usuarios[:-1]
            #limpiar texto
            texto_limpio = " ".join(re.findall(r'\b[a-z,á,é,í,ó,ú,ñ]{2,20}\b', tweet.full_text.lower()))
            #insertar cada tweet a la base de datos de sqk server    
            cursor_tweet.execute(sql_tweet,tweet.id_str,tweet.created_at,tweet.full_text, texto_limpio, tweet.favorite_count, tweet.retweet_count,lista_hastags, lista_usuarios,
                   tweet.user.screen_name, tweet.user.followers_count, tweet.user.friends_count,0,0,0,0,0,0,0,0,0,0,0)
        #avanzar a la siguiente cuenta de twitter
        cuenta_entidad = cursor_entidad.fetchone() 
#guardar datos en tweets
sql2.commit()

#ejecutar el procedimiento almacenado de clasificación general
sentencia = "EXEC [dbo].[clasifica_general];" 
try:
    cursor_procs.execute(sentencia)
    cursor_procs.commit()
except Exception as e:
    print('*'*100)
    print(e)
#cerrar conexiones
sql3.close()
sql2.close()
sql1.close()

