import mysql.connector
import pandas as pd
import os
import numpy as np
import warnings
import re
import collections

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np

from PIL import Image
from pptx import Presentation
from pptx.parts.image import Image


from copy import copy

# sns.set()
import pandas as pd
import pymysql
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder









def invertir(x):
  if x == 1:
    return str(int(x * 4))
  elif x == 2:
    return str(int(x * 1.5))
  elif x == 3:
    return str(int(x / 1.5))
  else:
    return str(int(x / 4))
  



#######################################################################################################################
###################################              GET_TOP_PRIORIZACION                           #######################
#######################################################################################################################

def get_top_priorizacion(df_modulo, numero_modulo):
    df_mx_prio = df_modulo[df_modulo["TIPO_PREGUNTA"] == 'compare']
    for pregunta in df_mx_prio["EJERCICIO"].unique():

        # Filtramos por la pregunta y nos quedamos solo con las respuestas
        pregunta_df = df_mx_prio[df_mx_prio["EJERCICIO"] == pregunta]['RESPUESTA']

        mapeo_respuesta_valores = {}
        for pares_respuesta_valores in list(df_mx_prio[df_mx_prio["EJERCICIO"] == pregunta].VALORES.unique()):
            pares_respuesta_valores = pares_respuesta_valores.split(",")
            for respuesta_valor in pares_respuesta_valores:
                label, label_id = respuesta_valor.split(": ")
                label = label.strip()
                if label_id not in mapeo_respuesta_valores:
                    mapeo_respuesta_valores[label_id] = label

        df_selection_aux = (df_mx_prio[df_mx_prio["EJERCICIO"] == pregunta].RESPUESTA.value_counts(normalize=True) * 100).round(1)
        df_selection_aux.index.name = "Label"
        df_selection_aux = df_selection_aux.reset_index().rename(columns=({"RESPUESTA": "Value"}))
        df_selection_aux["Label"] = df_selection_aux["Label"].map(mapeo_respuesta_valores)
        df_selection_aux["PREGUNTA"] = pregunta

        df_selection_aux_output = df_selection_aux.copy() 
        df_selection_aux_output.sort_values(by='proportion', ascending=False).reset_index(drop=True).to_csv(f'top_priorizacion_{numero_modulo}.csv', mode='a', sep=';', index=False, header=False)







#######################################################################################################################
###################################              GET_TOP_PONDERADO_PRIORIZACION                 #######################
#######################################################################################################################

def get_top_ponderado_priorizacion (df_modulo, numero_modulo):
    df_mx_prio = df_modulo[df_modulo["TIPO_PREGUNTA"] == 'compare']
    for pregunta in df_mx_prio["EJERCICIO"].unique():

        mapeo_respuesta_valores = {}
        for pares_respuesta_valores in list(df_mx_prio[df_mx_prio["EJERCICIO"] == pregunta].VALORES.unique()):
            pares_respuesta_valores = pares_respuesta_valores.split(",")
            for respuesta_valor in pares_respuesta_valores:
                label, label_id = respuesta_valor.split(": ")
                label = label.strip()
                if label_id not in mapeo_respuesta_valores:
                    mapeo_respuesta_valores[label_id] = label

        df_selection_aux = (df_mx_prio[df_mx_prio["EJERCICIO"] == pregunta].RESPUESTA.value_counts(normalize=True) * 100).round(1)
        df_selection_aux.index.name = "Label"
        df_selection_aux = df_selection_aux.reset_index().rename(columns=({"RESPUESTA": "Value"}))
        df_selection_aux["Label"] = df_selection_aux["Label"].map(mapeo_respuesta_valores)
        df_selection_aux["PREGUNTA"] = pregunta
            
        df_selection_aux_output = df_selection_aux.copy() 
        # Guardamos como ascending=True para que sea retro-compatible con el código original para Ejercicios de Priorización
        # Para Ejercicios de Priorización se calculaba un puntaje de orden promedio, donde menor era más priorizado
        # Luego, se cargaba el top_ponderado.csv y se lo daba vuelta al orden
        # Para replicar este comportamiento, guardamos nuestros valores con ascending=True, porque aquí mayor es más priorizado
        df_selection_aux_output.sort_values(by='proportion', ascending=True).reset_index(drop=True).to_csv(f'top_ponderado_{numero_modulo}.csv', mode='a',sep=';', index=False, header=False)




#######################################################################################################################
###################################              GET_TOP_BOOLEAN                                #######################
#######################################################################################################################


def get_top_boolean (df_modulo, numero_modulo):
    df_mx_boolean = df_modulo[df_modulo["TIPO_PREGUNTA"] == 'boolean']

    for i in df_mx_boolean["EJERCICIO"].unique():
        
        df_bool = df_mx_boolean[df_mx_boolean["EJERCICIO"] == i]

        df_bool_output = df_bool.copy()

        df_bool_output = df_bool_output[df_bool_output["RESPUESTA"] == '1'].groupby(['PREGUNTA']).count().sort_values(['ID_MÓDULO'], ascending=False)["ID_MÓDULO"].reset_index()
        df_bool_output['EJERCICIO'] = i  

        df_bool_output.to_csv(f'top_boolean_{numero_modulo}.csv', mode='a', sep=';', index=False, header=False)







