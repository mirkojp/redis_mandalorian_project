# Imagen base liviana de Python
FROM python:3.11-slim

# Variables para evitar archivos .pyc y loguear automáticamente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Copiar e instalar dependencias Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el proyecto completo y el archivo de entorno
COPY . /app/
COPY .env /app/.env

# Exponer el puerto por defecto de Django
EXPOSE 8000

# Comando por defecto (por si no se sobreescribe en docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
