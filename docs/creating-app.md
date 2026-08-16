# 🛠️ Guia Prático: Criando Apps, Views e URLs no Django

Este guia assume que você está utilizando a pasta `apps/` para organizar os componentes do seu projeto.

---

## 🚀 Passo 1: Criando o App

Abra o terminal na raiz do seu projeto (onde está o arquivo `manage.py`) e execute o comando para criar um app (por exemplo, chamaremos de `core`):

```bash
python manage.py startapp core apps/core

```

*(Se o Django criar a pasta `core` diretamente na raiz, basta movê-la para dentro de uma pasta chamada `apps/`).*

---

## ⚙️ Passo 2: Registrando o App no `settings.py`

Para que o Django reconheça o novo app, você precisa adicioná-lo à lista de aplicativos instalados.

Abra o arquivo `config/settings.py` e adicione o caminho do app no `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... apps padrões do Django ...
    'apps.core',
]

```

---

## 💻 Passo 3: Criando a sua View

As views controlam a lógica de resposta da sua aplicação. Vamos criar uma view simples que renderiza uma página de boas-vindas.

Abra o arquivo `apps/core/views.py` e adicione o código:

```python
from django.shortcuts import render

def home_view(request):
    context = {
        'titulo': 'Bem-vindo ao meu projeto com NGINX e Django!'
    }
    return render(request, 'core/home.html', context)

```

---

## 🎨 Passo 4: Criando o Template HTML

Para organizar os arquivos visuais do app, crie uma estrutura de pastas para templates dentro do próprio app: `apps/core/templates/core/`.

Crie o arquivo **`apps/core/templates/core/home.html`**:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Home</title>
</head>
<body>
    <h1>{{ titulo }}</h1>
    <p>Esta página foi renderizada através de uma View no app core!</p>
</body>
</html>

```

---

## 🔗 Passo 5: Configurando as URLs do App

Cada app pode (e deve) ter seu próprio arquivo de rotas para manter o código modular.

1. Crie um arquivo chamado **`urls.py`** dentro de `apps/core/`.
2. Adicione o mapeamento das rotas do app:

```python
from django.urls import path
from .views import home_view

urlpatterns = [
    path('', home_view, name='core-home'),
]

```

---

## 🌐 Passo 6: Conectando o App na `url.py` Principal

Agora você precisa dizer ao projeto principal para escutar as rotas do seu novo app `core`.

Abra o arquivo **`config/urls.py`** e inclua as rotas do app:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Conectando as rotas do app core na raiz do site
    path('', include('apps.core.urls')),
]

```

---

## ▶️ Passo 7: Testando o Resultado

Com tudo configurado, suba o seu ambiente (seja via `docker compose up --build` ou rodando o servidor local) e acesse no navegador:

👉 **`http://localhost`** (ou `http://localhost:8000` caso esteja testando direto no Django).

Você verá a mensagem enviada pela sua nova View renderizada na tela!