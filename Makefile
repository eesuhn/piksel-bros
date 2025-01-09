VENV = .venv
PACKAGE = app
MAIN = main.py

all: venv

venv: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	@echo "\033[0;33mvenv\033[0m: Setting up virtual environment..."
	@python3 -m venv $(VENV) > /dev/null 2>&1

	@echo "\033[0;33mvenv\033[0m: Installing requirements..."
	@./$(VENV)/bin/pip install -r requirements.txt > /dev/null 2>&1

	@echo "\033[0;33mvenv\033[0m: Installing pre-commit hooks..."
	@./$(VENV)/bin/pre-commit install > /dev/null 2>&1

	@echo "\033[0;32mDone!\033[0m"

run: venv
	@./$(VENV)/bin/python3 $(MAIN)

debug: venv
	@./$(VENV)/bin/python3 $(MAIN) --debug

edit: venv
	@./$(VENV)/bin/python3 $(MAIN) --edit

clean:
	@if [ -d $(VENV) ]; then \
		./$(VENV)/bin/pyclean . > /dev/null 2>&1 || true; \
	fi

fclean: clean
	@if [ -d $(VENV) ]; then \
		rm -rf $(VENV) .mypy_cache/ build/ dist/; \
	fi

re: fclean all

lint: venv
	@./$(VENV)/bin/pycodestyle --ignore=E501 $(PACKAGE)
	@./$(VENV)/bin/pylint $(PACKAGE)
	@./$(VENV)/bin/mypy $(PACKAGE)

build: venv
	@echo "\033[0;33mBuilding...\033[0m"
	@./$(VENV)/bin/pyinstaller build.spec --clean > /dev/null 2>&1
	@echo "\033[0;32mDone!\033[0m"

.PHONY: all venv run debug edit clean fclean re lint build
