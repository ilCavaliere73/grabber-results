try:
    print("1. Caricamento app...")
    from app import create_app
    
    print("2. Creazione istanza Flask...")
    app = create_app()

    # QUESTA PARTE È FONDAMENTALE PER FAR PARTIRE IL SERVER
    if __name__ == "__main__":
        print("3. Avvio server su http://0.0.0.0:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)

except Exception as e:
    print(f"❌ ERRORE RILEVATO: {e}")
    import traceback
    traceback.print_exc()