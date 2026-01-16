# ✅ CHECKLIST - Uruchomienie Aplikacji Streamlit

## Krok 1: Zakończ trening modelu ML

- [ ] Uruchom wszystkie komórki w notebooku `halfmarathon_model_pipeline.ipynb`
- [ ] Sprawdź czy model został przesłany do Vercel Blob (komórka finalna)
- [ ] Skopiuj URL modelu z outputu (będzie potrzebny w kroku 3)
- [ ] Uruchom komórkę 74 (eksport danych) - sprawdź czy plik `APP/data/halfmarathon_2023_2024.csv` został utworzony

## Krok 2: Przygotuj klucze API

### Vercel Blob (WYMAGANE):
- [ ] Załóż konto na https://vercel.com/
- [ ] Utwórz Blob Store: Storage → Blob → Create Store
- [ ] Wygeneruj token: Settings → Tokens → Create Token (Read & Write)
- [ ] Skopiuj token

### OpenAI (OPCJONALNE - dla komentarzy AI):
- [ ] Załóż konto na https://platform.openai.com/
- [ ] Wygeneruj API Key: API Keys → Create new secret key
- [ ] Skopiuj klucz

### Langfuse (OPCJONALNE - dla monitoringu):
- [ ] Załóż konto na https://cloud.langfuse.com/
- [ ] Utwórz projekt
- [ ] Skopiuj klucze: Project Settings → API Keys

## Krok 3: Konfiguracja aplikacji

- [ ] Otwórz folder `APP/`
- [ ] Skopiuj plik `.env.example` jako `.env`:
  ```bash
  copy .env.example .env
  ```
- [ ] Otwórz plik `.env` i uzupełnij klucze:
  ```
  BLOB_READ_WRITE_TOKEN=<twój_token_vercel>
  OPENAI_API_KEY=<twój_klucz_openai>  (opcjonalnie)
  LANGFUSE_SECRET_KEY=<twój_secret_key>  (opcjonalnie)
  LANGFUSE_PUBLIC_KEY=<twój_public_key>  (opcjonalnie)
  ```

- [ ] Otwórz plik `config.py`
- [ ] Znajdź linię ~44: `VERCEL_BLOB_MODEL_URL = ""`
- [ ] Wklej URL modelu (skopiowany z kroku 1):
  ```python
  VERCEL_BLOB_MODEL_URL = "https://twoj-url.vercel-storage.com/..."
  ```

## Krok 4: Instalacja zależności

- [ ] Otwórz terminal w folderze `APP/`
- [ ] Utwórz wirtualne środowisko:
  ```bash
  python -m venv venv
  ```
- [ ] Aktywuj środowisko:
  - **Windows**: `venv\Scripts\activate`
  - **Linux/Mac**: `source venv/bin/activate`
- [ ] Zainstaluj zależności:
  ```bash
  pip install -r requirements.txt
  ```

## Krok 5: Weryfikacja danych

- [ ] Sprawdź czy plik istnieje: `APP/data/halfmarathon_2023_2024.csv`
- [ ] Rozmiar pliku powinien być ~4-5 MB
- [ ] Jeśli pliku brak - uruchom komórkę 74 w notebooku

## Krok 6: Uruchomienie aplikacji

- [ ] Upewnij się że venv jest aktywne (powinno być `(venv)` przed promptem)
- [ ] Uruchom aplikację:
  ```bash
  streamlit run app.py
  ```
- [ ] Przeglądarka powinna otworzyć się automatycznie na `http://localhost:8501`
- [ ] Jeśli nie - otwórz ręcznie ten adres

## Krok 7: Testowanie

- [ ] W panelu bocznym wypełnij formularz:
  - Imię: "TestUser"
  - Płeć: Mężczyzna
  - Wiek: 30
  - Czas na 5km: 25 minut

- [ ] Kliknij "🚀 Przewiduj mój czas!"

- [ ] Sprawdź czy widzisz:
  - ✅ Przewidywany czas końcowy (format H:MM:SS)
  - ✅ Tempo na kilometr
  - ✅ Klasyfikację ogólną
  - ✅ Pozycję w kategorii
  - ✅ Statystyki średnich czasów
  - ✅ Komentarz AI (jeśli OpenAI skonfigurowane)
  - ✅ Tabelę Top 10
  - ✅ Przycisk "Pobierz pełne dane (Excel)"
  - ✅ Symulator czasów

## Rozwiązywanie problemów

### Błąd: "Brak BLOB_READ_WRITE_TOKEN"
✅ Sprawdź czy plik `.env` istnieje w folderze `APP/`
✅ Sprawdź czy token jest poprawnie skopiowany (bez spacji)

### Błąd: "Brak VERCEL_BLOB_MODEL_URL"
✅ Sprawdź `config.py` linię ~44
✅ URL powinien zaczynać się od `https://`

### Błąd: "Nie można załadować danych"
✅ Sprawdź czy plik `APP/data/halfmarathon_2023_2024.csv` istnieje
✅ Uruchom komórkę 74 w notebooku

### Błąd: "Model nie pasuje do danych"
✅ Upewnij się, że model został przesłany z najnowszą wersją danych
✅ Sprawdź czy kolumny w CSV to: Płeć, 5km, Rocznik, Kategoria wiekowa, Kraj

### Aplikacja ładuje się długo
✅ To normalne przy pierwszym uruchomieniu (pobieranie modelu ~5-10 MB)
✅ Kolejne uruchomienia będą szybkie dzięki cache'owaniu

### Komentarze AI nie działają
✅ Sprawdź czy `OPENAI_API_KEY` jest w pliku `.env`
✅ Sprawdź czy masz środki na koncie OpenAI
✅ Aplikacja działa bez AI - to opcjonalna funkcja

---

## 🎉 Gotowe!

Jeśli wszystkie kroki zostały wykonane, aplikacja powinna działać poprawnie.

**Pierwszy raz może potrwać 10-15 sekund** (pobieranie i cache'owanie modelu).

**Następne predykcje będą natychmiastowe!** 🚀

---

### Pytania?

Sprawdź plik `README.md` dla pełnej dokumentacji.
