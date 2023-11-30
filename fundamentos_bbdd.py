import streamlit as st
import pandas as pd
from sklearn import datasets
import numpy as np
import duckdb
from sklearn.datasets import fetch_california_housing

def main():

    # Cargar el conjunto de datos de viviendas de California
    housing = fetch_california_housing()
    # Inicializar una conexión DuckDB
    con = duckdb.connect(database=':memory:')
    # Crear un DataFrame de pandas con los datos
    # delitos = pd.read_csv('files/Delitos.csv')
    archivos_csv = [
        'files/Actividades_Economicas.csv',
        'files/Centros_comerciales.csv',
        'files/Delitos.csv',
        'files/Fiscalia.csv',
        'files/Municipio.csv',
        'files/Ocurrencia_Delictiva.csv',
        'files/Comercios.csv',
    ]
    
    for archivo in archivos_csv:
        # Extraer el nombre de la tabla del nombre del archivo (sin la extensión .csv)
        nombre_tabla = archivo.split('/')[-1].split('.')[0]
    
        # Leer el archivo CSV y registrarlo en la base de datos
        df = pd.read_csv(archivo)
        con.register(nombre_tabla, df)
    
    # Crear un DataFrame de pandas con los datos
    data = pd.DataFrame(data=housing.data, columns=housing.feature_names)
    # diccionario_datos = pd.read_excel('BBDD_files/Diccionario de datos.xlsx')
    # Agregar la columna objetivo (target) al DataFrame

    url_diccionario_datos = 'https://github.com/jcval94/UP_Fundamentos_BBDD/raw/main/BBDD_files/Diccionario%20de%20datos.xlsx'
    # Cargar el DataFrame en DuckDB
    con.register('data', data)

    # Cargar el HTML desde el archivo
    with open('BBDD_files/Presentacion.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Título de la aplicación
    st.title("Proyeto final - Fundamentos de BBDD")

    # # Menú del lado izquierdo
    # st.sidebar.title("Menú")

    # # Opción para mostrar la imagen
    # if st.sidebar.checkbox("Mostrar Imagen"):
    #     st.image("images/mi_imagen.png")

    # Nueva pestaña para la imagen
    st.sidebar.title("Pestañas")
    selected_tab = st.sidebar.radio("Selecciona una pestaña:", ["Objetivos", "Exploración de Datos", "BBDD"])

    if selected_tab == "Exploración de Datos":
        # Muestra del conjunto de datos
        st.subheader("Muestra del conjunto de datos de comercios en la CDMX")
        st.write(df.head())

        # Campo de entrada de texto para la consulta SQL
        consulta_sql = st.text_area("Introduce tu consulta SQL:", value='SELECT * FROM data WHERE MedHouseVal > 1')

        # Botón para ejecutar la consulta SQL
        if st.button("Ejecutar Consulta SQL"):
            if consulta_sql:
                try:
                    # Ejecutar una consulta SQL en el DataFrame
                    result = con.execute(consulta_sql)
                    # Obtener el resultado como un DataFrame de Pandas
                    result_df = result.fetchdf()
                    st.write("Resultado de la consulta:")
                    st.write(result_df)
                except Exception as e:
                    st.write("Ocurrió un error al ejecutar la consulta:", e)

                # Estadísticas descriptivas
                st.subheader("Estadísticas descriptivas")
                st.write(result_df.describe())

        # # Filtrar y mostrar datos específicos
        # st.subheader("Filtrar datos")
        # filtro = st.slider("Filtrar por precio (target):", float(data[target].min()), float(data[target].max()))
        # filtered_data = data[data[target] < filtro]
        # st.write(filtered_data)

    elif selected_tab == "BBDD":
        # Botón de descarga directa del diccionario de datos en el cuerpo principal
        st.markdown(
            f'<a href="{url_diccionario_datos}" download="Diccionario_de_datos.xlsx">📥 Descargar Diccionario de Datos</a>',
            unsafe_allow_html=True
        )

        # Pestaña para mostrar la imagen
        st.sidebar.title("")
        st.markdown(
            f'Diagrama ER & Esquema'
        )
        
        st.image("images/diagrama_er.png")

        st.image("images/bbdd_fundamentos.png")

        # Botón para descargar el diccionario de datos
        # st.sidebar.download_button(
        #     label="Descargar Diccionario de Datos",
        #     data=diccionario_datos.to_excel(),
        #     file_name="diccionario_datos.xlsx",
        #     key="descargar_diccionario_datos"
        # )

    elif selected_tab == "Objetivos":
        # Pestaña exclusiva para mostrar el contenido HTML
        st.markdown(html_content, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
