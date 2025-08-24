# Quotes Project (Django)

Мини-приложение: случайная цитата (с учётом веса), лайки/дизлайки, счётчик просмотров, форма добавления, ТОП-10 и дашборд.

## Быстрый старт

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте:
- `/` — случайная цитата;
- `/add/` — добавление;
- `/top/` — ТОП-10 по лайкам;
- `/dashboard/` — простой дашборд;
- `/admin/` — админка.

## Примечания

- Антидубликаты через `text_normalized` + валидацию модели.
- Не более 3 активных цитат на источник — валидация в `clean()`.
- Взвешенный выбор реализован на Python через `random.choices`.
- Голосование и просмотры атомарные (через `transaction.atomic` и F-выражения).
