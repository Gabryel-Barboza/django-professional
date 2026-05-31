# ──────────────────────────────────────────────────────────────────────
# DOCKERFILE — Construção da Imagem Django
# ──────────────────────────────────────────────────────────────────────
# A imagem é uma "receita" com tudo que a aplicação precisa pra rodar:
# SO base + dependências de sistema + pacotes Python + código fonte.
#
# CONCEITOS-CHAVE:
#   FROM        →  imagem base (Python 3.12 slim = ~120MB, sem pacotes desnecessários)
#   RUN         →  executa comandos durante o build (instalar pacotes .deb)
#   WORKDIR     →  diretório de trabalho dentro do container
#   COPY        →  copia arquivos do host para a imagem
#   Cache       →  cada instrução vira uma camada; se não mudou, reusa do cache
#   Estratégia  →  o que muda com mais frequência vai pra última camada
#
# ORDEM DE CAMADAS (da mais estável → mais volátil):
#   1. FROM           (só muda se trocar versão do Python)
#   2. RUN apt-get    (só muda se adicionar/remover pacotes)
#   3. COPY req.txt   (muda quando adiciona/remove dependências)
#   4. RUN pip install (só roda se requirements.txt mudou)
#   5. COPY . .       (muda a cada alteração no código)
# ──────────────────────────────────────────────────────────────────────

FROM python:3.12-slim-bookworm

# Pacotes de sistema para compilar o mysqlclient (driver nativo MySQL).
#   pkg-config                → localiza bibliotecas instaladas
#   build-essential           → compilador C (gcc, make, etc.)
#   default-libmysqlclient-dev → headers e libs do MySQL
# O rm -rf no final limpa o cache do apt — prática essencial para
# manter a imagem enxuta (cada MB importa em produção).
RUN apt-get update && apt-get install -y pkg-config build-essential default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /web

# COPY com cache: copiar requirements.txt ANTES do código permite que
# o Docker reutilize a camada do pip install se as dependências não mudaram.
# Isso acelera drasticamente o build em desenvolvimento.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Só agora copia o código (última camada = a que mais muda).
# O .dockerignore define o que NÃO entra na imagem.
COPY . .

# O CMD foi movido para start.sh para permitir múltiplos comandos (migrate + runserver).
# Em produção, troque runserver por Gunicorn/uWSGI + nginx.
