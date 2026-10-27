# Feedback Microservices Architecture 🚀

Этот репозиторий представляет собой микросервисную архитектуру для обработки заявок с формы обратной связи. Проект демонстрирует взаимодействие сервисов на разных языках программирования (C# и Java) с использованием брокера сообщений и базы данных.

## 🏗 Архитектура и сервисы

1. **`05-feedback-api-dotnet` (C# / ASP.NET Core)**
   - REST API для приема заявок.
   - Валидация данных (Data Annotations).
   - Хранение в базе данных **SQLite** (Entity Framework Core).
   - Swagger UI для документации.
   - Вызов gRPC-сервиса после сохранения заявки.

2. **`06-notifier-grpc-dotnet` (C# / gRPC)**
   - gRPC-сервис для отправки email-уведомлений.
   - Выступает в роли **Consumer** (потребителя) для очереди RabbitMQ.
   - Читает сообщения из очереди `feedback.notify` и логирует их.

3. **`07-feedback-api-java` (Java / Spring Boot)**
   - Альтернативный REST API для приема заявок.
   - Публикует события (JSON) в очередь **RabbitMQ**.
   - Хранит заявки в памяти (для демонстрации Event-Driven подхода).

4. **`rabbitmq` (Docker)**
   - Брокер сообщений для асинхронного обмена данными между Java и C# сервисами.

## 🛠 Стек технологий
- **Backend:** C#, ASP.NET Core, gRPC, Java, Spring Boot
- **Базы данных:** SQLite, Entity Framework Core
- **Брокер сообщений:** RabbitMQ
- **Инфраструктура:** Docker, Docker Compose
- **Документация:** Swagger / OpenAPI

## ⚙️ Как запустить проект целиком

1. Убедитесь, что у вас установлен **Docker Desktop**.
2. В корне проекта выполните команду:
   ```bash
   docker compose up --build