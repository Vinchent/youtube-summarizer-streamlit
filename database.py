# File: database.py
# Gestisce tutte le operazioni con il database SQLite per la cronologia.

import sqlite3
import json # Useremo JSON per salvare la trascrizione che può essere lunga

DB_NAME = "history.db"

def init_db():
    """
    Inizializza il database e crea la tabella 'history' se non esiste.
    AGGIUNTO: Campo 'author' per il nome del canale.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Aggiungiamo la colonna 'author' alla tabella
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL, 
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
    AGGIUNTO: Inserimento del valore 'author'.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Usiamo INSERT OR REPLACE per gestire i duplicati. Aggiunto 'author'.
    cursor.execute("""
        INSERT OR REPLACE INTO history (id, url, title, author, summary, transcript)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        video_data['id'],
        video_data['url'],
        video_data['title'],
        video_data['author'],
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
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM history ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def delete_single_record(video_id: str):
    """
    Elimina un singolo record dalla cronologia basandosi sull'ID del video.
    Restituisce True se il record è stato eliminato, False se non esisteva.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM history WHERE id = ?", (video_id,))
    exists = cursor.fetchone()[0] > 0
    
    if exists:
        cursor.execute("DELETE FROM history WHERE id = ?", (video_id,))
        conn.commit()
    
    conn.close()
    return exists

def clear_history_db():
    """
    Cancella tutti i record dalla tabella 'history'.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()