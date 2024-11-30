# Librerías
import streamlit as st
import requests
import leafmap.foliumap as leafmap

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

    # Título de la Web App con cabecera H2
    st.markdown("<h2 style='text-align: center; color: black;'> Clima actual en España </h2>",
                unsafe_allow_html=True)
    
    # Descripción de lo que realiza la aplicación web
    st.write('''En esta aplicación se realiza una monitorización y una vista actual del clima
             actual de todas las provincias y ciudades autónomas de España.''')

    st.markdown("- La cámara se muestra en tiempo real por la pantalla hasta que se pulsa el botón `Take Photo`, momento en el "
                "que se pasa a procesar el fotograma elegido con el modelo de detección de trofozoítos.")
    st.markdown("- Si se pulsa el botón `Clear Photo` se elimina el fotograma procesado y se vuelve a mostrar por pantalla la "
                "cámara en tiempo real.")

    # Se crea un mapa centrado en Madrid
    m = leafmap.Map(center=(40.4168, -3.7038), zoom=6)

    # Agregar marcadores básicos con coordenadas y descripciones
    m.add_marker(location=(40.4168, -3.7038), popup="Madrid: Capital de España")
    m.add_marker(location=(41.3879, 2.16992), popup="Barcelona: Ciudad cosmopolita")
    m.add_marker(location=(37.3891, -5.9845), popup="Sevilla: Famosa por su cultura y arte")

    # Mostrar el mapa en la app de Streamlit
    m.to_streamlit(height=600)

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
