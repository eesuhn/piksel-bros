#!/bin/bash
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC=$(tput sgr0)

VENV_DIR="venv-piksel-bros"

if [ ! -d "$VENV_DIR" ]; then
	printf "${YELLOW}Building Environment...\n"
	python3 -m venv $VENV_DIR
	source "$VENV_DIR/bin/activate"

	printf "Installing Requirements...${NC}\n"
	pip install -r requirements.txt

	printf "${GREEN}Environment Built!${NC}\n"
fi

source "$VENV_DIR/bin/activate"
