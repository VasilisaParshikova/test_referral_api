# Описание
API для реферальной системы, поддерживающий регистрацию и аутентификацию пользователей через JWT и Oauth 2.0.


### Стек
- Python 3.11
- FastAPI
- PostgreSQL
- Docker

полный список зависимостей указан в файле requirements.txt

# Установка
### Склонировать репозиторий

- `git clone https://github.com/VasilisaParshikova/test_referral_api`

### Настройка окружения

- Регистрация приложения в Google Cloud Console
  - Создайте новый проект или выберите существующий.
  - Перейдите в раздел "OAuth consent screen" (Экран согласия OAuth), выберите тип "External" (Внешний), заполните все необходимые поля, такие как название приложения, поддержка и т.д.
  - В разделе "Credentials" (Учетные данные) выберите "Create Credentials" -> "OAuth 2.0 Client IDs" (Идентификатор клиента OAuth 2.0).
  - Укажите тип приложения "Web application" и добавьте URI перенаправления (корректный URL для случая запуска проекта локально находится в файле env.example)
- Создайте secret key для JWT (команда: openssl rand -hex 32)
- Установить Docker
- Сформируйте файлы переменных окружения, согласно .env.example и .env.compose.example

### Запуск

- docker-compose up -d

### Документация

- После запуска приложения документация к api будет доступна по ссылке {your_domain.com}/docs
