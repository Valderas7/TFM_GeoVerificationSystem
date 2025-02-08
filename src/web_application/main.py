# Librerías
import streamlit as st
import datetime
import pandas as pd
import requests
import leafmap.foliumap as leafmap
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from utils.html_entities import convert_to_html_entities
from utils.geography_utils import (get_provinces_and_autonomous_cities,
                                   translate_province_list)

# Se definen constantes a usar
temp_name_constant = "Temperatura (°C)"
humidity_name_constant = "Humedad (%)"

# Se guarda en una variable la URL de la API Gateway desplegada con AWS
api_gateway_url = 'https://mjb5qk45si.execute-api.us-east-1.amazonaws.com/prod'

# Barra lateral para mostrar las opciones disponibles
st.sidebar.title("Secciones")
action = st.sidebar.radio(label="Elige una sección para seleccionar el tipo "
                          "de datos a mostrar.",
                          options=["Mapa Interactivo de Datos "
                                   "Climáticos en España",
                                   "Exploración de Datos Climáticos por "
                                   "Provincia",
                                   "Estadísticas Generales"])

# Si se elige la opción 'Mapa Interactivo de Datos Climáticos en España'
if action == "Mapa Interactivo de Datos Climáticos en España":

    # Título de la Web App con cabecera H2
    st.markdown("<h2 style='text-align: center; color: black;'> Mapa "
                "Interactivo de Información <br> Climática en España </h2>",
                unsafe_allow_html=True)

    # Descripción de lo que realiza la aplicación web
    st.markdown("En esta sección se muestra información climática actualizada"
                " de cada provincia de España de forma visual y dinámica. "
                "Este mapa interactivo muestra datos como el clima, la "
                "temperatura, la humedad o las precipitaciones (en caso de "
                "que las hubiera) utilizando marcadores informativos para "
                "cada ubicación.")

    st.markdown("Para ver la información de una provincia basta con "
                "hacer `click` en cualquier marcador del mapa para mostrar "
                "el `popup` con toda la información meteorológica actual "
                "correspondiente a dicha provincia.")

    # Se crea un mapa centrado en Madrid sin herramientas de dibujo
    m = leafmap.Map(center=(40.4168, -3.7038), zoom=6, draw_control=False)

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
            f"<b>Provincia:</b> "
            f"{convert_to_html_entities(provincia_dict['Nombre'])}<br>"
            f"<b>Clima:</b> "
            f"{convert_to_html_entities(provincia_dict['Clima'])}<br>"
            f"<b>Temperatura:</b> "
            f"{provincia_dict['Temperatura']} &#176;C<br>"
            f"<b>Humedad:</b> {provincia_dict['Humedad']} %<br>"
            f"<b>Nubosidad:</b> {provincia_dict['Nubosidad']} %<br>"
            f"<b>{convert_to_html_entities('Presión Atmosférica')}:</b> "
            f"{provincia_dict['Presion_Atmosferica']} hPa<br>"
            f"<b>Viento:</b> {provincia_dict['Velocidad_Viento']} m/s<br>"
        )

        # Si las precipitaciones del diccionario son mayores de 0 mm/h...
        if float(provincia_dict['Precipitaciones']) > 0.0:

            # Se agregan las precipitaciones al 'popup'
            popup_content += (
                f"<b>Precipitaciones:</b> "
                f"{provincia_dict['Precipitaciones']} mm/h<br>"
            )

        # Si las nevadas del diccionario son mayores de 0 mm/h...
        if float(provincia_dict['Nevadas']) > 0.0:

            # Se agregan las nevadas al 'popup'
            popup_content += (
                f"<b>Nevadas:</b> "
                f"{provincia_dict['Nevadas']} mm/h<br>"
            )

        # Se crea un 'popup' con el contenido y se especifica su ancho máximo
        popup = folium.Popup(popup_content, max_width=400, sticky=False)

        # Añadir el marcador al mapa en la localización indicada con el
        # 'popup' de la información meteorológica
        m.add_marker(location=([lat, lon]), popup=popup)

    # Renderiza el mapa en Streamlit
    m.to_streamlit()

