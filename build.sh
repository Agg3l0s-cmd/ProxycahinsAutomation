#!/bin/bash

python -m venv myvenv

source venv/bin/activate

pip install -r requirements.txt

playwright install firefox chromium

chmod +x main.py
