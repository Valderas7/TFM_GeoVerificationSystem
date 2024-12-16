# Librerías
import streamlit as st
import pandas as pd
import requests
import leafmap.foliumap as leafmap
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from utils.html_entities import convert_to_html_entities
from utils.geography_utils import (get_provinces_and_autonomous_cities,
                                   translate_province_list)

# Se guarda en una variable la URL de la API Gateway desplegada con AWS
api_gateway_url = 'https://mjb5qk45si.execute-api.us-east-1.amazonaws.com/prod'

# Barra lateral para mostrar las opciones disponibles
st.sidebar.title("Secciones")
action = st.sidebar.radio("Elige una opción:",
                          options=["Situación meteorológica actual",
                                   "Consultar provincia específica",
                                   "Estadísticas"])

# Si se elige la opción 'Ver mapa general'
if action == "Situación meteorológica actual":

    # Título de la Web App con cabecera H2
    st.markdown("<h2 style='text-align: center; color: black;'> Visualizador "
                "Interactivo de Datos Climáticos de España </h2>",
                unsafe_allow_html=True)

    # Descripción de lo que realiza la aplicación web
    st.markdown("Consulta información climática actualizada de cada "
                "provincia de España de forma visual y dinámica. Este mapa "
                "interactivo muestra datos como el clima, la temperatura, la "
                "humedad o las precipitaciones y nevadas (en caso de que las "
                "hubiera) utilizando marcadores informativos para cada "
                "ubicación.")

    st.markdown("Para ver la información de una provincia basta con "
                "hacer `click` en cualquier marcador del mapa para mostrar "
                "el `popup` con toda la información meteorológica actual "
                "correspondiente a dicha provincia.")

    # Se crea un mapa centrado en Madrid
    m = leafmap.Map(center=(40.4168, -3.7038), zoom=6)

    # Se realiza petición GET a la API Gateway en /clima
    response = requests.get(f"{api_gateway_url}/clima").json()

    # Se veritica si la clave 'data' está en la respuesta JSON...
    if 'data' in response:

        # En ese caso se almacena la clave 'data', que es la lista de todos
        # los JSON de respuesta de todas las provincias y ciudades autónomas
        response_list = response['data']

    # Si no...
    else:

        # Mensaje de error de 'streamlit'
        st.error("No se pudo obtener datos de la API. Revisa la conexión.")
        st.stop()

    # Para cada diccionario de la lista...
    for provincia_dict in response_list:

        # Se extraen los campos de 'Latitud' y 'Longitud'
        lat = provincia_dict.get("Latitud")
        lon = provincia_dict.get("Longitud")

        # Si la latitud es un 'string'...
        if isinstance(lat, str):

            # Intenta ejecutar el bloque de código
            try:

                # Se convierte el valor a un float
                lat = float(lat)

            # Si hay error...
            except ValueError:

                # Se muestra mensaje de 'warning' y se continúa
                st.warning("Latitud inválida para "
                           f"{provincia_dict['Nombre']}: {lat}")
                continue

        # Si la longitud es un 'string'...
        if isinstance(lon, str):

            # Intenta ejecutar el bloque de código
            try:

                # Se convierte el valor a un float
                lon = float(lon)

            # Si hay error de valor...
            except ValueError:

                # Se muestra mensaje de 'warning' y se continúa
                st.warning(f"Longitud inválida para "
                           f"{provincia_dict['Nombre']}: {lon}")
                continue

        # Si la latitud o la longitud son None...
        if lat is None or lon is None:

            # Se muestra mensaje de 'warning' y se continúa
            st.warning(f"Coordenadas faltantes para "
                       f"{provincia_dict['Nombre']}")
            continue

        # Se crea un contenido 'popup' con el nombre de la provincia,
        # además de los demás datos de clima, temperatura, etc, sustituyendo
        # las 'ñ' y las tildes por sus códigos numéricos HTML con la
        # función 'convert_to_html_entities'
        popup_content = (
            f"Provincia: "
            f"{convert_to_html_entities(provincia_dict['Nombre'])}<br>"
            f"Clima: {convert_to_html_entities(provincia_dict['Clima'])}<br>"
            f"Temperatura: {provincia_dict['Temperatura']} &#176;C<br>"
            f"Humedad: {provincia_dict['Humedad']} %<br>"
            f"Nubosidad: {provincia_dict['Nubosidad']} %<br>"
            f"{convert_to_html_entities('Presión Atm')}: "
            f"{provincia_dict['Presion_Atmosferica']} hPa<br>"
            f"Viento: {provincia_dict['Velocidad_Viento']} m/s<br>"
        )

        # Si las precipitaciones del diccionario son mayores de 0 mm/h...
        if float(provincia_dict['Precipitaciones']) > 0.0:

            # Se agregan las precipitaciones al 'popup'
            popup_content += (
                f"Precipitaciones: "
                f"{provincia_dict['Precipitaciones']} mm/h<br>"
            )

        # Si las nevadas del diccionario son mayores de 0 mm/h...
        if float(provincia_dict['Nevadas']) > 0.0:

            # Se agregan las nevadas al 'popup'
            popup_content += (
                f"Nevadas: "
                f"{provincia_dict['Nevadas']} mm/h<br>"
            )

        # Se crea un 'popup' con el contenido y se especifica su ancho máximo
        popup = folium.Popup(popup_content, max_width=400, sticky=False)

        # Añadir el marcador al mapa en la localización indicada con el
        # 'popup' de la información meteorológica
        m.add_marker(location=([lat, lon]), popup=popup)

    # Renderiza el mapa en Streamlit
    m.to_streamlit()

