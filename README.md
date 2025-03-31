# Market.io Backend v.1.0

Backend для маркетплейсу, створений на **FastAPI** з автентифікацією через **JWT** та базою даних **PostgreSQL**.

## Технології

- **FastAPI** – фреймворк для побудови швидких та асинхронних API
- **Pydantic** – валідація та серіалізація даних
- **SQLAlchemy** + **Alembic** – ORM та управління міграціями бази даних
- **FastAPI Users** – система автентифікації з JWT
- **Poetry** – управління залежностями
- **PostgreSQL** – основна база даних
- **Docker Compose** – для запуску сервісів

## Встановлення та запуск

### 1. Клонування репозиторію
```bash
git clone https://github.com/smartware10/market.io.backend.git
cd market.io.backend
```

### 2. Генерація RSA-ключової пари
- Перейдіть у папку ***./src/certs/***
- Згенерувати ключі для підпису та верифікації JWT-токенів

### 3. Встановлення Poetry (якщо не встановлений)
```bash
pip install poetry
```

### 4. Створення віртуального середовища та його активація
```bash
python -m venv .venv
```

####  Активація:
- Для **Linux/MacOS**:
```bash
source .venv/bin/activate
```

- Для **Windows**:
```bash
.venv\Scripts\activate
```

### 5. Встановлення залежностей за допомогою Poetry
- Встановити всі залежності, вказані у файлі *pyproject.toml*:
```bash
poetry install
```

### 6. Файл конфігурації (.env)
Створи *.env*-файл у корені проєкту на основі *.env.template*-файлу.

### 7. Запуск бази даних через Docker Compose
```bash
docker compose up -d
```

### 8. Виконання міграцій
```bash
cd src/
alembic upgrade head
```

### 9. Запуск сервера
```bash
python main.py
```

Сервер буде доступний за адресою:
http://127.0.0.1:8000


## API Документація
Документацію можна переглянути у браузері:

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## Автор
*smartware10*
