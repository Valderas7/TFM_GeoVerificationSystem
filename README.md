# TFM CIDaeN

En este repositorio se recopila todo el código desarrollado para el Trabajo Final de Máster del Máster de Ciencia de Datos e Ingeniería de Datos en la Nube.


## Estructura

- **.github**: Directorio donde se recopilan los `YAML` que se encargan de definir los flujos de `CI/CD` de `Github Actions`. En el proceso de integración continua se realiza `linting` del código de `Python` y en el proceso de despliegue continuo se ejecuta el aprovisionamiento de la infraestructura de `AWS` mediante `Terraform`.


- **img**: Carpeta para recopilar imágenes.


- **infra**: En esta carpeta se recopilan todos los archivos de configuración de `Terraform` desarrollados con `HCL` y estructurados en módulos y los recursos como `layers` y códigos de las `Lambda` en `.zip`.


- **src**: Directorio donde se almacenan los códigos de `Python` desarrollados para las funciones `Lambda` así como para la aplicación web de `Streamlit`.


- **test**: Carpeta donde se almacenan los tests unitarios creados de las funciones de `Python`.