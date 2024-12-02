# Diccionario de mapeo para valores de clima
mapeo_weather = {
    'Ash': 'Ceniza_Volcánica',
    'Clear': 'Despejado',
    'Clouds': 'Nublado',
    'Drizzle': 'Llovizna',
    'Dust': 'Tormenta_Polvo',
    'Fog': 'Niebla',
    'Haze': 'Calima',
    'Mist': 'Neblina',
    'Rain': 'Lluvioso',
    'Sand': 'Tormenta_Arena',
    'Smoke': 'Humareda',
    'Snow': 'Nevado',
    'Squall': 'Turbonada',
    'Thunderstorm': 'Tormenta_Eléctrica'
}

# Diccionario de mapeo para valores de provincias
mapeo_name = {
    'A Coruña': 'La Coruña',
    'Almeria': 'Almería',
    'Araba / Álava': 'Álava',
    'Balearic Islands': 'Islas Baleares',
    'Biscay': 'Vizcaya',
    'Caceres': 'Cáceres',
    'Cadiz': 'Cádiz',
    'Castellon': 'Castellón',
    'Cordoba': 'Córdoba',
    'Girona': 'Gerona',
    'Gipuzkoa': 'Guipúzcoa',
    'Jaen': 'Jaén',
    'Leon': 'León',
    'Lleida': 'Lérida',
    'Navarre': 'Navarra',
    'Ourense': 'Orense',
    'Principality of Asturias': 'Asturias',
    'Province of Huelva': 'Huelva',
    'Seville': 'Sevilla'
}


# Función para transformar los valores de la clave 'Clima' y 'Nombre' del
# diccionario obtenido tras consultar la API de OpenWeatherMap
def translate_weather_dict(api_dict: dict) -> dict:

    # Se verifica si la clave 'Clima' existe en 'api_dict' y si el valor
    # de dicha clave aparece en el diccionario de mapeo
    if 'Clima' in api_dict and api_dict['Clima'] in mapeo_weather:

        # Se cambia el valor de la clave 'Clima' usando el mapeo
        api_dict['Clima'] = mapeo_weather[api_dict['Clima']]

    # Se verifica si la clave 'Nombre' existe en 'api_dict' y si el valor
    # de dicha clave aparece en el diccionario de mapeo
    if 'Nombre' in api_dict and api_dict['Nombre'] in mapeo_name:

        # Se cambia el valor de la clave 'Nombre' usando el mapeo
        api_dict['Nombre'] = mapeo_name[api_dict['Nombre']]

    # Se devuelve el diccionario con los nuevos valores de 'Nombre' y 'Clima'
    return api_dict
