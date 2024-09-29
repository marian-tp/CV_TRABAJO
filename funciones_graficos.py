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
from matplotlib.lines import Line2D


from copy import copy

# sns.set()
import pandas as pd
import pymysql
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder
from collections import defaultdict






#######################################################################################################################
###################################              GRÁFICAS BAR CHART INFORME FIN MÓDULO        #########################
#######################################################################################################################



# Se crea un gráfico de barras con 'cercanía, confiabilidad, credibilidad, orientación a si mismo' en el eje x'

# Ejemplo de aplicación en el .pptx, diapositiva 66
    # Reto 'El perfil de confianza' del episodio 'Episodio 1.Confianza' del módulo 2
    # En la plataforma, el módulo 2 aparece como '1.Confianza'. Cuando quieres volver hacia atrás, si que aparece como 'Episodio 1.Confianza'


def get_selection_bar(df_empresa):
    df_selection = df_empresa[df_empresa['TIPO_PREGUNTA'] == 'selection']

    for ejercicio in df_selection["EJERCICIO"].unique():
        values = []
        df_ejercicio = df_selection[df_selection["EJERCICIO"] == ejercicio]

        for tema in sorted(df_ejercicio["TEMA"].unique()):
            df_tema = df_ejercicio[df_ejercicio["TEMA"] == tema]
            df_tema = df_tema["RESPUESTA"].astype('int')
            media_tema = round((df_tema.sum() / len(df_tema)), 1)
            values.append(media_tema)

        columns = sorted(df_ejercicio["TEMA"].unique())

        plt.figure(figsize=(20, 10))
        my_palette = sns.color_palette(["#FFC12A"], n_colors=1)
        sns.set_theme(font_scale=2.1, style="whitegrid", palette=my_palette)

        ax = sns.barplot(x=columns, y=values, saturation=1, palette=my_palette)
        
        # Se adapta el eje y
        max_value = max(values)
        upper_limit = np.ceil(max_value / 0.5) * 0.5 + 0.5  
        ax.set_ylim(0, upper_limit)

        ax.yaxis.set_major_locator(plt.MultipleLocator(0.5))
        ax.yaxis.grid(True, color='grey', linestyle='--', linewidth=0.5, alpha=0.7)

        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f', label_type='center', color="white")

        plt.tight_layout()
        plt.savefig(ejercicio + '.png', bbox_inches='tight')
        plt.close()




#######################################################################################################################
###################################              GRÁFICAS PIE       #########################
#######################################################################################################################


                        #FUNCIÓN PARA EXTRAER LAS GRÁFICAS STACKED BAR CHART SEGREGADAS EN EJERCICIOS "BOOLEAN"
#######################################################################################################################



def plot_pie(porcentaje_proteccion, porcentaje_aprendizaje, ejercicio):
    valores = [porcentaje_proteccion, porcentaje_aprendizaje]
    etiquetas = ['Modo Protección', 'Modo Aprendizaje']
    colores = ["#31808E", "#4BC29F"] 

    fig, ax = plt.subplots(figsize=(10, 10))  # Ajustamos el tamaño de la figura
    wedges, texts, autotexts = ax.pie(valores, labels=etiquetas, autopct="%0.1f%%", startangle=90, colors=colores, textprops={'fontsize': 32, 'color': 'white', 'fontweight': 'bold'})
    ax.axis('equal')

    # Ajustar los márgenes
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    
    plt.savefig(ejercicio + '.png', bbox_inches='tight', format='png')
    plt.close()




def grafica_pie(df_empresa, ejercicio):

    df_slider_ejercicio = df_empresa[df_empresa["EJERCICIO"] == ejercicio]

    proteccion = []
    aprendizaje = []

    
    for pregunta in df_slider_ejercicio['PREGUNTA'].unique():
        media_respuesta = df_slider_ejercicio[df_slider_ejercicio['PREGUNTA'] == pregunta]['RESPUESTA'].mean()
        if "protec" in pregunta.lower():
            proteccion.append(media_respuesta)
        elif "aprend" in pregunta.lower():
            aprendizaje.append(media_respuesta)

    porcentaje_proteccion = sum(proteccion) / len(proteccion) if proteccion else 0
    porcentaje_aprendizaje = sum(aprendizaje) / len(aprendizaje) if aprendizaje else 0

    plot_pie (porcentaje_proteccion, porcentaje_aprendizaje, ejercicio)





