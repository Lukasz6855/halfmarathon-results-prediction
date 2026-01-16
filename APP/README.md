# 🏃 Aplikacja Przewidywania Czasu w Półmaratonie

> **Aplikacja Streamlit** do przewidywania czasu końcowego w Półmaratonie Wrocławskim na podstawie danych historycznych z lat 2023-2024.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![PyCaret](https://img.shields.io/badge/PyCaret-3.0+-green.svg)](https://pycaret.org/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)]()

---

## 📋 Spis Treści

- [Funkcje](#-funkcje)
- [Demo](#-demo)
- [Jak to działa](#-jak-to-działa)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Konfiguracja](#️-konfiguracja)
- [Uruchomienie](#-uruchomienie)
- [Struktura Projektu](#-struktura-projektu)
- [API Keys](#-jak-zdobyć-klucze-api)
- [Troubleshooting](#-rozwiązywanie-problemów)
- [FAQ](#-faq)
- [Autor](#-autor)

---

## 🎯 Funkcje

### ✨ Główne funkcjonalności:

| Funkcja | Opis | Status |
|---------|------|--------|
| **🤖 Przewidywanie ML** | Model wytrenowany na 21,957 wynikach | ✅ Aktywne |
| **📊 Statystyki** | Porównanie z poprzednimi edycjami | ✅ Aktywne |
| **🏆 Ranking** | Szacowana pozycja w klasyfikacji | ✅ Aktywne |
| **💬 Komentarze AI** | GPT-4 analizuje Twój wynik | 🔌 Opcjonalne |
| **🎮 Symulator** | Testuj różne scenariusze | ✅ Aktywne |
| **📥 Export Excel** | Pobierz dane historyczne | ✅ Aktywne |
| **📈 Monitoring** | Langfuse tracking LLM | 🔌 Opcjonalne |

### 🎨 Interfejs użytkownika:

- **Responsywny design** - działa na desktop i mobile
- **Interaktywne wykresy** - wizualizacje statystyk
- **Cache'owanie** - szybkie przeładowanie bez ponownych obliczeń
- **Dark mode friendly** - przyjazny dla oka

---

## 📺 Demo

### Przykładowy widok aplikacji:

```
┌─────────────────────────────────────────────────────┐
│  🏃 Przewidywanie Czasu - Półmaraton Wrocławski     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Panel boczny:                                      │
│  ├─ Imię: Jan                                      │
│  ├─ Płeć: Mężczyzna                                │
│  ├─ Wiek: 35                                       │
│  └─ Czas 5km: 25:00                                │
│                                                     │
│  [🚀 Przewiduj mój czas!]                          │
│                                                     │
├─────────────────────────────────────────────────────┤
│  📊 TWÓJ PRZEWIDYWANY CZAS                          │
│  1:52:34  (tempo: 5:20/km)                         │
├─────────────────────────────────────────────────────┤
│  📈 Statystyki i Porównania                         │
│  ├─ Pozycja ogólna: 2,450 / 10,876                │
│  │  Szybszy niż: 77.5% zawodników                  │
│  ├─ Pozycja w kategorii M35: 421 / 1,234          │
│  │  Szybszy niż: 65.9% w kategorii                │
│  └─ Średnia w kategorii: 2:05:23                   │
└─────────────────────────────────────────────────────┘
```

---

## 🔬 Jak to działa?

### Pipeline predykcji:

```
1. Użytkownik wprowadza dane
   └─> Płeć, Wiek, Czas na 5km
       │
2. Przygotowanie danych
   └─> Konwersja: minuty → sekundy
       └─> Obliczenie: wiek → rocznik
           │
3. Model ML (PassiveAggressiveRegressor)
   └─> Input: [Płeć, 5km_sekundy, Rocznik]
       └─> Output: Czas_końcowy (sekundy)
           │
4. Post-processing
   └─> Konwersja: sekundy → HH:MM:SS
       └─> Obliczenie: tempo/km
           │
5. Statystyki historyczne
   └─> Porównanie z danymi 2023-2024
       └─> Ranking, percentyl, kategoria
           │
6. Opcjonalnie: AI Commentary
   └─> OpenAI GPT-4 generuje komentarz
       └─> Langfuse loguje wywołanie
```

### Model ML:

- **Algorytm**: PassiveAggressiveRegressor  
- **Dokładność**: MAE = 297.6 sekund (~5 minut)  
- **Cechy**: 3 parametry (Płeć, Czas_5km, Rocznik)  
- **Dane treningowe**: 21,957 wyników (2023-2024)

---

## 💻 Wymagania

### Python:
- **Wersja**: Python 3.10+ (zalecane 3.11)

### Konta/Klucze API:

| Usługa | Wymagane | Opis |
|--------|----------|------|
| **Vercel Blob** | ✅ TAK | Hosting modelu ML |
| **OpenAI** | ❌ NIE | Komentarze AI (opcjonalne) |
| **Langfuse** | ❌ NIE | Monitoring LLM (opcjonalne) |

---

## 🔧 Instalacja

### 1. Przejdź do folderu APP
```bash
cd APP
```

### 2. Utwórz wirtualne środowisko
```bash
python -m venv venv
```

### 3. Aktywuj środowisko

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

**Czas instalacji**: ~5-10 minut (PyCaret ma wiele zależności)

---

## ⚙️ Konfiguracja

### 1. Utwórz plik `.env`

Skopiuj `.env.example` (jeśli istnieje) lub utwórz nowy plik `.env`:

```env
# ============================================
# WYMAGANE - Vercel Blob (do pobrania modelu)
# ============================================
BLOB_READ_WRITE_TOKEN=vercel_blob_rw_xxxxxxxxxxxxx

# ============================================
# OPCJONALNE - OpenAI (komentarze AI)
# ============================================
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# ============================================
# OPCJONALNE - Langfuse (monitoring LLM)
# ============================================
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxxxxxxx
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxxxxxx
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

⚠️ **Uwaga**: Plik `.env` jest w `.gitignore` - nie zostanie wysłany na GitHub!

### 2. Zaktualizuj URL modelu w `config.py`

Po wytrenowaniu modelu (w notebooku `EDA-ML/`), skopiuj URL z output komórki 69 i wklej do:

```python
# config.py (linia ~58)
VERCEL_BLOB_MODEL_URL = "https://xxx.vercel-storage.com/models/halfmarathon_model_3features_YYYYMMDD_HHMMSS.pkl"
```

### 3. Sprawdź dostępność danych

Upewnij się, że plik istnieje:
```
data/halfmarathon_2023_2024.csv
```

Jeśli nie ma - uruchom komórkę 78 w notebooku ML (eksport danych).

---

## 🚀 Uruchomienie

### Uruchom aplikację Streamlit:
```bash
streamlit run app.py
```

Aplikacja uruchomi się pod adresem: **http://localhost:8501**

### Pierwsze uruchomienie:

1. **Panel boczny** - wypełnij formularz:
   - Imię/Nick: `Jan` lub `Anna`
   - Płeć: `Mężczyzna` / `Kobieta`
   - Wiek: `18-99 lat`
   - Czas na 5km: `10-90 minut` + sekundy

2. **Kliknij**: `🚀 Przewiduj mój czas!`

3. **Zobacz wyniki**:
   - ✅ Przewidywany czas końcowy (HH:MM:SS)
   - ✅ Tempo na kilometr (MM:SS/km)
   - ✅ Pozycja w klasyfikacji ogólnej
   - ✅ Pozycja w kategorii wiekowej
   - ✅ Statystyki średnich czasów
   - ✅ Komentarz AI (jeśli OpenAI skonfigurowane)
   - ✅ Tabela zwycięzców
   - ✅ Symulator czasów

---

## 📁 Struktura Projektu

```
APP/
├── app.py                          # Główna aplikacja Streamlit
├── config.py                       # Konfiguracja (stałe, URL modelu)
├── requirements.txt                # Zależności Python
├── .env                            # Klucze API (nie commitować!)
├── .gitignore                      # Pliki ignorowane przez Git
├── README.md                       # Ten plik
├── CHECKLIST.md                    # Checklist uruchomienia
│
├── data/                           # Dane historyczne
│   └── halfmarathon_2023_2024.csv  # 21,957 wyników (2023+2024)
│
├── model/                          # Modele lokalne (opcjonalnie)
│   └── (modele cachowane z Blob)
│
└── utils/                          # Moduły pomocnicze
    ├── __init__.py                 # Package init
    ├── data_loader.py              # Ładowanie danych CSV
    ├── model_loader.py             # Pobieranie modelu z Vercel Blob
    ├── predictor.py                # Predykcja czasu
    ├── stats_calculator.py         # Statystyki i ranking
    ├── openai_helper.py            # Integracja OpenAI + Langfuse
    └── langfuse_helper.py          # Helper Langfuse (legacy)
```

### Opis modułów:

| Moduł | Funkcje | Opis |
|-------|---------|------|
| `data_loader.py` | `load_historical_data()` | Wczytanie CSV + konwersja czasu |
| `model_loader.py` | `load_model_from_blob()` | Pobieranie modelu z Vercel |
| `predictor.py` | `predict_time()` | Predykcja + formatowanie |
| `stats_calculator.py` | `estimate_ranking()` | Obliczenia statystyczne |
| `openai_helper.py` | `generate_commentary()` | Komentarze AI (GPT-4) |

---

## 🔑 Jak zdobyć klucze API?

### 1️⃣ Vercel Blob (WYMAGANE)

**Krok 1**: Załóż konto  
👉 https://vercel.com/signup

**Krok 2**: Utwórz Blob Store  
- Dashboard → Storage → **Create Database** → **Blob Store**
- Nadaj nazwę: `halfmarathon-models`

**Krok 3**: Wygeneruj token  
- Settings → Tokens → **Create Token**
- **Uprawnienia**: Read & Write
- Skopiuj token → wklej do `.env` jako `BLOB_READ_WRITE_TOKEN`

---

### 2️⃣ OpenAI (OPCJONALNE)

**Krok 1**: Załóż konto  
👉 https://platform.openai.com/signup

**Krok 2**: Doładuj konto  
- Billing → **Add payment method**
- Minimum: $5 (wystarczy na ~200-500 komentarzy)

**Krok 3**: Wygeneruj klucz API  
- API Keys → **Create new secret key**
- Skopiuj klucz → wklej do `.env` jako `OPENAI_API_KEY`

**Koszt**: ~$0.001-0.002 za komentarz (model `gpt-4o-mini`)

---

### 3️⃣ Langfuse (OPCJONALNE)

**Krok 1**: Załóż konto  
👉 https://cloud.langfuse.com/auth/sign-up

**Krok 2**: Utwórz projekt  
- **Create Project** → Nadaj nazwę: `Halfmarathon Predictor`

**Krok 3**: Skopiuj klucze API  
- Project Settings → **API Keys**
- Skopiuj:
  - `Secret Key` → `LANGFUSE_SECRET_KEY`
  - `Public Key` → `LANGFUSE_PUBLIC_KEY`

**Langfuse**: Darmowy tier (50k events/miesiąc) - wystarczy!

---

## 📊 Dane Treningowe

### Źródło:
- **Wydarzenie**: Półmaraton Wrocławski
- **Lata**: 2023 i 2024
- **Rekordów**: 21,957 (po czyszczeniu)

### Statystyki:

| Kategoria | Wartość |
|-----------|---------|
| **Mężczyźni** | 10,876 (50.0%) |
| **Kobiety** | 11,081 (50.0%) |
| **Najszybszy czas** | 1:03:17 (M) |
| **Średni czas** | 1:58:42 |
| **Kategorie wiekowe** | 18 (M18-M70, K18-K70) |

---

## 🐛 Rozwiązywanie Problemów

### ❌ Błąd: `ModuleNotFoundError: No module named 'streamlit'`
**Rozwiązanie**:
```bash
pip install -r requirements.txt
```

---

### ❌ Błąd: `BLOB_READ_WRITE_TOKEN not found`
**Rozwiązanie**:
1. Sprawdź czy plik `.env` istnieje w folderze `APP/`
2. Token musi być bez cudzysłowów:
   ```env
   # ✅ DOBRZE:
   BLOB_READ_WRITE_TOKEN=vercel_blob_rw_xxx
   
   # ❌ ŹLE:
   BLOB_READ_WRITE_TOKEN="vercel_blob_rw_xxx"
   ```

---

### ❌ Błąd: `Cannot load model from URL`
**Możliwe przyczyny**:
1. **URL nieprawidłowy** - sprawdź `config.py` linia ~58
2. **Token wygasł** - wygeneruj nowy w Vercel
3. **Brak połączenia** - sprawdź internet

**Debug**:
```python
# Otwórz Python console i sprawdź:
import requests
import os
token = os.getenv("BLOB_READ_WRITE_TOKEN")
print(f"Token: {token[:20]}...")  # Pierwsze 20 znaków
```

---

### ❌ Błąd: `KeyError: '5 km Czas_sekundy'`
**Rozwiązanie**:
- Plik CSV nie ma wymaganej kolumny
- Uruchom ponownie komórkę 78 w notebooku ML (eksport danych)

---

### ⚠️ Komentarze AI nie działają
**Możliwe przyczyny**:
1. Brak `OPENAI_API_KEY` w `.env`
2. Brak środków na koncie OpenAI
3. Nieprawidłowy klucz (sprawdź na platform.openai.com)

**Info**: Aplikacja działa bez AI - to funkcja opcjonalna!

---

### 🐌 Aplikacja ładuje się długo (pierwsze uruchomienie)
**To normalne!**
- Pobieranie modelu z Vercel: ~5-10 sekund
- Inicjalizacja PyCaret: ~2-3 sekundy
- **Kolejne uruchomienia**: <1 sekunda (dzięki cache)

---

## ❓ FAQ

### 1. Czy mogę użyć aplikacji offline?
**NIE** - model jest hostowany na Vercel Blob. Można go jednak pobrać lokalnie i zmienić `model_loader.py`.

### 2. Jak dokładne są predykcje?
**MAE ~5 minut**. Dla większości zawodników błąd wynosi 3-7 minut.

### 3. Czy mogę dodać swoje dane?
**TAK** - dodaj nowe rekordy do CSV i przetrenuj model w notebooku ML.

### 4. Ile kosztuje hosting?
- **Vercel Blob**: Darmowy tier (10 GB)
- **Streamlit**: Darmowy tier (public apps)
- **OpenAI**: ~$0.001 za predykcję z komentarzem

### 5. Czy mogę zmienić wydarzenie (np. Maraton Warszawski)?
**TAK** - potrzebujesz tylko:
1. Nowe dane CSV (z analogicznymi kolumnami)
2. Przetrenować model w notebooku
3. Zaktualizować `config.py` (nazwa wydarzenia, lata, itp.)

---

## 👨‍💻 Autor

Projekt stworzony w ramach kursu **"Od Zera do AI"**  
**Moduł 9**: Machine Learning - Predykcja czasu w biegu

---

## 📄 Licencja

- **Kod**: Do użytku edukacyjnego
- **Dane**: Publicznie dostępne wyniki Półmaratonu Wrocławskiego
- **Model ML**: Własność autora projektu

---

## 🙏 Podziękowania

- **Półmaraton Wrocławski** - za udostępnienie wyników
- **PyCaret** - za framework AutoML
- **Streamlit** - za framework webowy
- **OpenAI** - za API GPT-4
- **Langfuse** - za monitoring LLM

---

**Potrzebujesz pomocy?**  
📖 Sprawdź [CHECKLIST.md](CHECKLIST.md) - szczegółowy przewodnik uruchomienia  
📖 Sprawdź [EDA-ML/README.md](../EDA-ML/README.md) - dokumentacja trenowania modelu

**Problemy?**  
👉 Sekcja [Troubleshooting](#-rozwiązywanie-problemów)  
👉 Sprawdź logi w konsoli

---

Made with ❤️ and Python 🐍

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

## ⚙️ Konfiguracja

### 1. Utwórz plik `.env` z kluczami API

Skopiuj plik `.env.example` i uzupełnij wartości:

```bash
copy .env.example .env
```

**Minimalna konfiguracja (tylko model):**
```env
BLOB_READ_WRITE_TOKEN=your_vercel_blob_token_here
```

**Pełna konfiguracja (z AI i monitoringiem):**
```env
BLOB_READ_WRITE_TOKEN=your_vercel_blob_token_here
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxxxxxxx
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxxxxxx
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 2. Uzupełnij URL modelu w `config.py`

Po wytrenowaniu i uploadzie modelu do Vercel Blob, skopiuj URL i wklej do pliku `config.py`:

```python
# config.py (linia ~44)
VERCEL_BLOB_MODEL_URL = "https://twoj-url-do-modelu.vercel-storage.com/..."
```

### 3. Sprawdź dostępność danych

Upewnij się, że plik `data/halfmarathon_2023_2024.csv` istnieje. Jeśli nie, uruchom komórkę eksportu w notebooku ML (`halfmarathon_model_pipeline.ipynb` - komórka 74).

## 🚀 Uruchomienie

### Uruchom aplikację Streamlit

```bash
streamlit run app.py
```

Aplikacja uruchomi się domyślnie pod adresem: **http://localhost:8501**

### Pierwsze uruchomienie

1. **Wypełnij formularz** w panelu bocznym:
   - Imię/Nick
   - Płeć (Mężczyzna/Kobieta)
   - Wiek (18-99 lat)
   - Czas na 5km (10-90 minut)

2. **Kliknij "🚀 Przewiduj mój czas!"**

3. **Zobacz wyniki**:
   - Przewidywany czas końcowy
   - Tempo na kilometr
   - Pozycja w klasyfikacji
   - Statystyki kategorii wiekowej
   - Komentarz trenera AI (jeśli OpenAI skonfigurowane)

4. **Eksperymentuj** z symulatorem czasów

## 📁 Struktura Projektu

```
APP/
│
├── app.py                      # Główna aplikacja Streamlit
├── config.py                   # Konfiguracja (stałe, ustawienia)
├── requirements.txt            # Zależności Python
├── .env.example                # Szablon zmiennych środowiskowych
├── .gitignore                  # Pliki ignorowane przez Git
├── README.md                   # Ta instrukcja
│
├── data/                       # Dane historyczne
│   └── halfmarathon_2023_2024.csv
│
└── utils/                      # Moduły pomocnicze
    ├── __init__.py
    ├── data_loader.py          # Ładowanie danych CSV
    ├── model_loader.py         # Pobieranie modelu z Vercel Blob
    ├── predictor.py            # Logika przewidywania
    ├── stats_calculator.py     # Obliczanie statystyk
    ├── openai_helper.py        # Integracja z OpenAI
    └── langfuse_helper.py      # Monitoring LLM
```

## 🔑 Jak zdobyć klucze API?

### Vercel Blob Storage (WYMAGANE)

1. Załóż konto na [Vercel](https://vercel.com/)
2. Przejdź do: **Storage** → **Blob** → **Create Store**
3. Wygeneruj token: **Settings** → **Tokens** → **Create Token**
4. Skopiuj token do `.env`

### OpenAI (OPCJONALNE - dla komentarzy AI)

1. Załóż konto na [OpenAI](https://platform.openai.com/)
2. Przejdź do: **API Keys** → **Create new secret key**
3. Skopiuj klucz do `.env`
4. Model używany: `gpt-4o-mini` (tani i szybki)

### Langfuse (OPCJONALNE - dla monitoringu)

1. Załóż konto na [Langfuse](https://cloud.langfuse.com/)
2. Utwórz projekt
3. Skopiuj klucze z ustawień projektu do `.env`

## 📊 Dane Treningowe

- **Źródło**: Półmaraton Wrocławski 2023 + 2024
- **Liczba rekordów**: 21,957
- **Kolumny**: Płeć, Wiek, Rocznik, Kategoria wiekowa, Czas na 5km, Kraj, Czas końcowy
- **Model**: Random Forest Regressor (PyCaret)
- **Metryka**: MAE ~2-3 minuty

## 🐛 Rozwiązywanie Problemów

### Błąd: "Brak BLOB_READ_WRITE_TOKEN"
✅ Upewnij się, że plik `.env` istnieje i zawiera poprawny token

### Błąd: "Brak VERCEL_BLOB_MODEL_URL"
✅ Uzupełnij URL w pliku `config.py` (linia ~44)

### Błąd: "Nie można załadować danych"
✅ Uruchom komórkę eksportu w notebooku ML (komórka 74)

### Aplikacja jest wolna
✅ To normalne przy pierwszym uruchomieniu (ładowanie modelu ~5-10 MB)
✅ Kolejne przewidywania są szybkie dzięki cache'owaniu

## 📝 Licencja

Projekt edukacyjny - Kurs "Od Zera do AI" (Moduł 9)

## 👨‍💻 Autor

Aplikacja stworzona jako projekt edukacyjny z wykorzystaniem:
- **Streamlit** - interfejs webowy
- **PyCaret** - training modelu ML
- **OpenAI GPT-4** - komentarze AI
- **Langfuse** - monitoring LLM
- **Vercel Blob** - storage modelu

---

🏃 **Powodzenia w przewidywaniu swoich czasów!** 🎯
