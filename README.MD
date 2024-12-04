# Referral System API

Реферальная система с авторизацией по номеру телефона. Реализовано с использованием Django и Django Rest Framework (DRF).

## Функционал API

1. Авторизация:
    - Отправка кода подтверждения.
    - Проверка кода подтверждения.
2. Управление профилем:
    - Получение данных профиля.
    - Активация инвайт-кода.
    - Просмотр списка пользователей, которые ввели ваш инвайт-код.

## Установка и запуск

1) Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/acivate
```

2) Установка зависимостей
```bash
pip install -r requirements.txt
```

3) Создание миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

4) В корне проекта представлен файл Referral System API.postman_collection.json с коллекциями, можете его использовать для тестирования URL