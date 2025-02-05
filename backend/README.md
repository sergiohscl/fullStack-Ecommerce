# PROJETO API DJANGO E DRF PARA CADASTRO DE CARROS.

## Criar venv e instalar Django e DRF

    python3 -m venv venv
    . venv/bin/activate

    pip install django
    pip install djangorestframework
    pip install flake8
    pip install Pillow
    pip install drf-yasg
    pip install django-filter
    pip install django-rql ( https://django-rql.readthedocs.io/en/latest/getting_started/ )

## Criar e inicializar projeto Django

    django-admin startproject core .
    python manage.py migrate
    python manage.py createsuperuser

## Criar e instalar as dependências no projeto

    pip freeze > requirements.txt
    pip install -r requirements.txt

## Rodar o sistema e acessar o admin

    python manage.pu runserver

## Criar app de carros

    python manage.py startapp cars

## Autenticação por JWT. ( https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html )

    pip install djangorestframework-simplejwt

## CORS permite que seus recursos sejam acessados ​​em outros domínios. ( https://pypi.org/project/django-cors-headers/ )

    pip install django-cors-headers


# Rodando projeto em Docker

## Create Network
docker create network library-network

## Rodar container Postgre na versão 16.3
docker run --name dbproducts -e POSTGRES_PASSWORD=admin13$ -e POSTGRES_USER=postgres -e POSTGRES_DB=dbproducts -p 5433:5432 -d --network library-network postgres:16.3

## Rodar Pgadmin 4
docker run --name pgadmin4 -e PGADMIN_DEFAULT_EMAIL=admin@admin.com -e PGADMIN_DEFAULT_PASSWORD=admin -p 15432:80 -d --network library-network dpage/pgadmin4:8.9

## Buildar a imagem
    docker build -t sergiohscl/ecommerce-image .

## Rodar o container com a imagem da aplicação
    docker run --name backend-django -p 8000:8000 -d --network library-network sergiohscl/ecommerce-image
