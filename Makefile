
PYTHON=../tmp/env/bin/python

build: 
	echo build

develop:
	$(PYTHON) setup.py develop

test:
	$(PYTHON) -m unittest discover -p '*tests.py' -v

clean:
	echo clean
