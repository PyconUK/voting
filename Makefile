help:
	@echo 'Makefile for PyCon UK proposal voting'
	@echo ''
	@echo 'Usage:'
	@echo '   make deploy                      deploy to heroku'
	@echo '   make setup                       set up dev environment'
	@echo ''

deploy:
	git push heroku master

setup:
	pip install -r requirements.txt
	python manage.py migrate


.PHONY: help deploy serve
