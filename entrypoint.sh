#!/bin/sh

# Aplica as migrações do banco de dados
poetry run python manage.py migrate

# Coleta os arquivos estáticos
poetry run python manage.py collectstatic --noinput

# Inicia o servidor
exec "$@"
