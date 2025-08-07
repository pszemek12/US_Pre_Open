US_Open

Krótkie wprowadzenie do spółek przed amerykańskim otwarciem

Ten skrypt Python pobiera:
Zmianę procentową kontraktu ES=F (E-mini S&P 500 Futures) z Yahoo Finance
Aktualne ceny pre-market dla wybranych tickerów

Wynik jest wyświetlany w konsoli i zapisywany do pliku US_PRE_price.txt w tej samej lokalizacji, co skrypt (lub plik .exe).

Wymagania:
Python 3.6+
Biblioteka yfinance

Instalacja
Sklonuj repozytorium lub pobierz skrypt:

git clone https://github.com/pszemek12/US_Open.git
cd US_Open


Sposób użycia
Uruchom skrypt i podaj tickery oddzielone przecinkami:

Przykład interakcji:

Podaj tickery (AAPL,MSFT,...): AAPL,MSFT
🇺🇸 *Krótkie wprowadzenie...*
Kontrakt na SPX (+0.35%) vs. poprzedni close US
Apple Inc. (AAPL) (premarket: 135.67; +0.42%)
Microsoft Corporation (MSFT) (premarket: 256.12; -0.10%)
...
created by Pszemo © :)
Date: 2025-06-22
Time: 08:15:30

Dane zapisane do pliku:
/path/to/US_PRE_price.txt

Naciśnij Enter, aby zakończyć...


Skopiuj tylko ten plik .exe (przy --onefile) i uruchom na dowolnym komputerze bez Pythona.

Licencja
© Pszemo. Wszelkie prawa zastrzeżone.

