


import streamlit as st
import pandas as pd
from sklearn import datasets
import numpy as np
from sklearn.datasets import fetch_california_housing

def main():

    # Cargar el conjunto de datos de viviendas de California
    housing = fetch_california_housing()

    # Crear un DataFrame de pandas con los datos
    data = pd.DataFrame(data=housing.data, columns=housing.feature_names)

    # Agregar la columna objetivo (target) al DataFrame
    data['MedHouseVal'] = housing.target

    target = 'MedHouseVal'
    # Título de la aplicación
    st.title("Exploración del Conjunto de Datos de Precios de Casas de Boston")

    # Mostrar una muestra de los datos
    st.subheader("Muestra del conjunto de datos")
    st.write(data.head())

    # Seleccionar una columna para visualizar
    columna_seleccionada = st.selectbox("Selecciona una columna:", data.columns)

    # Campo de entrada de texto para la consulta SQL
    consulta_sql = st.text_area("Introduce tu consulta SQL:", value='SELECT * FROM data WHERE MedHouseVal > 1')

    # Botón para ejecutar la consulta
    if st.button("Ejecutar Consulta SQL"):
        if consulta_sql:
            try:
                result = data.query(consulta_sql)
                st.write("Resultado de la consulta:")
                st.write(result)
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


if __name__ == "__main__":
    main()

