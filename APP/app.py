"""
Aplikacja Streamlit - Przewidywanie czasu w Półmaratonie Wrocławskim
Autor: AI Assistant
Data: 2026-01-12
"""

import streamlit as st  # Framework do tworzenia aplikacji webowych
import pandas as pd  # Biblioteka do pracy z danymi
import os  # Operacje na systemie plików
from dotenv import load_dotenv  # Ładowanie zmiennych środowiskowych

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Import modułów z aplikacji
from config import *  # Import wszystkich stałych z konfiguracji
from utils.data_loader import load_historical_data, get_data_summary  # Import funkcji do ładowania danych
from utils.model_loader import load_model_from_local, get_model_info  # Import funkcji do ładowania modelu
from utils.predictor import prepare_input_data, predict_time, calculate_age_category  # Import funkcji predykcji
from utils.stats_calculator import (  # Import funkcji statystyk
    get_winners, get_averages, get_category_stats,
    estimate_ranking, format_time_from_seconds,
    get_winners_by_category, get_average_times_by_category
)
from utils.openai_helper import (  # Import funkcji OpenAI (z automatycznym Langfuse)
    initialize_openai_client, generate_commentary, check_openai_availability
)

# ============================================
# KONFIGURACJA STRONY
# ============================================
st.set_page_config(
    page_title=f"Przewidywanie czasu - {EVENT_NAME}",  # Tytuł w przeglądarce
    page_icon="🏃",  # Ikona w przeglądarce
    layout="wide",  # Szeroki layout
    initial_sidebar_state="expanded",  # Sidebar rozwinięty domyślnie
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "🏃 Aplikacja do przewidywania czasu w półmaratonie wykorzystująca Machine Learning"
    }
)

# ============================================
# META TAGI OPEN GRAPH (dla LinkedIn)
# ============================================
st.markdown("""
<head>
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="Przewidywanie czasu w Półmaratonie Wrocławskim 🏃" />
    <meta property="og:description" content="Aplikacja AI wykorzystująca Machine Learning do przewidywania Twojego czasu w półmaratonie na podstawie wieku, płci i doświadczenia. Sprawdź swoją prognozę!" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=1200&h=630&fit=crop" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="pl_PL" />
    
    <!-- Additional Meta Tags -->
    <meta name="description" content="Przewiduj swój czas w Półmaratonie Wrocławskim używając zaawansowanego modelu Machine Learning. Wprowadź swój wiek, płeć i doświadczenie biegowe." />
    <meta name="keywords" content="półmaraton, wrocław, przewidywanie czasu, machine learning, AI, bieganie" />
</head>
""", unsafe_allow_html=True)

