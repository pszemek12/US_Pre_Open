@echo off
REM Przechodzimy do katalogu skryptu
cd /d "%~dp0"
REM Uruchamiamy Streamlit w tle, bez konsoli (pythonw) i minimalizujemy okno
start "" /min pythonw -m streamlit run app.py
