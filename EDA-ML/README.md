# 🤖 ML Pipeline - Trenowanie Modelu Przewidywania Czasu

> **Notebook do trenowania modelu Machine Learning** przewidującego czas końcowy w półmaratonie na podstawie danych historycznych z Półmaratonu Wrocławskiego 2023-2024.

---

## 📋 Spis Treści

- [Opis Projektu](#-opis-projektu)
- [Dane](#-dane)
- [Pipeline ML](#-pipeline-ml)
- [Struktura Notebooka](#-struktura-notebooka)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Uruchomienie](#-uruchomienie)
- [Wyniki](#-wyniki)
- [Eksport](#-eksport)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Opis Projektu

Ten notebook implementuje **kompletny pipeline Machine Learning** od surowych danych do gotowego modelu predykcyjnego:

### Cel:
Przewidywanie czasu końcowego w półmaratonie (21.1 km) na podstawie:
- **Płci** zawodnika (M/K)
- **Wieku** (przeliczonego na rocznik urodzenia)
- **Czasu na 5 km** w sekundach (kluczowy parametr)

### Dane źródłowe:
- **21,957 wyników** z Półmaratonu Wrocławskiego
- **2 edycje**: 2023 i 2024
- **Format**: CSV z danymi zawodników

---

## 📊 Dane

### Surowe dane wejściowe:
```
data/
├── Polmaraton_Wroclawski_2023.csv    # Edycja 2023
└── Polmaraton_Wroclawski_2024.csv    # Edycja 2024
```

### Kolumny wykorzystywane:
| Kolumna | Typ | Opis |
|---------|-----|------|
| `Płeć` | string | 'M' lub 'K' |
| `5 km Czas` | string | Format 'HH:MM:SS' (konwertowane na sekundy) |
| `Rocznik` | int | Rok urodzenia |
| `Czas` | string | Czas końcowy 'H:MM:SS' (cel predykcji) |
| `Kategoria wiekowa` | string | np. 'M35', 'K40' (do statystyk) |

### Przetwarzanie danych:

**1. Konwersja formatów:**
```python
# '5 km Czas' (tekst) → '5 km Czas_sekundy' (int)
'00:25:30' → 1530  # 25 minut 30 sekund = 1530 sekund
```

**2. Obliczanie rocz nika:**
```python
# Wiek → Rocznik
Wiek: 35 (w 2024) → Rocznik: 1989
```

**3. Data Leakage Prevention:**
- Usunięto kolumny z informacjami o czasie końcowym
- Zachowano tylko: `Płeć`, `5 km Czas_sekundy`, `Rocznik`

---

## 🔬 Pipeline ML

### Etapy pipeline:

```
1. Wczytanie danych          (CSV → DataFrame)
   ↓
2. Eksploracja danych         (EDA, statystyki, wizualizacje)
   ↓
3. Czyszczenie                (duplikaty, braki, outliers)
   ↓
4. Feature Engineering        (konwersja czasu, rocznik)
   ↓
5. Data Leakage Prevention    (usunięcie kolumn docelowych)
   ↓
6. Wybór cech                 (3 cechy: Płeć, 5km_sekundy, Rocznik)
   ↓
7. Setup PyCaret              (train/test split 80/20)
   ↓
8. Porównanie modeli          (15+ algorytmów)
   ↓
9. Tuning hiperparametrów     (Top 5 modeli, 10 iteracji)
   ↓
10. Wybór najlepszego         (min MAE)
   ↓
11. Finalizacja               (trening na 100% danych)
   ↓
12. Walidacja                 (5 przypadków testowych)
   ↓
13. Export                    (model + dane do Vercel/APP)
```

---

## 📓 Struktura Notebooka

### Sekcje notebooka:

**Krok 1-3: Przygotowanie środowiska**
- Import bibliotek
- Konfiguracja ścieżek
- Funkcje pomocnicze

**Krok 4-6: Wczytywanie i łączenie danych**
- Import plików CSV (2023 + 2024)
- Łączenie w jeden DataFrame
- Standaryzacja kolumn

**Krok 7-8: Eksploracja danych (EDA)**
- Podstawowe statystyki
- Rozkłady czasów
- Analiza kategorii wiekowych
- Wizualizacje

**Krok 9-10: Czyszczenie danych**
- Usuwanie duplikatów
- Obsługa braków danych
- Identyfikacja outlierów
- Filtrowanie nieprawidłowych wartości

**Krok 11: Feature Engineering**
- **Konwersja czasu** 'HH:MM:SS' → sekundy (int)
- **Obliczanie rocznika** z wieku
- **Data Leakage** - usunięcie kolumn docelowych

**Krok 12: Wybór cech (Feature Selection)**
```python
selected_features = [
    'Płeć',                 # Kategoryczna (M/K)
    '5 km Czas_sekundy',    # Numeryczna (int) - KLUCZ!
    'Rocznik'               # Numeryczna (int)
]
target = 'Czas_sekundy'     # Cel: czas w sekundach
```

**Krok 13: Setup PyCaret**
- Inicjalizacja środowiska ML
- Split: 80% train, 20% test
- Normalizacja, encoding

**Krok 14: Porównanie modeli**
- Testowanie 15+ algorytmów
- Metryki: MAE, RMSE, R², MAPE
- Wybór Top 5

**Krok 15: Tuning hiperparametrów**
- Optymalizacja Top 5 modeli
- 10 iteracji tuningu
- Grid Search / Random Search

**Krok 16: Wybór finalnego modelu**
- Porównanie PRZED vs PO tuningu
- Wybór modelu z najmniejszym MAE
- **Wynik**: PassiveAggressiveRegressor
  - **MAE: 297.6 sekund (~5 minut)**

**Krok 17: Finalizacja**
- Trening na pełnym datasecie (100%)
- Zapisanie metadanych

**Krok 18: Upload do Vercel Blob**
```python
# Model zapisywany jako:
halfmarathon_model_3features_YYYYMMDD_HHMMSS.pkl
```

**Krok 19: Walidacja**
- Przykładowe predykcje
- Formatowanie wyników (sekundy → HH:MM:SS)

**Krok 20: Testy walidacyjne**
- 5 przypadków testowych
- Weryfikacja różnych profili (szybcy/wolni, M/K, różne kategorie)

**Krok 21: Eksport danych**
- Export: `APP/data/halfmarathon_2023_2024.csv`
- Dane gotowe do użycia w aplikacji

---

## 💻 Wymagania

### Python:
- **Wersja**: Python 3.10+

### Biblioteki:
```txt
pandas>=2.0.0              # Manipulacja danymi
numpy>=1.24.0              # Operacje numeryczne
matplotlib>=3.7.0          # Wizualizacje
seaborn>=0.12.0            # Wizualizacje statystyczne
scikit-learn>=1.3.0        # Modele ML
pycaret[full]>=3.0.0       # AutoML framework
requests>=2.31.0           # API Vercel Blob
python-dotenv>=1.0.0       # Zmienne środowiskowe
```

---

## 🔧 Instalacja

### 1. Sklonuj repozytorium
```bash
cd EDA-ML/
```

### 2. Utwórz środowisko wirtualne
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 4. Skonfiguruj zmienne środowiskowe

Utwórz plik `.env` w folderze `EDA-ML/`:
```env
# Vercel Blob - do uploadu modelu
BLOB_READ_WRITE_TOKEN=vercel_blob_rw_xxxxxxxxxxxxx

# Opcjonalnie - ścieżki (domyślnie wykrywane automatycznie)
DATA_DIR=./data
MODEL_DIR=./model
PLOTS_DIR=./plots
```

### 5. Przygotuj dane

Umieść pliki CSV w folderze `data/`:
```
data/
├── Polmaraton_Wroclawski_2023.csv
└── Polmaraton_Wroclawski_2024.csv
```

---

## 🚀 Uruchomienie

### Uruchom Jupyter Notebook:
```bash
jupyter notebook halfmarathon_model_pipeline.ipynb
```

### Lub Jupyter Lab:
```bash
jupyter lab halfmarathon_model_pipeline.ipynb
```

### Wykonaj wszystkie komórki:
```
Kernel → Restart & Run All
```

**Czas wykonania**: ~10-15 minut (w zależności od sprzętu)

---

## 📈 Wyniki

### Finalny model:

**Algorytm**: PassiveAggressiveRegressor  
**MAE**: 297.6 sekund (~4.96 minut)  
**Dokładność**: ~5 minut błędu predykcji

### Przykładowe predykcje:

| Płeć | Wiek | Czas 5km | Predykcja | Rzeczywisty | Błąd |
|------|------|----------|-----------|-------------|------|
| M | 35 | 25:00 | 1:52:30 | 1:48:15 | +4:15 |
| K | 28 | 28:00 | 2:08:45 | 2:05:30 | +3:15 |
| M | 45 | 22:00 | 1:42:10 | 1:38:50 | +3:20 |

### Wizualizacje wygenerowane:
```
plots/
├── correlation_matrix.png          # Korelacje między cechami
├── target_distribution.png         # Rozkład czasu końcowego
├── feature_importance.png          # Ważność cech
└── predictions_vs_actual.png       # Predykcje vs rzeczywiste
```

---

## 📦 Eksport

### Po zakończeniu pipeline:

**1. Model ML:**
```
Uploadowany do Vercel Blob:
https://xxx.vercel-storage.com/models/halfmarathon_model_3features_YYYYMMDD_HHMMSS.pkl

Lokalnie zapisany w:
model/halfmarathon_model_simplified_3features.pkl
```

**2. Dane dla aplikacji:**
```
APP/data/halfmarathon_2023_2024.csv
- Zawiera wszystkie dane 2023+2024
- Gotowe do użycia w aplikacji Streamlit
```

**3. Metadane modelu:**
```json
{
  "model_type": "PassiveAggressiveRegressor",
  "training_date": "2026-01-15 22:41:49",
  "dataset_size": 21957,
  "features": ["Płeć", "5 km Czas_sekundy", "Rocznik"],
  "target": "Czas_sekundy",
  "mae_cv": 297.63,
  "mae_minutes": 4.96
}
```

---

## 🐛 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'pycaret'`
**Rozwiązanie**:
```bash
pip install pycaret[full]
```

### Problem: `KeyError: '5 km Czas'`
**Rozwiązanie**: Sprawdź nazwy kolumn w CSV. Notebook oczekuje:
- `Płeć`, `5 km Czas`, `Rocznik`, `Czas`, `Kategoria wiekowa`

### Problem: Upload do Vercel Blob nie działa
**Rozwiązanie**:
1. Sprawdź `BLOB_READ_WRITE_TOKEN` w `.env`
2. Token musi mieć uprawnienia **Read & Write**
3. Sprawdź połączenie internetowe

### Problem: MAE jest bardzo wysokie (> 500 sekund)
**Możliwe przyczyny**:
- Nieprawidłowa konwersja czasu (sprawdź funkcję `time_to_seconds()`)
- Outliers nie zostały usunięte
- Błędne mapowanie kategorii

### Problem: Notebook się zawiesza przy tuningu
**Rozwiązanie**:
- Zmniejsz liczbę iteracji: `tune_model(model, n_iter=5)` zamiast 10
- Zmniejsz liczbę modeli do tuningu (z 5 do 3)

---

## 📚 Dodatkowe Informacje

### Dlaczego 3 cechy?
- **Płeć**: Istotna różnica między mężczyznami a kobietami (~15-20% czasu)
- **5 km Czas**: Najsilniejszy predyktor (r=0.85+)
- **Rocznik**: Wiek wpływa na wydolność (krzywa spadkowa po 35 r.ż.)

### Dlaczego sekundy zamiast tekstu?
- Tekst 'HH:MM:SS' traktowany jako **kategoryczny** (1331 kategorii!)
- Model nie rozumie relacji: 1800s > 1500s
- **Sekundy (int)** = zmienna **numeryczna ciągła** ✅

### Alternatywne podejścia:
- **Więcej cech**: Dodanie `Kraj`, `Kategoria wiekowa` nie poprawiło MAE
- **Deep Learning**: Dla 22k rekordów - overkill, dłuższy trening, podobny wynik
- **Ensemble**: Może poprawić o ~1-2%, ale komplikuje deployment

---

## 📝 Następne Kroki

Po zakończeniu treningu:

1. ✅ Skopiuj **URL modelu** z output komórki 69 (Upload)
2. ✅ Wklej URL do `APP/config.py` (linia ~58)
3. ✅ Sprawdź czy plik `APP/data/halfmarathon_2023_2024.csv` istnieje
4. ✅ Przejdź do folderu `APP/` i uruchom aplikację Streamlit

```bash
cd ../APP
streamlit run app.py
```

---

## 👨‍💻 Autor

Projekt stworzony w ramach kursu **"Od Zera do AI"**  
**Moduł 9**: Machine Learning - Predykcja czasu w biegu

---

## 📄 Licencja

Dane: Publicznie dostępne wyniki Półmaratonu Wrocławskiego  
Kod: Do użytku edukacyjnego

---

**Potrzebujesz pomocy?** Sprawdź sekcję [Troubleshooting](#-troubleshooting) lub README w folderze `APP/`
