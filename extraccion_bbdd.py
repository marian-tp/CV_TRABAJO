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

import pandas as pd
import pymysql
import logging
import sshtunnel
from sshtunnel import SSHTunnelForwarder





def extraccion_sql_1 (mydb, empresa = None):

    try:

        query = f"""


        SELECT
            ex.ID as "ID",
            co.ID as "ID_COMPAÑÍA",
            co.name as "COMPAÑÍA",
            gr_wo.group_id as "ID_GRUPO",
            gr.name as "GRUPO",
            ex.participant_id as "ID_PARTICIPANTE",
            ex.exercise_id as "ID_PREGUNTA",
            po.post_title as "PREGUNTA",
            po.ID as "ID_POST",
            ex.response as "RESPUESTA",
            pm1.meta_value AS "TIPO_PREGUNTA",
            pm2.meta_value AS "VALORES"
        
        FROM wp_bcg_exercise_response ex

        JOIN wp_bcg_group_workshops gr_wo
            ON ex.group_workshop_id=gr_wo.ID
        JOIN wp_bcg_group gr
            ON gr.ID = gr_wo.group_id
        JOIN wp_bcg_company co
            ON gr.company_id = co.ID
        JOIN wp_posts po
            ON po.ID = ex.exercise_id
        JOIN wp_postmeta pm1 
            ON pm1.post_id = po.ID AND pm1.meta_key = 'tipo_pregunta'
        LEFT JOIN wp_postmeta pm2 
            ON pm2.post_id = po.ID AND pm2.meta_key = 'value'
        

                """

        if empresa != None:
            query += f"""WHERE co.name = '{empresa}' ;"""
    
    
    except Exception as e:
        print(str(e))

    extraccion_df = pd.read_sql(query, mydb)

    return extraccion_df






def extract_temas(id_preg, mydb):
    query = f"""
        SELECT post_id AS "ID_TEMA" ,
        post_title as "TEMA"
        FROM wp_postmeta
        LEFT JOIN wp_posts
        ON wp_posts.ID = wp_postmeta.post_id
        WHERE meta_key = 'preguntas' and meta_value like '%\"{id_preg}\"%'
            """

    temas_df = pd.read_sql(query, mydb)

    return temas_df





def extract_ejer(id_tema, mydb):
    query = f"""
        SELECT post_id AS "ID_EJERCICIO" ,
        post_title as "EJERCICIO"
        FROM wp_postmeta
        LEFT JOIN wp_posts
        ON wp_posts.ID = wp_postmeta.post_id
        WHERE meta_key = 'temas' and meta_value like '%\"{id_tema}\"%'

            """

    ejercicios_df = pd.read_sql(query, mydb)

    return ejercicios_df




def extract_episodio (id_ej, mydb):
    query = f"""
        SELECT post_id AS "ID_EPISODIO",
        post_title AS "EPISODIO"
        FROM wp_postmeta
        LEFT JOIN wp_posts
        ON wp_posts.ID = wp_postmeta.post_id
        WHERE meta_key = 'ejercicios' and meta_value like '%\"{id_ej}\"%'

        """

    episodios_df = pd.read_sql(query, mydb)
    return episodios_df



        
def extract_modulo (idepis, mydb):
    query = f"""
        SELECT post_id AS "ID_MÓDULO",
        post_title AS "MÓDULO"
        FROM wp_postmeta
        LEFT JOIN wp_posts
        ON wp_posts.ID = wp_postmeta.post_id
        WHERE meta_key = 'episodios' and meta_value like '%\"{idepis}\"%'

        """
    
    modulos_df = pd.read_sql(query, mydb)
    return modulos_df





# Ej en meta_value: Conversaciones valientes (Parte 1). Este es uno de los retos del Episodio 3. Conversaciones valientes del módulo 3
def extract_grupo_ejercicio(mydb):
    query = f"""
        SELECT post_id, meta_value
        FROM wp_postmeta
        WHERE meta_key = 'grupo_ejercicio'
        """

    grupos_ejercicios_df = pd.read_sql(query, mydb)

    return grupos_ejercicios_df




# En el excel que pasa la empresa con los email de los empleados y otros criterios como el cargo, la empresa, la edad,... 
# se necesita hacer merge con los usuarios que están en la plataforma ya que puede que se hayan añadido o quitado alguno

def extract_users(mydb):
    query = f"""
        SELECT ID, user_nicename, user_email
        FROM wp_users 
        """

    users = pd.read_sql(query, mydb)

    return users




def extract_profesionales (mydb, nombre_empresa):
    # Query para obtener el número de profesionales que han realizado los ejercicios de Mindset Management

    query_profesionales = f"""
    
        SELECT COUNT(DISTINCT participant_id) AS total_participants_unique
        FROM (
            SELECT 
                gr.name as "group_name",
                gr.company_id as "company_id",
                co.name as "company_name",
                par.ID as "participant_id"

            FROM wp_bcg_group_participants par
            LEFT JOIN qafe878.wp_bcg_group gr ON gr.ID = par.group_id
            LEFT JOIN wp_bcg_company co ON co.ID = gr.company_id
            WHERE co.name = '{nombre_empresa}'
            )
            as sub;"""


    df_profesionales = pd.read_sql(query_profesionales, mydb)
    
    return df_profesionales












































# # # Ejecutar consulta SQL sobre la base de datos y recuperar conjunto de datos específico
# # def extraccion_sql(mydb, lista_empresas):

