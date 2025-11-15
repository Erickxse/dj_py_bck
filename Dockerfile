# ===== build =====
FROM python:3.12-slim AS build
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Paquetes de build para wheels que lo necesiten (cffi/cryptography/pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev libjpeg62-turbo-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

# ===== runtime =====
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Libs runtime necesarias para Pillow y cffi
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo zlib1g libffi8 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /wheels /wheels
RUN pip install --no-index --find-links=/wheels /wheels/*

COPY . .
# Expón y arranca con gunicorn
ENV PORT=8000
EXPOSE 8000
CMD bash -lc "python manage.py migrate && \
              python manage.py collectstatic --noinput && \
              gunicorn artex_api.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --timeout 90"
