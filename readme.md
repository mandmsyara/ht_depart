Backend приложение на FastAPI для работы с отделами - создание, перенос, удаление отделов, создание карточек сотрудников.

Запуск приложения:

    docker compose up --build

Доступ по адерсу:

    http://localhost:8000

Документация OpenAPI:

    http://localhost:8000/docs

Запуск тестов:

    docker compose exec app pytest -v

Стек: 

Python

FastAPI

PostgreSQL

SQLAlchemy

pytest

Docker / docker-compose

Базы данных: 

org_structure_db - основная база приложения, для нее созданы миграции через Alembic

org_structure_test_db - база данных postgres без миграций, заполняется при проведении 
тестов, потом вся информация с нее удаляется

Основные эндпоинты
POST   /departments/
GET    /departments/{department_id}
PATCH  /departments/{department_id}
DELETE /departments/{department_id}
POST   /departments/{department_id}/employees/

Пример удаления подразделения

Каскадное удаление:

DELETE /departments/1?mode=cascade

Удаление с переносом сотрудников:

DELETE /departments/1?mode=reassign&reassign_to_department_id=2

Проверка линтером

```bash
docker compose exec app ruff check .