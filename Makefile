install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

runserver:
	poetry run python manage.py runserver

shell:
	poetry run python manage.py shell

prepare-translation:
	poetry run django-admin makemessages --ignore="static" --ignore=".env" -l en

complete-translation:
	poetry run django-admin compilemessages
