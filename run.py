import os
from app import create_app

# Creiamo l'app al livello principale del file
app = create_app()

# Questo serve ancora per far funzionare il tasto "Play" sul tuo PC
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)