# Si se elige la opción 'Consultar provincia específica'...
if action == "Consultar provincia específica":

    # Título de la aplicación
    st.markdown(
        "<h2 style='text-align: center; color: black;'> Consultar Provincia "
        "Específica </h2>", unsafe_allow_html=True
    )

    # Descripción de lo que realiza la aplicación web
    st.markdown("Consulta información climática actualizada de una "
                "provincia específica. Al introducir dicha provincia en el "
                "cuadro de texto se muestra el `JSON` de respuesta de la "
                "`API` con todos los datos climáticos además de mostrar en "
                "el mapa donde está situada dicha provincia.")

    # Se obtiene la lista de provincias y ciudades autónomas; y tras obtenerla
    # se llama a 'translate_province_list' para renombrar correctamente
    # algunas provincias (Ej: Áraba a Álava)
    provinces_list = translate_province_list(
        get_provinces_and_autonomous_cities()
    )

    # Se introduce un 'widget' de selección de provincia
    provincia = st.selectbox(label="Selecciona el nombre de la provincia:",
                             options=provinces_list, index=None,
                             placeholder="Elige una provincia")

    # Cuando se introduce una provincia...
    if provincia:

        # Se hace una solicitud GET a la API Gateway en '/clima/{provincia}'
        # (aunque la provincia tenga tilde, en la URL aparece sin él)
        response = requests.get(f"{api_gateway_url}/clima/{provincia}")

        # Si la respuesta es satisfactoria...
        if response.status_code == 200:

            # Se almacena la respuesta JSON
            data = response.json()

            # Si la respuesta JSON existe...
            if data:

                # Se muestra el JSON de la respuesta en la aplicación web
                st.json(data)

                # Se recopilan los valores de latitud y longitud de la
                # provincia
                lat, lon = float(data['Latitud']), float(data['Longitud'])

                # Se crea un mapa centrado en los valores de latitud y
                # longitud de la provincia
                map_provincia = leafmap.Map(center=(lat, lon), zoom=6)

                # Se añade el marcador de la provincia al mapa
                map_provincia.add_marker(location=(lat, lon))

                # Se renderiza el mapa en Streamlit
                map_provincia.to_streamlit()

            # Si la respuesta JSON no existe...
            else:

                # Mensaje de 'warning' en Streamlit
                st.warning(
                    "No se encontraron datos para la provincia especificada."
                )

        # Si la respuesta de la solicitud GET no es satisfactoria...
        else:

            # Mensaje de error en Streamlit
            st.error(
                "Error al obtener los datos. Verifica el nombre de la "
                "provincia."
            )

