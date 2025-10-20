#!/bin/bash

VERSION="0.0.1"

pip install --break-system-packages -r requirements.txt streamlit-desktop-app

rm -rf build dist

# TODO, might use PyInstaller

streamlit-desktop-app build app.py --name "MyStreamlitApp${VERSION}"