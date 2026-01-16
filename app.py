"""
Wrapper dla Streamlit Cloud
Uruchamia aplikację z folderu APP/
"""
import sys
import os

# Pobierz ścieżkę do głównego folderu
root_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(root_dir, 'APP')

# Zmień working directory na APP/
os.chdir(app_dir)

# Dodaj APP do ścieżki Pythona
sys.path.insert(0, app_dir)

# Teraz załaduj i uruchom aplikację
with open(os.path.join(app_dir, 'app.py'), 'r', encoding='utf-8') as f:
    code = f.read()
    exec(code)
