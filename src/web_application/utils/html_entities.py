# Se define el diccionario para mapear los caracteres de tildes y 'ñ' a sus
# entidades numéricas HTML
html_entities = {
    'á': '&#225;',
    'é': '&#233;',
    'í': '&#237;',
    'ó': '&#243;',
    'ú': '&#250;',
    'ñ': '&#241;',
    'Á': '&#193;',
    'É': '&#201;',
    'Í': '&#205;',
    'Ó': '&#211;',
    'Ú': '&#218;',
    'Ñ': '&#209;',
    '°': '&#176;'
}


# Función para convertir el texto en
def convert_to_html_entities(text):

    # Para cada clave y valor del diccionario 'html_entities'...
    for char, entity in html_entities.items():

        # Se reemplazan los caracteres conflictivos (tildes, 'ñ', etc...) por
        # sus entidades numéricas HTML respectivas
        text = text.replace(char, entity)

    # Se devuelve el texto transformado
    return text
