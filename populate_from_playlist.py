# File: populate_from_playlist.py
# Scansiona una playlist di YouTube, genera riassunti per ogni video in parallelo e popola il database.

import os
import time
import yt_dlp
from summarizer import YouTubeSummarizer
import database as db
import concurrent.futures
from functools import partial

CONCURRENT_WORKERS = 5  # be careful! youtube may block your IP!!!

def process_single_video(entry: dict, i: int, total_videos: int, summarizer: YouTubeSummarizer) -> str:
    """
    Funzione eseguita da ogni thread. Processa un singolo video.
    Restituisce una stringa con lo stato dell'operazione.
    """
    video_id = entry['id']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    log_prefix = f"[Video {i+1}/{total_videos} | ID: {video_id}]"
    
    try:
        # 1. Recupero informazioni (ora include l'autore)
        transcript, title, author, error = summarizer.get_video_info(video_id)
        if error:
            return f"{log_prefix} ⚠️  SKIPPED: Impossibile ottenere le info. Errore: {error}"
        
        # 2. Generazione riassunto
        summary, error = summarizer.summarize(transcript, title)
        if error:
            return f"{log_prefix} ⚠️  SKIPPED: Impossibile generare il riassunto. Errore: {error}"
            
        # 3. Creazione del dizionario dati (con autore) e salvataggio
        video_data = {
            "id": video_id,
            "url": video_url,
            "title": title,
            "author": author, # Aggiunto l'autore
            "summary": summary,
            "transcript": transcript
        }
        
        db.add_history(video_data)
        time.sleep(1)
        return f"{log_prefix} ✅ SUCCESS: '{title}' di '{author}' salvato nel database."

    except Exception as e:
        return f"{log_prefix} ❌ FAILED: Si è verificato un errore inaspettato: {e}"
    
        

def process_playlist_parallel(playlist_url: str, api_key: str):
    """
    Estrae i video da una playlist e li processa in parallelo usando un ThreadPool.
    """
    print("--- Inizio del processo di popolamento parallelo dalla playlist ---")
    
    try:
        summarizer = YouTubeSummarizer(api_key=api_key)
        db.init_db() # Inizializza il DB con la nuova tabella
        print(f"Database e Summarizer inizializzati. Verranno usati {CONCURRENT_WORKERS} thread concorrenti.")
    except ValueError as e:
        print(f"❌ Errore di configurazione: {e}")
        return
    
    print(f"\nRecupero dei video dalla playlist: {playlist_url}")
    try:
        ydl_opts = {'extract_flat': True, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            if 'entries' not in playlist_info:
                print("❌ Errore: URL non valido o non è una playlist.")
                return
            video_entries = playlist_info['entries']
            total_videos = len(video_entries)
            print(f"✅ Trovati {total_videos} video. Avvio dell'elaborazione parallela...")

    except Exception as e:
        print(f"❌ Impossibile recuperare la playlist: {e}")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        task_processor = partial(process_single_video, summarizer=summarizer)
        
        future_to_video = {
            executor.submit(task_processor, entry, i, total_videos): entry 
            for i, entry in enumerate(video_entries)
        }
        
        for future in concurrent.futures.as_completed(future_to_video):
            try:
                result_message = future.result()
                print(result_message)
            except Exception as e:
                print(f"❌ Si è verificato un errore critico durante l'esecuzione del thread: {e}")

    print("\n--- Processo di popolamento completato! ---")

# --- Blocco di Esecuzione Principale ---
if __name__ == '__main__':
    PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL9PLR7E2lKYqup-d4_7i0XLTXR3arOWAx"
    
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    
    if not gemini_api_key:
        print("\n❌ ERRORE: La variabile d'ambiente 'GEMINI_API_KEY' non è impostata.")
        print("   Per favore, impostala prima di eseguire lo script.")
    else:
        start_time = time.time()
        process_playlist_parallel(PLAYLIST_URL, gemini_api_key)
        end_time = time.time()
        print(f"\nTempo totale di esecuzione: {end_time - start_time:.2f} secondi.")