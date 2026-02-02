"""
Model Loader - Moduł do ładowania modelu z lokalnego folderu
"""

import streamlit as st  # Framework Streamlit
import os  # Operacje systemowe
from pycaret.regression import load_model  # PyCaret do ładowania modelu

@st.cache_resource  # Cache'uj model - wczytaj tylko raz
def load_model_from_local():
    """
    Ładuje model ML z lokalnego folderu model/
    
    Returns:
        model: Wczytany model PyCaret/scikit-learn
        
    Raises:
        Exception: Jeśli nie udało się wczytać modelu
    """
    try:
        # Określ ścieżkę do modelu
        current_dir = os.path.dirname(os.path.dirname(__file__))  # Folder APP
        model_path = os.path.join(current_dir, "model", "halfmarathon_model_3features_20260115_224149")
        
        # Sprawdź czy plik istnieje
        if not os.path.exists(model_path + ".pkl"):
            st.error(f"❌ Nie znaleziono pliku modelu: {model_path}.pkl")
            st.info("💡 Upewnij się, że plik modelu znajduje się w folderze APP/model/")
            st.stop()
        
        # Wyświetl status ładowania
        with st.spinner("⏳ Ładowanie modelu z lokalnego folderu..."):
            # Załaduj model przez PyCaret (bez rozszerzenia .pkl)
            model = load_model(model_path)
            
        # Oblicz rozmiar pliku
        file_size_mb = os.path.getsize(model_path + ".pkl") / 1024 / 1024
        st.success(f"✅ Model załadowany pomyślnie z lokalnego folderu! (rozmiar: {file_size_mb:.2f} MB)")
        
        return model
                
    except Exception as e:  # Inny błąd
        st.error(f"❌ Nieoczekiwany błąd podczas ładowania modelu: {e}")
        st.stop()


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
