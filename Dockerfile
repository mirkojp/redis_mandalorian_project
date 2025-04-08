# Imagen base liviana de Python
FROM python:3.11-slim

# Evitar archivos pyc y forzar logs a consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2 y otros
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Copiar requirements e instalar dependencias Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo el contenido del proyecto (incluye manage.py y settings)
COPY . /app/

# Exponer el puerto 8000 (usado por gunicorn)
EXPOSE 8000

# Comando por defecto (si no se sobreescribe en Render)
CMD ["gunicorn", "redis_mandalorian_project.wsgi:application", "--bind", "0.0.0.0:8000"]

