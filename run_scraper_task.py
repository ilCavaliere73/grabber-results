import os
import sqlite3
from app.scraper import get_diretta_results as get_diretta_pro

def save_to_db(results):
    # QUESTA È LA RIGA MAGICA: Crea la cartella 'data' se non c'è
    if not os.path.exists('data'):
        os.makedirs('data')
        print("📁 Cartella 'data' creata con successo.")

    conn = sqlite3.connect('data/results.db')
    cursor = conn.cursor()
    
    # Creiamo una tabella con un vincolo di UNICITÀ sulle squadre (così non duplichiamo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         home TEXT, away TEXT, score TEXT, 
         UNIQUE(home, away))
    ''')
    
    for m in results:
        # 'INSERT OR REPLACE' aggiorna il risultato se la coppia casa-fuori esiste già
        cursor.execute('''
            INSERT OR REPLACE INTO matches (home, away, score) 
            VALUES (?, ?, ?)
        ''', (m['home'], m['away'], m['score']))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # 1. Grabba i dati
    data = get_diretta_pro()
    # 2. Salva nel DB
    save_to_db(data)