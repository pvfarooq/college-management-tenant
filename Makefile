.PHONY: help
help:
	@echo "Available targets:"
	@echo "  db.migration.migrate - Create django migrations and migrate to database"
	@echo "  django.sh            - Run python interactive shell"
	@echo "  django.bash          - Run bash shell in django container"
	@echo "  db.volume.delete     - Delete database volume"


.PHONY: db.migration.migrate
db.migration.migrate:
	@echo "Running django migrate..."
	docker compose run --rm django python manage.py makemigrations
	docker compose run --rm django python manage.py migrate


.PHONY: django.sh
django.sh:
	docker compose run --rm django python manage.py shell_plus --ipython


.PHONY: django.bash
django.bash:
	docker compose run --rm django /bin/bash


.PHONY: db.volume.delete
db.volume.delete:
	docker compose down
	docker volume rm clg_mgmt_tenant_postgres_data | true