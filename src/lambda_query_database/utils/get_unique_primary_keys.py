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
        re.sub(pattern=r'\[[^\]]*\]', repl='', string=name)
        .replace("*", "").strip()
        for name in spain_provinces_and_cities_names
    ]

    # Se devuelve la lista con los nombres de las provincias y ciudades ya
    # filtrados para escribirlos directamente en la API REST
    return spain_provinces_and_cities_names


# Diccionario de mapeo para valores de provincias
mapeo_name = {
    'Alacant': 'Alicante',
    'A Coruña': 'La Coruña',
    'Almeria': 'Almería',
    'Araba': 'Álava',
    'Illes Balears': 'Islas Baleares',
    'Bizkaia': 'Vizcaya',
    'Caceres': 'Cáceres',
    'Cadiz': 'Cádiz',
    'Castelló': 'Castellón',
    'Cordoba': 'Córdoba',
    'Girona': 'Gerona',
    'Gipuzkoa': 'Guipúzcoa',
    'Jaen': 'Jaén',
    'Leon': 'León',
    'Lleida': 'Lérida',
    'Nafarroa': 'Navarra',
    'Ourense': 'Orense',
    'Principality of Asturias': 'Asturias',
    'Province of Huelva': 'Huelva',
    'Seville': 'Sevilla'
}


# Función para transformar los valores de la lista de provincias de la
# función 'get_provinces_and_autonomous_cities' a los valores que hay
# almacenados en DynamoDB
def translate_province_list(province_list: list) -> list:

    # Se obtiene el valor mapeado de 'mapeo_name' para cada provincia de la
    # lista 'province_list'. Si no existe la provincia en 'mapeo_name', se
    # deja su valor original en la lista
    return [mapeo_name.get(province, province) for province in province_list]
