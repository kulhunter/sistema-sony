# Usar una imagen oficial de Python ligera
FROM python:3.10-slim

# Instalar ExifTool como administrador absoluto (root) en la máquina virtual
RUN apt-get update && apt-get install -y libimage-exiftool-perl exiftool && rm -rf /var/lib/apt/lists/*

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app
COPY app.py .

# Comando de inicio seguro
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "300", "app:app"]
