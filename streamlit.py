import streamlit as st  # Importa el módulo streamlit para crear aplicaciones web interactivas
import pandas as pd  # Importa el módulo pandas para manipulación y análisis de datos

# Define el nombre del archivo de entrada que contiene los datos
input_file_name = 'TCE-PB-Contratos_2024.csv'

# Lee el archivo CSV y lo carga en un DataFrame de pandas
df = pd.read_csv(input_file_name, sep=';', encoding='latin-1')

# Establece el título de la aplicación web
st.title("TCE PB - Licitações (2024)")

def convert_float(value):
    try:
        new_value = str(value)
        new_value = new_value.replace(',', '.')
        new_value = float(new_value)
        return new_value
    except:
        return value

column_analysis = 'valor_contratado'
df[column_analysis] = df[column_analysis].apply(lambda x: convert_float(x))

top_k = 10

global_mean = df[column_analysis].mean()

map_text = {
    'cpf_cnpj_licitante': f'Top {top_k} valores por CPF/CNPJ Licitante em relação a média',
    'numero_licitacao': f'Top {top_k} valores por Número de Licitação em relação a média',
    'ente': f'Top {top_k} valores por Ente em relação a média',
    'cod_modalidade_licitacao': f'Top {top_k} Código Modalidade de Licitação por Ente em relação a média'}

for column in ['cpf_cnpj_licitante', 'numero_licitacao',
                'ente', 'cod_modalidade_licitacao']:
    df_top = df.groupby(column)[column_analysis].mean()
    df_top = pd.DataFrame(df_top.nlargest(top_k).reset_index())
    df_top[column_analysis] = round(df_top[column_analysis], 2)
    df_top['Proporção'] = round(df_top[column_analysis]/global_mean, 1)
    st.text(map_text[column])
    st.dataframe(df_top)

import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

pr = df.profile_report()
st_profile_report(pr)
pr.to_file("contratos_profiling.html")