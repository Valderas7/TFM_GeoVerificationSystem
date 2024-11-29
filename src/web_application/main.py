# Librerías
import leafmap.leafmap as leafmap
import streamlit as st
import requests
import ipywidgets as widgets

# Se guarda en una variable la URL de la API Gateway desplegada con AWS
api_gateway_url = 'https://mjb5qk45si.execute-api.us-east-1.amazonaws.com/prod'

# Barra lateral para mostrar las opciones disponibles
st.sidebar.title("Opciones")
action = st.sidebar.radio("Elige una opción:", 
                          options=["Ver mapa general",
                                   "Consultar provincia específica",
                                   "Estadísticas"])

# Si se elige la opción 'Ver mapa general'
if action == "Ver mapa general":

    # Título de la aplicación 
    st.title("Mapa del clima en España")
    
    # Se realiza petición GET a la API Gateway en /clima
    response = requests.get(f"{api_gateway_url}/clima").json()

    # Se entra dentro de la clave 'data' que es donde está la lista con todos
    # los JSON de respuesta
    response_list = response['data']

    # Crear mapa con Leafmap con centro en España y zoom adecuado
    m = leafmap.Map(center=[40.0, -3.0], zoom=6)

    # Para cada diccionario de la lista...        
    for provincia_dict in response_list:
        
        # Se añade un marcador al mapa de Leafmap con los campos de latitud
        # longitud de la provincia
        popup_content=(
            f"Provincia: {provincia_dict['Nombre']}<br>"
            f"Clima: {provincia_dict['Clima']}<br>"
            f"Temperatura: {provincia_dict['Temperatura']} °C<br>"
            f"Humedad: {provincia_dict['Humedad']}%"
        )

        # Crear un widget HTML para el popup
        popup = widgets.HTML(value=popup_content)

        # Añadir el marcador con el popup al mapa
        m.add_marker(
            location=(provincia_dict["Latitud"], provincia_dict["Longitud"]),
            popup=popup
        )
    
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
