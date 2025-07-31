# File: database.py
# Gestisce tutte le operazioni con il database SQLite per la cronologia.

import sqlite3
import json # Useremo JSON per salvare la trascrizione che può essere lunga

DB_NAME = "history.db"

def init_db():
    """
    Inizializza il database e crea la tabella 'history' se non esiste.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Creiamo la tabella. Usiamo TEXT per tutti i campi per semplicità.
    # L'ID del video di YouTube sarà la nostra chiave primaria per evitare duplicati.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            transcript TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_history(video_data: dict):
    """
    Aggiunge un nuovo record alla cronologia.
    Se un video con lo stesso ID esiste già, lo aggiorna (UPSERT).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Usiamo INSERT OR REPLACE per gestire i duplicati: se l'ID esiste, la riga viene sostituita.
    cursor.execute("""
        INSERT OR REPLACE INTO history (id, url, title, summary, transcript)
        VALUES (?, ?, ?, ?, ?)
    """, (
        video_data['id'],
        video_data['url'],
        video_data['title'],
        video_data['summary'],
        video_data['transcript']
    ))
    conn.commit()
    conn.close()

def get_history() -> list[dict]:
    """
    Recupera tutti i record dalla cronologia, ordinati dal più recente.
    """
    conn = sqlite3.connect(DB_NAME)
    # Restituisce le righe come dizionari per un facile utilizzo
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM history ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    # Converte le righe del database in una lista di dizionari standard
    return [dict(row) for row in rows]

def clear_history_db():
    """
    Cancella tutti i record dalla tabella 'history'.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()

