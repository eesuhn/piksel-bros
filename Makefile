VENV = .venv
PACKAGE = app
MAIN = main.py

all: venv

venv: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

run: venv
	@./$(VENV)/bin/python3 $(MAIN)

debug: venv
	@./$(VENV)/bin/python3 $(MAIN) --debug

edit: venv
	@./$(VENV)/bin/python3 $(MAIN) --editor

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

.PHONY: all venv run clean re lint
