test:
	docker-compose exec web python manage.py test

bash:
	docker-compose exec web bash

runserver:
	docker-compose run --rm --service-ports web python manage.py runserver 0.0.0.0:8000

start:
	docker-compose up

stop:
	docker-compose down

restart:
	make start
	make stop
