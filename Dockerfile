# syntax=docker/dockerfile:1

##########################################################################
# Stage 1 — builder: instala as dependências numa virtualenv isolada
##########################################################################
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Dependências de compilação (rede de segurança caso algum pacote precise
# ser buildado em vez de usar wheel). Não vão para a imagem final.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Virtualenv que será copiada inteira para o estágio final.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


##########################################################################
# Stage 2 — runtime: imagem enxuta, sem toolchain, rodando como não-root
##########################################################################
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=app.settings

# Usuário e grupo de sistema sem privilégios.
RUN addgroup --system --gid 1001 django \
    && adduser --system --uid 1001 --ingroup django --home /app django

# Copia a virtualenv já pronta do builder (mesma base = glibc compatível).
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

# Diretórios de estáticos/mídia já com dono correto (volumes herdam o dono).
RUN mkdir -p /app/static /app/media \
    && chown -R django:django /app/static /app/media

# Código da aplicação (respeitando o .dockerignore).
COPY --chown=django:django . .

# Entrypoint com terminadores de linha normalizados (evita CRLF do Windows).
RUN sed -i 's/\r$//' /app/docker/entrypoint.sh \
    && chmod +x /app/docker/entrypoint.sh

USER django

EXPOSE 8000

# Healthcheck: considera saudável qualquer resposta HTTP < 500 na raiz.
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request,sys; \
        sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/').status < 500 else 1)" \
        || exit 1

ENTRYPOINT ["/app/docker/entrypoint.sh"]

# gunicorn (WSGI) — workers e timeout ajustáveis conforme a carga.
CMD ["gunicorn", "app.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
