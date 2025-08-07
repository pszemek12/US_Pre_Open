import streamlit as st
from datetime import datetime
import yfinance as yf
import os

# Ustawienia Streamlit
st.set_page_config(page_title="US Pre Mkt Wrap", layout="wide")
st.title("🗽 US Pre Mkt Wrap 🚀")

# Funkcje pobierające dane pre-market
def fetch_es_change():
    """Pobiera preMarketChangePercent dla ES=F."""
    es = yf.Ticker("ES=F")
    info = es.info
    cp = info.get('preMarketChangePercent') or info.get('regularMarketChangePercent')
    if cp is None:
        raise ValueError("Brak procentowej zmiany dla S&P 500 futures. :()")
    return round(cp, 2)


def fetch_premarket(symbol):
    """
    Zwraca (last_price, change_percent, company_name) dla pre-market:
     – najpierw z ticker.info,
     – w fallbacku z history(prepost).
    """
    t = yf.Ticker(symbol)
    info = t.info
    name = info.get('shortName') or info.get('longName') or symbol

    pm_price = info.get('preMarketPrice')
    pm_pct   = info.get('preMarketChangePercent')
    if pm_price is not None and pm_pct is not None:
        return round(pm_price, 2), round(pm_pct, 2), name

    hist = t.history(period="2d", interval="1d")
    if hist['Close'].size < 2:
        raise ValueError(f"Za mało danych dziennych dla {symbol}")
    prev_close = hist['Close'].iloc[-1]

    intraday = t.history(period="1d", interval="1m", prepost=True)
    if intraday.index.tz is None:
        intraday = intraday.tz_localize('UTC').tz_convert('America/New_York')
    else:
        intraday = intraday.tz_convert('America/New_York')

    pre = intraday.between_time("04:00", "09:30")
    if pre.empty:
        raise ValueError(f"Brak danych pre-market dla {symbol}")
    last = pre['Close'].iloc[-1]
    pct  = (last - prev_close) / prev_close * 100
    return round(last, 2), round(pct, 2), name

# Stały tekst niewidoczny w UI, tylko w pliku
fixed_text = "🇺🇸 *Krótkie wprowadzenie do spółek przed amerykańskim otwarciem*"

# Parametry aplikacji
ticker_count = 6

# Sekcja głównego newsa
st.subheader("Główny news dnia")
main_news = st.text_area(
    "Wpisz główny news, który pojawi się przed listą spółek:",
    height=80,
    key="main_news"
)

# Sekcja wprowadzania tickerów i odpowiadające im newsy
st.header("Wprowadź tickery i odpowiadające im newsy")
entries = []
for i in range(1, ticker_count + 1):
    col1, col2 = st.columns([1, 5])
    with col1:
        ticker = st.text_input(f"Ticker #{i}", key=f"ticker_{i}")
    with col2:
        news = st.text_area(f"News dla #{i}", height=50, key=f"news_{i}")
    entries.append((ticker.strip(), news.strip()))

# Generowanie zawartości pliku
def build_txt():
    lines = [fixed_text, ""]

    # Główny news
    if main_news.strip():
        lines.append(f"*{main_news.strip()}*")
        lines.append("")

    # Pre-market SPX futures
    try:
        es_pct = fetch_es_change()
        lines.append(f"Kontrakt na SPX *{es_pct:+}%* vs. poprzedni close US")
    except Exception as e:
        lines.append(f"S&P 500 futures => błąd pobierania danych: {e} :()")
    lines.append("")

    # Informacje o tickerach
    for ticker, news_text in entries:
        if ticker:
            symbol = ticker.upper()
            try:
                price, pct, name = fetch_premarket(symbol)
                line = f"{symbol} ({name}) => premarket: *{pct:+}%* @ USD {price}"
            except Exception:
                line = f"{symbol} => brak danych pre-market"
        else:
            line = ""
        if news_text:
            line += f" => {news_text}" if line else news_text
        if line:
            lines.append(line)

    # Dodaj sekcje ETF sektorowe pre-market
    lines.append("")
    lines.append("Sektory pre-market:")
    # Lista par (nazwa, symbol)
    sectors = [("Technologia", "XLK"), ("Finanse", "XLF"), ("Energia", "XLE"), ("Industrial", "XLI"), ("Health Care", "XLV")]
    for sec_name, sec_sym in sectors:
        try:
            price, pct, _ = fetch_premarket(sec_sym)
            lines.append(f"{sec_name} => *{pct:+}%*")
        except Exception:
            lines.append(f"{sec_name} {sec_sym} => brak danych pre-market")

    return "\n".join(lines)

# Podgląd na żywo pliku
live_preview = build_txt()
with st.expander("Pokaż podgląd pliku TXT (na żywo)", expanded=True):
    st.code(live_preview, language="text")

# Generuj WhatsUp i zapisz plik w folderze Output
today_str = datetime.now().strftime("%d.%m.%Y")
file_name = f"US_PRE_OPEN {today_str}.txt"
if st.button("🟢 Generuj WhatsUp"):
    # Utwórz folder Output, jeśli nie istnieje
    script_dir = os.path.dirname(__file__)
    output_dir = os.path.join(script_dir, "Output")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(live_preview)
    st.success(f"Plik zapisany w folderze Output jako {file_name}.")
else:
    st.info("Kliknij '🟢 Generuj WhatsUp', aby zapisać raport.")