# Si se elige la opción 'Estadísticas'...
if action == "Estadísticas":

    # Título de la aplicación
    st.markdown(
        "<h2 style='text-align: center; color: black;'> Estadísticas "
        "Generales </h2>", unsafe_allow_html=True
    )

    # Descripción de lo que realiza la aplicación web
    st.markdown("En esta sección se muestran estadísticas a partir de la "
                "información climática recopilada para cada una de las "
                "provincias.")

    # Se intenta ejecutar el siguiente bloque de código...
    try:

        # Se realiza la solicitud 'GET /clima' y obtener el JSON de
        # respuesta de todas las provincias
        response = requests.get(f"{api_gateway_url}/clima").json()

    # Si hay excepción con la solicitud a la API...
    except requests.RequestException:

        # Se indica un mensaje de error de Streamlit
        st.error("No se pudo conectar con la API. Intentalo más tarde.")

        # Se para la aplicación
        st.stop()

    # Si la clave 'data' existe en la respuesta
    if "data" in response:

        # Se almacena dicha clave en 'response_list'
        response_list = response["data"]

        # Se crea un dataframe para facilitar el manejo de datos (cada clave
        # de los JSON es una columna)
        data = pd.DataFrame(response_list)

        # Se recopilan en una lista las columnas numéricas de tipo 'string'
        columns_float = [
            "Temperatura",
            "Humedad",
            "Velocidad_Viento",
            "Presion_Atmosferica",
            "Precipitaciones",
            "Nevadas",
            "Nubosidad",
        ]

        # Para cada columna...
        for col in columns_float:

            # Se convierten los valores a tipo 'float'
            data[col] = data[col].astype(float)

        # 1. **Promedios Generales**
        st.subheader("Promedios Generales")
        promedios = data[columns_float].mean().round(2)
        st.write(promedios)

        # 2. **Máximos y Mínimos**
        st.subheader("Máximos y Mínimos de Temperatura")
        max_temp = data.loc[data['Temperatura'].idxmax()]
        min_temp = data.loc[data['Temperatura'].idxmin()]

        st.write(f"Provincia más cálida: {max_temp['Nombre']} ({max_temp['Temperatura']} °C)")
        st.write(f"Provincia más fría: {min_temp['Nombre']} ({min_temp['Temperatura']} °C)")

        # 3. **Distribución de Temperaturas**
        st.subheader("Distribución de Temperaturas")
        temperaturas = data[['Nombre', 'Temperatura']].sort_values(by='Temperatura', ascending=False)
        st.bar_chart(temperaturas.set_index('Nombre')['Temperatura'])

        # 4. **Distribución de Humedad**
        st.subheader("Distribución de Humedad")
        humedad = data[['Nombre', 'Humedad']].sort_values(by='Humedad', ascending=False)
        st.bar_chart(humedad.set_index('Nombre')['Humedad'])

        # 5. **Frecuencia de Condiciones Climáticas**
        st.subheader("Frecuencia de Condiciones Climáticas")
        clima_counts = data['Clima'].value_counts()
        st.bar_chart(clima_counts)

        # 6. **Precipitaciones Totales**
        st.subheader("Precipitaciones Totales")
        precipitaciones = data[['Nombre', 'Precipitaciones']].sort_values(by='Precipitaciones', ascending=False)
        st.bar_chart(precipitaciones.set_index('Nombre')['Precipitaciones'])

        # 7. **Top 10 Más Calientes**
        st.subheader("Top 10 Más Calientes")
        top_10_calientes = data[['Nombre', 'Temperatura']].sort_values(by='Temperatura', ascending=False).head(10)
        st.bar_chart(top_10_calientes.set_index('Nombre')['Temperatura'])

        # 8. **Top 10 Más Frías**
        st.subheader("Top 10 Más Frías")
        top_10_frias = data[['Nombre', 'Temperatura']].sort_values(by='Temperatura', ascending=True).head(10)
        st.bar_chart(top_10_frias.set_index('Nombre')['Temperatura'])

        # 9. **Correlación entre Variables**
        st.subheader("Matriz de Correlación")
        corr = data[columns_float].corr()
        fig = plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        st.pyplot(fig)

        # 10. **Distribución de Velocidad del Viento**
        st.subheader("Distribución de Velocidad del Viento")
        viento = data[['Nombre', 'Velocidad_Viento']].sort_values(by='Velocidad_Viento', ascending=False)
        st.bar_chart(viento.set_index('Nombre')['Velocidad_Viento'])
