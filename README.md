# Cервис , который будет решать задачу, связанную с визуализацией данных и взаимодействием с базой данных

Небольшой сервис на Python, который будет решать задачу, связанную с визуализацией данных и взаимодействием с базой данных
Для удобства работы с проектом развернут Swagger

## Установка

1. Клонируйте репозиторий:
```
git clone git@github.com:valentine9304/superset.git
```
2. Запускаем PostgresSQL
3. Создайте .env файл по типу env_example
4. Устанавливаем виртуальное окружение, активируем его
```
  python -m venv venv 
  source venv/Scripts/activate  ( WINDOWS)
  . venv/bin/activate (LINUX)
```
5. Устаналиваем зависимоти pip install -r requirements.txt
6. Делаем миграцию и записываем рандомные данные в базу
```
alembic revision --autogenerate -m "create tables"
alembic upgrade head
python migrate_data.py
```
7. Запускаем Flask локально
```
flask run --port=8000
```
8. Заходим по адресу [http://localhost:8000](http://localhost:8000)

Либо запускаем через Docker:

2. Заходим в директорию с проектом
3. Разверните приложение через docker
```
docker-compose up --build
```
4. Заходим по адресу [http://localhost:8000](http://localhost:8000)


## Автор
:trollface: Валентин :sunglasses:  
