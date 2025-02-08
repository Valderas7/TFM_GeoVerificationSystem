# Librerías
import pycountry
import re

# Diccionario de mapeo para valores de provincias
mapeo_name = {
    'Alacant': 'Alicante',
    'A Coruña': 'La Coruña',
    'Araba': 'Álava',
    'Illes Balears': 'Islas Baleares',
    'Bizkaia': 'Vizcaya',
    'Castelló': 'Castellón',
    'Girona': 'Gerona',
    'Gipuzkoa': 'Guipúzcoa',
    'Lleida': 'Lérida',
    'Nafarroa': 'Navarra',
    'Ourense': 'Orense',
    }


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
        re.sub(pattern=r'\[[^\]]*\]', repl='', string=name)
        .replace("*", "").strip()
        for name in spain_provinces_and_cities_names
    ]

    # Se devuelve la lista con los nombres de las provincias y ciudades ya
    # filtrados para escribirlos directamente en la API REST
    return spain_provinces_and_cities_names


# Función para transformar los valores de las provincias de la lista retornada
# por la función 'get_provinces_and_autonomous_cities'
def translate_province_list(province_list: list) -> list:

    # Se crea una nueva lista iterando sobre cada provincia de la lista
    # 'province_list' y comprobando si existe esta clave en 'mapeo_name', en
    # cuyo caso se obtiene el nuevo valor. Si no existe la clave, se mantiene
    # el valor original de la provincia
    provincias_actualizadas = [mapeo_name.get(provincia, provincia)
                               for provincia in province_list]

    # Se devuelve la lista actualizada con los valores correctos de provincias
    return provincias_actualizadas
