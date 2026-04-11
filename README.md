# CX Content Pipeline - RSS Aggregator

Збирає 21 RSS-фід в один XML-файл і публікує на GitHub Pages.

## Як працює

1. GitHub Actions запускається щодня о 8:00 (Kyiv time), пн-пт
2. Python-скрипт збирає останні статті з 21 джерела
3. Генерує один RSS XML-файл
4. Публікує на GitHub Pages

## Твій агрегований фід

Після налаштування фід буде доступний за адресою:

```
https://YOUR_USERNAME.github.io/cx-rss-pipeline/feed.xml
```

Цей URL вставляєш у Make в RSS-ноду.

## Налаштування

1. Створи новий репозиторій на GitHub: `cx-rss-pipeline`
2. Завантаж туди файли: `aggregate.py`, `.github/workflows/aggregate.yml`
3. В Settings репозиторію -> Pages -> Source: виберь "GitHub Actions"
4. Запусти workflow вручну: Actions -> Aggregate RSS Feeds -> Run workflow
5. Через 1-2 хвилини фід буде доступний за URL вище

## Додавання нових джерел

Відкрий `aggregate.py`, додай URL у список `FEEDS`. Commit. Готово.
