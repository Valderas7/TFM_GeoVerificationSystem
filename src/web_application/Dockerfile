# Imagen base de Python 3.11
FROM python:3.11-slim

# Directorio dentro de la imagen en el que se está trabajando
WORKDIR /app

# Se copia el 'main.py' al directorio 'app' de la imagen
COPY main.py ./

# Se copia la carpeta 'utils al directorio 'app/utils' de la imagen
COPY utils/ ./utils/

# Se actualiza el sistema y se instalan las dependencias de la aplicación web
RUN apt-get update && pip install --no-cache-dir leafmap==0.40.1 \
    matplotlib==3.9.2 \
    pandas==2.2.3 \
    pycountry==24.6.1 \
    requests==2.32.3 \
    seaborn==0.13.2 \
    streamlit==1.40.2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Se expone el puerto 80 ya que será en éste donde se servirá la aplicación
EXPOSE 80

# Comprobación de funcionamiento en el localhost de la imagen en el puerto 80
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:80/_stcore/health"]

# Se ejecuta la APP de streamlit con el código copiado en la imagen
# especificando la IP (127.0.0.1) y el puerto (80) donde se servirá
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=80", "--server.address=0.0.0.0"]