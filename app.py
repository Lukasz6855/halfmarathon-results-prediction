"""Wrapper dla Streamlit Cloud.

Uruchamia aplikację z folderu APP/ w sposób kompatybilny ze Streamlit Cloud
(bez użycia exec()).
"""

import os
import runpy
import sys


root_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(root_dir, "APP")

# Ustaw working directory na APP/ (żeby działały ścieżki względne do data/, model/ itd.)
os.chdir(app_dir)

# Dodaj APP do sys.path, żeby działały importy typu: `from config import ...`, `from utils import ...`
sys.path.insert(0, app_dir)

# Uruchom APP/app.py jako główny moduł
runpy.run_path(os.path.join(app_dir, "app.py"), run_name="__main__")
