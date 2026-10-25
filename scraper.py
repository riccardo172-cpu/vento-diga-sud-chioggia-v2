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
        
        if rows:
            latest_row = rows[-1]
            cols = latest_row.find_all('td')
            
            if len(cols) >= 5:
                timestamp = cols[0].get_text().strip()
                water_level = cols[1].get_text().strip()
                wind_dir = cols[2].get_text().strip()
                wind_speed = cols[3].get_text().strip()
                wind_gust = cols[4].get_text().strip()
                
                print("--- ULTIMO DATO RILEVATO ---")
                print(f"Orario: {timestamp}")
                print(f"Direzione Vento: {wind_dir}°")
                print(f"Velocità Vento: {wind_speed} m/s")
                print(f"Raffica Max: {wind_gust} m/s")
            else:
                print("Formato riga non riconosciuto.")
        else:
            print("Nessuna riga trovata nella pagina.")

    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

if __name__ == "__main__":
    scrape_and_push()
