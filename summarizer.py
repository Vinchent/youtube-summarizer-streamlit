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
    Una classe per ottenere trascrizione, titolo, autore e riassunto di un video YouTube
    utilizzando l'API di Gemini in modo strutturato.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("La chiave API di Gemini non è stata fornita.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash-lite',
            system_instruction="Sei un assistente esperto nel creare riassunti concisi e chiari da trascrizioni di video. Il tuo obiettivo è estrarre i punti salienti e le informazioni chiave, formattandoli in un elenco puntato in italiano."
        )

    def get_video_info(self, video_id: str) -> tuple[str | None, str | None, str | None, str | None]:
        """
        Recupera trascrizione, titolo e autore di un video di YouTube.
        Restituisce (trascrizione, titolo, autore, errore).
        """
        # --- Estrazione Trascrizione ---
        ytt_api = YouTubeTranscriptApi()
        try:
            transcript_list = ytt_api.fetch(video_id, languages=['it', 'en'])
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_list)
        except TranscriptsDisabled:
            return None, None, None, f"Le trascrizioni sono disabilitate per il video ID: {video_id}."
        except Exception as e:
            return None, None, None, f"Impossibile recuperare la trascrizione per il video ID {video_id}: {e}"

        # --- Estrazione Titolo e Autore con yt-dlp ---
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                video_title = info.get("title", "Titolo non disponibile")
                video_author = info.get("uploader", "Autore non disponibile") # 'uploader' è il campo corretto per il canale
        except Exception as e:
            video_title = "questo video" 
            video_author = "sconosciuto"
            print(f"Attenzione: Impossibile recuperare titolo/autore. Errore: {e}")

        return transcript_text, video_title, video_author, None

    def summarize(self, transcript: str, video_title: str) -> tuple[str | None, str | None]:
        """
        Utilizza Gemini per riassumere la trascrizione.
        Restituisce (riassunto, errore).
        """
        if not transcript:
            return None, "Nessuna trascrizione fornita per il riassunto."

        prompt = f"""
        Analizza la seguente trascrizione del video intitolato "{video_title}" e crea un riassunto dei punti principali in formato bullet points.

        --- TRASCRIZIONE ---
        {transcript}
        --- FINE TRASCRIZIONE ---
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text, None
        except Exception as e:
            return None, f"Si è verificato un errore durante la generazione del riassunto con Gemini: {e}"

    @staticmethod
    def get_video_id(link: str) -> str | None:
        if "v=" in link:
            return link.split("v=")[1].split("&")[0]
        if "youtu.be/" in link:
            return link.split("youtu.be/")[1].split("?")[0]
        return None