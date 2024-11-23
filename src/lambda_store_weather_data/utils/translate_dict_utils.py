# Función para transformar los valores de la clave 'weather' del diccionario
# obtenido tras consultar la API de OpenWeatherMap
def translate_weather_dict(api_dict: dict) -> dict:

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

    # Se verifica si la clave 'Clima' existe en 'api_dict' y si el valor
    # de dicha clave aparece en el diccionario de mapeo
    if 'Clima' in api_dict and api_dict['Clima'] in mapeo_weather:

        # Se cambia el valor de la clave 'Clima' usando el mapeo
        api_dict['Clima'] = mapeo_weather[api_dict['Clima']]

        # Se devuelve el diccionario con los nuevos valores de 'Clima'
        return api_dict
