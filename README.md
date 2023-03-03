### ЯП - Спринт 10 - Проект YaMDb (групповой проект). Яндекс.Практикум
### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий (Category) может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

Полная документация к API находится по эндпоинту /redoc

### Стек технологий использованный в проекте:
-   Python 3.9
-   Django 3.2
-   Django REST Framework
-   REST API
-   SQLite
-   Аутентификация по JWT-токену

## Запуск проекта
1. Клонировать репозиторий и перейти в него в командной строке.
Установите и активируйте виртуальное окружение c учетом версии Python 3.9 (выбираем python не ниже 3.7)

2. Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```

2. Развертывание в репозитории виртуального окружения
```
python3.9 -m venv venv
```
3. Запуск виртуального окружения
```
source venv/Scripts/activate
```
4. Установка зависимостей в виртуальном окружении
```
pip install -r requirements.txt
```

5. Выполнение миграций
```
python manage.py migrate
```

6. Запуск проекта
```
python manage.py runserver
```

## Документация
Документация будет доступна после запуска проекта по адресу `/redoc/`.

## Ресурсы API YaMDb
Ресурс auth: аутентификация.

Ресурс users: пользователи.

Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.

Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.

Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
