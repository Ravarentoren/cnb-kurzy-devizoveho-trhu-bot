# -*- coding: utf-8 -*-
"""
CNB Kurzy devizoveho trhu Bot v1.0

Tento skript stáhne POSLEDNÍ PLATNÝ kurzovní lístek z JSON API
České národní banky a uloží ho do souboru CSV s datem platnosti v názvu.
Funguje i o víkendech a svátcích.

Autor:Tento skript byl vytvořen [Ravarentoren] za asistence umělé inteligence Gemini od společnosti Google. Logika pro stahování a parsování dat byla generována a laděna v rámci dialogu.
"""

import requests
import csv
from datetime import datetime

# URL adresa pro POSLEDNÍ PLATNÝ kurzovní lístek
url = "https://api.cnb.cz/cnbapi/exrates/daily"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("Spouštím stahování posledního platného kurzu ČNB...")

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status() 

    data = response.json()
    kurzy = data.get('rates')

    if kurzy:
        # Získáme datum, ke kterému jsou kurzy platné
        datum_platnosti = kurzy[0].get('validFor')
        print(f"✅ Úspěšně zpracováno {len(kurzy)} měn platných k {datum_platnosti}.")

        nazev_souboru = f"cnb_kurzy_{datum_platnosti}.csv"
        print(f"Ukládám data do souboru: {nazev_souboru}")

        with open(nazev_souboru, mode='w', newline='', encoding='utf-8') as soubor:
            zapisovac = csv.writer(soubor)
            zapisovac.writerow(['Země', 'Měna', 'Kód', 'Množství', 'Kurz'])
            
            for kurz in kurzy:
                zapisovac.writerow([
                    kurz.get('country'),
                    kurz.get('currency'),
                    kurz.get('currencyCode'),
                    kurz.get('amount'),
                    kurz.get('rate')
                ])
        
        print(f"🎉 Hotovo! Soubor '{nazev_souboru}' byl úspěšně vytvořen.")

    else:
        print("❌ V přijatých datech z API chybí kurzovní lístek ('rates').")

except requests.exceptions.RequestException as e:
    print(f"❌ Došlo k chybě při připojování k API: {e}")
except KeyError:
    print("❌ Formát přijatých dat z API je neplatný.")
