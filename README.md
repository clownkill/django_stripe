# Тестовое задание 
 
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)

Тестовое задание.

Django сервис для взаимодействия с API [stripe.com](https://stripe.com)


### Требования

Для запуска проекта необходимо:
- Docker
- Docker Compose

## Переменные окружения

### Переменные django-сервиса

Определите переменные окружения в файле `.env` в формате: `ПЕРЕМЕННАЯ=значение`:
- `DEBUG` — дебаг-режим. Поставьте `True` для включения, `False` — для 
выключения отладочного режима. По умолчанию дебаг-режим отключен.
- `SECRET_KEY` — секретный ключ проекта, например: `fwei3$@K!fjslfji;erfkdsewyiwerlfskfhfjdslfsf3`
- `ALLOWED_HOSTS` — список разрешенных хостов.
- `SQL_ENGINE` - django engine базы данных 
- `SQL_DATABASE` - имя базы данных
- `SQL_USER` - имя пользователся базы данных
- `SQL_PASSWORD` - пароль пользователя базы данных
- `SQL_HOST` - хост базы данных (имя сервиса БД в docker-compose)
- `SQL_PORT` - порт базы данных
- `DATABASE` - тип базы данных (postgres - для проверки состояния БД при запуске)
- `STRIPE_PUBLISHABLE_KEY` - публичный ключ API [stripe.com](https://stripe.com)
- `STRIPE_SECRET_KEY` - секретный ключ API [stripe.com](https://stripe.com)

### Переменные базы данных

- `POSTGRES_USER` - имя пользователя
- `POSTGRES_PASSWORD` - пароль пользователя
- `POSTGRES_DB` - имя базы данных

## Установка и запуск на локальном сервере

- Скачайте код из репозитория
- Соберите проект с помощью Docker Compose:
```shell
docker-compose build
```
- Запустите проект с помощью Docker Compose:
```shell
  docker-compose up
```
- Создайте файл `.env` в корневой папке и пропишите необходимые переменные 
окружения в формате: `ПЕРЕМЕННАЯ=значение`


- Выполните миграцию БД:
```commandline
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
- Соберите статику:
```shell
docker-compose exec web python manage.py collectstatic
```

### Панель администратора

Панель администратора сайта доступна по адресу `sitename/admin/`. Для
создания учетной записи администратора используйте команду:
```commandline
docker-compose exec web python manage.py createsuperuser
```
