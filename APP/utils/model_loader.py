"""
Model Loader - Moduł do ładowania modelu z Vercel Blob
"""

import streamlit as st  # Framework Streamlit
import requests  # Biblioteka do zapytań HTTP
import os  # Operacje systemowe
import time  # Do opóźnień przy retry
import tempfile  # Do tworzenia plików tymczasowych
from pycaret.regression import load_model  # PyCaret do ładowania modelu
from config import VERCEL_BLOB_MODEL_URL  # Import URL z config

@st.cache_resource  # Cache'uj model - wczytaj tylko raz
def load_model_from_blob(max_retries=3):
    """
    Pobiera model ML z Vercel Blob Storage
    
    Args:
        max_retries (int): Maksymalna liczba prób pobrania
        
    Returns:
        model: Wczytany model PyCaret/scikit-learn
        
    Raises:
        Exception: Jeśli nie udało się pobrać modelu
    """
    # Pobierz token z zmiennych środowiskowych
    token = os.getenv("BLOB_READ_WRITE_TOKEN")  # Token dostępu do Vercel Blob
    
    # Walidacja tokenu
    if not token:  # Jeśli brak tokenu
        st.error("❌ Brak BLOB_READ_WRITE_TOKEN w zmiennych środowiskowych!")  # Wyświetl błąd
        st.info("💡 Upewnij się, że plik .env zawiera poprawny token")  # Wskazówka
        st.stop()  # Zatrzymaj aplikację
    
    # Walidacja URL
    if not VERCEL_BLOB_MODEL_URL:  # Jeśli brak URL w config
        st.error("❌ Brak VERCEL_BLOB_MODEL_URL w pliku config.py!")  # Błąd
        st.stop()  # Zatrzymaj
    
    # Przygotuj nagłówki HTTP
    headers = {
        "Authorization": f"Bearer {token}",  # Token autoryzacyjny
    }
    
    # Pętla retry dla odporności na błędy
    for attempt in range(1, max_retries + 1):  # Próby od 1 do max_retries
        try:
            # Wyświetl status pobierania
            with st.spinner(f"⏳ Pobieranie modelu z Vercel Blob (próba {attempt}/{max_retries})..."):
                # Wykonaj zapytanie GET
                response = requests.get(
                    VERCEL_BLOB_MODEL_URL,  # URL do modelu
                    headers=headers,  # Nagłówki z tokenem
                    timeout=120  # Timeout 120 sekund
                )
                
                # Sprawdź status odpowiedzi
                response.raise_for_status()  # Rzuć wyjątek jeśli status != 200
                
                # Zapisz model do pliku tymczasowego
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as tmp_file:
                    tmp_file.write(response.content)  # Zapisz zawartość
                    tmp_path = tmp_file.name  # Ścieżka do pliku tymczasowego
                
                # Załaduj model przez PyCaret (bez rozszerzenia .pkl)
                model_path_without_ext = tmp_path.replace('.pkl', '')  # Usuń rozszerzenie
                model = load_model(model_path_without_ext)  # Wczytaj model PyCaret
                
                # Usuń plik tymczasowy
                try:
                    os.remove(tmp_path)  # Usuń plik
                except:
                    pass  # Ignoruj błąd usuwania
                
                st.success(f"✅ Model załadowany pomyślnie! (rozmiar: {len(response.content) / 1024 / 1024:.2f} MB)")  # Sukces
                return model  # Zwróć model
                
        except requests.exceptions.HTTPError as e:  # Błąd HTTP
            if response.status_code == 503 and attempt < max_retries:  # Jeśli 503 i są jeszcze próby
                delay = 5 * attempt  # Opóźnienie: 5s, 10s, 15s
                st.warning(f"⚠️ Serwis chwilowo niedostępny (503). Ponowna próba za {delay}s...")  # Ostrzeżenie
                time.sleep(delay)  # Czekaj
                continue  # Spróbuj ponownie
            else:  # Inny błąd HTTP lub brak prób
                st.error(f"❌ Błąd HTTP {response.status_code}: {e}")  # Wyświetl błąd
                st.stop()  # Zatrzymaj
                
        except requests.exceptions.Timeout:  # Timeout
            st.error(f"❌ Przekroczono czas oczekiwania (120s) - próba {attempt}/{max_retries}")  # Błąd
            if attempt < max_retries:  # Jeśli są jeszcze próby
                time.sleep(5)  # Czekaj 5s
                continue  # Spróbuj ponownie
            else:  # Brak prób
                st.stop()  # Zatrzymaj
                
        except Exception as e:  # Inny błąd
            st.error(f"❌ Nieoczekiwany błąd podczas ładowania modelu: {e}")  # Wyświetl błąd
            st.stop()  # Zatrzymaj
    
    # Jeśli dotarliśmy tutaj - wszystkie próby nieudane
    st.error(f"❌ Nie udało się załadować modelu po {max_retries} próbach")  # Błąd końcowy
    st.stop()  # Zatrzymaj aplikację


def get_model_info(model):
    """
    Zwraca informacje o załadowanym modelu
    
    Args:
        model: Model PyCaret/scikit-learn
        
    Returns:
        dict: Słownik z informacjami o modelu
    """
    try:
        info = {}  # Pusty słownik
        
        # Pobierz nazwę klasy modelu
        info['model_name'] = type(model).__name__  # Nazwa klasy
        
        # Pobierz moduł
        info['model_module'] = type(model).__module__  # Moduł (sklearn, pycaret itp.)
        
        # Sprawdź czy to finalize model PyCaret
        if hasattr(model, 'steps'):  # Jeśli ma atrybuty Pipeline
            info['is_pipeline'] = True  # To jest pipeline
            info['steps_count'] = len(model.steps)  # Liczba kroków
        else:
            info['is_pipeline'] = False  # To nie pipeline
        
        return info  # Zwróć słownik
        
    except Exception as e:  # Błąd
        return {"error": str(e)}  # Zwróć błąd