# Si se elige la opción 'Exploración de Datos Climáticos por Provincia'...
if action == "Exploración de Datos Climáticos por Provincia":

    # Título de la aplicación
    st.markdown(
        "<h2 style='text-align: center; color: black;'> Exploración de Datos "
        "Climáticos por Provincia </h2>", unsafe_allow_html=True
    )

    # Descripción de lo que realiza la aplicación web
    st.markdown("Esta sección permite visualizar los datos climáticos de las "
                "últimas `24 horas` de una provincia específica, además de "
                "mostrar los valores máximos y mínimos alcanzados durante "
                "dicho periodo. Para ver los datos climáticos de una hora en "
                "concreto hay que seleccionar en la ventana de selección la "
                "provincia de interés.")
    st.markdown("- Una vez seleccionada, se muestra una tabla donde "
                "aparecen los valores máximos y mínimos durante las últimas "
                "24 horas.")
    st.markdown("- Con el `slider` se selecciona la hora dentro del intervalo"
                " de 24 horas de la cual mostrar los datos climáticos en el "
                "mapa de `Leafmap`.")

    # Se obtiene la lista de provincias y ciudades autónomas; y tras obtenerla
    # se llama a 'translate_province_list' para renombrar correctamente
    # algunas provincias (Ej: Áraba a Álava)
    provinces_list = sorted(
        translate_province_list(get_provinces_and_autonomous_cities())
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

                # Se recopilan los valores de latitud y longitud de la
                # provincia de cualquier diccionario de la lista
                lat, lon = (float(data[0]['Latitud']),
                            float(data[0]['Longitud']))

                # Se crea un mapa centrado en los valores de latitud y
                # longitud de la provincia seleccionada y sin controles de
                # dibujo
                map_provincia = leafmap.Map(center=(lat, lon), zoom=6,
                                            draw_control=False)

                # Se añade el marcador de la provincia al mapa
                map_provincia.add_marker(location=(lat, lon))

                # Se convierte la lista de diccionarios a un 'dataframe'
                province_df = pd.DataFrame(data)

                # Se crea otro 'dataframe' para mostrar los valores máximos y
                # mínimos de la provincia durante este periodo de 24 horas
                tabla_max_min = pd.DataFrame({
                    "Variable": [
                        temp_name_constant, humidity_name_constant,
                        "Viento (m/s)", "Nubosidad (%)"
                    ],
                    "Mínimo": [
                        province_df["Temperatura"].astype(float).min(),
                        province_df["Humedad"].astype(float).min(),
                        province_df["Velocidad_Viento"].astype(float).min(),
                        province_df["Nubosidad"].astype(float).min()
                    ],
                    "Máximo": [
                        province_df["Temperatura"].astype(float).max(),
                        province_df["Humedad"].astype(float).max(),
                        province_df["Velocidad_Viento"].astype(float).max(),
                        province_df["Nubosidad"].astype(float).max()
                    ]}
                )

                # Se muestra el 'dataframe' en Streamlit
                st.dataframe(tabla_max_min, use_container_width=True)

                # Se convierte el tiempo Unix a formato 'datetime64' de pandas
                # (YYYY-MM-DD HH:mm:ss) indicando que la época está indicada
                # en segundos. Además, se redondea los valores al minuto más
                # cercano, truncando los segundos a '00' (para que no haya
                # problemas a la hora de filtrar datos por fecha)
                province_df["Fecha"] = pd.to_datetime(
                    province_df["Marca_Temporal"],
                    unit="s"
                ).dt.floor("min")

                # Se busca el 'datetime' de 'pandas' más lejano y el más
                # reciente y se convierten a objetos 'datetime' estándar de
                # Python para poder usarlos en el 'slider' de Streamlit
                min_fecha = province_df["Fecha"].min().to_pydatetime()
                max_fecha = province_df["Fecha"].max().to_pydatetime()

                # Para crear espacio
                st.text("")

                # Se crea un 'slider' de Streamlit para seleccionar los datos
                # de una de las horas entre 'min_fecha' y 'max_fecha' en pasos
                # de dos horas
                fecha_seleccionada = st.slider(
                    "Selecciona una hora:",
                    min_value=min_fecha,
                    max_value=max_fecha,
                    value=min_fecha,
                    format="DD-MM-YYYY HH:mm",
                    step=datetime.timedelta(hours=2)
                )

                # Filtrar datos del 'dataframe' para seleccionar los de la
                # fecha y hora seleccionadas en el 'slider'
                datos_fecha = (
                    province_df.loc[
                        province_df['Fecha'] == fecha_seleccionada]
                )

                # Si existen datos en el 'dataframe' para la fecha y hora
                # seleccionadas en el 'slider'...
                if not datos_fecha.empty:

                    # Se selecciona la fila del 'dataframe' (será una serie de
                    # 'pandas')
                    fila = datos_fecha.iloc[0]

                    # Se crea un texto para añadir a un 'popup' del mapa
                    popup_text = (
                        f"<b>Clima:</b> "
                        f"{convert_to_html_entities(fila['Clima'])}<br>"
                        f"<b>Temperatura:</b> "
                        f"{fila['Temperatura']} &#176;C<br>"
                        f"<b>Humedad:</b> {fila['Humedad']}%<br>"
                        f"<b>Viento:</b> {fila['Velocidad_Viento']} m/s<br>"
                        f"<b>Nubosidad:</b> {fila['Nubosidad']}%<br>"
                    )

                    # Si las precipitaciones de la serie de 'pandas' son
                    # mayores de 0 mm/h...
                    if float(fila['Precipitaciones']) > 0.0:

                        # Se agregan las precipitaciones al 'popup'
                        popup_text += (
                            f"<b>Precipitaciones:</b> "
                            f"{fila['Precipitaciones']} mm/h<br>"
                        )

                    # Si las nevadas de la serie de 'pandas' son mayores de
                    # 0 mm/h...
                    if float(fila['Nevadas']) > 0.0:

                        # Se agregan las nevadas al 'popup'
                        popup_text += (
                            f"<b>Nevadas:</b> {fila['Nevadas']} mm/h<br>"
                        )

                    # Se crea un 'popup' con el contenido y se especifica su
                    # ancho máximo
                    popup = folium.Popup(popup_text, max_width=400,
                                         sticky=False, show=True)

                    # Se añade un marcador en el mapa de 'Streamlit' en la
                    # localización de la provincia con la información del
                    # 'popup'
                    map_provincia.add_marker(
                        location=(fila['Latitud'], fila['Longitud']),
                        popup=popup
                    )

                # Si no hay datos para la hora seleccionada...
                else:

                    # Mensaje de error en Streamlit
                    st.error(f"No se encontraron datos para {provincia} a "
                             "la hora especificada.")

                # Para crear espacio entre el 'slider' y el mapa
                st.text("")

                # Se renderiza el mapa de 'Leafmap' en Streamlit
                map_provincia.to_streamlit()

            # Si la respuesta JSON no existe...
            else:

                # Mensaje de error en Streamlit
                st.error(
                    f"No se encontraron datos para {provincia}."
                )

        # Si la respuesta de la solicitud GET no es satisfactoria...
        else:

            # Mensaje de error en Streamlit
            st.error("Error al obtener los datos de la API.")

    # Si no...
    else:

        # No se hace nada
        pass

# Si se elige la opción 'Estadísticas'...
if action == "Estadísticas Generales":

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

        # Se cambian dos valores de la columna 'Dato'
        promedios_df['Dato'] = promedios_df['Dato'].replace(
            {'Velocidad_Viento': 'Viento',
             'Presion_Atmosferica': 'Presión'}
        )

        # Se almacena un diccionario para añadir las unidades a la columna
        # 'Promedio' del 'dataframe'
        unidades = {
            'Temperatura': 'ºC',
            'Humedad': '%',
            'Viento': 'm/s',
            'Presión': 'hPa',
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

        # Se centra el dataframe con HTML
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

        # Se crea una figura con matplotlib
        figure = plt.figure(figsize=(12, 6))

        # Se dibuja el diagrama de barras con los nombres de las provincias
        # en el Eje X y las temperaturas en el Eje Y, coloreando las barras
        # más rojas o más azules según haya más o menos temperatura
        sns.barplot(
            x='Nombre',
            y='Temperatura',
            data=data.sort_values(by='Nombre'),
            palette='coolwarm',
            hue='Temperatura',
            legend=False
        )

        # Se rota 90º los nombres de las provincias y se ponen las etiquetas
        # en el Eje X y en el Eje Y
        plt.xticks(rotation=90)
        plt.xlabel("Provincias", labelpad=12)
        plt.ylabel(temp_name_constant, labelpad=12)

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

        # Se almacenan los valores máximos y mínimos para fijar las dos
        # gráficas en el mismo Eje Y
        temp_min = min(data['Temperatura'])
        temp_max = max(data['Temperatura'])

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
            # Eje X. También se establece el límite del Eje Y
            plt.xticks(rotation=90)
            plt.xlabel("Provincias")
            plt.ylabel(temp_name_constant)
            plt.ylim(temp_min - 1, temp_max + 1)

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
            # Eje X. También se establece el límite del Eje Y
            plt.xticks(rotation=45)
            plt.xlabel("Provincias")
            plt.ylabel(temp_name_constant)
            plt.ylim(temp_min - 1, temp_max + 1)

            # Se muestra la figura en Streamlit
            st.pyplot(plt, use_container_width=True)

        # Para crear espacio
        st.text("")
        st.text("")

        # 3. Distribución de Humedad
        st.markdown("<h4 style='text-align: center; color: black;'> Distri"
                    "bución de Humedad </h4>", unsafe_allow_html=True)

        st.markdown("Esta visualización presenta la distribución del "
                    "porcentaje de humedad registrado en todas las provincias"
                    " y ciudades autónomas de España. Este análisis permite "
                    "comparar los niveles de humedad entre las diferentes "
                    "regiones, destacando las provincias con los valores más "
                    "altos y más bajos. La humedad es un indicador clave del "
                    "clima local, y su visualización proporciona una "
                    "perspectiva clara de las condiciones atmosféricas en el "
                    "territorio nacional.")

        # Se crea una figura con matplotlib
        figure = plt.figure(figsize=(14, 6))

        # Se dibuja el diagrama de barras con los nombres de las provincias
        # en el Eje X y los porcentajes en el Eje Y, coloreando las barras
        # cada vez más azules según haya más humedad
        sns.barplot(
            x='Nombre',
            y='Humedad',
            data=data.sort_values(by='Nombre'),
            palette='Blues',
            hue='Humedad',
            legend=False,
        )

        # Se rota 90º los nombres de las provincias y se ponen las etiquetas
        # en el Eje X y en el Eje Y
        plt.xticks(rotation=90)
        plt.xlabel("Provincias", fontsize=12)
        plt.ylabel(humidity_name_constant, fontsize=12)

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

        # Se almacenan los valores máximos y mínimos para fijar las dos
        # gráficas en el mismo Eje Y
        humidity_min = min(data['Humedad'])
        humidity_max = max(data['Humedad'])

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
            # Eje X. También se establece el límite del Eje Y
            plt.xticks(rotation=45)
            plt.xlabel("Provincias")
            plt.ylabel(humidity_name_constant)
            plt.ylim(humidity_min - 1, humidity_max + 1)

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
            # Eje X. También se establece el límite del Eje Y
            plt.xticks(rotation=45)
            plt.xlabel("Provincias")
            plt.ylabel("Humedad (%)")
            plt.ylim(humidity_min - 1, humidity_max + 1)

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

        # Se crea una figura con matplotlib
        figure = plt.figure(figsize=(14, 6))

        # Se cuentan los valores de la columna 'Clima' normalizandolos en
        # porcentajes, y posteriormente se resetea el índice de la serie
        # resultante para convertirla a dataframe
        percent_df = (
            (data['Clima'].value_counts(normalize=True) * 100).reset_index()
        )

        # Se dibuja el diagrama de barras con los nombres de los climas en
        # el Eje Y y los porcentajes en el Eje X
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
            plt.text(x=row['proportion'] + 1.25,
                     y=index,
                     s=f"{row['proportion']:.1f}%",
                     ha='center')

        # Se rota 45 los nombres de los climas y se ponen las etiquetas
        # en el Eje X y en el Eje Y
        plt.yticks(rotation=45)
        plt.xlabel("Porcentaje", labelpad=25)
        plt.ylabel("Clima", labelpad=15)

        # Se muestra el gráfico de seaborn en Streamlit
        st.pyplot(figure, use_container_width=True)

        # Se crea espacio
        st.text("")
        st.text("")

        # 5. Precipitaciones Totales
        st.markdown("<h4 style='text-align: center; color: black;'> Precipita"
                    "ciones </h4>", unsafe_allow_html=True)

        st.markdown("La siguiente visualización representa la precipitación "
                    "acumulada en las provincias de España donde se "
                    "registraron precipitaciones. En el eje X se muestran las"
                    " provincias ordenadas según sus precipitaciones "
                    "individuales, mientras que el eje Y representa la "
                    "cantidad acumulada de precipitación en milímetros/hora. "
                    "\n\nEl área sombreada bajo la curva ayuda a visualizar "
                    "la tendencia de acumulación. Además, sobre cada punto "
                    "se anota la precipitación individual de la "
                    "provincia correspondiente, lo que permite identificar "
                    "la cantidad de lluvias en cada provincia.")

        # Se crea un nuevo dataframe filtrando las provincias con
        # precipitaciones, ordenándolas ascendentemente
        df_precipitaciones = (
            data.loc[data['Precipitaciones'] > 0]
            .sort_values(by='Precipitaciones')
        )

        # Si se encuentran provincias con precipitaciones...
        if len(df_precipitaciones) > 0:

            # Se crea una figura con matplotlib
            figure = plt.figure(figsize=(14, 6))

            # A este nuevo dataframe, se le crea una columna 'Acumulado' que
            # va sumando acumulativamente las precipitaciones de cada
            # provincia
            df_precipitaciones["Acumulado"] = (
                df_precipitaciones["Precipitaciones"].cumsum()
            )

            # Se dibuja un gráfico de lineas de las provincias con lluvias
            # mostrando la lluvia acumulativa total
            sns.lineplot(data=df_precipitaciones,
                         x="Nombre",
                         y='Acumulado',
                         marker="o")

            # Se rellena el área debajo del gráfico de línea con una
            # transparencia de 0.2
            plt.fill_between(x=df_precipitaciones["Nombre"],
                             y1=df_precipitaciones["Acumulado"],
                             alpha=0.2)

            # Para cada índice y fila de 'df_precipitaciones'...
            for index, row in df_precipitaciones.iterrows():

                # Se escribe en texto la precipitación que hay en cada
                # provincia indicando la posición del texto en el Eje X e Y
                plt.text(x=row['Nombre'],
                         y=row["Acumulado"] + 0.05,
                         s=f"{row['Precipitaciones']}",
                         ha='center')

            # Etiquetas en los Ejes y rotación de 'ticks' en el Eje X
            plt.ylabel("Precipitación Acumulada (mm/h)", labelpad=15)
            plt.xlabel("Provincia", labelpad=15)
            plt.xticks(rotation=45)

        # Si no se encuentran provincias con precipitaciones...
        else:

            # Se crea un gráfico
            figure, ax = plt.subplots(figsize=(8, 4))

            # Se añade un texto para indicar que no hay datos de
            # precipitaciones (alineado en el centro horizontal y
            # verticalmente)
            ax.text(x=0.5, y=0.5, s="Sin datos de precipitaciones",
                    fontsize=14, ha="center", va="center")

            # Se eliminan los 'ticks' del Eje X y Eje Y, además del rectángulo
            # del gráfico
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(False)

        # Se muestra el gráfico en Streamlit
        st.pyplot(figure, use_container_width=True)

        # Se crea espacio
        st.text("")
        st.text("")

        # 6. Velocidad del Viento
        st.markdown("<h4 style='text-align: center; color: black;'> Velocidad"
                    " del Viento </h4>", unsafe_allow_html=True)

        st.markdown("Este histograma representa la distribución de la "
                    "velocidad del viento. Cada barra del gráfico indica "
                    "la frecuencia de velocidades que se encuentran dentro "
                    "de un intervalo específico. El Eje X muestra los "
                    "intervalos de velocidad, mientras que el Eje Y "
                    "representa el número de veces que esas velocidades "
                    "son registradas.")

        # Se crea una figura con matplotlib
        figure = plt.figure(figsize=(14, 6))

        # Se dibuja el diagrama de barras con los nombres de las provincias
        # en el Eje X y los porcentajes en el Eje Y, coloreando las barras
        # cada vez más azules según haya más humedad
        sns.histplot(
            data=data.sort_values(by='Nombre'),
            x='Velocidad_Viento',
            bins=7,
        )

        # Se rota 90º los nombres de las provincias y se ponen las etiquetas
        # en el Eje X y en el Eje Y
        plt.xticks(rotation=90)
        plt.xlabel("Velocidad del Viento (m/s)", labelpad=12)
        plt.ylabel("Frecuencia", labelpad=12)

        # Se muestra el gráfico de seaborn en Streamlit
        st.pyplot(figure, use_container_width=True)

        # Se crea espacio
        st.text("")
        st.text("")

        # 7. Correlación entre Variables
        st.markdown("<h4 style='text-align: center; color: black;'> Matriz "
                    "de Correlación </h4>", unsafe_allow_html=True)

        st.markdown("Por útimo, se muestra un gráfico que representa la "
                    "correlación entre las distintas variables numéricas.")

        # Se calcula la correlación entre todas las columnas numéricas del
        # dataframe 'data' que tienen algún dato válido (no cero)
        columns_with_data = [col for col in columns_float if
                             (data[col] != 0).sum() > 0]
        corr = data[columns_with_data].corr()

        # Se crea una figura con matplotlib
        fig = plt.figure(figsize=(10, 8))

        # Se dibuja un mapa de calor con las correlaciones calculadas
        sns.heatmap(corr, annot=True, cmap='coolwarm', cbar=True,
                    vmin=-1.0, vmax=1.0)

        # Se rotan 45 grados los 'ticks'
        plt.xticks(rotation=45)

        # Se muestra la figura en Streamlit
        st.pyplot(fig)
