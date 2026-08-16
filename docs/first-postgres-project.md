# Conexão com PostgreSQL

Esta etapa registra a integração do projeto Django com o PostgreSQL em container.

## Objetivo

Permitir que a aplicação Django utilize um banco relacional persistente, com credenciais separadas em variáveis de ambiente e sem expor segredos no repositório.

## 1. Criar o arquivo de ambiente

Criar a pasta e o arquivo:

```bash
mkdir -p envs
```

Arquivo: `envs/postgres.env`

```env
POSTGRES_DB=meubanco
POSTGRES_USER=meuusuario
POSTGRES_PASSWORD=suasenha
DB_NAME=meubanco
DB_USER=meuusuario
DB_PASSWORD=suasenha
DB_HOST=db
DB_PORT=5432
```

## 2. Proteger as variáveis sensíveis

Adicionar no `.gitignore`:

```text
envs/
```

## 3. Atualizar o docker-compose.yml

```yaml
services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - envs/postgres.env
    ports:
      - "5432:5432"

  web:
    build: .
    volumes:
      - .:/app
    expose:
      - "8000"
    environment:
      - DEBUG=False
      - ALLOWED_HOSTS=localhost,127.0.0.1
      - DB_HOST=db
      - DB_PORT=5432
    env_file:
      - envs/postgres.env
    depends_on:
      - db

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web

volumes:
  postgres_data:
```

## 4. Instalar driver do PostgreSQL

No `requirements.txt`:

```text
django
gunicorn
psycopg2-binary>=2.9
```

## 5. Configurar o banco no Django

No arquivo `config/settings.py`:

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'meubanco'),
        'USER': os.environ.get('DB_USER', 'meuusuario'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'suasenha'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## Verificação

Subir os containers com a nova configuração:

```bash
docker compose up -d --build
```

Testar a comunicação com o PostgreSQL:

```bash
docker compose exec web python manage.py migrate
```

Resultado esperado:

- o container do banco inicia corretamente;
- o Django consegue conectar ao PostgreSQL;
- as migrações do Django são aplicadas sem erro;
- mensagens como `Applying ... OK` aparecem no terminal.

## Confirmação do ambiente

Se a migration executa com sucesso, a aplicação está corretamente integrada com:

- Django;
- NGINX;
- PostgreSQL.

Esse é o estado funcional documentado até o momento.