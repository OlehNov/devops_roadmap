MANAGE_PATH = src/manage.py
DUMP_PATH = src/dump.json

dump:
	python $(MANAGE_PATH) dumpdata --exclude auth.permission --exclude contenttypes > $(DUMP_PATH)

makemigrations: dump
	python $(MANAGE_PATH) makemigrations

migrate: makemigrations
	python $(MANAGE_PATH) migrate

flush: migrate
	echo yes | python $(MANAGE_PATH) flush

load_bump: flush
	python $(MANAGE_PATH) loaddata $(DUMP_PATH)

run: load_bump
	python $(MANAGE_PATH) runserver 8181

up:
	docker compose up --build --force-recreate

down:
	docker compose down -v