"""
Moduł do ładowania danych historycznych z CSV
"""
import pandas as pd  # Import biblioteki pandas do pracy z danymi
import streamlit as st  # Import streamlit do cache'owania
from config import DATA_FILE  # Import ścieżki do pliku z konfiguracją


def time_to_seconds(time_str):
    """
    Konwertuje czas w formacie HH:MM:SS na sekundy
    
    Args:
        time_str (str): Czas w formacie HH:MM:SS lub H:MM:SS
        
    Returns:
        int: Liczba sekund lub None jeśli błąd
    """
    try:
        # Jeśli wartość jest NaN lub None
        if pd.isna(time_str):  # Sprawdź czy NaN
            return None  # Zwróć None
        
        # Konwersja string na sekundy
        parts = str(time_str).split(':')  # Rozdziel na części
        
        if len(parts) == 3:  # HH:MM:SS
            hours = int(parts[0])  # Godziny
            minutes = int(parts[1])  # Minuty
            seconds = int(parts[2])  # Sekundy
            return hours * 3600 + minutes * 60 + seconds  # Całkowita liczba sekund
        elif len(parts) == 2:  # MM:SS
            minutes = int(parts[0])  # Minuty
            seconds = int(parts[1])  # Sekundy
            return minutes * 60 + seconds  # Całkowita liczba sekund
        else:
            return None  # Niepoprawny format
            
    except:  # Jeśli błąd konwersji
        return None  # Zwróć None


@st.cache_data  # Dekorator - dane będą załadowane tylko raz i cache'owane
def load_historical_data():
    """
    Ładuje dane historyczne z półmaratonu 2023 i 2024
    
    Returns:
        pd.DataFrame: DataFrame z danymi historycznymi
    """
    try:
        df = pd.read_csv(DATA_FILE, encoding='utf-8-sig')  # Wczytaj CSV z polskimi znakami
        
        # Dodaj kolumnę 'Rok' jeśli istnieje 'rok' (małymi literami)
        if 'rok' in df.columns and 'Rok' not in df.columns:  # Jeśli jest 'rok' ale nie ma 'Rok'
            df['Rok'] = df['rok']  # Skopiuj wartości
        
        # Konwertuj kolumnę 'Czas' (HH:MM:SS) na sekundy jeśli nie ma 'Czas_sekundy'
        if 'Czas' in df.columns and 'Czas_sekundy' not in df.columns:  # Jeśli jest 'Czas' ale nie ma 'Czas_sekundy'
            df['Czas_sekundy'] = df['Czas'].apply(time_to_seconds)  # Konwersja na sekundy
        
        # Konwertuj kolumnę '5 km Czas' na sekundy jeśli nie ma '5 km Czas_sekundy'
        # Obsługuje zarówno starą nazwę '5km_sekundy' jak i nową '5 km Czas_sekundy'
        if '5 km Czas_sekundy' not in df.columns:  # Jeśli nie ma nowej kolumny
            if '5km_sekundy' in df.columns:  # Jeśli jest stara nazwa
                df['5 km Czas_sekundy'] = df['5km_sekundy']  # Skopiuj wartości
            elif '5 km Czas' in df.columns:  # Jeśli jest tylko tekstowa kolumna
                df['5 km Czas_sekundy'] = df['5 km Czas'].apply(time_to_seconds)  # Konwersja
        
        # Dodaj 'Imię i nazwisko' jeśli istnieją kolumny 'Imię' i 'Nazwisko'
        if 'Imię' in df.columns and 'Nazwisko' in df.columns and 'Imię i nazwisko' not in df.columns:
            df['Imię i nazwisko'] = df['Imię'].fillna('') + ' ' + df['Nazwisko'].fillna('')  # Połącz imię i nazwisko
            df['Imię i nazwisko'] = df['Imię i nazwisko'].str.strip()  # Usuń spacje na końcach
        
        return df  # Zwróć DataFrame
    except FileNotFoundError:  # Jeśli plik nie istnieje
        st.error(f"❌ Nie znaleziono pliku z danymi: {DATA_FILE}")  # Wyświetl błąd
        st.stop()  # Zatrzymaj aplikację
    except Exception as e:  # Jeśli inny błąd
        st.error(f"❌ Błąd podczas wczytywania danych: {e}")  # Wyświetl błąd
        st.stop()  # Zatrzymaj aplikację


def get_data_summary(df):
    """
    Zwraca podsumowanie danych (liczba rekordów, lata, itp.)
    
    Args:
        df (pd.DataFrame): DataFrame z danymi
        
    Returns:
        dict: Słownik z podsumowaniem
    """
    summary = {
        'total_records': len(df),  # Całkowita liczba rekordów
        'years': sorted(df['Rok'].unique()) if 'Rok' in df.columns else [],  # Lata (wielka litera)
        'columns': list(df.columns),  # Lista kolumn
        'records_by_year': df.groupby('Rok').size().to_dict() if 'Rok' in df.columns else {}  # Liczba rekordów per rok
    }
    return summary  # Zwróć słownik z podsumowaniem
