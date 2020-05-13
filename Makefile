test:
	docker-compose exec web python manage.py test

bash:
	docker-compose exec web bash
