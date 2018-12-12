dev-tests:
	pipenv run python -m unittest

dev-format:
	pipenv run black actiwatch
	pipenv run flake8 --ignore="E501,E266,W503" actiwatch

package-dist:
	pipenv run python setup.py sdist bdist_wheel

upload-dist:
	pipenv run python -m twine upload dist/*
