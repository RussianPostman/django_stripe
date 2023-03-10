# django_stripe

Этот проект демонстрирует простую интеграцию платёжного сервиса Stripe в Django проект.

## Структура базы данных
Начинается всё с того, что в админ панели создаётся модель товара (Item). К каждому экземпляру модели можно прикрепить несколько объектов: скидок (Discount) и налогов (Tax). Также можно создать подборку из нескольких товаров (Item) в модели (Order). При совершении покупки в модель (Transaction) записывается информация о совершённой сделки.

## Структура представления
Пользователю доступны две страницы с возможностью покупки: в первом случае - отдельного товара, во втором - подборки. Пользователю достаточно нажать на кнопку покупки, ввести данные карты и электронную почту, привязанную к Stripe аккаунту.
```
http://127.0.0.1/item/view/<int:item_id>/
http://127.0.0.1/order/view/<int:item_id>/
```

После нажатия на кнопку покупки в нутри сервиса происходит оценка стоимости товара с учетом скидок и налогов, создаётся stripe Payment Intent. В случае успешной оплаты, в базе данных создаётся запись об успешной транзакции (Transaction).

# Установка и проверка

## Схема наполнения файла .env проекта django_stripe
Файл необходимо разместить в директории django_stripe/infra/

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=************** # Секретный ключ вашего проекта
STRIPE_PUBLIC_KEY==************** Публичный ключ Stripe (https://dashboard.stripe.com/test/apikeys)
STRIPE_SECRET_KEY==************** секретный ключ Stripe (https://dashboard.stripe.com/test/apikeys)
STRIPE_WEBHOOK_SECRET==************** Stripe (https://stripe.com/docs/webhooks/go-live)
```
Для запуска проекта необходимо клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/RussianPostman/django_stripe.git
cd infra
docker-compose up -d --build
docker-compose exec web python manage.py makemigrations simple_strape
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

Для создания и просмотра данный, перейти в браузере по адресу:
```
http://127.0.0.1/admin
```
Для тестирования процесса покупки:
```
http://127.0.0.1/item/view/<int:item_id>/
http://127.0.0.1/order/view/<int:item_id>/
```
Для проверки оплаты используйте тестовай номер карты: "4242424242424242". В поле даты окончания работы карты введите любую будущую дату. CVC и почтовый  индекс заполните любыми числами. 