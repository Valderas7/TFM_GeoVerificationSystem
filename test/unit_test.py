# Librerías
import pytest
from src.web_application.utils.html_entities import convert_to_html_entities
from src.web_application.utils.geography_utils import translate_province_list


# Test para la función 'convert_to_html_entities'
def test_convert_to_html_entities():

    # Caso de prueba 1: Texto con tildes y ñ
    input_text = "El niño comió camarón y jalapeños con limón."
    expected_output = "El ni&#241;o comi&#243; camar&#243;n y jalape&#241;os con lim&#243;n."
    assert convert_to_html_entities(input_text) == expected_output

    # Caso de prueba 2: Texto sin caracteres especiales
    input_text = "Hola, ¿cómo estás?"
    expected_output = "Hola, ¿c&#243;mo est&#225;s?"
    assert convert_to_html_entities(input_text) == expected_output

    # Caso de prueba 3: Texto con caracteres especiales en mayúsculas
    input_text = "¡FELIZ AÑO NUEVO!"
    expected_output = "¡FELIZ A&#209;O NUEVO!"
    assert convert_to_html_entities(input_text) == expected_output

    # Caso de prueba 4: Texto vacío
    input_text = ""
    expected_output = ""
    assert convert_to_html_entities(input_text) == expected_output

    # Caso de prueba 5: Texto sin caracteres que deban ser convertidos
    input_text = "Hello, world!"
    expected_output = "Hello, world!"
    assert convert_to_html_entities(input_text) == expected_output


# Test para la función 'translate_province_list'
def test_translate_province_list():

    # Caso de prueba 1: Lista con nombres que necesitan traducción
    input_list = ['Alacant', 'A Coruña', 'Araba']
    expected_output = ['Alicante', 'La Coruña', 'Álava']
    assert translate_province_list(input_list) == expected_output

    # Caso de prueba 2: Lista con nombres que no necesitan traducción
    input_list = ['Madrid', 'Barcelona', 'Sevilla']
    expected_output = ['Madrid', 'Barcelona', 'Sevilla']
    assert translate_province_list(input_list) == expected_output

    # Caso de prueba 3: Lista mixta
    input_list = ['Alacant', 'Madrid', 'A Coruña']
    expected_output = ['Alicante', 'Madrid', 'La Coruña']
    assert translate_province_list(input_list) == expected_output

    # Caso de prueba 4: Lista vacía
    input_list = []
    expected_output = []
    assert translate_province_list(input_list) == expected_output


# Ejecuta las pruebas
if __name__ == '__main__':
    pytest.main()