# Сервис укорачивания ссылок Yacut

Сервис укорачивания ссылок Yacut предназначен для уменьшения страшной и большой ссылки в одну маленькую, и очень компактную ссылку. В проекте также есть как API, так и собственная веб-страница. 

### Технологии
- Python
- Flask
- SQLAlchemy
- Jinja2
- Аlembic
- SQLite

## Установка

1. Склонируйте репозиторий.
```bash
git clone https://github.com/daniltivodar/yacut.git
```

2. Создайте и активируйте виртуальное окружение, заполнив его зависимостями из файла **requirements.txt**.
```bash
cd yacut
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

3. Наполнить файл .env следующими командами:
```bash
FLASK_APP=yacut
FLASK_DEBUG=1
SECRET_KEY=MY SECRET KEY
DATABASE_URI=sqlite:///db.sqlite3
```

4. Запустить сервис можно командой:
```bash
flask db init
flask db upgrade
flask run
```

## API documentation
**https://editor.swagger.io/** - сайт для работы с документацией API.

##Создатель
**[Данил Тиводар](https://github.com/daniltivodar)**
