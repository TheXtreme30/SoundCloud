# SoundCloud

Платформа позволяет пользователям загружать, находить, слушать и скачивать музыку.


### Технологии

- Python >= 3.10
- Django Rest Framework
- Docker
- Postgres
- NGINX

## Старт

#### 1) В корне проекта создать .env и прописать свои настройки

    DEBUG
    SECRET_KEY
    DJANGO_ALLOWED_HOSTS

    # Data Base
    POSTGRES_DB
    POSTGRES_ENGINE
    POSTGRES_USER
    POSTGRES_PASSWORD
    POSTGRES_HOST
    POSTGRES_PORT

    # Google client
    GOOGLE_CLIENT_ID
    GOOGLE_SECRET_KEY

#### 2) Создать образ и запустить контейнер

    docker-compose up --build

##### 3) Создать супер-пользователя

    docker exec -it sound_cloud_web bash
    python manage.py createsuperuser
