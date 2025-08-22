# Task Manager API

RESTful API для управления задачами с использованием FastAPI, PostgreSQL, Docker и pytest.

## Функционал

- **CRUD операции** для задач:
  - `POST /tasks/` — создать задачу
  - `GET /tasks/{uuid}` — получить задачу
  - `GET /tasks/` — список задач
  - `PUT /tasks/{uuid}` — обновить задачу
  - `DELETE /tasks/{uuid}` — удалить задачу
- Поддержка статусов: `created`, `in_progress`, `completed`
- Автоматическая документация через **Swagger UI**
- Полное покрытие тестами

## Запуск проекта

### Вариант 1: Через Docker 

```bash
docker-compose up --build
```
### Вариант 2: Локально ( с виртуальным окружением )

```bash
# 1. Создать виртуальное окружение
python -m venv venv

# 2. Активировать (Windows)
venv\Scripts\activate.bat

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить сервер
uvicorn app.main:app --reload

```


##  Структура проекта

\`\`\`
task_manager/
├── app/
│   ├── crud.py       # CRUD логика
│   ├── database.py   # Подключение к БД 
|   ├── main.py       # FastAPI приложение
│   ├── models.py     # SQLAlchemy модели 
│   ├── schemas.py    # Pydantic схемы
│   └── database.py   # Подключение к БД
├── tests/
│   └── test_tasks.py # Тесты с pytest
├── .gitignore        # Исключение venv, __pycache__ и т.д.
├── requirements.txt  # Зависимости
├── pyproject.toml    # Настройки black, isort
├── Dockerfile
├── docker-compose.yml
└── README.md         # Этот файл
\`\`\`


