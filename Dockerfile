# ===== Build Stage =====
FROM python:3.12-slim AS builder

# Instalar dependencias del sistema necesarias para compilar paquetes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ===== Runtime Stage =====
FROM python:3.12-slim

# Instalar solo las dependencias runtime necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para mayor seguridad
RUN useradd -m -u 1000 django && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R django:django /app

WORKDIR /app

# Copiar dependencias Python instaladas desde builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el código de la aplicación
COPY --chown=django:django . .

# Variables de entorno por defecto
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=artex_api.settings \
    PORT=8000

# Cambiar al usuario no-root
USER django

# Exponer puerto
EXPOSE 8000

# Script de entrada para ejecutar migraciones y collectstatic
COPY --chown=django:django <<'EOF' /app/entrypoint.sh
#!/bin/bash
set -e

echo "==> Esperando a que la base de datos esté lista..."
python << END
import sys
import time
import pymysql
import os

max_retries = 30
retry_interval = 2

for i in range(max_retries):
    try:
        conn = pymysql.connect(
            host=os.getenv('DATABASE_HOST', 'db'),
            user=os.getenv('DATABASE_USER', 'root'),
            password=os.getenv('DATABASE_PASSWORD', ''),
            port=int(os.getenv('DATABASE_PORT', 3306)),
            connect_timeout=5
        )
        conn.close()
        print("Base de datos lista!")
        sys.exit(0)
    except Exception as e:
        print(f"Intento {i+1}/{max_retries}: Base de datos no lista - {e}")
        if i < max_retries - 1:
            time.sleep(retry_interval)
        else:
            print("ERROR: No se pudo conectar a la base de datos")
            sys.exit(1)
END

echo "==> Ejecutando migraciones..."
python manage.py migrate --noinput

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "==> Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
EOF

RUN chmod +x /app/entrypoint.sh

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/admin/', timeout=5)" || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
