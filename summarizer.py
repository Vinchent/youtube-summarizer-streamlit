# File: summarizer.py (Versione Migliorata)
# Contiene la logica di business per la trascrizione e il riassunto.
# Prerequisiti: pip install google-generativeai youtube-transcript-api pytube

import os
import google.generativeai as genai
from google.generativeai import types
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter
import yt_dlp

class YouTubeSummarizer:
    """
    Una classe per ottenere trascrizione, titolo e riassunto di un video YouTube
    utilizzando l'API di Gemini in modo strutturato.
    """

    def __init__(self, api_key: str):
        """Inizializza il client dell'API di Gemini."""
        if not api_key:
            raise ValueError("La chiave API di Gemini non è stata fornita.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash-lite',
            # Impostiamo qui l'istruzione di sistema, così vale per tutte le chiamate
            system_instruction="Sei un assistente esperto nel creare riassunti concisi e chiari da trascrizioni di video. Il tuo obiettivo è estrarre i punti salienti e le informazioni chiave, formattandoli in un elenco puntato in italiano."
        )

    def get_video_info(self, video_id: str) -> tuple[str | None, str | None, str | None]:
        """
        Recupera trascrizione e titolo di un video di YouTube.
        Restituisce (trascrizione, titolo, errore).
        """
        # --- Estrazione Trascrizione ---
        ytt_api = YouTubeTranscriptApi()
        try:
            transcript_list = ytt_api.fetch(video_id, languages=['it', 'en'])
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_list)
        except TranscriptsDisabled:
            return None, None, f"Le trascrizioni sono disabilitate per il video ID: {video_id}."
        except Exception as e:
            return None, None, f"Impossibile recuperare la trascrizione per il video ID {video_id}: {e}"

        # --- Estrazione Titolo con Pytube ---
        try:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                video_title = info.get("title")
        except Exception as e:
            # Se non riusciamo a prendere il titolo, non è un problema bloccante.
            video_title = "questo video" 
            print(f"Attenzione: Impossibile recuperare il titolo del video. Errore: {e}")

        return transcript_text, video_title, None

    def summarize(self, transcript: str, video_title: str) -> tuple[str | None, str | None]:
        """
        Utilizza Gemini per riassumere la trascrizione (ora con system_instruction).
        Restituisce (riassunto, errore).
        """
        if not transcript:
            return None, "Nessuna trascrizione fornita per il riassunto."

        # Ora il prompt è più pulito, perché l'istruzione generale è già nel modello
        prompt = f"""
        Analizza la seguente trascrizione del video intitolato "{video_title}" e crea un riassunto dei punti principali in formato bullet points.

        --- TRASCRIZIONE ---
        {transcript}
        --- FINE TRASCRIZIONE ---
        """
        
        try:
            # La chiamata ora è più semplice, le istruzioni di sistema sono già configurate
            response = self.model.generate_content(prompt)
            return response.text, None
        except Exception as e:
            return None, f"Si è verificato un errore durante la generazione del riassunto con Gemini: {e}"

    @staticmethod
    def get_video_id(link: str) -> str | None:
        """Estrae l'ID del video da un link di YouTube (metodo statico)."""
        if "v=" in link:
            return link.split("v=")[1].split("&")[0]
        if "youtu.be/" in link:
            return link.split("youtu.be/")[1].split("?")[0]
        return None

# --- Esempio di Utilizzo ---
if __name__ == '__main__':
    print("--- Esecuzione in modalità test ---")
    
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("\nErrore: La variabile d'ambiente GEMINI_API_KEY non è stata impostata.")
    else:
        try:
            summarizer = YouTubeSummarizer(api_key=api_key)
            # Usa un link di un video reale per il test
            # video_link = input("\nInserisci il link di un video di YouTube per il test: ")
            video_link ="https://www.youtube.com/watch?v=VW772c2_lpk"
            
            video_id = YouTubeSummarizer.get_video_id(video_link)
            if not video_id:
                print("Link non valido.")
            else:
                print(f"\nVideo ID estratto: {video_id}")
                
                print("\n--- Recupero Info Video ---")
                transcript, title, error = summarizer.get_video_info(video_id)
                
                if error:
                    print(f"Errore: {error}")
                else:
                    print(f"Titolo: {title}")
                    print("Trascrizione recuperata con successo.")
                    
                    print("\n--- Generazione Riassunto ---")
                    summary, error = summarizer.summarize(transcript, title)
                    if error:
                        print(f"Errore: {error}")
                    else:
                        print("\nRiassunto Generato:\n")
                        print(summary)

        except ValueError as e:
            print(f"Errore di configurazione: {e}")
        except Exception as e:
            print(f"Si è verificato un errore inaspettato: {e}")