# Librerías
import pycountry
import re


# Función para obtener los nombres de las provincias y ciudades autónomas
# de España
def get_provinces_and_autonomous_cities() -> list:

    # Se obtienen en una lista los datos de las provincias y ciudades
    # autónomas de España
    spain_provinces_and_cities_data = [
        subdivision for subdivision in pycountry.subdivisions if
        subdivision.country_code == "ES" and
        (
            subdivision.type == "Province" or
            subdivision.type == "Autonomous city in north africa"
        )
    ]

    # Se obtienen solamente los nombres de las provincias y ciudades autónomas
    spain_provinces_and_cities_names = [
        subdivision.name for subdivision in spain_provinces_and_cities_data
    ]

    # Se eliminan los paréntesis y su contenido en cada uno de los nombres,
    # además de los "*"
    spain_provinces_and_cities_names = [
        re.sub(pattern=r'\[[^\]]*\]', repl='', string=name) # r'\[.*?\]'
        .replace("*", "").strip()
        for name in spain_provinces_and_cities_names
    ]

    # Se devuelve la lista con los nombres de las provincias y ciudades ya
    # filtrados para escribirlos directamente en la API REST
    return spain_provinces_and_cities_names
