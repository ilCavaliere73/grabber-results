from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
import os
# Importiamo la logica che hai in run_scraper_task o direttamente lo scraper
from .scraper import get_diretta_results 
from datetime import datetime


main = Blueprint('main', __name__)

# Funzione per formattare la data da YYYY-MM-DD a DD/MM/YYYY
def format_date_it(date_str):
    if not date_str or date_str == "Tutte":
        return date_str
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    except:
        return date_str

def get_db_connection():
    # Usiamo un percorso assoluto per evitare dubbi su dove sia il file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Se il tuo file è in una cartella 'data' dentro 'app'
    db_path = os.path.join(base_dir, '..', 'data', 'results.db')
    conn = sqlite3.connect(db_path)

    # Esegui questo per aggiornare lo schema se hai già il DB vecchio
    try:
        conn.execute('ALTER TABLE matches ADD COLUMN date TEXT')
    except sqlite3.OperationalError:
        # Se la colonna esiste già, ignora l'errore
        pass

    # Aggiungiamo 'status' qui
    conn.execute('''
        CREATE TABLE IF NOT EXISTS matches 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         home TEXT, away TEXT, score TEXT, status TEXT)
    ''')
    conn.row_factory = sqlite3.Row
    return conn


@main.route('/')
def index():
    # 1. TENTA LA CONNESSIONE AUTOMATICA ALL'APERTURA
    # Eseguiamo un aggiornamento silenzioso
    results = get_diretta_results()
    if results:
        conn = get_db_connection()
        cursor = conn.cursor()
        for m in results:
            cursor.execute('''
                INSERT OR REPLACE INTO matches (home, away, score, status, date) 
                VALUES (?, ?, ?, ?, ?)
            ''', (m['home'], m['away'], m['score'], m.get('status', 'SERIE A'), m['date']))
        conn.commit()
        conn.close()

    conn = get_db_connection()
    
    # 2. Recupera tutte le date per la select
    all_dates_raw = conn.execute('SELECT DISTINCT date FROM matches ORDER BY date DESC').fetchall()
    all_dates = [d['date'] for d in all_dates_raw]

    # 3. Gestione data selezionata o data attuale
    selected_date = request.args.get('date')
    
    # Se non è selezionata, proviamo a prendere la data di oggi (se presente) 
    # o l'ultima data disponibile nel database
    if not selected_date and all_dates:
        today_str = datetime.now().strftime('%Y-%m-%d')
        selected_date = today_str if today_str in all_dates else all_dates[0]

    # 4. Recupera i match filtrati
    matches = conn.execute('SELECT * FROM matches WHERE date = ? ORDER BY id DESC', (selected_date,)).fetchall()
    
    conn.close()

    return render_template('dashboard.html', 
                           matches=matches, 
                           all_dates=all_dates, 
                           selected_date=selected_date,
                           format_date=format_date_it) # Passiamo la funzione al template

@main.route('/test-grabber', methods=['POST'])
def test_grabber():
    results = get_diretta_results()
    if results:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # OPERAZIONE UNA TANTUM: Svuota per rimettere le date giuste
        # Una volta fatto il primo caricamento, puoi commentare questa riga
        cursor.execute('DELETE FROM matches') 
        
        for m in results:
            cursor.execute('''
                INSERT OR REPLACE INTO matches (home, away, score, status, date) 
                VALUES (?, ?, ?, ?, ?)
            ''', (m['home'], m['away'], m['score'], m.get('status', 'SERIE A'), m['date']))
        
        conn.commit()
        conn.close()
    return redirect(url_for('main.index'))