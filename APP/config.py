"""
Konfiguracja aplikacji - stałe, nazwy, ustawienia
"""
from datetime import datetime
import os

# Ścieżka do katalogu APP (gdzie znajduje się config.py)
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================
# INFORMACJE O WYDARZENIU
# ============================================
EVENT_NAME = "Półmaraton Wrocławski"  # Nazwa wydarzenia
EVENT_YEARS = [2023, 2024]  # Lata których dotyczą dane
CURRENT_YEAR = datetime.now().year  # Aktualny rok (do obliczeń rocznika)

# ============================================
# KATEGORIE WIEKOWE (zgodne z danymi treningowymi)
# ============================================
# Kategorie dla mężczyzn
AGE_CATEGORIES_MEN = {
    (18, 29): "M20",  # 18-29 lat
    (30, 39): "M30",  # 30-39 lat
    (40, 49): "M40",  # 40-49 lat
    (50, 59): "M50",  # 50-59 lat
    (60, 69): "M60",  # 60-69 lat
    (70, 79): "M70",  # 70-79 lat
    (80, 99): "M80",  # 80+ lat
}

# Kategorie dla kobiet
AGE_CATEGORIES_WOMEN = {
    (18, 29): "K20",  # 18-29 lat
    (30, 39): "K30",  # 30-39 lat
    (40, 49): "K40",  # 40-49 lat
    (50, 59): "K50",  # 50-59 lat
    (60, 69): "K60",  # 60-69 lat
    (70, 99): "K70",  # 70+ lat
}

# Dla kompatybilności wstecz - domyślne kategorie (mężczyźni)
AGE_CATEGORIES = AGE_CATEGORIES_MEN

# ============================================
# OGRANICZENIA WEJŚCIOWE
# ============================================
MIN_AGE = 18  # Minimalny wiek zawodnika
MAX_AGE = 99  # Maksymalny wiek zawodnika
MIN_TIME_5KM = 10  # Minimalny czas na 5km (minuty)
MAX_TIME_5KM = 90  # Maksymalny czas na 5km (minuty)

# ============================================
# VERCEL BLOB
# ============================================
BLOB_BASE_URL = "https://blob.vercel-storage.com"  # Bazowy URL Vercel Blob
MODEL_BLOB_PATH = "models"  # Ścieżka do modeli w Blob Storage
# URL do modelu - UWAGA: Wklej tutaj URL otrzymany po uploadzie modelu do Vercel Blob
VERCEL_BLOB_MODEL_URL = "https://eon9lclh7qwsfg3p.public.blob.vercel-storage.com/models/halfmarathon_model_3features_20260115_224149-EkAGpjfo0BzVLWrf8E1xsSBpNNhBh4.pkl"  # TODO: Wypełnić po uploadzie modelu (z notebooka)

# ============================================
# LANGFUSE
# ============================================
LANGFUSE_TRACE_NAME = "halfmarathon_prediction"  # Nazwa trace w Langfuse

# ============================================
# OPENAI
# ============================================
OPENAI_MODEL = "gpt-4o-mini"  # Model OpenAI do generowania komentarzy
OPENAI_TEMPERATURE = 0.7  # Temperatura (kreatywność odpowiedzi)
OPENAI_MAX_TOKENS = 300  # Maksymalna długość odpowiedzi

# ============================================
# DOMYŚLNE WARTOŚCI
# ============================================
DEFAULT_COUNTRY = "POL"  # Domyślny kraj (Polska)
DEFAULT_GENDER = "M"  # Domyślna płeć (Mężczyzna)

# ============================================
# MAPOWANIE PŁCI
# ============================================
GENDER_MAPPING = {
    "Mężczyzna": "M",  # Mężczyzna → M
    "Kobieta": "K"  # Kobieta → K
}

# ============================================
# ŚCIEŻKI DO PLIKÓW
# ============================================
DATA_FILE = os.path.join(APP_DIR, "data", "halfmarathon_2023_2024.csv")  # Plik z danymi historycznymi