# ============================================
# STYLE CSS - PREMIUM DESIGN
# ============================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hero Banner - Nowa Koncepcja */
    .hero-banner {
        position: relative;
        width: 100%;
        border-radius: 15px;
        margin-bottom: 2rem;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    .hero-image {
        width: 100%;
        height: 350px;
        object-fit: cover;
        object-position: center;
        display: block;
        margin: 0;
        padding: 0;
    }
    
    .hero-text-section {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.2rem 2rem;
        text-align: center;
        margin: 0;
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 0.5rem 0;
        line-height: 1.3;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-title-emoji {
        color: #FF6B00;
        font-size: 2.2rem;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #ecf0f1;
        margin: 0;
        font-weight: 400;
        line-height: 1.5;
    }
    
    .hero-subtitle strong {
        color: #FF6B00;
        font-weight: 600;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    /* Prediction Box - Premium */
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        text-align: center;
        box-shadow: 0 20px 60px rgba(102,126,234,0.4);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .prediction-label {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        font-weight: 400;
        margin-bottom: 0.5rem;
    }
    
    .prediction-time {
        font-size: 4rem;
        font-weight: 700;
        color: white;
        margin: 10px 0;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .prediction-pace {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.95);
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Stat Cards */
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 10px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #FF6B00;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .stat-card.orange {
        border-left-color: #FF6B00;
    }
    
    .stat-card.blue {
        border-left-color: #667eea;
    }
    
    .stat-card.green {
        border-left-color: #28a745;
    }
    
    .stat-card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #FF6B00;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #333;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #FF6B00;
        display: inline-block;
    }
    
    /* Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border-left: 5px solid #667eea;
        color: #333;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .info-box strong {
        color: #222;
    }
    
    /* AI Commentary Box */
    .ai-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border-left: 5px solid #FF6B00;
        box-shadow: 0 10px 30px rgba(255,107,0,0.2);
        color: #333;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .ai-box strong {
        color: #222;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #FF6B00;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HERO BANNER Z UNSPLASH
# ============================================
# Zdjęcie maratonu z Unsplash
unsplash_image_url = "https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=1600&h=400&fit=crop"

st.markdown(f"""
<div class="hero-banner">
    <img class="hero-image" src="{unsplash_image_url}" alt="Marathon">
    <div class="hero-text-section">
        <h1 class="hero-title"><span class="hero-title-emoji">🏃</span> Przewidywanie Czasu w Półmaratonie</h1>
        <p class="hero-subtitle">{EVENT_NAME} • Edycje <strong>{EVENT_YEARS[0]}-{EVENT_YEARS[1]}</strong> • <strong>21,957</strong> wyników • 🤖 Machine Learning</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# SEKCJA INFORMACYJNA
# ============================================
with st.expander("ℹ️ O aplikacji", expanded=True):  # Rozwijana sekcja z informacjami
    st.markdown("""
    ### Jak działa ta aplikacja?
    
    Ta aplikacja wykorzystuje **wytrenowany model Machine Learning** do przewidywania Twojego czasu w półmaratonie 
    na podstawie danych historycznych z **Półmaratonu Wrocławskiego** z lat **2023 i 2024**.
    
    #### 📊 Dane treningowe:
    - **21,957 wyników** z dwóch edycji wydarzenia
    - Połączone dane z 2023 i 2024 roku
    - Dane przygotowane z wykorzystaniem technik przetwarzania ML
    
    #### 🤖 Model predykcyjny:
    - Wytrenowany na rzeczywistych wynikach zawodników
    - Używa **3 kluczowych parametrów**: płeć, wiek (rocznik), czas na 5km (w sekundach)
    - Czas na 5km traktowany jako zmienna numeryczna dla lepszej dokładności
    - Przewiduje końcowy czas z dokładnością **~5 minut** (MAE = 297.6 sekund)
    
    #### 🎯 Jak z tego skorzystać:
    1. **Wypełnij formularz** w panelu bocznym (imię, płeć, wiek, czas na 5km)
    2. **Otrzymaj przewidywany czas** końcowy
    3. **Porównaj się** ze statystykami z poprzednich edycji
    4. **Eksperymentuj** z symulatorem czasów
    
    ---
    
    💡 **Wskazówka**: Twój czas na 5km to najważniejszy czynnik predykcji. 
    Jeśli nie znasz swojego czasu, spróbuj pobiec 5km i zmierz czas!
    """)

# ============================================
# ŁADOWANIE DANYCH I MODELU
# ============================================
@st.cache_data  # Cache'uj dane aby nie wczytywać za każdym razem
def load_app_data():
    """Wczytaj wszystkie dane potrzebne do aplikacji"""
    df = load_historical_data()  # Wczytaj dane historyczne
    summary = get_data_summary(df)  # Pobierz podsumowanie danych
    return df, summary  # Zwróć dane i podsumowanie

# Wczytaj dane
try:
    df_historical, data_summary = load_app_data()  # Załaduj dane i podsumowanie
    
    # Wyświetl info o danych
    st.sidebar.success(f"✅ Załadowano {data_summary['total_records']:,} rekordów")  # Potwierdzenie
    
except Exception as e:  # Jeśli błąd podczas ładowania
    st.error(f"❌ Błąd inicjalizacji aplikacji: {e}")  # Wyświetl błąd
    st.stop()  # Zatrzymaj aplikację

# Wczytaj model ML
try:
    model = load_model_from_local()  # Załaduj model z lokalnego folderu
    model_info = get_model_info(model)  # Pobierz info o modelu
    st.sidebar.success(f"✅ Model {model_info.get('model_name', 'N/A')} załadowany")  # Potwierdzenie
except Exception as e:  # Jeśli błąd
    st.error(f"❌ Błąd ładowania modelu: {e}")  # Wyświetl błąd
    st.stop()  # Zatrzymaj

# Inicjalizuj klienta OpenAI (z Langfuse wrapper jeśli skonfigurowany)
openai_client = None  # Domyślnie None

if check_openai_availability():  # Jeśli OpenAI skonfigurowane
    openai_client = initialize_openai_client()  # Inicjalizuj klienta (automatycznie z Langfuse jeśli dostępny)
    if openai_client:  # Jeśli sukces
        st.sidebar.success("✅ OpenAI połączone")  # Potwierdzenie

# ============================================
# PANEL BOCZNY - FORMULARZ
# ============================================
st.sidebar.header("📝 Twoje Dane")  # Nagłówek panelu bocznego

# Imię/Nick
user_name = st.sidebar.text_input(
    "Twoje imię lub nick:",  # Etykieta pola
    value="",  # Wartość domyślna
    placeholder="np. Jan, Anna, Runner123",  # Placeholder
    help="Podaj swoje imię lub pseudonim (tylko do identyfikacji, nie wpływa na predykcję)"  # Tooltip
)

# Płeć
gender_display = st.sidebar.selectbox(
    "Płeć:",  # Etykieta
    options=list(GENDER_MAPPING.keys()),  # Lista opcji z config.py
    help="Wybierz płeć - wpływa na przewidywany czas"  # Tooltip
)
gender = GENDER_MAPPING[gender_display]  # Zamień na kod (M/K)

# Wiek
age = st.sidebar.number_input(
    "Wiek:",  # Etykieta
    min_value=MIN_AGE,  # Minimalna wartość z config.py
    max_value=MAX_AGE,  # Maksymalna wartość z config.py
    value=30,  # Wartość domyślna
    step=1,  # Krok zmiany
    help="Podaj swój wiek (18-99 lat)"  # Tooltip
)

# Czas na 5km (dwa suwaki: minuty i sekundy)
st.sidebar.markdown("**Czas na 5 km:**")  # Nagłówek sekcji

col_min, col_sec = st.sidebar.columns(2)  # Dwie kolumny dla minut i sekund

with col_min:
    time_5km_minutes = st.number_input(
        "Minuty:",
        min_value=MIN_TIME_5KM,
        max_value=MAX_TIME_5KM,
        value=25,
        step=1,
        key="time_5km_min"
    )

with col_sec:
    time_5km_seconds_only = st.number_input(
        "Sekundy:",
        min_value=0,
        max_value=59,
        value=0,
        step=1,
        key="time_5km_sec"
    )

# Oblicz całkowity czas w sekundach
time_5km_seconds = time_5km_minutes * 60 + time_5km_seconds_only
time_5km_display = f"{time_5km_minutes:02d}:{time_5km_seconds_only:02d}"
st.sidebar.info(f"⏱️ Wybrany czas: **{time_5km_display}** (MM:SS) = {time_5km_seconds} sekund")

# Walidacja zakresu czasów 5km (ostrzeżenie o ekstrapolacji)
# Na podstawie analizy danych treningowych:
# Kobiety: najszybszy czas 5km = 17:18 (1038s), najwolniejszy = 63:45 (3825s)
# Mężczyźni: najszybszy czas 5km = 15:06 (906s), najwolniejszy = 52:32 (3152s)
if gender == 'K':
    min_safe_time = 1038  # 17:18 dla kobiet
    max_safe_time = 3825  # 63:45 dla kobiet
    gender_text = "kobiet"
else:
    min_safe_time = 906  # 15:06 dla mężczyzn
    max_safe_time = 3152  # 52:32 dla mężczyzn
    gender_text = "mężczyzn"

if time_5km_seconds < min_safe_time:
    min_safe_display = f"{min_safe_time//60}:{min_safe_time%60:02d}"
    st.sidebar.warning(
        f"⚠️ Czas {time_5km_display} jest szybszy niż najlepszy w danych treningowych ({min_safe_display} dla {gender_text}). "
        f"Predykcja może być mniej dokładna (ekstrapolacja)."
    )
elif time_5km_seconds > max_safe_time:
    max_safe_display = f"{max_safe_time//60}:{max_safe_time%60:02d}"
    st.sidebar.warning(
        f"⚠️ Czas {time_5km_display} jest wolniejszy niż najwolniejszy w danych treningowych ({max_safe_display} dla {gender_text}). "
        f"Predykcja może być mniej dokładna (ekstrapolacja)."
    )

# Przycisk do przewidywania lub reset
if st.session_state.get('prediction_done', False):
    # Jeśli już wykonano predykcję, pokaż przycisk resetu
    st.sidebar.success(f"✅ Aktywna predykcja dla: **{st.session_state.user_name}**")
    if st.sidebar.button(
        "🔄 Nowa predykcja",
        type="secondary",
        use_container_width=True
    ):
        # Wyczyść session_state i przeładuj
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Przycisk do przewidywania
predict_button = st.sidebar.button(
    "🚀 Przewiduj mój czas!",  # Tekst przycisku
    type="primary",  # Styl przycisku (primary = niebieski)
    use_container_width=True  # Przycisk na całą szerokość
)

# ============================================
# INICJALIZACJA SESSION STATE
# ============================================
# Jeśli kliknięto przycisk, zapisz dane w session_state
if predict_button:
    st.session_state.prediction_done = True
    st.session_state.user_name = user_name
    st.session_state.gender = gender
    st.session_state.age = age
    st.session_state.time_5km_seconds = time_5km_seconds
    st.session_state.time_5km_minutes = time_5km_minutes
    st.session_state.time_5km_display = time_5km_display

# ============================================
# SEKCJA GŁÓWNA - PLACEHOLDER
# ============================================
if not st.session_state.get('prediction_done', False):  # Jeśli nie wykonano jeszcze predykcji
    st.info("👈 Wypełnij formularz w panelu bocznym i kliknij '🚀 Przewiduj mój czas!'")  # Info

else:  # Jeśli wykonano predykcję (zapisaną w session_state)
    # Odczytaj dane z session_state
    user_name = st.session_state.user_name
    gender = st.session_state.gender
    age = st.session_state.age
    time_5km_seconds = st.session_state.time_5km_seconds
    time_5km_minutes = st.session_state.time_5km_minutes
    time_5km_display = st.session_state.time_5km_display
    
    # Walidacja danych
    if not user_name.strip():  # Jeśli imię puste
        st.error("❌ Proszę podać imię lub nick!")  # Błąd
        st.stop()  # Zatrzymaj
    
    # ============================================
    # PRZEWIDYWANIE CZASU (tylko raz, potem cache w session_state)
    # ============================================
    if 'prediction_result' not in st.session_state:
        st.success(f"✅ Witaj, {user_name}! Trwa przewidywanie...")  # Potwierdzenie
        
        with st.spinner("🤖 Trwa przewidywanie czasu..."):
            # Przygotuj dane wejściowe
            df_input = prepare_input_data(
                gender=gender,  # Płeć
                age=age,  # Wiek
                time_5km_seconds=time_5km_seconds,  # Czas na 5km w sekundach
                country=DEFAULT_COUNTRY  # Kraj (POL)
            )
            
            # Wykonaj predykcję
            prediction_result = predict_time(model, df_input)  # Przewiduj czas
            
            # Zapisz w session_state
            st.session_state.prediction_result = prediction_result
    else:
        # Odczytaj z cache
        prediction_result = st.session_state.prediction_result
    
    # ============================================
    # WYŚWIETL WYNIK PREDYKCJI - PREMIUM CARD
    # ============================================
    st.markdown(f"""
    <div class="prediction-box">
        <div class="prediction-label">🎯 Przewidywany czas końcowy dla <strong>{user_name}</strong></div>
        <div class="prediction-time">{prediction_result["time_formatted"]}</div>
        <div class="prediction-pace">⚡ Tempo: {prediction_result['pace_per_km']} na kilometr</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # OBLICZ STATYSTYKI (tylko raz, potem cache)
    # ============================================
    if 'age_category' not in st.session_state:
        # Kategoria wiekowa (przekaż płeć do funkcji)
        age_category = calculate_age_category(age, gender)  # Oblicz kategorię z uwzględnieniem płci
        
        # Płeć po polsku (do wyświetlania)
        gender_pl = "mężczyzn" if gender == 'M' else "kobiet"
        
        # Statystyki kategorii
        category_stats = get_category_stats(df_historical, age_category, gender)  # Statystyki
        
        # Szacowana pozycja
        ranking_general = estimate_ranking(
            df_historical,
            prediction_result['time_seconds'],
            gender
        )  # Pozycja ogólna
        
        ranking_category = estimate_ranking(
            df_historical,
            prediction_result['time_seconds'],
            gender,
            age_category
        )  # Pozycja w kategorii
        
        # Zapisz w session_state
        st.session_state.age_category = age_category
        st.session_state.gender_pl = gender_pl
        st.session_state.category_stats = category_stats
        st.session_state.ranking_general = ranking_general
        st.session_state.ranking_category = ranking_category
    else:
        # Odczytaj z cache
        age_category = st.session_state.age_category
        gender_pl = st.session_state.gender_pl
        category_stats = st.session_state.category_stats
        ranking_general = st.session_state.ranking_general
        ranking_category = st.session_state.ranking_category
    
    # ============================================
    # SEKCJA STATYSTYK - PREMIUM CARDS
    # ============================================
    st.markdown("---")
    st.markdown('<div class="section-header">📊 Statystyki i Porównania</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Kolumny dla statystyk
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card orange">
            <div class="stat-card-title">🏅 Klasyfikacja Ogólna</div>
        </div>
        """, unsafe_allow_html=True)
        if ranking_general['estimated_position']:
            # Formatowanie liczb ze spacją jako separatorem tysięcy
            pos_formatted = f"{ranking_general['estimated_position']:,}".replace(',', ' ')
            total_formatted = f"{ranking_general['total_runners']:,}".replace(',', ' ')
            st.metric(
                "Szacowana pozycja",
                f"{pos_formatted}/{total_formatted}",
                help="Twoja przewidywana pozycja wśród wszystkich uczestników"
            )
            # Progress bar
            percentile = 100 - ranking_general['faster_than_percent']
            st.progress(percentile / 100)
            st.markdown(f"**✨ Szybszy niż:** {ranking_general['faster_than_percent']}% zawodników")
        else:
            st.info("Brak danych")
    
    with col2:
        st.markdown(f"""
        <div class="stat-card blue">
            <div class="stat-card-title">🎖️ Kategoria {age_category}</div>
        </div>
        """, unsafe_allow_html=True)
        if ranking_category['estimated_position']:
            # Formatowanie liczb ze spacją jako separatorem tysięcy
            pos_cat_formatted = f"{ranking_category['estimated_position']:,}".replace(',', ' ')
            total_cat_formatted = f"{ranking_category['total_runners']:,}".replace(',', ' ')
            st.metric(
                "Pozycja w kategorii",
                f"{pos_cat_formatted}/{total_cat_formatted}",
                help=f"Twoja pozycja w kategorii wiekowej {age_category}"
            )
            # Progress bar
            percentile_cat = 100 - ranking_category['faster_than_percent']
            st.progress(percentile_cat / 100)
            st.markdown(f"**✨ Szybszy niż:** {ranking_category['faster_than_percent']}% w kategorii")
        else:
            st.info("Brak danych")
    
    with col3:
        st.markdown("""
        <div class="stat-card green">
            <div class="stat-card-title">📈 Średnie czasy</div>
        </div>
        """, unsafe_allow_html=True)
        if category_stats['count'] > 0:
            st.metric(
                "Średnia w kategorii",
                format_time_from_seconds(category_stats['mean']),
                help="Średni czas w Twojej kategorii wiekowej"
            )
            # Formatowanie liczby zawodników ze spacją jako separatorem
            count_formatted = f"{category_stats['count']:,}".replace(',', ' ')
            st.markdown(f"**👥 Zawodników:** {count_formatted}")
            st.markdown(f"**📊 Mediana:** {format_time_from_seconds(category_stats['median'])}")
            st.markdown(f"**🏆 Najlepszy:** {format_time_from_seconds(category_stats['min'])}")
        else:
            st.info("Brak danych")
    
    # ============================================
    # KOMENTARZ AI (OPENAI) - generuj tylko raz
    # ============================================
    if openai_client:  # Jeśli OpenAI dostępne
        st.markdown("---")
        st.markdown('<div class="section-header">🤖 Komentarz Trenera AI</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if 'commentary' not in st.session_state:
            with st.spinner("Generuję spersonalizowany komentarz..."):
                # Generuj komentarz (Langfuse wrapper automatycznie loguje)
                commentary = generate_commentary(
                    client=openai_client,
                    user_name=user_name,
                    predicted_time_formatted=prediction_result['time_formatted'],
                    gender=gender,
                    age=age,
                    age_category=age_category,
                    category_stats=category_stats,
                    ranking_info=ranking_category
                )
                
                # Zapisz w session_state
                st.session_state.commentary = commentary
        else:
            # Odczytaj z cache
            commentary = st.session_state.commentary
        
        if commentary:  # Jeśli wygenerowano komentarz
            st.markdown(f"""
            <div class="ai-box">
                <strong>💬 {user_name}, oto moja analiza Twojego wyniku:</strong><br><br>
                {commentary}
            </div>
            """, unsafe_allow_html=True)
    
    # ============================================
    # ZWYCIĘZCY Z KATEGORII UŻYTKOWNIKA
    # ============================================
    st.markdown("---")
    st.markdown('<div class="section-header">🏆 Zwycięzcy z Twojej Kategorii</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"**📍 Twoja kategoria:** {age_category} ({gender_pl})")
    
    # Pobierz wszystkich zwycięzców
    all_winners = get_winners_by_category(df_historical)
    
    # Filtruj tylko zwycięzców z kategorii użytkownika
    user_category_winners = all_winners[
        (all_winners['Kategoria wiekowa'] == age_category) &
        (all_winners['Płeć'] == gender)
    ].copy()
    
    if len(user_category_winners) > 0:
        # Przygotuj DataFrame do wyświetlenia
        if '5km_formatted' in user_category_winners.columns:
            display_cols = ['Rok', 'Imię i nazwisko', 'Czas_formatted', '5km_formatted', 'Kraj']
            col_names = ['Rok', 'Zawodnik', 'Czas końcowy', 'Czas 5km', 'Kraj']
        else:
            display_cols = ['Rok', 'Imię i nazwisko', 'Czas_formatted', 'Kraj']
            col_names = ['Rok', 'Zawodnik', 'Czas końcowy', 'Kraj']
        
        winners_display = user_category_winners[display_cols].copy()
        winners_display.columns = col_names
        
        st.dataframe(
            winners_display,
            use_container_width=True,
            hide_index=True
        )
        
        # Dodaj informację porównawczą
        best_time = user_category_winners['Czas_sekundy'].min()
        diff_to_winner = prediction_result['time_seconds'] - best_time
        
        if diff_to_winner > 0:
            st.info(f"📈 Twój przewidywany czas jest o **{diff_to_winner//60} min {diff_to_winner%60} s** wolniejszy od najlepszego czasu w Twojej kategorii")
        else:
            st.success(f"🚀 Gratulacje! Twój przewidywany czas jest lepszy niż najlepszy zarejestrowany wynik!")
    else:
        st.warning(f"Brak danych o zwycięzcach w kategorii {age_category} dla płci {gender_pl}")
    
    # ============================================
    # SYMULATOR CZASÓW
    # ============================================
    st.markdown("---")
    st.markdown('<div class="section-header">🎮 Symulator Czasów</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <strong>💡 Jak to działa?</strong><br>
        Dostosuj parametry poniżej i kliknij przycisk, aby zobaczyć jak zmiana wieku, płci lub czasu na 5km wpływa na przewidywany czas końcowy.
    </div>
    """, unsafe_allow_html=True)
    
    # Formularz - blokuje reruns do momentu kliknięcia submit
    with st.form(key="simulator_form"):
        # Suwaki symulacji
        sim_col1, sim_col2 = st.columns(2)
        
        with sim_col1:
            sim_age = st.slider(
                "Wiek:",
                min_value=MIN_AGE,
                max_value=MAX_AGE,
                value=age,
                key="sim_age_slider"
            )
        
        with sim_col2:
            sim_gender_display = st.selectbox(
                "Płeć:",
                options=list(GENDER_MAPPING.keys()),
                index=0 if gender == 'M' else 1,
                key="sim_gender_select"
            )
            sim_gender = GENDER_MAPPING[sim_gender_display]
        
        # Czas na 5km z minutami i sekundami
        st.markdown("**Czas na 5 km:**")
        sim_time_col1, sim_time_col2 = st.columns(2)
        
        with sim_time_col1:
            sim_time_5km_minutes = st.number_input(
                "Minuty:",
                min_value=MIN_TIME_5KM,
                max_value=MAX_TIME_5KM,
                value=time_5km_minutes,
                step=1,
                key="sim_time_5km_min"
            )
        
        with sim_time_col2:
            sim_time_5km_seconds_only = st.number_input(
                "Sekundy:",
                min_value=0,
                max_value=59,
                value=time_5km_seconds_only,
                step=1,
                key="sim_time_5km_sec"
            )
        
        # Przycisk submit w formularzu
        submit_button = st.form_submit_button("🚀 Symulacja dla nowych parametrów", type="primary", use_container_width=True)
    
    # Wykonaj symulację tylko po kliknięciu przycisku
    if submit_button:
        # Oblicz całkowity czas w sekundach
        sim_time_5km_seconds = sim_time_5km_minutes * 60 + sim_time_5km_seconds_only
        sim_time_5km_display = f"{sim_time_5km_minutes:02d}:{sim_time_5km_seconds_only:02d}"
        
        with st.spinner("Obliczam..."):
            # Przygotuj dane symulacji
            sim_df_input = prepare_input_data(
                gender=sim_gender,
                age=sim_age,
                time_5km_seconds=sim_time_5km_seconds,
                country=DEFAULT_COUNTRY
            )
            
            # Przewiduj
            sim_prediction = predict_time(model, sim_df_input)
            
            # Wyświetl wynik symulacji
            st.markdown("---")
            st.markdown(f"**Parametry symulacji:** Wiek: {sim_age}, Płeć: {sim_gender_display}, Czas 5km: {sim_time_5km_display} ({sim_time_5km_seconds}s)")
            st.success(f"### 🎯 Przewidywany czas: **{sim_prediction['time_formatted']}**")
            st.info(f"**Tempo:** {sim_prediction['pace_per_km']}")
            
            # Porównaj z oryginalnym wynikiem
            diff_seconds = sim_prediction['time_seconds'] - prediction_result['time_seconds']
            if diff_seconds > 0:
                st.warning(f"⬆️ Wolniejszy o {abs(diff_seconds)//60} min {abs(diff_seconds)%60} s względem Twojego wyniku")
            elif diff_seconds < 0:
                st.success(f"⬇️ Szybszy o {abs(diff_seconds)//60} min {abs(diff_seconds)%60} s względem Twojego wyniku")
            else:
                st.info("➡️ Identyczny czas jak Twój wynik")
    
    # ============================================
    # EKSPORT DANYCH DO EXCELA
    # ============================================
    st.markdown("---")
    st.markdown("### 📥 Eksport Danych")
    st.markdown("""
    <div class="info-box">
        <strong>📊 Dostępne dane:</strong><br>
        Pełna baza wyników Półmaratonu Wrocławskiego z lat 2023-2024 (21 957 rekordów) w formacie Excel.
    </div>
    """, unsafe_allow_html=True)
    
    # Przycisk do pobrania pre-generowanego pliku Excel
    # Ścieżka względem lokalizacji app.py (działa lokalnie i na Streamlit Cloud)
    excel_file_path = os.path.join(os.path.dirname(__file__), "data", "polmaraton_wroclaw_2023_2024.xlsx")
    
    try:
        with open(excel_file_path, "rb") as file:
            excel_data = file.read()
        
        st.download_button(
            label="⬇️ Pobierz pełne dane (Excel)",
            data=excel_data,
            file_name=f"polmaraton_wroclaw_{EVENT_YEARS[0]}_{EVENT_YEARS[1]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    except FileNotFoundError:
        st.error("❌ Plik Excel nie został znaleziony. Skontaktuj się z administratorem.")
    
# ============================================
# STOPKA
# ============================================
st.sidebar.markdown("---")  # Separator
st.sidebar.caption("🤖 Powered by AI & PyCaret")  # Stopka
st.sidebar.caption(f"📊 Dane: {EVENT_NAME} {EVENT_YEARS[0]}-{EVENT_YEARS[1]}")  # Info o danych
