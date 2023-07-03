# Cryptocurrency Exchange

Проект **Криптообменник** является платформой для обмена фиатных денег на криптовалюту и обратно. На подобие обменников которые вы видите на сайте **BestChange**.

## Установка и запуск проекта

Для клонирования репозитория выполните следующую команду:

```
git clone https://github.com/saniksin/Cryptocurrency-Exchange
```

После клонирования репозитория активируйте виртуальное окружение.

Установите зависимости из файла **requirements.txt**:

```
pip install -r requirements.txt
```

## Использование Docker контейнера

Вы также можете использовать Docker контейнер для разворачивания проекта. Для этого выполните следующие шаги:

**Загрузите образ** из Docker Hub
```
docker pull saniksin/app:django_app
```

Запустите контейнер, прокинув необходимые файлы и порт:
- замените **path_to_sqlite_file** на путь к файлу db.sqlite3
- замените **path_to_env_file** на путь к файлу .env

```
docker run -p 8000:8000 -v myvolume:/apps -v **path_to_sqlite_file**/db.sqlite3:/app/db.sqlite3 -v **path_to_env_file**/.env:/app/.env -d saniksin/app:django_app
```

Убедитесь, что у вас имеются файлы **db.sqlite3** и **.env** (файл .env должен быть по аналогичным .env_example).
