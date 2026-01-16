"""
OpenAI Helper - Moduł do generowania komentarzy AI za pomocą GPT-4
"""

import streamlit as st  # Framework Streamlit
import os  # Operacje systemowe
from config import OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS  # Stałe z config

# Spróbuj użyć Langfuse OpenAI wrapper dla automatycznego logowania
# Jeśli Langfuse nie jest dostępny, użyj standardowego OpenAI
try:
    from langfuse.openai import OpenAI  # Langfuse wrapper dla OpenAI
    LANGFUSE_AVAILABLE = True
except ImportError:
    from openai import OpenAI  # Standardowy OpenAI client
    LANGFUSE_AVAILABLE = False


def initialize_openai_client():
    """
    Inicjalizuje klienta OpenAI z API key
    Automatycznie używa Langfuse wrapper jeśli dostępny
    
    Returns:
        OpenAI: Klient OpenAI lub None jeśli błąd
    """
    # Pobierz API key z zmiennych środowiskowych
    api_key = os.getenv("OPENAI_API_KEY")  # Klucz API
    
    # Walidacja klucza
    if not api_key:  # Jeśli brak klucza
        st.warning("⚠️ Brak OPENAI_API_KEY - funkcja komentarzy AI jest wyłączona")  # Ostrzeżenie
        return None  # Zwróć None
    
    try:
        # Utwórz klienta OpenAI (z Langfuse wrapper jeśli dostępny)
        client = OpenAI(api_key=api_key)  # Inicjalizacja klienta
        
        # Informuj o statusie Langfuse
        if LANGFUSE_AVAILABLE and os.getenv("LANGFUSE_SECRET_KEY") and os.getenv("LANGFUSE_PUBLIC_KEY"):
            st.sidebar.info("📊 Langfuse: monitoring aktywny (OpenAI wrapper)")
        
        return client  # Zwróć klienta
        
    except Exception as e:  # Jeśli błąd inicjalizacji
        st.error(f"❌ Błąd inicjalizacji OpenAI: {e}")  # Wyświetl błąd
        return None  # Zwróć None


def generate_commentary(
    client,
    user_name,
    predicted_time_formatted,
    gender,
    age,
    age_category,
    category_stats,
    ranking_info
):
    """
    Generuje komentarz AI na temat wyniku użytkownika
    
    Args:
        client (OpenAI): Klient OpenAI
        user_name (str): Imię użytkownika
        predicted_time_formatted (str): Przewidywany czas (H:MM:SS)
        gender (str): Płeć ('M' lub 'K')
        age (int): Wiek
        age_category (str): Kategoria wiekowa (np. 'M35')
        category_stats (dict): Statystyki kategorii (mean, median, min, max)
        ranking_info (dict): Informacje o pozycji (estimated_position, percentile)
        
    Returns:
        str: Wygenerowany komentarz AI lub None jeśli błąd
    """
    # Sprawdź czy klient jest dostępny
    if client is None:  # Jeśli brak klienta
        return None  # Zwróć None
    
    # Przygotuj płeć po polsku
    gender_pl = "mężczyzna" if gender == 'M' else "kobieta"  # Polskie oznaczenie
    
    # Przygotuj statystyki kategorii
    if category_stats['count'] > 0:  # Jeśli są dane w kategorii
        mean_time = f"{category_stats['mean']//3600}:{(category_stats['mean']%3600)//60:02d}:{category_stats['mean']%60:02d}"
        median_time = f"{category_stats['median']//3600}:{(category_stats['median']%3600)//60:02d}:{category_stats['median']%60:02d}"
        stats_text = f"Średni czas w kategorii {age_category}: {mean_time}, mediana: {median_time}"
    else:  # Brak danych
        stats_text = f"Brak danych historycznych dla kategorii {age_category}"
    
    # Przygotuj informacje o pozycji
    if ranking_info['estimated_position'] is not None:  # Jeśli są dane rankingowe
        ranking_text = f"Szacowana pozycja: {ranking_info['estimated_position']}/{ranking_info['total_runners']} (percentyl: {ranking_info['percentile']})"
        faster_text = f"Byłbyś szybszy niż {ranking_info['faster_than_percent']}% zawodników w tej kategorii"
    else:  # Brak danych
        ranking_text = "Brak danych rankingowych"
        faster_text = ""
    
    # Stwórz prompt dla GPT
    prompt = f"""
    Jesteś ekspertem od biegania i trenerem. Przeanalizuj poniższe wyniki przewidywanego czasu w półmaratonie i napisz krótki, motywujący komentarz (2-3 zdania) w języku polskim.
    
    Dane zawodnika:
    - Imię: {user_name}
    - Płeć: {gender_pl}
    - Wiek: {age} lat
    - Kategoria wiekowa: {age_category}
    - Przewidywany czas: {predicted_time_formatted}
    
    Kontekst statystyczny:
    - {stats_text}
    - {ranking_text}
    - {faster_text}
    
    Komentarz powinien:
    1. Ocenić wynik (świetny/dobry/przeciętny/wymaga pracy)
    2. Porównać do średniej w kategorii
    3. Dać motywującą wskazówkę lub gratulacje
    
    Bądź entuzjastyczny ale realistyczny. Nie używaj emoji.
    """
    
    try:
        # Wywołaj API OpenAI
        response = client.chat.completions.create(
            model=OPENAI_MODEL,  # Model z config.py (gpt-4o-mini)
            messages=[
                {"role": "system", "content": "Jesteś ekspertem od biegania i trenerem. Twoje komentarze są krótkie, motywujące i oparte na danych."},
                {"role": "user", "content": prompt}
            ],
            temperature=OPENAI_TEMPERATURE,  # Temperatura z config (0.7)
            max_tokens=OPENAI_MAX_TOKENS  # Max tokens z config (300)
        )
        
        # Wyciągnij wygenerowany tekst
        commentary = response.choices[0].message.content.strip()  # Treść odpowiedzi
        
        return commentary  # Zwróć komentarz
        
    except Exception as e:  # Jeśli błąd API
        st.warning(f"⚠️ Nie udało się wygenerować komentarza AI: {e}")  # Ostrzeżenie
        return None  # Zwróć None


def check_openai_availability():
    """
    Sprawdza czy OpenAI API jest dostępne
    
    Returns:
        bool: True jeśli dostępne, False jeśli nie
    """
    api_key = os.getenv("OPENAI_API_KEY")  # Pobierz klucz
    return api_key is not None and api_key.strip() != ""  # Sprawdź czy niepusty
