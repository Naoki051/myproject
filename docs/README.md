# Documentação do projeto

Esta pasta reúne a documentação da criação e configuração do projeto até o momento atual.

## Ordem de acompanhamento

1. [first-django-project.md](first-django-project.md)  
   Configuração inicial do ambiente Docker + Django.

2. [creating-app.md](creating-app.md)  
   Criação do app Django, views, templates e URLs.

3. [first-nginx-project.md](first-nginx-project.md)  
   Integração do NGINX como proxy reverso.

4. [first-postgres-project.md](first-postgres-project.md)  
   Configuração da conexão com PostgreSQL.

## Verificações gerais do ambiente

Ao longo do processo, as verificações mais importantes são:

```bash
docker compose up --build
docker compose ps
docker compose logs -f
docker compose exec web python manage.py check
docker compose exec web python manage.py migrate
```

## Resultado esperado até o momento

- Projeto Django inicializado com Docker;
- App criado e integrado ao projeto;
- NGINX configurado como proxy reverso;
- PostgreSQL conectado ao Django via variáveis de ambiente e driver `psycopg2`;
- Aplicação pronta para evoluir com regras de negócio, modelos e templates específicos do projeto.