# #     try:
# #         query = f"""
# #         SELECT
# #         ex.ID as "ID",
# #         po1.ID as "ID_MÓDULO",
# #         po1.post_title as "MÓDULO",
# #         co.ID as "ID_COMPAÑÍA",
# #         co.name as "COMPAÑÍA",
# #         gr_wo.group_id as "ID_GRUPO",
# #         gr.name as "GRUPO",
# #         ex.participant_id as "ID_PARTICIPANTE",
# #         ex.exercise_id as "ID_PREGUNTA",
# #         po.post_title as "PREGUNTA",
# #         po.ID as "ID_POST",
# #         ex.response as "RESPUESTA"
# #     FROM qafe878.wp_bcg_exercise_response ex


# #     join qafe878.wp_bcg_group_workshops gr_wo
# #         on ex.group_workshop_id=gr_wo.ID
# #     join qafe878.wp_bcg_group gr
# #         on gr.ID = gr_wo.group_id
# #     join qafe878.wp_bcg_company co
# #         on gr.company_id = co.ID
# #     join qafe878.wp_posts po
# #         on po.ID = ex.exercise_id
# #     join qafe878.wp_posts po1
# #         on po1.ID = gr_wo.workshop_id

# #         """

# #         # Si el listado de empresas es distinto a None, el código filtra por el listado de empresas
# #         if lista_empresas != None:

# #             if type(lista_empresas) is not tuple:

# #                 query += f"""WHERE co.name = '{lista_empresas}' ;"""

# #             else:

# #                 query += f"""WHERE co.name IN {lista_empresas} ;"""

# #         # Si el listado de empresas es None, la consulta selecciona todas las compañías disponibles
# #         result_dataFrame = pd.read_sql(query, mydb)

# #     except Exception as e:
# #         print(str(e))

# #     return result_dataFrame





# def extraccion_sql(self, empresa = None):

#     try:

#         query = f"""
#             SELECT
#             ex.ID as "ID",
#             po1.ID as "ID_MÓDULO",
#             po1.post_title as "MÓDULO",
#             co.ID as "ID_COMPAÑÍA",
#             co.name as "COMPAÑÍA",
#             gr_wo.group_id as "ID_GRUPO",
#             gr.name as "GRUPO",
#             ex.participant_id as "ID_PARTICIPANTE",
#             ex.exercise_id as "ID_PREGUNTA",
#             po.post_title as "PREGUNTA",
#             po.ID as "ID_POST",
#             ex.response as "RESPUESTA"
#         FROM qafe878.wp_bcg_exercise_response ex


#         join qafe878.wp_bcg_group_workshops gr_wo
#             on ex.group_workshop_id=gr_wo.ID
#         join qafe878.wp_bcg_group gr
#             on gr.ID = gr_wo.group_id
#         join qafe878.wp_bcg_company co
#             on gr.company_id = co.ID
#         join qafe878.wp_posts po
#             on po.ID = ex.exercise_id
#         join qafe878.wp_posts po1
#             on po1.ID = gr_wo.workshop_id

#             """
    
#         if empresa != None:
#             query += f"""WHERE co.name = '{empresa}' ;"""
        
        
#     except Exception as e:
#         print(str(e))

#     extraccion_df = pd.read_sql(query, self.mydb)

#     return extraccion_df









# def extract_temas(idpreg, mydb):
#     query = f"""
#         SELECT post_id AS "ID_TEMA" ,
#         post_title as "TEMA"
#         FROM wp_postmeta
#         LEFT JOIN wp_posts
#         ON wp_posts.ID = wp_postmeta.post_id
#         WHERE meta_key = 'preguntas' and meta_value like '%\"{idpreg}\"%'
#             """

#     tema = pd.read_sql(query, mydb)

#     return tema





# def extract_ejer(idtema, mydb):
#     query = f"""
#         SELECT post_id AS "ID_EJERCICIO" ,
#         post_title as "EJERCICIO"
#         FROM wp_postmeta
#         LEFT JOIN wp_posts
#         ON wp_posts.ID = wp_postmeta.post_id
#         WHERE meta_key = 'temas' and meta_value like '%\"{idtema}\"%'

#             """

#     tema = pd.read_sql(query, mydb)

#     return tema





# # Se extraen el tipo de pregunta y los valores que pueda tener

# # tema      (Ej: TIPO PREGUNTA      ID_PREGUNTA
# #                   slider                  198)


# # tema1     (Ej: VALORES
# #               '0,20,40,60,80,100'

# def extract_tipo_preg(idpreg, mydb):
#     query = f"""
#         SELECT meta_value AS "TIPO_PREGUNTA",
#         post_id AS "ID_PREGUNTA"
#         from wp_postmeta
#         WHERE meta_key = 'tipo_pregunta' and post_id={idpreg}

#             """

#     tema = pd.read_sql(query, mydb)


#     query = f"""
#         SELECT meta_value as VALORES
#         FROM wp_postmeta
#         LEFT JOIN wp_posts
#         ON wp_posts.ID = wp_postmeta.post_id
#         WHERE post_id = {idpreg} and meta_key = 'value'
#             """

#     tema1 = pd.read_sql(query, mydb)
#     tema['VALORES'] = tema1['VALORES']
#     return tema





# def extract_users(mydb):
#     query = f"""
#         SELECT ID, user_nicename, user_email
#         FROM wp_users """

#     users = pd.read_sql(query, mydb)

#     return users





# # Ej en meta_value: Conversaciones valientes (Parte 1). Este es uno de los retos del Episodio 3. Conversaciones valientes del módulo 3
# def extract_grupo_ejercicio(mydb):
#     query = f"""
#         SELECT *
#         FROM wp_postmeta
#         WHERE meta_key = 'grupo_ejercicio'
#         """

#     grupos = pd.read_sql(query, mydb)

#     return grupos




