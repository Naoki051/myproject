# Configuração inicial do projeto Django com Docker

Este documento registra a primeira etapa da criação do projeto: preparar o ambiente Docker, instalar o Django e inicializar a estrutura base do projeto.

## Objetivo

Garantir que o projeto consiga subir em containers e que o Django fique disponível para desenvolvimento local.

## Pré-requisitos

- Docker Desktop instalado
- Docker Compose disponível
- Git e editor de código (VS Code recomendado)

## 1. Estrutura mínima do projeto

Na raiz do projeto, criar os arquivos básicos:

### requirements.txt

```text
django
```

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
```

## 2. Inicialização do projeto Django

Na raiz do projeto, executar:

```bash
docker compose run --rm web django-admin startproject config .
```

Esse comando cria a estrutura base do Django com:

- `manage.py`
- pasta `config/`
- configurações iniciais do projeto

## 3. Subir o projeto

```bash
docker compose up --build
```

A aplicação deve ficar acessível em:

- http://localhost:8000

## Verificação

Abra o navegador e confirme que a página padrão do Django aparece.

Também é possível verificar o estado do container:

```bash
docker compose ps
```

Se o serviço `web` estiver em execução e a página carregar, a configuração inicial do Django foi concluída com sucesso.

## Comandos úteis

```bash
docker compose up -d
docker compose down
docker compose logs -f
docker compose run --rm web python manage.py migrate
```

## Resultado esperado

- Ambiente Docker funcionando;
- Projeto Django criado na pasta raiz;
- Servidor respondendo em localhost:8000.

Este é o ponto de partida para a criação do app, a configuração de URLs e a integração com NGINX e PostgreSQL.