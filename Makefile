.PHONY: help
help:
	@echo "Available targets:"
	@echo "  django.sh            - Run python interactive shell"
	@echo "  django.bash          - Run bash shell in django container"
	@echo "  django.test          - Run django tests"
	@echo "  django.superuser     - Create django superuser"
	@echo "  db.migration.migrate - Create django migrations and migrate to database"
	@echo "  db.migration.clean   - Remove all django migrations (Dangerous!)"
	@echo "  db.volume.delete     - Delete database volume"
	@echo "  docker.image.build   - Build docker image"
	@echo "  docker.image.push    - Push docker image to registry"
	@echo "  code.format          - Format code using black, isort and flake8"
	@echo "  git.prune.deleted    - Delete local branches that have been deleted on remote"


.PHONY: docker.image.build
docker.image.build:
	docker compose down
	docker build -t clg_mgmt_tenant-django:1.0 .
	docker tag clg_mgmt_tenant-django:1.0 ghcr.io/pvfarooq/college-management-tenant/clg_mgmt_tenant-django:1.0

.PHONY: docker.image.push
docker.image.push:
	docker push ghcr.io/pvfarooq/college-management-tenant/clg_mgmt_tenant-django:1.0

.PHONY: github.docker.login
github.docker.login:
	docker login ghcr.io -u pvfarooq


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


.PHONY: code.format
code.format:
	@echo "Running code linters and formatters..."
	docker compose run --rm django sh -c "black . && isort . && flake8 ."


.PHONY: django.test
django.test:
	docker compose run --rm django coverage run manage.py test $(app)
	docker compose run --rm django coverage report
	make code.format

.PHONY: django.superuser
django.superuser:
	docker compose run --rm django python manage.py createsuperuser

.PHONY: django.migrations.clean
django.migrations.clean:
	@echo "Are you sure you want to delete all migrations? [y/n] " && read ans && [ $${ans:-n} = y ]; \
	if [ $$? -eq 0 ]; then \
		echo "Removing migration files..." ; \
		find . -path "*/migrations/*.py" -not -name "__init__.py" -delete ; \
	else \
		echo "Aborted"; \
	fi

.PHONY: git.prune.deleted
git.prune.deleted:
	@echo "Pruning deleted branches..."
	git fetch -p && git branch -vv | awk '/: gone]/{print $1}' | xargs git branch -D
