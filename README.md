# GB_Haba-Haba_project
Командная разработка по методологии Agile: SCRUM

- Django Modified Preorder Tree Traversal: https://pypi.org/project/django-mptt/
- Django Debug Toolbar: https://pypi.org/project/django-debug-toolbar/
- Django environ: https://pypi.org/project/django-environ/
- Pillow: https://pypi.org/project/Pillow/
- Редактор текстового поля: https://pypi.org/project/django-summernote/ 


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


## Наполнение базы:
- Удалить все миграции. Файлы из папок 'migrations' 
- Удалить базу данных. Файл db.sqlite3 
- Выполнить: python manage.py makemigrations 
- Выполнить: python manage.py migrate 
- Выполнить: python manage.py createsuperuser 
- Удалить папку и ее содержимое из папки 'media' 
- Выполнить: python manage.py fill_db

## Бэкап статей:
```sh
python manage.py save_db
```
