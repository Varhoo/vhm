
all: autopep8 pip 

autopep8:
	find . -name "*.py"  | grep -e ^./vhmlib -e ^./[^/]*.py \
	 | xargs autopep8 --in-place --aggressive --aggressive 

rpm:
	python setup.py bdist --format=rpm
	rpmbuild -ba vhm-client.spec rpmbuild --define "_topdir ${PWD}/build/bdist.linux-x86_64/rpm/"

pip:
	python setup.py sdist upload

build:
	python setup.py sdist
