import requests
import json
import os
from datetime import datetime

def get_diretta_results():
    # La tua lista ufficiale Serie A
    SQUADRE_A = {
        "atalanta", "bologna", "cagliari", "como", "cremonese",
        "fiorentina", "genoa", "verona", "inter", "juventus",
        "lazio", "lecce", "milan", "napoli", "parma",
        "pisa", "roma", "sassuolo", "torino", "udinese"
    }

    # API Key corretta
    #API_KEY = "68b860d0d90846788fbd0c2d142ec8aa"
    
    API_KEY = os.environ.get('FOOTBALL_API_KEY')

    if not API_KEY:
        print("ERRORE: La chiave API non è stata trovata nelle variabili d'ambiente!")

    url = "https://api.football-data.org/v4/competitions/SA/matches"
    headers = {'X-Auth-Token': API_KEY}

    try:
        print("\n--- CHIAMATA API FOOTBALL-DATA ---")
        response = requests.get(url, headers=headers, timeout=10)
        
        # SALVA IL FILE PER IL DEBUG (Ora con estensione .json)
        # Questo ti permetterà di vedere la struttura esatta che arriva dall'API
        with open('debug_feed.json', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # L'API risponde in JSON, non serve html.unescape
        data = response.json()
        results = []

        if 'matches' not in data:
            print("Errore: La risposta API non contiene match. Controlla debug_feed.json")
            return []

        for match in data.get('matches', []):
            # Estrazione nomi squadre
            home = match['homeTeam']['shortName'].replace(" AC", "").replace(" FC", "").strip()
            away = match['awayTeam']['shortName'].replace(" AC", "").replace(" FC", "").strip()
            
            # Punteggio (Full Time)
            score_data = match.get('score', {}).get('fullTime', {})
            h_score = score_data.get('home')
            a_score = score_data.get('away')
            
            if h_score is not None:
                score_str = f"{h_score} - {a_score}"
            else:
                score_str = "vs"
            
            # DATA: L'API la fornisce in 'utcDate' (es: 2024-08-25T18:30:00Z)
            # Prendiamo solo la parte YYYY-MM-DD
            match_date = match['utcDate'].split('T')[0]

            # Controllo rigoroso sui nomi
            if home.lower() in SQUADRE_A and away.lower() in SQUADRE_A:
                results.append({
                    "home": home,
                    "away": away,
                    "score": score_str,
                    "date": match_date,
                    "status": match.get('status')
                })
        
        print(f"--- Fine: {len(results)} match Serie A processati ---")
        return results

    except Exception as e:
        print(f"Errore critico API: {e}")
        return []