def get_slider_pie(df_empresa):

    # Filtramos por el campo slider
    df_tipo_pregunta = df_empresa[df_empresa['TIPO_PREGUNTA'] == 'slider']
    df_tipo_pregunta["RESPUESTA"] = df_tipo_pregunta["RESPUESTA"].astype('int')


    # Iteramos por los ejercicios existentes
    for ejercicio in df_tipo_pregunta["EJERCICIO"].unique():
        df_pie = df_tipo_pregunta[df_tipo_pregunta['EJERCICIO'] == ejercicio]

        if ejercicio != 'Mi función como líder y niveles de liderazgo':  
            grafica_pie(df_pie, ejercicio)
            print("GRÁFICA get_slider_pie")





def get_boolean_pie(df_empresa):    

    # Filtramos por el campo booleano
    df_mx_boolean = df_empresa[df_empresa["TIPO_PREGUNTA"] == 'boolean']
    df_mx_boolean["RESPUESTA"] = df_mx_boolean["RESPUESTA"].astype('int')
    

    # Iteramos por los ejercicios existentes
    for ejercicio in df_mx_boolean["EJERCICIO"].unique():
        df_ejercicio_bool = df_mx_boolean[df_mx_boolean['EJERCICIO'] == ejercicio]

        valor_0 = (df_ejercicio_bool['RESPUESTA'] == 0).sum()
        valor_1 = (df_ejercicio_bool['RESPUESTA'] == 1).sum()

        total = valor_0 + valor_1
        porcentaje_proteccion = (valor_0 / total) if total > 0 else 0
        porcentaje_aprendizaje = (valor_1 / total) if total > 0 else 0


        plot_pie (porcentaje_proteccion, porcentaje_aprendizaje, ejercicio)
    
    print("GRÁFICA get_boolean_pie")








#######################################################################################################################
###################################              SLIDER_PIE_LIDERES                           #########################
#######################################################################################################################

def slider_pie_lideres (df_modulo):
    # Suponemos que df_modulo es tu DataFrame
    df_modulo['RESPUESTA'] = df_modulo['RESPUESTA'].astype(int)
    df_lider = df_modulo['EJERCICIO'].unique()
    funciones = ["Experto", "Triunfador", "Facilitador", "Cocreador", "Integrador"]
    colores = ['#00495E', '#FF9E01', '#52D0B7', '#00B050', '#B50042']
    color_map = dict(zip(funciones, colores))

    medias = {}

    if 'Mi función como líder y niveles de liderazgo' in df_lider:
        df_slider = df_modulo[df_modulo['EJERCICIO'] == 'Mi función como líder y niveles de liderazgo']

        # Crear subplots dinámicamente según la cantidad de temas únicos
        temas_unicos = df_slider['TEMA'].unique()
        fig, axes = plt.subplots(nrows=1, ncols=len(temas_unicos), figsize=(5 * len(temas_unicos), 5))

        for i, tema in enumerate(temas_unicos):
            df_tema = df_slider[df_slider['TEMA'] == tema]
            
            for funcion in funciones:
                df_funcion = df_tema[df_tema['PREGUNTA'] == funcion]
                media = df_funcion['RESPUESTA'].mean()
                if pd.notna(media):  # Solo agregar si la media no es NaN
                    medias[(tema, funcion)] = media

            # Preparar datos para el gráfico de pastel
            labels = [func for func in funciones if (tema, func) in medias]
            sizes = [medias[(tema, func)] for func in funciones if (tema, func) in medias]
            colors = [color_map[func] for func in labels]

            # Dibujar el pie chart
            ax = axes[i] if len(temas_unicos) > 1 else axes  # Asegurar compatibilidad si hay un solo tema
            wedges, _, autotexts = ax.pie(sizes, labels=labels, startangle=140, colors=colors, autopct=lambda p: '{:.1f}'.format(p * sum(sizes) / 100), textprops={'color': 'white', 'fontsize': 10, 'fontweight': 'bold'})
            #ax.set_title(f'{tema}', fontsize=12)  # Título del gráfico pie

        plt.tight_layout()
        plt.savefig('pie_lideres.png', bbox_inches='tight')

        # Crear leyenda como un subplot adicional
        fig_legend, ax_legend = plt.subplots(figsize=(7, 1))
        ax_legend.axis('off')
        legend_elements = [Line2D([0], [0], marker='o', color='w', label=func, markerfacecolor=color, markersize=12) for func, color in zip(funciones, colores)]
        ax_legend.legend(handles=legend_elements, loc="center", ncol=len(funciones), fontsize=10)
        fig_legend.subplots_adjust(top=0.8, left=0.09)
        fig_legend.savefig("leyenda.png")

        plt.close(fig)
        plt.close(fig_legend)