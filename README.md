# 💬 Async Chat API

Это асинхронный чат-сервис, реализованный на FastAPI. Поддерживает:

- WebSocket-соединения
- Групповые и личные чаты
- Хранение истории сообщений
- JWT-аутентификацию
- Отправку email-уведомлений
- Асинхронную работу с базой данных PostgreSQL
- Покрытие тестами (pytest + httpx)

---

## 🚀 Стек технологий

- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy (Async)**
- **PostgreSQL**
- **Alembic**
- **Pydantic v2**
- **JWT (OAuth2)**
- **Email (SMTP)**
- **WebSockets**
- **pytest + httpx**
- **Docker (опционально)**

---

## 📦 Установка

1. **Клонируй репозиторий:**

```bash
git clone https://github.com/your-username/chat-api.git
cd chat-api
```
Создай .env файл (см env-example)

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=chat_db
DB_HOST=localhost

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30

SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_email_password

## 🖥️ Запуск проекта
Запусти проект используя команду make up 

## 🗄️ Миграции
Для работы проекта необходимо применить миграции используя команду make migrate

## Заполнение тестовыми данными

Для заполнения тестовыми данными используй команду make init_data

## Команды
Подробнее о командах можно посмотреть в Makefile

## API

Swagger работает по ссылке /docs

## WS 
Для подключения к WS
ws://localhost:8000/ws/chat/{chat_id}

## 🧑‍💻 Автор

Разработчик: [Семён Шикота]
Telegram: [@toylep]
Email: [toylenium@mail.ru]