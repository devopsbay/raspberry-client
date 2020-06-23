PIP=pip3
include .env
export $(shell sed 's/=.*//' .env)

install:
	sh initial-env.sh
	$(PIP) install -r requirements.txt

install-dev:
	sh initial-env.sh
	$(PIP) install -r requirements-dev.txt
	cp nfcclient/settings/dev.local.py nfcclient/settings/local.py

update:
	$(PIP) install -r requirements.txt

clean:
	rm nfcclient/settings/local.py

pytest-cov:
	pytest --cov-config .coveragerc --cov=nfcclient --cov-report html tests

run:
	env
	PYTHONPATH=. python3 nfcclient/app.py