# Projeto Django com Docker 🐳

Guia passo a passo para configurar, subir e executar um projeto Django do zero utilizando containers Docker no seu ambiente de desenvolvimento.

---

## 🛠️ Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas no seu computador:

* **Docker Desktop** (com suporte ao comando moderno `docker compose`)
* **Git**
* Um editor de código (como o **VS Code**)

---

## 📁 Estrutura do Projeto

Na raiz do seu projeto, você precisará de apenas três arquivos principais de configuração antes de iniciar o Django:

1. **`requirements.txt`** - Gerenciador de dependências do Python.
2. **`Dockerfile`** - A receita para construir a imagem do container.
3. **`docker-compose.yml`** - O orquestrador para subir os serviços.

---

## 🚀 Passo a Passo de Instalação

### 1. Criar e clonar a estrutura de pastas

Abra o seu terminal e execute:

```bash
mkdir Projects
cd Projects
mkdir myapp
cd myapp
git init

```

### 2. Criar os arquivos de configuração

Crie os arquivos abaixo na raiz da pasta `myapp`:

* **`requirements.txt`**

```text
django

```

* **`Dockerfile`**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

```

* **`docker-compose.yml`**

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

---

## ⚙️ Inicializando o Projeto Django

Como o ambiente roda dentro do Docker, vamos criar a estrutura base do Django usando um comando temporário:

```bash
docker compose run --rm web django-admin startproject config .

```

*Isso criará a pasta de configurações (`config/`) e o arquivo executável `manage.py` direto na sua pasta local.*

---

## ▶️ Rodando o Projeto

Para colocar a aplicação no ar, execute:

```bash
docker compose up

```

### 🌐 Acessando a aplicação

Abra o seu navegador e acesse:
👉 [http://localhost:8000](http://localhost:8000)

Você deverá ver a página oficial de boas-vindas do Django!

---

## 🛑 Comandos Úteis do Dia a Dia

* **Subir em segundo plano (modo detached):**
```bash
docker compose up -d

```


* **Parar os containers:**
```bash
docker compose down

```


* **Ver logs em tempo real:**
```bash
docker compose logs -f

```


* **Executar comandos do Django (como migrações):**
```bash
docker compose run --rm web python manage.py migrate

```