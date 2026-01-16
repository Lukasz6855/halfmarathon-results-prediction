"""
Langfuse Helper - Moduł do monitorowania wywołań LLM za pomocą Langfuse
"""

import streamlit as st  # Framework Streamlit
from langfuse import Langfuse  # Biblioteka Langfuse
import os  # Operacje systemowe
from datetime import datetime  # Data i czas


def initialize_langfuse_client():
    """
    Inicjalizuje klienta Langfuse
    
    Returns:
        Langfuse: Klient Langfuse lub None jeśli błąd
    """
    # Pobierz dane uwierzytelniające z zmiennych środowiskowych
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")  # Klucz prywatny
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")  # Klucz publiczny
    host = os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")  # Host (domyślnie cloud)
    
    # Walidacja kluczy
    if not secret_key or not public_key:  # Jeśli brak któregoś klucza
        st.info("ℹ️ Langfuse nie jest skonfigurowane - monitorowanie LLM wyłączone")  # Info
        return None  # Zwróć None
    
    try:
        # Utwórz klienta Langfuse
        client = Langfuse(
            secret_key=secret_key,  # Klucz prywatny
            public_key=public_key,  # Klucz publiczny
            host=host  # Host Langfuse
        )
        
        return client  # Zwróć klienta
        
    except Exception as e:  # Jeśli błąd inicjalizacji
        st.warning(f"⚠️ Błąd inicjalizacji Langfuse: {e}")  # Ostrzeżenie
        return None  # Zwróć None


def create_trace(client, user_name, session_id=None):
    """
    Tworzy nowy trace (ślad sesji) w Langfuse
    
    Args:
        client (Langfuse): Klient Langfuse
        user_name (str): Imię użytkownika
        session_id (str, optional): ID sesji (jeśli None - wygeneruj z timestamp)
        
    Returns:
        dict: Słownik z informacjami o trace (name, user_id, session_id) lub None jeśli błąd
    """
    # Sprawdź czy klient jest dostępny
    if client is None:  # Jeśli brak klienta
        return None  # Zwróć None
    
    try:
        # Wygeneruj session_id i timestamp jeśli nie podano
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Timestamp
        if session_id is None:  # Jeśli brak ID
            session_id = f"session_{user_name}_{timestamp}"  # ID sesji
        
        # W Langfuse 2.x nie używamy client.trace() bezpośrednio
        # Zamiast tego zwracamy dict z parametrami trace które będą użyte w generation()
        trace_info = {
            "client": client,  # Zapisz referencję do klienta
            "name": "halfmarathon_prediction",  # Nazwa trace
            "user_id": user_name,  # ID użytkownika
            "session_id": session_id,  # ID sesji
            "metadata": {
                "application": "Halfmarathon Time Predictor",  # Aplikacja
                "timestamp": datetime.now().isoformat()  # Znacznik czasu
            }
        }
        
        return trace_info  # Zwróć informacje o trace
        
    except Exception as e:  # Jeśli błąd
        st.warning(f"⚠️ Nie udało się przygotować trace w Langfuse: {e}")  # Ostrzeżenie
        return None  # Zwróć None


def log_generation(
    trace,
    model,
    prompt,
    completion,
    usage=None,
    metadata=None
):
    """
    Loguje wywołanie LLM (generation) do Langfuse
    
    Args:
        trace: Słownik z informacjami o trace (zwrócony przez create_trace)
        model (str): Nazwa modelu (np. 'gpt-4o-mini')
        prompt (str): Prompt wysłany do modelu
        completion (str): Odpowiedź z modelu
        usage (dict, optional): Informacje o zużyciu tokenów
        metadata (dict, optional): Dodatkowe metadane
        
    Returns:
        generation: Obiekt generation lub None jeśli błąd
    """
    # Sprawdź czy trace jest dostępny
    if trace is None:  # Jeśli brak trace
        return None  # Zwróć None
    
    try:
        # Pobierz klienta z trace_info
        client = trace.get("client")
        if client is None:
            return None
        
        # Przygotuj dane użycia (usage)
        if usage is None:  # Jeśli brak danych użycia
            usage = {}  # Pusty słownik
        
        # Przygotuj metadane
        if metadata is None:  # Jeśli brak metadanych
            metadata = {}  # Pusty słownik
        
        # Połącz metadane z trace
        combined_metadata = {**trace.get("metadata", {}), **metadata}
        combined_metadata['logged_at'] = datetime.now().isoformat()  # Czas logowania
        
        # W Langfuse 2.x używamy trace() który zwraca obiekt trace
        # a potem wywołujemy generation() na tym obiekcie
        trace_obj = client.trace(
            name=trace.get("name"),
            user_id=trace.get("user_id"),
            session_id=trace.get("session_id"),
            metadata=trace.get("metadata", {})
        )
        
        # Teraz wywołaj generation na obiekcie trace
        generation = trace_obj.generation(
            name="ai_commentary_generation",  # Nazwa generowania
            model=model,  # Model
            model_parameters={
                "temperature": 0.7,  # Temperatura (z config)
                "max_tokens": 300  # Max tokens (z config)
            },
            input=prompt,  # Prompt wejściowy
            output=completion,  # Wygenerowana odpowiedź
            usage=usage,  # Zużycie tokenów
            metadata=combined_metadata  # Metadane
        )
        
        return generation  # Zwróć generation
        
    except AttributeError as e:  # Jeśli brak metody
        st.warning(f"⚠️ Problem z API Langfuse: {e}. Sprawdź dokumentację dla wersji 2.x")
        return None
    except Exception as e:  # Jeśli błąd
        st.warning(f"⚠️ Nie udało się zalogować generation w Langfuse: {e}")  # Ostrzeżenie
        return None  # Zwróć None


def finalize_trace(trace, status="success", output=None):
    """
    Finalizuje trace (zamyka sesję) - w Langfuse 2.x to jest opcjonalne
    
    Args:
        trace: Słownik z informacjami o trace
        status (str): Status trace ('success', 'error')
        output (dict, optional): Końcowy output sesji
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    # Sprawdź czy trace jest dostępny
    if trace is None:  # Jeśli brak trace
        return False  # Zwróć False
    
    try:
        # W Langfuse 2.x finalizacja trace jest automatyczna
        # Możemy opcjonalnie użyć client.flush() aby wymusić wysłanie danych
        client = trace.get("client")
        if client:
            client.flush()  # Wyślij wszystkie zgromadzone dane
        
        return True  # Sukces
        
    except Exception as e:  # Jeśli błąd
        st.warning(f"⚠️ Nie udało się sfinalizować trace w Langfuse: {e}")  # Ostrzeżenie
        return False  # Zwróć False


def check_langfuse_availability():
    """
    Sprawdza czy Langfuse jest dostępne (klucze skonfigurowane)
    
    Returns:
        bool: True jeśli dostępne, False jeśli nie
    """
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")  # Klucz prywatny
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")  # Klucz publiczny
    
    # Zwróć True jeśli oba klucze są niepuste
    return (
        secret_key is not None and secret_key.strip() != "" and
        public_key is not None and public_key.strip() != ""
    )
