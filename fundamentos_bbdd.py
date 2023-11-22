import streamlit as st
import pandas as pd
from sklearn import datasets
import numpy as np
import duckdb
from sklearn.datasets import fetch_california_housing

def main():

    # Cargar el conjunto de datos de viviendas de California
    housing = fetch_california_housing()

    # Crear un DataFrame de pandas con los datos
    data = pd.DataFrame(data=housing.data, columns=housing.feature_names)
    dicc_dat = pd.read_excel('BBDD_files/Diccionario de datos.xlsx')
    # Agregar la columna objetivo (target) al DataFrame
    data['MedHouseVal'] = housing.target

    target = 'MedHouseVal'

    # Inicializar una conexión DuckDB
    con = duckdb.connect(database=':memory:')
    # Cargar el DataFrame en DuckDB
    con.register('data', data)

    # Cargar el HTML desde el archivo
    with open('BBDD_files/Presentacion.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Título de la aplicación
    st.title("Exploración del Conjunto de Datos de Precios de Casas de California")

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
        st.subheader("Muestra del conjunto de datos")
        st.write(data.head())

        # Seleccionar una columna para visualizar
        columna_seleccionada = st.selectbox("Selecciona una columna:", data.columns)

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
        st.write(data.describe())

        # Filtrar y mostrar datos específicos
        st.subheader("Filtrar datos")
        filtro = st.slider("Filtrar por precio (target):", float(data[target].min()), float(data[target].max()))
        filtered_data = data[data[target] < filtro]
        st.write(filtered_data)

    elif selected_tab == "BBDD":
        # Añadir el botón para descargar el diccionario de datos
        st.sidebar.markdown("""
        [Descargar Diccionario de Datos](data:application/octet-stream;base64,{} "Descargar Diccionario de Datos")
        """.format(df_to_excel_download_link(dicc_dat)), unsafe_allow_html=True)

        # Pestaña para mostrar la imagen
        st.image("images/bbdd_fundamentos.png")

    elif selected_tab == "Objetivos":
        # Pestaña exclusiva para mostrar el contenido HTML
        st.markdown(html_content, unsafe_allow_html=True)

# Función para convertir un DataFrame de Pandas a un enlace de descarga en formato Excel
def df_to_excel_download_link(df, filename="diccionario_datos.xlsx", sheet_name="Sheet1"):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Descargar archivo</a>'


if __name__ == '__main__':
    main()
