# Librerías
import streamlit as st
import requests
import leafmap.foliumap as leafmap
import folium
from utils.html_entities import convert_to_html_entities

# Se guarda en una variable la URL de la API Gateway desplegada con AWS
api_gateway_url = 'https://mjb5qk45si.execute-api.us-east-1.amazonaws.com/prod'

# Barra lateral para mostrar las opciones disponibles
st.sidebar.title("Opciones")
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
                "interactivo muestra datos como el clima, la temperatura y "
                "la humedad, utilizando marcadores informativos para cada "
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
            f"Provincia: {convert_to_html_entities(provincia_dict['Nombre'])}<br>"
            f"Clima: {convert_to_html_entities(provincia_dict['Clima'])}<br>"
            f"Temperatura: {provincia_dict['Temperatura']} &#176;C<br>"
            f"Humedad: {provincia_dict['Humedad']} %<br>"
            f"Nubosidad: {provincia_dict['Nubosidad']} %<br>"
            f"{convert_to_html_entities('Presión Atm')}: {provincia_dict['Presion_Atmosferica']} hPa<br>"
            f"Viento: {provincia_dict['Velocidad_Viento']} m/s<br>"
        )

        # Si las precipitaciones del diccionario son mayores de 0 mm/h...
        if float(provincia_dict['Precipitaciones']) > 0.0:

            # Se agregan las precipitaciones al 'popup'
            popup_content += f"Precipitaciones: {provincia_dict['Precipitaciones']} mm/h<br>"

        # Si las nevadas del diccionario son mayores de 0 mm/h...
        if float(provincia_dict['Nevadas']) > 0.0:

            # Se agregan las nevadas al 'popup'
            popup_content += f"Nevadas: {provincia_dict['Nevadas']} mm/h<br>"
        
        # Se crea un 'popup' con el contenido y se especifica su ancho máximo
        popup = folium.Popup(popup_content, max_width=400)

        # Añadir el marcador en la localización indicada con el 'popup' de la
        # información meteorológica
        m.add_marker(location=([lat, lon]), popup=popup)
    
    # Renderiza el mapa en Streamlit
    m.to_streamlit()

# Si se elige la opción 'Consultar provincia específica'...
if action == "Consultar provincia específica":

    # Título de la aplicación
    st.markdown("<h2 style='text-align: center; color: black;'> Consulta por Provincia </h2>", unsafe_allow_html=True)

    # Se introduce un 'widget' de texto de entrada
    provincia = st.text_input("Introduce el nombre de la provincia:")

    # Cuando se introduce una provincia...
    if provincia:

        # Se hace una solicitud GET a la API Gateway en '/clima/{provincia}'
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
                map_provincia = leafmap.Map(center=(lat, lon), zoom=8)

                # Se crea un 'popup' 
                popup = folium.Popup(f"{provincia.capitalize()}<br>{data}")

                # Se añade el marcador de la provincia al mapa con el 'popup'
                # creado
                map_provincia.add_marker(location=(lat, lon), popup=popup)

                # Se renderiza el mapa de la provincia en Streamlit
                map_provincia.to_streamlit()
            
            # Si la respuesta JSON no existe...
            else:

                # Mensaje de 'warning' en Streamlit
                st.warning("No se encontraron datos para la provincia especificada.")

        # Si la respuesta de la solicitud GET no es satisfactoria...
        else:

            # Mensaje de error en Streamlit
            st.error("Error al obtener los datos. Verifica el nombre de la provincia.")

# Si se elige la opción 'Estadísticas'...
if action == "Estadísticas":

    # Título de la aplicación
    st.markdown("<h2 style='text-align: center; color: black;'> Estadísticas Generales </h2>", unsafe_allow_html=True)

    # Realiza la solicitud GET a /clima
    response = requests.get(f"{api_gateway_url}/clima").json()

    # Si existe la clave 'data' en la respuesta...
    if 'data' in response:

        # Se almacena en 'response_list'
        response_list = response['data']

        # Extraer datos para las estadísticas
        temperaturas = [float(prov['Temperatura']) for prov in response_list]
        humedad = [float(prov['Humedad']) for prov in response_list]
        provincias = [prov['Nombre'] for prov in response_list]

        # Mostrar gráficos
        st.bar_chart({"Provincias": provincias, "Temperatura": temperaturas})
        st.line_chart({"Provincias": provincias, "Humedad": humedad})

        # Mostrar máximos y mínimos
        max_temp = max(response_list, key=lambda x: float(x['Temperatura']))
        min_temp = min(response_list, key=lambda x: float(x['Temperatura']))
        st.write(f"Provincia más cálida: {max_temp['Nombre']} ({max_temp['Temperatura']} °C)")
        st.write(f"Provincia más fría: {min_temp['Nombre']} ({min_temp['Temperatura']} °C)")
    else:
        st.error("No se pudo obtener datos para estadísticas.")

if action == "Descargar datos":
    st.download_button("Descargar datos", data=str(response), file_name="datos_climaticos.csv")

