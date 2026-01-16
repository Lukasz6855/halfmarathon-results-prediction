"""
Stats Calculator - Moduł do obliczania statystyk z danych historycznych
"""

import pandas as pd  # Praca z DataFrame
import numpy as np  # Operacje numeryczne (NaN handling)
import streamlit as st  # Framework Streamlit
from io import BytesIO  # Do eksportu Excel w pamięci


def get_winners(df, year=None, gender=None):
    """
    Zwraca zwycięzców (najlepsze czasy) dla danego roku i płci
    
    Args:
        df (pd.DataFrame): Dane historyczne
        year (int, optional): Rok edycji (jeśli None - wszystkie lata)
        gender (str, optional): Płeć ('M' lub 'K', jeśli None - obie płcie)
        
    Returns:
        pd.DataFrame: Top 10 najlepszych czasów
    """
    df_filtered = df.copy()  # Kopia danych
    
    # Filtruj po roku jeśli podano
    if year is not None:  # Jeśli określono rok
        df_filtered = df_filtered[df_filtered['Rok'] == year]  # Filtruj
    
    # Filtruj po płci jeśli podano
    if gender is not None:  # Jeśli określono płeć
        df_filtered = df_filtered[df_filtered['Płeć'] == gender]  # Filtruj
    
    # Sortuj po czasie (rosnąco) i weź top 10
    df_winners = df_filtered.nsmallest(10, 'Czas_sekundy')  # 10 najszybszych
    
    # Konwertuj sekundy na format H:MM:SS dla czytelności
    df_winners['Czas_formatted'] = df_winners['Czas_sekundy'].apply(
        lambda x: f"{int(x)//3600}:{(int(x)%3600)//60:02d}:{int(x)%60:02d}"  # Format H:MM:SS
    )
    
    return df_winners  # Zwróć DataFrame z TOP 10


def get_averages(df, group_by=['Rok', 'Płeć']):
    """
    Oblicza średnie czasy dla różnych grup
    
    Args:
        df (pd.DataFrame): Dane historyczne
        group_by (list): Lista kolumn do grupowania (domyślnie Rok i Płeć)
        
    Returns:
        pd.DataFrame: DataFrame ze średnimi czasami
    """
    # Grupuj i oblicz średnią
    df_avg = df.groupby(group_by)['Czas_sekundy'].mean().reset_index()  # Średnia dla grup
    
    # Zmień nazwę kolumny
    df_avg.rename(columns={'Czas_sekundy': 'Średni_czas_sekundy'}, inplace=True)  # Nowa nazwa
    
    # Konwertuj średni czas na format H:MM:SS
    df_avg['Średni_czas_formatted'] = df_avg['Średni_czas_sekundy'].apply(
        lambda x: f"{int(x)//3600}:{(int(x)%3600)//60:02d}:{int(x)%60:02d}"  # Format
    )
    
    # Zaokrąglij sekundy
    df_avg['Średni_czas_sekundy'] = df_avg['Średni_czas_sekundy'].round(0).astype(int)  # Int
    
    return df_avg  # Zwróć DataFrame


def get_category_stats(df, age_category, gender):
    """
    Zwraca statystyki dla konkretnej kategorii wiekowej i płci
    
    Args:
        df (pd.DataFrame): Dane historyczne
        age_category (str): Kategoria wiekowa (np. 'M35')
        gender (str): Płeć ('M' lub 'K')
        
    Returns:
        dict: Słownik ze statystykami (mean, median, min, max, count)
    """
    # Filtruj dane
    df_filtered = df[
        (df['Kategoria wiekowa'] == age_category) &  # Kategoria
        (df['Płeć'] == gender)  # Płeć
    ]
    
    # Jeśli brak danych
    if len(df_filtered) == 0:  # Pusta ramka
        return {
            'count': 0,  # Brak rekordów
            'mean': None,  # Brak średniej
            'median': None,  # Brak mediany
            'min': None,  # Brak minimum
            'max': None  # Brak maksimum
        }
    
    # Oblicz statystyki
    stats = {
        'count': len(df_filtered),  # Liczba zawodników
        'mean': int(df_filtered['Czas_sekundy'].mean()),  # Średnia (int)
        'median': int(df_filtered['Czas_sekundy'].median()),  # Mediana (int)
        'min': int(df_filtered['Czas_sekundy'].min()),  # Minimum (int)
        'max': int(df_filtered['Czas_sekundy'].max())  # Maksimum (int)
    }
    
    return stats  # Zwróć słownik


