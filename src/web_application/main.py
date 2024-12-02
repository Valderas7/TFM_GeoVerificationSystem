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
                st.warning(f"Latitud inválida para {provincia_dict['Nombre']}: {lat}")
                continue

        # Si la longitud es un 'string'...
        if isinstance(lon, str):

            # Intenta ejecutar el bloque de código
            try:

                # Se convierte el valor a un float
                lon = float(lon)

            # Si hay error...
            except ValueError:

                # Se muestra mensaje de 'warning' y se continúa
                st.warning(f"Longitud inválida para {provincia_dict['Nombre']}: {lon}")
                continue
        
        # Si la latitud o la longitud son None...
        if lat is None or lon is None:

            # Se muestra mensaje de 'warning' y se continúa
            st.warning(f"Coordenadas faltantes para {provincia_dict['Nombre']}")
            continue

        # Se crea un contenido 'popup' con el nombre de la provincia,
        # sustituyendo las 'ñ' y las tildes por sus códigos numéricos HTML con
        # la función 'convert_to_html_entities'; además de los demás datos de
        # clima, temperatura, etc.
        popup_content = (
            f"Provincia: {convert_to_html_entities(provincia_dict['Nombre'])}<br>"
            f"Clima: {convert_to_html_entities(provincia_dict['Clima'])}<br>"
            f"Temperatura: {provincia_dict['Temperatura']} &#176;C<br>"
            f"Humedad: {provincia_dict['Humedad']}%"
        )
        
        # Se crea el popup con el contenido y se especifica su ancho máximo
        popup = folium.Popup(popup_content, max_width=400)

        # Añadir el marcador con el icono y el popup al mapa
        m.add_marker(location=([lat, lon]), popup=popup)
    
    # Renderiza el mapa en Streamlit
    m.to_streamlit()

# Si se elige la opción de consultar los datos de una provincia específica...
elif action == "Consultar provincia específica":
    st.title("Consulta el clima de una provincia")
    provincia = st.sidebar.text_input("Nombre de la provincia:")
    if st.sidebar.button("Consultar"):
        response = requests.get(f"{api_gateway_url}/clima/{provincia}")
        if response.status_code == 200:
            data = response.json()
            st.write(f"**Clima en {data['Nombre']}:**")
            st.json(data)
        else:
            st.error("No se encontró la provincia. Intenta de nuevo.")

elif action == "Estadísticas":
    st.title("Estadísticas generales")
    response = requests.get(f"{api_gateway_url}/clima").json()
    temperaturas = [float(p["Temperatura"]) for p in response]
    st.metric("Temperatura promedio", f"{sum(temperaturas) / len(temperaturas):.2f} °C")
