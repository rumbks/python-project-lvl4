install:
	poetry install

runserver:
	poetry run python manage.py runserver

translate:
	poetry run python manage.py makemessages -l ru --ignore .venv

compile_translations:
	poetry run python manage.py compilemessages --ignore .venv

make_migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

tests:
	poetry run pytest -vv tests

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

lint:
	poetry run flake8 .

.PHONY: tests