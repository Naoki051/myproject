# Criação do app Django e rotas da aplicação

Este documento consolida a etapa de criação do app principal do projeto, com view, template e configuração de URLs.

## Objetivo

Organizar a aplicação em um app modular dentro da pasta `apps/`, deixando a estrutura pronta para evoluir com templates, modelos e regras de negócio.

## 1. Criar o app

No diretório do projeto, executar:

```bash
docker compose run --rm web python manage.py startapp core apps/core
```

Se necessário, ajustar a estrutura para que o app fique em `apps/core`.

## 2. Registrar o app no Django

No arquivo `config/settings.py`, adicionar em `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core',
]
```

## 3. Criar a view

Arquivo: `apps/core/views.py`

```python
from django.shortcuts import render


def home_view(request):
    context = {
        'titulo': 'Bem-vindo ao projeto'
    }
    return render(request, 'core/home.html', context)
```

## 4. Criar o template

Estrutura:

```text
apps/core/templates/core/home.html
```

Conteúdo:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Home</title>
</head>
<body>
    <h1>{{ titulo }}</h1>
    <p>Esta página foi renderizada por uma view do app core.</p>
</body>
</html>
```

## 5. Configurar URLs do app

Arquivo: `apps/core/urls.py`

```python
from django.urls import path
from .views import home_view

urlpatterns = [
    path('', home_view, name='core-home'),
]
```

## 6. Incluir as URLs do app no projeto principal

Arquivo: `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
]
```

## Verificação

Depois de salvar os arquivos, executar:

```bash
docker compose exec web python manage.py check
```

Se não houver erros, reinicie o container ou suba novamente:

```bash
docker compose up --build
```

Acesse:

- http://localhost:8000
- ou http://localhost quando o NGINX estiver ativo

Resultado esperado: a página com o texto definido na view aparecer na tela.

## Observação

Essa etapa marca a criação do app principal da aplicação e estabelece a base para as próximas integrações.

Próxima etapa: configuração do NGINX como proxy reverso.