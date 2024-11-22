# TFM CIDaeN

En este repositorio se recopila todo el código desarrollado para el Trabajo Final de Máster del Máster de Ciencia de Datos e Ingeniería de Datos en la Nube.


## Estructura

- **.github**: Directorio donde se recopilan los `YAML` que se encargan de definir los flujos de `CI/CD` de `Github Actions`. En el proceso de integración continua se realiza `linting` del código de `Python` y en el proceso de despliegue continuo se ejecuta el aprovisionamiento de la infraestructura de `AWS` mediante `Terraform`.


- **infra**: En esta carpeta se recopilan todos los archivos de configuración de `Terraform` desarrollados con `HCL`.


- **src**: Carpeta donde se almacenan los códigos de `Python` como las funciones `Lambda`.