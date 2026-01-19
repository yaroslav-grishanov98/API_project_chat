# Шаг 1: Используем более актуальную и единую с локальной средой версию Python
FROM python:3.12-slim-bookworm

# Устанавливаем переменные окружения для более чистого запуска
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Шаг 2: Создаем непривилегированного пользователя, от которого будет работать приложение
RUN adduser --system --group app

COPY --chown=app:app requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

USER app

EXPOSE 8000

CMD ["uvicorn", "api_service.main:create_application", "--host", "0.0.0.0", "--port", "8000", "--factory"]