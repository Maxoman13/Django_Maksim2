Учебный проект по Django. Каталог карточек для повторения пройденного материала.
Установка и запуск проекта
1. Клонируйте репозиторий:

git clone https://github.com/yourusername/yourproject.git
cd yourproject

2. Создайте и активируйте виртуальное окружение:

python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate

3. Установите зависимости:

pip install -r requirements.txt

4. Скопируйте файл .env.example и переименуйте его в .env:

cp .env.example .env

5. Откройте файл .env и заполните следующие переменные окружения:

SECRET_KEY= Введите секретный ключ Джанго

DATABASE_URL=Введите путь к базе данных

EMAIL_HOST_PASSWORD=Введите пароль от почты

EMAIL_HOST=Введите хост от почты

EMAIL_PORT=Введите порт от почты

EMAIL_HOST_USER=Введите ваш email

DEBUG=Режим Debug

TELEGRAM_BOT_TOKEN=<ваш_токен_бота>

YOUR_PERSONAL_CHAT_ID=<ваш_чат_айди>




6. Примените миграции:

python manage.py migrate

7. Создайте суперпользователя для доступа к админ-панели Django:

python manage.py createsuperuser

8. Запустите сервер разработки:

python manage.py runserver
