**Django Project with Docker Compose**

Проект Django с полной инфраструктурой, включая PostgreSQL, Redis, Celery Worker и Celery Beat.

**Запуск проекта**

1. Создание файла .env 
2. Запуск сервисов при помощи команды _"docker-compose up -d --build"_
3. Проверка статуса запущенных контейнеров при помощи команды _"docker-compose ps"_

**Проверка работы сервисов**

* Для проверки работы сервисов запустите django-приложение по адресу: http://localhost:8000. 
* Для проверки подключения к БД запустите в терминале команду: _"docker-compose exec web python manage.py check --database default"_.
* Для проверки работы redis запустите команду: _"docker-compose exec redis redis-cli ping"_ (ответ "PONG")
* Для проверки работы celery запустите команду для вывода логов: _docker-compose logs -f celery-worker_

**Дополнительные команды:**

1) docker-compose down - остановка всех сервисов
2) docker-compose logs -f - просмотр логов