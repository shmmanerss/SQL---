#Университетский проект - Разработка базы данных для сети аптек

Консольное приложение для управления каталогом лекарств по категориям на базе PostgreSQL.

## Возможности

- Управление категориями лекарств (создание, чтение, редактирование, удаление)
- Управление лекарствами внутри каждой категории
- Хранение данных в PostgreSQL
- Автоматическое создание таблиц и заполнение тестовыми данными
- Поддержка кириллицы в Windows-консоли
- Обработка ошибок целостности БД (например, дубликаты)
В учебных целях в config.yaml используются простые учётные данные (myuser / 123). В реальном проекте обязательно замените их!
## Стек

- Python 3.8+
- PostgreSQL
- `psycopg2-binary` — драйвер PostgreSQL
- `PyYAML` — загрузка конфигурации

## Структура проекта
├── config.yaml # Конфигурация подключения к БД
├── dbconn.py # Класс DbConn — подключение к БД
├── dbtable.py # Базовый класс DbTable — CRUD-операции
├── main.py # Точка входа, консольное меню
├── seed_data.sql # SQL-скрипт с начальными данными
├── requirements.txt # Зависимости Python
└── tables/
├── category_table.py # Таблица категорий (drug_categories)
└── drug_table.py # Таблица лекарств (drugs)


## Установка

1. Клонируйте репозиторий и перейдите в каталог проекта:

   git clone <repo_url>
   cd <project_dir>

2. Создайте и активируйте виртуальное окружение в командной строке (рекомендуется):

python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

3. Установите зависимости:
   pip install -r requirements.txt

4. Убедитесь, что PostgreSQL установлен и запущен, и создайте базу данных:
CREATE DATABASE postgres;
CREATE USER myuser WITH PASSWORD '123';
GRANT ALL PRIVILEGES ON DATABASE postgres TO myuser;

6. Отредактируйте config.yaml под свою среду:
   dbname: postgres
   user: myuser
   password: 123
   host: localhost
   dbtableprefix: "public."
   
7. Запустите файл main.py в командной строке, готово! 
