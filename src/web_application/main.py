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
    st.markdown("En esta sección se presentan estadísticas basadas en la "
                "información recopilada de cada una de las provincias. Con "
                "el objetivo de facilitar la comprensión de los "
                "datos, se generarán gráficos y/o tablas que visualizan "
                "estos resultados de manera clara y concisa.")

    st.markdown("Estas representaciones visuales permiten observar patrones, "
                "tendencias y comparaciones entre las distintas provincias "
                "proporcionando una visión más accesible y comprensible de "
                "la información.")

    # Para crear espacio
    st.text("")

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

        # Para cada columna numérica...
        for col in columns_float:

            # Se convierten los valores del 'dataframe' a tipo 'float'
            data[col] = data[col].astype(float)

        # 1. Promedios generales de todas las variables numéricas
        st.markdown("<h4 style='text-align: center; color: black;'> Promedios"
                    " Generales </h4>", unsafe_allow_html=True)

        st.markdown("En esta tabla se presentan los promedios de los datos "
                    "correspondientes a todas las provincias y ciudades "
                    "autónomas de España, incluyendo variables como "
                    "temperatura, humedad, viento, presión atmosférica, "
                    "nubosidad, precipitaciones y nevadas.")

        # Se calcula la media de todas las columnas numéricas, redondeándolas
        # a dos decimales
        promedios = data[columns_float].mean().round(2)

        # Se resetea el índice de la serie de pandas, convirtiéndola en
        # dataframe. Posteriormente se renombran las columnas del dataframe
        promedios_df = (
            pd.DataFrame(promedios).reset_index()
            .rename(columns={"index": "Dato", 0: "Promedio"}))

        # Se almacena un diccionario para añadir las unidades a los promedios
        unidades = {
            'Temperatura': 'ºC',
            'Humedad': '%',
            'Velocidad_Viento': 'm/s',
            'Presion_Atmosferica': 'hPa',
            'Nubosidad': '%',
            'Precipitaciones': 'mm/h',
            'Nevadas': 'mm/h'
        }

        # Con la función 'apply' se añaden las unidades a los promedios
        promedios_df['Promedio'] = promedios_df.apply(
            lambda row: f"{row['Promedio']} {unidades.get(row['Dato'], '')}",
            axis=1)

        # Se convierte el dataframe a HTML
        html_table = promedios_df.to_html(index=False)

        # Se centra el dataframe con HTML usando CSS
        st.markdown(f'<div style="display: flex; justify-content: '
                    f'center;">{html_table}</div>', unsafe_allow_html=True)

        # Para crear espacio
        st.text("")
        st.text("")

        # 2. Distribución de Temperaturas
        st.markdown("<h4 style='text-align: center; color: black;'> Distri"
                    "bución de Temperaturas </h4>", unsafe_allow_html=True)

        st.markdown("Este gráfico muestra la distribución de las temperaturas"
                    " registradas en las distintas provincias y ciudades "
                    "autónomas de España. Las barras representan los valores "
                    "de temperatura. Esta visualización facilita la "
                    "comparación entre regiones y proporciona una visión "
                    "general de las diferencias térmicas a nivel nacional.")

        # Se crea una figura con seaborn
        figure = plt.figure(figsize=(12, 6))

        # Se dibuja el diagrama de barras con los nombres de las provincias
        # en el Eje X y las temperaturas en el Eje Y, coloreando las barras
        # más rojas o más azules según haya más o menos temperatura
        sns.barplot(
            x='Nombre',
            y='Temperatura',
            data=data[['Nombre', 'Temperatura']].sort_values(by='Nombre'),
            palette='coolwarm',
            hue='Temperatura',
            legend=False
        )

        # Se rota 90º los nombres de las provincias y se ponen las etiquetas
        # en el Eje X y en el Eje Y
        plt.xticks(rotation=90)
        plt.xlabel("Provincias", labelpad=12)
        plt.ylabel("Temperatura (°C)", labelpad=12)

        # Se muestra el gráfico de seaborn en Streamlit
        st.pyplot(figure, use_container_width=True)

        # Para crear espacio
        st.text("")

        # 2.1. Provincias con las 10 temperaturas más altas/bajas
        st.markdown("<h6 style='text-align: center; color: black;'> Provi"
                    "ncias con las temperaturas más altas/bajas </h6>",
                    unsafe_allow_html=True)

        st.markdown("Una vez visto el panorama general de las temperaturas "
                    "de todas las provincias, se muestran de todas ellas las "
                    "más extremas. Así, la gráfica de la izquierda muestra "
                    "las diez provincias con las temperaturas más altas de "
                    "España, mientras que la gráfica de la derecha representa"
                    " las diez provincias con las temperaturas más bajas.")

        # Se crean dos columnas con Streamlit
        col1, col2 = st.columns(2)

        # Para la columna de la izquierda...
        with col1:

            # Se calcula en el dataframe las filas con los 10 valores más
            # altos de temperatura
            hottest = data.nlargest(n=10, columns='Temperatura')

            # Se crea una figura
            plt.figure(figsize=(6, 4))

            # Se dibuja un diagrama de barras con las provincias en el Eje X y
            # las temperaturas en el Eje Y, coloreando las barras con más
            # intensidad si tienen mayor temperatura
            sns.barplot(x='Nombre', y='Temperatura', data=hottest,
                        palette='Reds_r')

            # Se personaliza el diagrama con etiquetas y rotación de las del
            # Eje X
            plt.xticks(rotation=90)
            plt.xlabel("Provincias")
            plt.ylabel("Temperatura (°C)")

            # Se muestra la figura en Streamlit
            st.pyplot(plt, use_container_width=True)

        # Para la columna de la derecha...
        with col2:

            # Se calcula en el dataframe las filas con los 10 valores más
            # bajos de temperatura
            coldest = data.nsmallest(n=10, columns='Temperatura')

            # Se crea una figura
            plt.figure(figsize=(6, 4))

            # Se dibuja un diagrama de barras con las provincias en el Eje X y
            # las temperaturas en el Eje Y, coloreando las barras con más
            # intensidad si tienen menor temperatura
            sns.barplot(x='Nombre', y='Temperatura', data=coldest,
                        palette='Blues_r')

            # Se personaliza el diagrama con etiquetas y rotación de las del
            # Eje X
            plt.xticks(rotation=45)
            plt.xlabel("Provincias")
            plt.ylabel("Temperatura (°C)")

            # Se muestra la figura en Streamlit
            st.pyplot(plt, use_container_width=True)

        # Para crear espacio
        st.text("")
        st.text("")

        # 3. Distribución de Humedad
        st.markdown("<h4 style='text-align: center; color: black;'> Distri"
                    "bución de Humedad </h4>", unsafe_allow_html=True)

        st.markdown("El siguiente gráfico presenta la distribución del "
                    "porcentaje de humedad registrado en todas las provincias"
                    " y ciudades autónomas de España. Este análisis permite "
                    "comparar los niveles de humedad entre las diferentes "
                    "regiones, destacando las provincias con los valores más "
                    "altos y más bajos. La humedad es un indicador clave del "
                    "clima local, y su visualización proporciona una "
                    "perspectiva clara de las condiciones atmosféricas en el "
                    "territorio nacional.")

        # Se crea una figura con seaborn
        figure = plt.figure(figsize=(14, 6))

        # Se dibuja el diagrama de barras con los nombres de las provincias
        # en el Eje X y los porcentajes en el Eje Y, coloreando las barras
        # cada vez más azules según haya más humedad
        sns.barplot(
            x='Nombre',
            y='Humedad',
            data=data[['Nombre', 'Humedad']].sort_values(by='Nombre'),
            palette='Blues',
            hue='Humedad',
            legend=False,
        )

        # Se rota 90º los nombres de las provincias y se ponen las etiquetas
        # en el Eje X y en el Eje Y
        plt.xticks(rotation=90)
        plt.xlabel("Provincias", fontsize=12)
        plt.ylabel("Humedad (%)", fontsize=12)

        # Se muestra el gráfico de seaborn en Streamlit
        st.pyplot(figure, use_container_width=True)

        # Se crea espacio
        st.text("")

        # 3.1. Provincias con los porcentajes de humedad más altos/bajos
        st.markdown("<h6 style='text-align: center; color: black;'> Provi"
                    "ncias con los porcentajes más altos/bajos de humedad"
                    "</h6>", unsafe_allow_html=True)

        st.markdown("Una vez visto el panorama general, se muestran los "
                    "porcentajes de humedad más extremos como en el caso de "
                    "la temperatura. Así, la gráfica de la izquierda muestra "
                    "las diez provincias con las humedades más altas, "
                    "mientras que la gráfica de la derecha representa las "
                    "diez provincias con las humedades más bajas.")

        # Se crean dos columnas con Streamlit
        col1, col2 = st.columns(2)

        # Para la columna de la izquierda...
        with col1:

            # Se calcula en el dataframe las filas con los 10 valores más
            # altos de humedad
            humidity_top = data.nlargest(n=10, columns='Humedad')

            # Se crea una figura
            plt.figure(figsize=(6, 4))

            # Se dibuja un diagrama de barras con las provincias en el Eje X y
            # las temperaturas en el Eje Y, coloreando las barras con más
            # intensidad si tienen mayor temperatura
            sns.barplot(x='Nombre', y='Humedad', data=humidity_top,
                        palette='Blues_r')

            # Se personaliza el diagrama con etiquetas y rotación de las del
            # Eje X
            plt.xticks(rotation=45)
            plt.xlabel("Provincias")
            plt.ylabel("Humedad (%)")

            # Se muestra la figura en Streamlit
            st.pyplot(plt, use_container_width=True)

        # Para la columna de la derecha...
        with col2:

            # Se calcula en el dataframe las filas con los 10 valores más
            # bajos de humedad
            humidity_down = data.nsmallest(n=10, columns='Humedad')

            # Se crea una figura
            plt.figure(figsize=(6, 4))

            # Se dibuja un diagrama de barras con las provincias en el Eje X y
            # las temperaturas en el Eje Y, coloreando las barras con más
            # intensidad si tienen menor temperatura
            sns.barplot(x='Nombre', y='Humedad', data=humidity_down,
                        palette=["#b3cde0"])

            # Se personaliza el diagrama con etiquetas y rotación de las del
            # Eje X
            plt.xticks(rotation=45)
            plt.xlabel("Provincias")
            plt.ylabel("Humedad (%)")

            # Se muestra la figura en Streamlit
            st.pyplot(plt, use_container_width=True)

        # Para crear espacio
        st.text("")
        st.text("")

        # 4. Condiciones Climáticas
        st.markdown("<h4 style='text-align: center; color: black;'> Condicion"
                    "es Climáticas </h4>", unsafe_allow_html=True)

        st.markdown("El siguiente gráfico presenta la distribución de las "
                    "condiciones climáticas. Cada barra representa una "
                    "categoría climática indicando su proporción respecto "
                    "al total de registros. Esta visualización facilita "
                    "identificar de forma intuitiva cuáles son las "
                    "condiciones más frecuentes y menos comunes, dando una "
                    "perspectiva clara de la predominancia de cada tipo de "
                    "clima en España.")

        # Se crea una figura con seaborn
        figure = plt.figure(figsize=(14, 6))

        # Se cuentan los valores de la columna 'Clima' normalizandolos en
        # porcentajes, y posteriormente se resetea el índice de la serie
        # resultante para convertirla a dataframe
        percent_df = (
            (data['Clima'].value_counts(normalize=True) * 100).reset_index()
        )

        # Se dibuja el diagrama de barras con los nombres de las provincias
        # en el Eje X y los porcentajes en el Eje Y, coloreando las barras
        # cada vez más azules según haya más humedad
        sns.barplot(
            data=percent_df,
            x=percent_df['proportion'],
            y=percent_df['Clima'],
            palette='YlGnBu'
        )

        # Para cada índice y fila de 'percent_df'...
        for index, row in percent_df.iterrows():

            # Se escribe en texto el porcentaje de cada barra sobre el gráfico
            # en las posiciones del Eje X e Y indicadas
            plt.text(x=row['proportion'] + 1.75,
                     y=index,
                     s=f"{row['proportion']:.1f}%",
                     ha='center')

        # Se rota 45 los nombres de los climas y se ponen las etiquetas
        # en el Eje X y en el Eje Y
        plt.yticks(rotation=45)
        plt.xlabel("Porcentaje (%)", labelpad=25)
        plt.ylabel("Clima", labelpad=15)

        # Se muestra el gráfico de seaborn en Streamlit
        st.pyplot(figure, use_container_width=True)

        # Se crea espacio
        st.text("")
        st.text("")

        # 6. **Precipitaciones Totales**
        st.subheader("Precipitaciones Totales")
        precipitaciones = data[['Nombre', 'Precipitaciones']].sort_values(by='Precipitaciones', ascending=False)
        st.bar_chart(precipitaciones.set_index('Nombre')['Precipitaciones'])

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
