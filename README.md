# Chat API Service

Это RESTful API для управления чатами и сообщениями, реализованный в соответствии с предоставленным заданием.

## Функционал

API предоставляет следующие возможности:
*   **Создание чатов**: POST `/v1/chats/`
*   **Отправка сообщений**: POST `/v1/chats/{id}/messages/`
*   **Получение чатов с сообщениями**: GET `/v1/chats/{id}` 
*   **Удаление чатов**: DELETE `/v1/chats/{id}` 

## Технологии

*   **FastAPI**: Современный, быстрый веб-фреймворк для создания API.
*   **Pydantic**: Используется для валидации данных, сериализации и десериализации.
*   **SQLAlchemy**: Мощная ORM для работы с базой данных.
*   **PostgreSQL**: Реляционная база данных.
*   **Alembic**: Инструмент для миграций базы данных.
*   **Docker & Docker Compose**: Для контейнеризации приложения и базы данных, обеспечения воспроизводимого окружения.
*   **pytest**: Фреймворк для тестирования API.

## Структура проекта

chat_api_service/ # Корневая директория проекта 
├── .venv/ # Виртуальное окружение
├── alembic/ # Каталог для миграций Alembic
│ ├── versions/ # Файлы миграций
│ └── env.py # Конфигурация запуска миграций
├── api_service/ # Основной пакет приложения FastAPI
│ ├── api/ # API роуты
│ │ └── v1/
│ │ └── endpoints/ # Обработчики API запросов
│ │ └── chats.py
│ │ └── init.py
│ ├── core/ # Базовые конфигурации и утилиты
│ │ ├── config.py # Настройки приложения
│ │ └── database.py # Настройка БД и сессии
│ ├── crud/ # CRUD операции (взаимодействие с БД)
│ │ ├── chats.py
│ │ ├── messages.py
│ │ └── init.py
│ ├── models/ # Определения моделей SQLAlchemy
│ │ ├── chat.py
│ │ ├── message.py
│ │ └── init.py
│ ├── schemas/ # Pydantic модели для запросов и ответов
│ │ ├── chat.py
│ │ ├── message.py
│ │ └── init.py
│ └── main.py # Точка входа FastAPI приложения
│ └── init.py
├── tests/ # Каталог для тестов
│ ├── conftest.py # Фикстуры для тестовой среды
│ └── test_chats.py # Тесты для API чатов и сообщений
├── .env.example # Пример файла переменных окружения
├── .dockerignore # Файлы, игнорируемые Docker при сборке
├── alembic.ini # Конфигурация Alembic
├── docker-compose.yml # Конфигурация Docker Compose
├── Dockerfile # Инструкции для сборки Docker образа
├── requirements.txt # Зависимости Python
└── README.md # Данный файл


## Инструкция по запуску

### 1. Установка Docker

Убедитесь, что у вас установлен Docker Desktop (или Docker Engine и Docker Compose) на вашей операционной системе.

### 2. Клонирование репозитория

```bash
git clone https://github.com/yaroslav-grishanov98/API_project_chat
cd chat_api_service 
```

### 3. Настройка переменных окружения

cp .env.example .env # Для Linux/macOS
copy .env.example .env # Для Windows

### 4. Запуск приложения через Docker Compose

docker compose up --build

### 5. Доступ к API

После успешного запуска, API будет доступно по адресу:

Основной URL: http://localhost:8000
Документация Swagger UI: http://localhost:8000/docs
Документация ReDoc: http://localhost:8000/redoc

### 6. Остановка приложения

docker compose down

## Запуск тестов

### 1. Активируйте виртуальное окружение

source .venv/bin/activate # Для Linux/macOS
.venv\Scripts\activate.bat # Для Windows

### 2. Установите зависимости

pip install -r requirements.txt

### 3. Запустите тесты

pytest
