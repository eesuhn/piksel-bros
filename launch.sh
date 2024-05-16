#!/bin/bash

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
NC=$(tput sgr0)

VENV_DIR="venv-piksel-bros"

if [ ! -d "$VENV_DIR" ]; then
	printf "${YELLOW}Building Environment...\n"
	python3 -m venv $VENV_DIR

	if [ $? -ne 0 ]; then
		printf "${RED}Error${NC}: Failed to build environment\n"
		return 1
	fi
	source "$VENV_DIR/bin/activate"

	printf "Installing Requirements...${NC}\n"
	pip install -r requirements.txt

	if [ $? -ne 0 ]; then
		printf "${RED}Error${NC}: Failed to install requirements\n"
		return 1
	fi
	printf "${GREEN}Environment Built!${NC}\n"
fi

printf "${GREEN}Launching Environment...${NC}\n"
source "$VENV_DIR/bin/activate"
return 0
