
rpm:
	python setup.py bdist --format=rpm
	rpmbuild -ba vhm-client.spec rpmbuild --define "_topdir ${PWD}/build/bdist.linux-x86_64/rpm/"

pip:
	python setup.py sdist upload
