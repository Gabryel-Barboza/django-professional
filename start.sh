#!/bin/bash

# ──────────────────────────────────────────────────────────────────────
# ENTRYPOINT — Script de inicialização do container
# ──────────────────────────────────────────────────────────────────────
# Usei um script separado (em vez de CMD direto no Dockerfile) porque
# preciso executar múltiplos comandos sequencialmente.
#
# Por que migrate antes do servidor?
#   Garante que TODAS as tabelas existem antes de atender requisições.
#   Sem isso, o primeiro request pode falhar com "table not found"
#   se o banco foi recriado ou clonado.
#
# runserver 0.0.0.0:8080
#   0.0.0.0  →  escuta em todas as interfaces (obrigatório no container)
#   127.0.0.1 →  só localhost (não receberia conexões de fora do container)
#   8080      →  porta alternativa para não conflitar com outras apps
#
# EM PRODUÇÃO: substitua runserver por:
#   gunicorn core.wsgi:application --bind 0.0.0.0:8080
# ──────────────────────────────────────────────────────────────────────

python manage.py migrate
python manage.py runserver 0.0.0.0:8080
