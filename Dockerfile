FROM python:3.12-slim-bookworm

# Dependências de build e depois limpeza
RUN apt-get update && apt-get install -y pkg-config build-essential default-libmysqlclient-dev  && rm -rf /var/lib/apt/lists/*

WORKDIR /web
# Separar em camadas para acelerar build
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando de entrada do container movido para script start.sh
