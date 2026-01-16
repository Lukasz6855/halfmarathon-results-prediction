"""
Predictor - Moduł do przewidywania czasu biegu
"""

import pandas as pd  # Praca z DataFrame
import streamlit as st  # Framework Streamlit
from config import AGE_CATEGORIES_MEN, AGE_CATEGORIES_WOMEN, CURRENT_YEAR, DEFAULT_COUNTRY  # Import stałych


def calculate_age_category(age, gender='M'):
    """
    Oblicza kategorię wiekową na podstawie wieku i płci
    
    Args:
        age (int): Wiek zawodnika
        gender (str): Płeć ('M' lub 'K')
        
    Returns:
        str: Kod kategorii (np. 'M20', 'M30', 'K20', 'K30')
    """
    # Wybierz odpowiednie mapowanie kategorii
    categories = AGE_CATEGORIES_MEN if gender == 'M' else AGE_CATEGORIES_WOMEN
    
    # Iteruj po kategoriach wiekowych
    for (min_age, max_age), category in categories.items():
        if min_age <= age <= max_age:  # Jeśli wiek mieści się w przedziale
            return category  # Zwróć kod kategorii
    
    # Jeśli wiek poza zakresem (nie powinno się zdarzyć przez walidację)
    # Zwróć najmłodszą kategorię dla danej płci
    return "M20" if gender == 'M' else "K20"


def calculate_rocznik(age, current_year=CURRENT_YEAR):
    """
    Oblicza rocznik (rok urodzenia) na podstawie wieku
    
    Args:
        age (int): Wiek zawodnika
        current_year (int): Aktualny rok
        
    Returns:
        int: Rocznik (rok urodzenia)
    """
    rocznik = current_year - age  # Oblicz rok urodzenia
    
    # Walidacja - sprawdź czy rocznik jest sensowny
    max_rocznik = current_year - 18  # Maksymalny rocznik (najmłodszy zawodnik = 18 lat)
    min_rocznik = current_year - 99  # Minimalny rocznik (najstarszy zawodnik = 99 lat)
    
    # Jeśli rocznik przekracza maksymalny (zawodnik za młody)
    if rocznik > max_rocznik:  # Np. obliczony rocznik to 2009, ale max to 2008
        rocznik = max_rocznik  # Użyj maksymalnego (18 lat)
        st.warning(f"⚠️ Skorygowano rocznik do {rocznik} (minimalny wiek: 18 lat)")  # Ostrzeżenie
    
    # Jeśli rocznik przekracza minimalny (zawodnik za stary)
    if rocznik < min_rocznik:  # Np. obliczony rocznik to 1920, ale min to 1927
        rocznik = min_rocznik  # Użyj minimalnego (99 lat)
        st.warning(f"⚠️ Skorygowano rocznik do {rocznik} (maksymalny wiek: 99 lat)")  # Ostrzeżenie
    
    return rocznik  # Zwróć rocznik


def prepare_input_data(gender, age, time_5km_seconds, country=DEFAULT_COUNTRY):
    """
    Przygotowuje dane wejściowe do formatu wymaganego przez model
    
    Args:
        gender (str): Płeć ('M' lub 'K')
        age (int): Wiek zawodnika
        time_5km_seconds (int): Czas na 5km w sekundach
        country (str): Kod kraju (domyślnie 'POL')
        
    Returns:
        pd.DataFrame: DataFrame z jednym wierszem gotowy do predykcji
    """
    # Oblicz rocznik
    rocznik = calculate_rocznik(age)  # Np. 1991
    
    # Utwórz słownik z danymi - TYLKO 3 cechy używane w modelu
    # Model wytrenowany na: ['Płeć', '5 km Czas_sekundy', 'Rocznik']
    data = {
        'Płeć': [gender],  # 'M' lub 'K'
        '5 km Czas_sekundy': [time_5km_seconds],  # ⚠️ WAŻNE: Czas w SEKUNDACH (int), nie tekst!
        'Rocznik': [rocznik],  # Rok urodzenia
    }
    
    # Konwertuj słownik na DataFrame
    df_input = pd.DataFrame(data)  # Jeden wiersz danych z 3 cechami
    
    return df_input  # Zwróć DataFrame


def predict_time(model, df_input):
    """
    Przewiduje czas biegu używając modelu ML
    
    Args:
        model: Wczytany model PyCaret/scikit-learn
        df_input (pd.DataFrame): Przygotowane dane wejściowe
        
    Returns:
        dict: Słownik z wynikami predykcji
            - 'time_seconds' (int): Przewidywany czas w sekundach
            - 'time_formatted' (str): Czas w formacie H:MM:SS
            - 'pace_per_km' (str): Tempo na kilometr (MM:SS/km)
    """
    try:
        # Wykonaj predykcję
        prediction = model.predict(df_input)  # Model zwraca numpy array
        
        # Wyciągnij wartość (pierwsze i jedyne przewidywanie)
        time_seconds = int(prediction[0])  # Konwersja na int
        
        # Konwersja sekund na format H:MM:SS
        hours = time_seconds // 3600  # Pełne godziny
        minutes = (time_seconds % 3600) // 60  # Pełne minuty
        seconds = time_seconds % 60  # Pozostałe sekundy
        time_formatted = f"{hours}:{minutes:02d}:{seconds:02d}"  # Format H:MM:SS
        
        # Oblicz tempo na kilometr (półmaraton = 21.0975 km)
        half_marathon_distance = 21.0975  # Dokładna długość półmaratonu
        pace_seconds_per_km = time_seconds / half_marathon_distance  # Sekundy/km
        pace_minutes = int(pace_seconds_per_km // 60)  # Minuty
        pace_seconds = int(pace_seconds_per_km % 60)  # Sekundy
        pace_per_km = f"{pace_minutes}:{pace_seconds:02d}/km"  # Format MM:SS/km
        
        # Zwróć wyniki jako słownik
        result = {
            'time_seconds': time_seconds,  # Czas w sekundach
            'time_formatted': time_formatted,  # Format H:MM:SS
            'pace_per_km': pace_per_km  # Tempo MM:SS/km
        }
        
        return result  # Zwróć słownik
        
    except Exception as e:  # Jeśli błąd podczas predykcji
        st.error(f"❌ Błąd podczas przewidywania: {e}")  # Wyświetl błąd
        st.stop()  # Zatrzymaj aplikację


def seconds_to_formatted_time(seconds):
    """
    Konwertuje sekundy na format H:MM:SS
    
    Args:
        seconds (int): Czas w sekundach
        
    Returns:
        str: Czas w formacie H:MM:SS
    """
    hours = seconds // 3600  # Pełne godziny
    minutes = (seconds % 3600) // 60  # Pełne minuty
    secs = seconds % 60  # Pozostałe sekundy
    return f"{hours}:{minutes:02d}:{secs:02d}"  # Format H:MM:SS
