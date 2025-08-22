# Сервис укорачивания ссылок Flask URL Shortener

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4+-red.svg)](https://www.sqlalchemy.org/)

Сервис для преобразования длинных URL в короткие и удобные ссылки. Проект предоставляет как веб-интерфейс, так и REST API для интеграции с другими сервисами.

## Возможности

### Основной функционал
- Преобразование длинных URL в короткие ссылки
- Веб-интерфейс для визуальной работы с сервисом
- REST API для программного доступа к функционалу

### Управление ссылками
- Создание и удаление коротких ссылок
- Просмотр статистики переходов по ссылкам
- Редирект с коротких ссылок на оригинальные URL

### Безопасность
- Валидация входящих URL
- Защита от нежелательных ссылок
- Безопасное хранение данных

## Технологический стек

- Python 3.9+ - Основной язык программирования
- Flask - Микрофреймворк для веб-приложений
- SQLAlchemy - ORM для работы с базой данных
- Jinja2 - Система шаблонов для веб-страниц
- Alembic - Управление миграциями базы данных
- SQLite - База данных

## Быстрый старт

### Предварительные требования
- Python 3.9 или новее
- Виртуальное окружение (рекомендуется)

### Установка и настройка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/daniltivodar/flask-url-shortener.git
cd flask-url-shortener
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте окружение:
Создайте файл .env и заполните его:
```bash
FLASK_APP=app
FLASK_DEBUG=0
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///db.sqlite3
```

5. Инициализируйте базу данных:
```bash
flask db upgrade
```

6. Запустите сервис:
```bash
flask run
```

## Документация API

После запуска сервиса документация доступна по адресу:
- API Documentation: http://127.0.0.1:5000/redoc

## Разработчик

**Данил Тиводар**  
[GitHub Профиль](https://github.com/daniltivodar)
