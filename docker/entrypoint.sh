#!/bin/sh
set -e

# Coleta os arquivos estáticos para o STATIC_ROOT (/app/static), idempotente.
echo "==> collectstatic"
python manage.py collectstatic --noinput --clear

# Aplica as migrations (controlado por AUTO_MIGRATE; padrão: true).
# Em cenários com múltiplas réplicas, defina AUTO_MIGRATE=false e rode
# 'manage.py migrate' uma única vez num job separado.
if [ "${AUTO_MIGRATE:-true}" = "true" ]; then
  echo "==> migrate"
  python manage.py migrate --noinput
fi

# Entrega o controle para o CMD (gunicorn).
exec "$@"