"""


#######################################################################################################################
###################################              GET_TOP_COMPARE                              #########################
#######################################################################################################################


df_modulo_compare = df_modulo1[df_modulo1["TIPO_PREGUNTA"] == 'compare']

resultados_finales = pd.DataFrame()

mapeo_respuesta_valores = {}
for ejercicio in df_mx_prio["EJERCICIO"].unique():
    valores_unicos = df_mx_prio[df_mx_prio["EJERCICIO"] == ejercicio]["VALORES"].unique()
    for pares_respuesta_valores in valores_unicos:
        pares_respuesta_valores = pares_respuesta_valores.split(",")
        for respuesta_valor in pares_respuesta_valores:
            label, label_id = respuesta_valor.split(":")
            label = label.strip()
            label_id = label_id.strip()
            mapeo_respuesta_valores[label_id] = label

    df_selection_aux = df_mx_prio[df_mx_prio["EJERCICIO"] == ejercicio]['RESPUESTA'].value_counts(normalize=True) * 100
    df_selection_aux = df_selection_aux.reset_index()
    df_selection_aux.columns = ['Label', 'Value']
    df_selection_aux['Value'] = df_selection_aux['Value'].round(1)

    df_selection_aux["Label"] = df_selection_aux["Label"].map(mapeo_respuesta_valores)
    df_selection_aux['Ejercicio'] = ejercicio

    resultados_finales = pd.concat([resultados_finales, df_selection_aux], ignore_index=True)






        
##############################################################################################################
# TABLA EJERCICIOS PRIORIZACIÓN. ELECCIONES PRIMERA POSICIÓN
##############################################################################################################


def get_top_priorizacion(df_empresa):
    resultados = []

    for ejercicio in df_empresa["EJERCICIO"].unique():
        
        primeras_opciones = df_empresa[(df_empresa['TIPO_PREGUNTA'] == 'priorization') & (df_empresa['EJERCICIO'] == ejercicio)]['RESPUESTA'].str.split(',').str.get(0)
        counts_primera_posicion = primeras_opciones.value_counts()

        total_respuestas = counts_primera_posicion.sum()
        porcentaje_primera_posicion = (counts_primera_posicion / total_respuestas) * 100

        df_porcentaje = porcentaje_primera_posicion.reset_index()
        df_porcentaje.columns = ['PREGUNTA', 'PORCENTAJE']
        df_porcentaje['EJERCICIO'] = ejercicio

        resultados.append(df_porcentaje)

    df_final = pd.concat(resultados, ignore_index=True)

    return df_final





def get_top_priorizacion_segregado (df_empresa, agrupacion):
    resultados = []

    df_empresa_priorizacion = df_empresa[(df_empresa['TIPO_PREGUNTA'] == 'priorization')]

    valores_agrupacion = df_empresa_priorizacion[agrupacion].unique()
    
    for valor in valores_agrupacion:
        df_filtrado = df_empresa_priorizacion[df_empresa_priorizacion[agrupacion] == valor]

    
        for ejercicio in df_filtrado["EJERCICIO"].unique():
        
            primeras_opciones = df_filtrado['RESPUESTA'].str.split(',').str.get(0)
            counts_primera_posicion = primeras_opciones.value_counts()

            total_respuestas = counts_primera_posicion.sum()
            porcentaje_primera_posicion = (counts_primera_posicion / total_respuestas) * 100

            df_porcentaje = porcentaje_primera_posicion.reset_index()
            df_porcentaje.columns = ['PREGUNTA', 'PORCENTAJE']
            df_porcentaje['EJERCICIO'] = ejercicio

            resultados.append(df_porcentaje)

    
    df_final = pd.concat(resultados, ignore_index=True)
    return df_final




    



def get_slider_segregado_data(df_empresa, agrupacion):
    df_tipo_pregunta = df_empresa[df_empresa['TIPO_PREGUNTA'] == 'slider']
    df_tipo_pregunta["RESPUESTA"] = df_tipo_pregunta["RESPUESTA"].astype('int')
    
    resultados = []
    
    valores_agrupacion = df_tipo_pregunta[agrupacion].unique()
    
    for valor in valores_agrupacion:
        df_filtrado = df_tipo_pregunta[df_tipo_pregunta[agrupacion] == valor]
        
        suma_proteccion = 0
        contador_proteccion = 0
        suma_aprendizaje = 0
        contador_aprendizaje = 0
        
        for pregunta in df_filtrado['PREGUNTA'].unique():
            media_respuesta = df_filtrado[df_filtrado['PREGUNTA'] == pregunta]['RESPUESTA'].mean()
            if "protec" in pregunta.lower():
                suma_proteccion += media_respuesta
                contador_proteccion += 1
            elif "aprend" in pregunta.lower():
                suma_aprendizaje += media_respuesta
                contador_aprendizaje += 1
        
        porcentaje_proteccion = (suma_proteccion / contador_proteccion) if contador_proteccion > 0 else 0
        porcentaje_aprendizaje = (suma_aprendizaje / contador_aprendizaje) if contador_aprendizaje > 0 else 0
        
        resultados.append({
            agrupacion: valor,
            'Porcentaje Proteccion': porcentaje_proteccion,
            'Porcentaje Aprendizaje': porcentaje_aprendizaje
        })
    
    df_final = pd.DataFrame(resultados)
    return df_final


"""