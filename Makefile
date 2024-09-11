VENV := .venv

all: venv

venv: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

run: venv
	@./$(VENV)/bin/python3 main.py

clean:
	@if [ -d $(VENV) ]; then \
		./$(VENV)/bin/pyclean . || true; \
		rm -rf $(VENV); \
	fi

re: clean all

lint: venv
	@./$(VENV)/bin/pycodestyle app
	@./$(VENV)/bin/pylint app

.PHONY: all venv run clean re lint
