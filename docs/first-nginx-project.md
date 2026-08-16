# Integração com NGINX como proxy reverso

A aplicação Django já estava funcionando em container. Agora a próxima etapa é colocar o NGINX na frente da aplicação para receber as requisições HTTP e encaminhar para o serviço Django.

## Objetivo

- reduzir a exposição direta do Django;
- centralizar o acesso pela porta 80;
- preparar o ambiente para produção com melhor organização de tráfego e estáticos.

## 1. Adicionar Gunicorn

Arquivo: `requirements.txt`

```text
django
gunicorn
```

## 2. Ajustar as configurações do Django

No arquivo `config/settings.py`, adicionar:

```python
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Isso permite que o Django aceite requisições vindas do proxy do NGINX.

## 3. Criar a configuração do NGINX

Pasta: `nginx/default.conf`

```nginx
server {
    listen 80;
    server_name localhost;

    location /static/ {
        alias /app/staticfiles/;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 4. Atualizar Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 5. Atualizar docker-compose.yml

```yaml
services:
  web:
    build: .
    volumes:
      - .:/app
    expose:
      - "8000"
    environment:
      - DEBUG=False
      - ALLOWED_HOSTS=localhost,127.0.0.1

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - .:/app
    depends_on:
      - web
```

## Verificação

Subir os serviços novamente:

```bash
docker compose up --build
```

Testar o acesso direto pelo NGINX:

```bash
curl -I http://localhost
```

Ou abrir no navegador:

- http://localhost

Resultado esperado:

- o NGINX responde na porta 80;
- a aplicação continua acessível sem expor diretamente o Django;
- a rota principal funciona via proxy.

## Observações

- O NGINX fica responsável pela entrada na aplicação.
- O Django continua rodando em um container interno, sem ser acessado diretamente no ambiente local.
- No próximo passo, a aplicação será conectada ao PostgreSQL.
