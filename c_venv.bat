@echo off
set venv=venv_mec
set project=Mecanica-Toretto

cd "../" && py -m venv %venv% && cd %project% && "../%venv%/Scripts/activate.bat" && pip install -r requirements.txt