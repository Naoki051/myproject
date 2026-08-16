# 🚀 Adicionando o NGINX como Proxy Reverso

Agora que sua aplicação Django está rodando, vamos adicionar o **NGINX**. Ele atuará como um "porteiro" para sua aplicação: receberá o tráfego externo, servirá arquivos estáticos de forma eficiente e repassará as requisições dinâmicas para o Django via **Gunicorn**.

---

## 🛠️ Passo 1: Atualizar dependências e o Django

Primeiro, precisamos de um servidor WSGI robusto (Gunicorn) e configurar o Django para rodar em modo produção.

1. **Atualize o `requirements.txt**`:
Adicione o Gunicorn ao arquivo:
```text
django
gunicorn

```


2. **Ajuste o `settings.py**`:
No seu arquivo `config/settings.py`, altere as configurações de segurança para permitir o proxy:
```python
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Adicione também ao final do arquivo:
STATIC_ROOT = BASE_DIR / 'staticfiles'

```



---

## 📁 Passo 2: Criar a configuração do NGINX

Na raiz do seu projeto `myapp`, crie uma pasta chamada `nginx` e dentro dela um arquivo `default.conf`:

* **`nginx/default.conf`**

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

---

## ⚙️ Passo 3: Atualizar `Dockerfile` e `docker-compose.yml`

Agora, diremos ao Docker para usar o Gunicorn e levantar o NGINX.

* **`Dockerfile`** (Atualizado):

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usando Gunicorn em vez de runserver
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

```

* **`docker-compose.yml`** (Atualizado):

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

---

## ▶️ Rodando o Projeto com NGINX

Como alteramos a estrutura, reconstrua as imagens e suba os serviços:

```bash
docker compose up --build

```

### 🌐 Testando

Agora, o Django não está mais na porta 8000. Acesse diretamente pela porta padrão:
👉 [http://localhost](http://localhost)
