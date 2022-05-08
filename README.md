## Учебный проект YaMDb
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.

Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Разработчики:
- [Данила Красов](https://github.com/Fr0stFree)
- [Александр Саратов](https://github.com/F1rebeard)
- [Лев Харьков](https://github.com/Kirsan94)
---
### Использованные технологии
- [Python](https://github.com/python)
- [Django](https://github.com/django/django)
- [Django Rest Framework](https://github.com/encode/django-rest-framework)
- [Simple JWT](https://github.com/jazzband/djangorestframework-simplejwt)
- [Swagger](https://github.com/axnsan12/drf-yasg)
---
### Запуск проекта
- Клонировать репозиторий
```
git clone git@github.com:F1rebeard/api_yamdb.git
```
- Установить и активировать виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate (Windows OS)
или
source venv/bin/activate (Unix OS)
```
- Установить необходимые зависимости requirements.txt
```
pip install -r requirements.txt
```
- Выполнить миграции:
```
python manage.py makemigrations
python manage.py migrate
```
Для заполнения БД тестовыми данными используем команду:
```
python manage.py load_csv users review titles genre comments category genre_title
```
Запустить проект:
```
python manage.py runserver
```
---
### Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладет правами администратора (admin)

### Регистрация нового пользователя
1. Получить код подтверждения на переданный email.
2. Права доступа: Доступно без токена.
3. Использовать имя 'me' в качестве username запрещено.
4. Поля email и username должны быть уникальными.
---
### Примеры запросов к API
#### Регистрация нового пользователя:
```
POST /v1/auth/signup/ HTTP/1.1
Content-Type: application/json
{
  "email": "foo@mail.com",
  "username": "foo"
}
```
#### Получение JWT-токена
```
POST /api/v1/auth/token/ HTTP/1.1
Content-Type: application/json
{
  "username": "foo",
  "confirmation_code": "bar"
}
```
#### Добавление категории
```
POST /api/v1/categories/ HTTP/1.1
Content-Type: application/json
{
  "name": "foo",
  "slug": "bar"
}
```
#### Удаление категории
```
DELETE /api/v1/categories/{slug}/ HTTP/1.1
```
#### Добавление жанра
```
POST /api/v1/genres/ HTTP/1.1
Content-Type: application/json
{
  "name": "foo",
  "slug": "bar"
}
```
#### Удаление жанра
```
DELETE /api/v1/genres/{slug}/ HTTP/1.1
```
#### Обновление публикации
```
PUT /api/v1/posts/{id}/ HTTP/1.1
Content-Type: application/json
{
  "text": "foobar"
}
```
#### Добавление произведения
```
POST /api/v1/titles/ HTTP/1.1
Content-Type: application/json
{
  "name": "foo",
  "year": 0,
  "description": "foobar",
  "genre": [
    "bar",
  ],
  "category": "barfoo"
}
```
#### Частичное обновление информации о произведении
```
PATCH /api/v1/titles/{titles_id}/ HTTP/1.1
Content-Type: application/json
{
  "name": "foo",
  "description": "bar",
  "genre": [
    "foobar"
  ],
}
```
#### Удаление произведения
```
DEL /api/v1/titles/{titles_id}/ HTTP/1.1
```
#### Получение списка всех пользователей
```
GET /api/v1/users/ HTTP/1.1
```
#### Добавление пользователя
```
POST /api/v1/users/ HTTP/1.1
Content-Type: application/json
{
  "username": "foo",
  "email": "foo@bar.fake"
}
```
#### Получение пользователя
```
GET /api/v1/users/{username}/ HTTP/1.1
```
#### Изменение данных пользователя
```
PATCH /api/v1/users/{username}/ HTTP/1.1
Content-Type: application/json
{
  "first_name": "foo",
  "last_name": "bar",
  "bio": "foobar"
}
```
#### Удаление пользователя
```
DELETE /api/v1/users/{username}/ HTTP/1.1
```
#### Получение данных о своей учетной записи
```
GET /api/v1/users/me/ HTTP/1.1
```
#### Изменение данных своей учетной записи
```
PATCH /api/v1/users/me/ HTTP/1.1
Content-Type: application/json
{
  "first_name": "foo",
  "last_name": "bar",
  "bio": "foobar"
}
```
