run:
	python src/app.py

test:
	pip install -e .
	pytest tests

package_create:
	pip install build
	python -m build

package_upload:
	pip install twine
	python -m twine upload dist/*

build_app:
	pip install pyinstaller
	pyinstaller --name "Auto League Closer" --icon icon.ico --specpath misc \
				--add-data "../src/leaguecloser/lib;leaguecloser/lib" \
				--add-data "../src/leaguecloser/data;leaguecloser/data" \
				--clean --noconfirm src/app.py

.PHONY: run test package_create package_upload build_app
