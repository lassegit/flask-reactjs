.PHONY: docs test

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"

env:
	virtualenv -p /usr/local/bin/python3 venv && \
	. venv/bin/activate && \
	make deps
deps:
	pip install -r requirements.txt

clean:
	python manage.py clean

lint:
	flake8 --exclude=venv,app/static .

test:
	py.test tests

dev:
	source venv/bin/activate && uwsgi --ini uwsgi-dev.ini --py-autoreload 1

prod:
	source venv/bin/activate && uwsgi --ini uwsgi.ini

createdb:
	source venv/bin/activate && python manage.py createdb

babelextract:
	source	venv/bin/activate && \
	pybabel extract -F app/babel.cfg -k lazy_gettext -o app/messages.pot app

babelcompile:
	source	venv/bin/activate && pybabel compile -d app/translations

# German
germaninit:
	source venv/bin/activate && \
	pybabel init -i app/messages.pot -d app/translations -l de

germanupdate:
	source venv/bin/activate && \
	pybabel update -i app/messages.pot -d app/translations -l de


