#!/bin/bash

echo "Password Manager Setup"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "  python main.py"
