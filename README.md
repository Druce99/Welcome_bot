Welcome_bot

Telegram-бот, который автоматизирует воронку продаж для владельца канала: проверка подписки, лид-магнит, прогрев отложенными сообщениями, оффер и сбор контактов покупателей.

Как это работает

Покупатель:

Нажимает /start, бот проверяет подписку на канал.
Получает приветствие и лид-магнит (файл).
Через заданное время получает прогревающие сообщения (отложенная отправка).
Видит оффер с ценой, нажимает «Хочу купить» и оставляет контакт или связывается с владельцем напрямую.

Владелец:

/setup — пошаговая настройка воронки (канал, приветствие, лид-магнит, прогрев, оффер и цена);
/leads — список заявок;
/stats — статистика воронки.
Стек

Python, aiogram 3, PostgreSQL 16, async SQLAlchemy 2, Alembic, Redis 7, APScheduler, Pydantic Settings, Docker Compose, uv.

Архитектура

Слои: handlers → services → repositories → models. Сессия БД передаётся в хендлеры через middleware.

src/
  handlers/       обработчики команд и кнопок
  services/       бизнес-логика воронки, заявок, статистики
  repositories/   доступ к БД
  models/         модели SQLAlchemy
  schemas/        схемы Pydantic
  states/         состояния диалога (FSM)
  keyboards/      клавиатуры
  middlewares/    сессия БД
  core/           конфиг, БД, планировщик
migrations/       миграции Alembic
Запуск
bash
git clone https://github.com/Druce99/Welcome_bot.git
cd Welcome_bot
cp .env.example .env     # BOT_TOKEN, OWNER_ID и адреса БД
docker compose up --build

Токен бота получите у @BotFather. В .env он хранится локально и в репозиторий не попадает.

Переменные окружения
Переменная	Назначение
BOT_TOKEN	токен бота
OWNER_ID	Telegram ID владельца
DATABASE_URL	подключение к PostgreSQL
REDIS_URL	подключение к Redis
