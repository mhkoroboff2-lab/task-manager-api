# Task Manager API

REST API для управления задачами, проектами и тегами.

##  Стек технологий
- **Backend:** Python, Django, Django REST Framework
- **Документация:** drf-spectacular (Swagger/OpenAPI)
- **БД:** SQLite

##  Установка и запуск
```bash
git clone <ссылка_на_репозиторий>
cd task_manager_api
python -m venv venv
source venv/Scripts/activate  # для Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver