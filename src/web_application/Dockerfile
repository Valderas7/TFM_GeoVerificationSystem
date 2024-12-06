# Imagen base
FROM python:3.11-slim AS build

# Directorio dentro de la imagen en el que se está trabajando
WORKDIR /app

# Se copia el 'main.py' al directorio 'app' de la imagen
COPY main.py ./

# Se copia la carpeta 'utils al directorio 'app/utils' de la imagen
COPY utils/ ./utils/

# Se actualiza el sistema y se instalan las dependencias de la aplicación web
RUN apt-get update && pip install --no-cache-dir streamlit==1.40.2 \
    requests==2.32.3 \
    leafmap==0.40.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Se expone el puerto 8501 ya que será en éste donde se servirá la aplicación
EXPOSE 8501

# Comprobación de funcionamiento en el localhost de la imagen en el puerto 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Se ejecuta la APP de streamlit con el código copiado en la imagen
# especificando la IP (127.0.0.1) y el puerto (8501) donde se servirá
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]