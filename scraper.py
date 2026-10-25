import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.comune.venezia.it/sites/default/files/publicCPSM2/stazioni/temporeale/Diga_Sud_Chioggia.html"
WORKER_URL = "https://vento-diga-sud-test.riccardo172.workers.dev/"
API_KEY = os.environ.get("API_KEY", "kitesurf_chioggia_2026_secret")

def scrape_and_push():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        
        last_row = None
        for row in rows:
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            if len(cols) >= 5 and ":" in cols[0] and "-" in cols[0]:
                last_row = cols

        if not last_row:
            print("Nessuna riga valida trovata.")
            return

        timestamp = last_row[0]
        water_level = float(last_row[1])
        wind_dir = float(last_row[2])
        wind_speed = float(last_row[3])
        wind_gust = float(last_row[4])

        print(f"Dati pronti per l'invio: orario {timestamp}")

        payload = {
            "timestamp": timestamp,
            "water_level": water_level,
            "wind_direction": wind_dir,
            "wind_speed": wind_speed,
            "wind_gust": wind_gust
        }
        
        worker_headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        r = requests.post(WORKER_URL, json=payload, headers=worker_headers, timeout=10)
        print("Risposta Worker:", r.status_code, r.text)

    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

if __name__ == "__main__":
    scrape_and_push()
