"""
Wrapper dla Streamlit Cloud
Uruchamia aplikację z folderu APP/
"""
import sys
import os

# Dodaj folder APP do ścieżki
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'APP'))

# Importuj główną aplikację
from APP.app import *
