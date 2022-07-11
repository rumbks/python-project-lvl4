runserver:
	poetry run python manage.py runserver

translate:
	poetry run python manage.py makemessages -l ru --ignore .venv

compile_translations:
	poetry run python manage.py compilemessages --ignore .venv