def estimate_ranking(df, predicted_time_seconds, gender, age_category=None):
    """
    Szacuje pozycję w klasyfikacji na podstawie przewidywanego czasu
    
    Args:
        df (pd.DataFrame): Dane historyczne
        predicted_time_seconds (int): Przewidywany czas w sekundach
        gender (str): Płeć ('M' lub 'K')
        age_category (str, optional): Kategoria wiekowa (jeśli None - klasyfikacja ogólna)
        
    Returns:
        dict: Słownik z szacowaną pozycją i statystykami
            - 'estimated_position' (int): Szacowana pozycja
            - 'total_runners' (int): Łączna liczba zawodników w kategorii
            - 'percentile' (float): Percentyl (0-100)
            - 'faster_than_percent' (float): Procent wolniejszych zawodników
    """
    # Filtruj dane po płci
    df_filtered = df[df['Płeć'] == gender]  # Filtruj po płci
    
    # Dodatkowo filtruj po kategorii wiekowej jeśli podano
    if age_category is not None:  # Jeśli określono kategorię
        df_filtered = df_filtered[df_filtered['Kategoria wiekowa'] == age_category]  # Filtruj
    
    # Liczba zawodników w kategorii
    total_runners = len(df_filtered)  # Łączna liczba
    
    # Jeśli brak danych
    if total_runners == 0:  # Pusta ramka
        return {
            'estimated_position': None,  # Brak pozycji
            'total_runners': 0,  # Brak zawodników
            'percentile': None,  # Brak percentyla
            'faster_than_percent': None  # Brak procentu
        }
    
    # Policz ilu zawodników miało lepszy (szybszy) czas
    faster_runners = len(df_filtered[df_filtered['Czas_sekundy'] < predicted_time_seconds])  # Szybsi
    
    # Policz ilu zawodników miało gorszy (wolniejszy) czas
    slower_runners = len(df_filtered[df_filtered['Czas_sekundy'] > predicted_time_seconds])  # Wolniejsi
    
    # Szacowana pozycja = liczba szybszych + 1
    # (jeśli 10 osób jest szybszych, to jesteś na 11 miejscu)
    estimated_position = faster_runners + 1  # Pozycja
    
    # Oblicz percentyl (procent zawodników którzy są wolniejsi)
    faster_than_percent = (slower_runners / total_runners) * 100  # Procent
    
    # Oblicz percentyl pozycji (0-100)
    percentile = (estimated_position / total_runners) * 100  # Percentyl
    
    result = {
        'estimated_position': estimated_position,  # Pozycja
        'total_runners': total_runners,  # Łączna liczba
        'percentile': round(percentile, 1),  # Percentyl zaokrąglony
        'faster_than_percent': round(faster_than_percent, 1)  # Procent wolniejszych
    }
    
    return result  # Zwróć słownik


def prepare_excel_export(df):
    """
    Przygotowuje DataFrame do eksportu jako Excel
    
    Args:
        df (pd.DataFrame): Dane do wyeksportowania
        
    Returns:
        BytesIO: Obiekt bajtowy z plikiem Excel w pamięci
    """
    # Utwórz bufor w pamięci
    output = BytesIO()  # Bufor bajtowy
    
    # Zapisz DataFrame do bufora jako Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:  # Użyj openpyxl
        df.to_excel(writer, index=False, sheet_name='Statystyki')  # Zapisz bez indeksu
    
    # Przesuń wskaźnik na początek bufora
    output.seek(0)  # Reset pozycji
    
    return output  # Zwróć bufor


