# GB_Haba-Haba_project
Командная разработка по методологии Agile: SCRUM

Django Modified Preorder Tree Traversal: https://pypi.org/project/django-mptt/ \
Django Debug Toolbar: https://pypi.org/project/django-debug-toolbar/ \
Django environ: https://pypi.org/project/django-environ/ \
Pillow: https://pypi.org/project/Pillow/
https://pypi.org/project/django-summernote/ - Редактор текстового поля


## Подсказки по запуску
- переименовать файл .env_example в .env
- создание БД (создать миграции и применить)
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```
- создать суперпользователя
```sh
python manage.py createsuperuser
```

- уже существующий в базе

| Пользователь | Пароль   |
|--------------|----------|
| admin        | habahaba |