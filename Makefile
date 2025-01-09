VENV = .venv
PACKAGE = app
MAIN = main.py

all: venv

venv: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt
	./$(VENV)/bin/pre-commit install

run: venv
	@./$(VENV)/bin/python3 $(MAIN)

debug: venv
	@./$(VENV)/bin/python3 $(MAIN) --debug

edit: venv
	@./$(VENV)/bin/python3 $(MAIN) --edit

clean:
	@if [ -d $(VENV) ]; then \
		./$(VENV)/bin/pyclean . || true; \
		rm -rf $(VENV); \
		rm -rf .mypy_cache; \
	fi

re: clean all

lint: venv
	@./$(VENV)/bin/pycodestyle --ignore=E501 $(PACKAGE)
	@./$(VENV)/bin/pylint $(PACKAGE)
	@./$(VENV)/bin/mypy $(PACKAGE)

build: venv
	@./$(VENV)/bin/pyinstaller build.spec --clean

.PHONY: all venv run debug edit clean re lint build