def format_time_from_seconds(seconds):
    """
    Formatuje sekundy na czytelny czas H:MM:SS
    
    Args:
        seconds (int/float): Czas w sekundach
        
    Returns:
        str: Czas w formacie H:MM:SS
    """
    # Sprawdź czy wartość jest None lub NaN
    if seconds is None or (isinstance(seconds, float) and pd.isna(seconds)):
        return "N/A"  # Zwróć N/A
    
    seconds = int(seconds)  # Konwersja na int
    hours = seconds // 3600  # Pełne godziny
    minutes = (seconds % 3600) // 60  # Pełne minuty
    secs = seconds % 60  # Pozostałe sekundy
    return f"{hours}:{minutes:02d}:{secs:02d}"  # Format H:MM:SS


def get_winners_by_category(df):
    """
    Zwraca zwycięzców dla każdej kategorii wiekowej i płci w każdym roku
    
    Args:
        df (pd.DataFrame): Dane historyczne
        
    Returns:
        pd.DataFrame: DataFrame ze zwycięzcami (min czas w każdej kategorii)
    """
    # Grupuj po roku, płci i kategorii, znajdź minimalny czas
    winners = df.loc[df.groupby(['Rok', 'Płeć', 'Kategoria wiekowa'])['Czas_sekundy'].idxmin()]
    
    # Dodaj sformatowany czas
    winners['Czas_formatted'] = winners['Czas_sekundy'].apply(
        lambda x: f"{int(x)//3600}:{(int(x)%3600)//60:02d}:{int(x)%60:02d}"
    )
    
    # Dodaj czas 5km sformatowany jeśli istnieje
    # Obsługa zarówno starej nazwy '5km_sekundy' jak i nowej '5 km Czas_sekundy'
    time_5km_col = None
    if '5 km Czas_sekundy' in winners.columns:
        time_5km_col = '5 km Czas_sekundy'
    elif '5km_sekundy' in winners.columns:
        time_5km_col = '5km_sekundy'
    
    if time_5km_col:
        winners['5km_formatted'] = winners[time_5km_col].apply(
            lambda x: f"{int(x)//60:02d}:{int(x)%60:02d}" if pd.notna(x) else "N/A"
        )
    
    # Sortuj po roku, płci i kategorii
    winners = winners.sort_values(['Rok', 'Płeć', 'Kategoria wiekowa'])
    
    return winners


def get_average_times_by_category(df):
    """
    Zwraca średnie czasy dla każdej kategorii wiekowej i płci w każdym roku
    
    Args:
        df (pd.DataFrame): Dane historyczne
        
    Returns:
        pd.DataFrame: DataFrame ze średnimi czasami
    """
    # Grupuj i oblicz średnią
    avg_times = df.groupby(['Rok', 'Płeć', 'Kategoria wiekowa']).agg({
        'Czas_sekundy': 'mean',
        'Płeć': 'count'  # Liczba zawodników
    }).reset_index()
    
    # Zmień nazwę kolumny z liczbą zawodników
    avg_times.columns = ['Rok', 'Płeć', 'Kategoria wiekowa', 'Średni_czas_sekundy', 'Liczba_zawodników']
    
    # Dodaj sformatowany czas
    avg_times['Średni_czas_formatted'] = avg_times['Średni_czas_sekundy'].apply(
        lambda x: f"{int(x)//3600}:{(int(x)%3600)//60:02d}:{int(x)%60:02d}"
    )
    
    # Sortuj
    avg_times = avg_times.sort_values(['Rok', 'Płeć', 'Kategoria wiekowa'])
    
    return avg_times
