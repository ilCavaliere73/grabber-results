from flask import Flask
import os

def create_app():
    # 1. Inizializza l'applicazione Flask
    app = Flask(__name__)

    # 2. Configurazione base
    app.config['SECRET_KEY'] = 'la-tua-chiave-segreta'

    # 3. Assicurati che la cartella data esista
    if not os.path.exists('data'):
        os.makedirs('data')

    # 4. Registra il Blueprint (DENTRO la funzione e indentato)
    from .routes import main
    app.register_blueprint(main)

    return app