.PHONY: clean install manage migrate run shell

ENVIRONMENT ?= development

clean:
	find . -name "*.pyc" -delete
	find . -type d -empty -delete

manage:
	ENVIRONMENT=$(ENVIRONMENT) ./ve/bin/python ./manage.py $(COMMAND)

migrate:
	COMMAND=migrate $(MAKE) manage

run:
	COMMAND=runserver $(MAKE) manage

shell:
	COMMAND=shell_plus $(MAKE) manage

install:
	[ ! -d ve/ ] && python3.6 -m venv ve/ || :
	./ve/bin/pip install -r requirements.txt
