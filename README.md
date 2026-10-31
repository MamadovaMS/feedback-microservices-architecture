# Feedback Microservices Architecture 🚀

Этот репозиторий комплексный проект микросервисной архитектуры для обработки заявок с формы обратной связи. Проект демонстрирует взаимодействие сервисов, написанных на разных языках программирования (**C#**, **Java**, **Python**), с использованием различных протоколов связи (**REST**, **gRPC**), брокера сообщений (**RabbitMQ**) и контейнеризации (**Docker**).

## 🏗 Архитектура проекта

Система построена по принципам **Event-Driven Architecture** (событийно-ориентированной архитектуры) и полиглотного программирования.

1. **Клиент (Telegram Bot)** собирает данные от пользователя и отправляет их по REST API.
2. **Feedback API (C#)** принимает заявку, валидирует её, сохраняет в базу данных (SQLite) и через **gRPC** отправляет уведомление.
3. **Альтернативный API (Java Spring Boot)** принимает заявку и публикует событие в очередь **RabbitMQ**.
4. **Сервис уведомлений (C#)** читает сообщения из RabbitMQ (выступая как Consumer) и логирует/обрабатывает их.

## 📦 Сервисы в репозитории

### 1. `05-feedback-api-dotnet` (C# / ASP.NET Core Web API)
*   **Роль:** Основной REST API для приема заявок.
*   **Технологии:** ASP.NET Core, Entity Framework Core (Code First), SQLite, Swagger/OpenAPI.
*   **Особенности:** Валидация входных данных через Data Annotations, интеграция gRPC-клиента, документация API через Swagger UI.
*   **Docker:** Упакован в контейнер, автоматически применяет миграции БД при старте.

### 2. `06-notifier-grpc-dotnet` (C# / gRPC)
*   **Роль:** Микросервис для отправки уведомлений.
*   **Технологии:** ASP.NET Core gRPC, Protocol Buffers (.proto), RabbitMQ.Client.
*   **Особенности:** Выступает в роли **gRPC-сервера** для синхронных вызовов и в роли **Consumer** для чтения сообщений из очереди RabbitMQ.

### 3. `07-feedback-api-java` (Java / Spring Boot)
*   **Роль:** Альтернативный REST API, демонстрирующий работу с очередями.
*   **Технологии:** Java 21, Spring Boot, Spring AMQP, Maven.
*   **Особенности:** Публикует события в очередь `feedback.notify` в формате JSON при получении заявки. Использует паттерн "Издатель-Подписчик" (Pub/Sub).

### 4. `08-chatbot-python` (Python / Telegram Bot)
*   **Роль:** Клиентское приложение (альтернативный интерфейс).
*   **Технологии:** Python 3.11, `python-telegram-bot`, `requests`.
*   **Особенности:** 
  *   Реализован **FSM** (Конечный автомат) для ведения пошагового диалога (Имя -> Email -> Тема -> Сообщение).
  *   Интеграция с REST API через `requests.post()`.
  *   Логирование диалогов в файл.
  *   Саркастичный и дружелюбный интерфейс с Inline-кнопками.

## 🛠 Стек технологий

*   **Backend:** C#, ASP.NET Core, Java 21, Spring Boot, Python
*   **Протоколы связи:** REST API, gRPC (Protocol Buffers)
*   **Базы данных:** SQLite, Entity Framework Core
*   **Брокер сообщений:** RabbitMQ (RabbitMQ Management)
*   **Контейнеризация:** Docker, Docker Compose
*   **Документация:** Swagger / OpenAPI
*   **Инструменты:** Git, Maven, Postman/Swagger, VS Code, 

## 🚀 Запуск проекта

### 1. Запуск через Docker (Рекомендуется)
Для запуска всей инфраструктуры (C# API, gRPC, Java API, RabbitMQ) в корне проекта выполните:
```bash    Swagger C# API: http://localhost:5283/swagger

Панель RabbitMQ: http://localhost:15672 (guest / guest)

2. Запуск Telegram-бота
Для работы бота требуется, чтобы C# API (05-feedback-api-dotnet) работал на порту 5283.

Перейдите в папку бота: cd 08-chatbot-python

Установите зависимости: pip install -r requirements.txt (если файла нет, установите вручную: pip install python-telegram-bot requests).

Запустите: python bot.py

Найдите бота в Telegram и напишите /start.



Чистая архитектура: Разделение на контроллеры, модели, сервисы и DTO.
docker-compose up --build
