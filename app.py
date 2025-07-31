# File: app.py (Versione con Database e Cronologia Persistente)
# Prerequisiti: pip install streamlit google-generativeai youtube-transcript-api pytube

import streamlit as st
import os
from summarizer import YouTubeSummarizer 
# Importiamo le funzioni dal nostro nuovo file per il database
import database as db

# --- Configurazione della Pagina ---
st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Stile CSS Personalizzato (Versione Originale) ---
st.markdown("""
<style>
    .stApp {
        background-color: #F0F2F6;
    }
    .stButton>button {
        color: #FFFFFF;
        background-color: #FF4B4B;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #E03C3C;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    .st-emotion-cache-19rxjzo.ef3psqc12 {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- Inizializzazione DB e Stato Sessione ---
# Inizializza il database (crea il file e la tabella se non esistono)
db.init_db()

# Carica la cronologia dal DB solo la prima volta che la sessione parte
if 'history_loaded' not in st.session_state:
    st.session_state.history = db.get_history()
    st.session_state.history_loaded = True
    st.session_state.selected_video = st.session_state.history[0] if st.session_state.history else None

# --- Funzioni di Logica ---

def process_summarization(api_key, video_link):
    if not api_key:
        st.error("Chiave API di Gemini non trovata!", icon="🚨")
        return
    if not video_link:
        st.warning("Per favore, inserisci un link di YouTube.", icon="⚠️")
        return

    try:
        summarizer = YouTubeSummarizer(api_key=api_key)
        video_id = YouTubeSummarizer.get_video_id(video_link)
        if not video_id:
            st.error("Il link di YouTube non è valido.", icon="❌")
            return

        with st.spinner("Recupero informazioni dal video... ⏳"):
            transcript, title, error = summarizer.get_video_info(video_id)
        if error:
            st.error(error, icon="❌")
            return
        
        with st.spinner("✨ Gemini sta creando il riassunto..."):
            summary, error = summarizer.summarize(transcript, title)
        if error:
            st.error(error, icon="❌")
            return
        
        video_data = {
            "id": video_id, "url": video_link, "title": title,
            "summary": summary, "transcript": transcript
        }
        
        # Salva nel database
        db.add_history(video_data)
        
        # Aggiorna lo stato della sessione locale
        # Rimuovi eventuali duplicati prima di aggiungere
        st.session_state.history = [v for v in st.session_state.history if v['id'] != video_id]
        st.session_state.history.insert(0, video_data)
        st.session_state.selected_video = video_data
        
        st.rerun()

    except Exception as e:
        st.error(f"Si è verificato un errore inaspettato: {e}", icon="🚨")

def select_video_from_history(video_data):
    st.session_state.selected_video = video_data

def clear_history():
    db.clear_history_db()
    st.session_state.history = []
    st.session_state.selected_video = None

# --- Interfaccia Utente ---
gemini_api_key = st.secrets.get("GEMINI_API_KEY")

with st.sidebar:
    st.title("📚 Cronologia")
    st.markdown("I tuoi riassunti recenti.")

    if st.session_state.history:
        for video in st.session_state.history:
            st.button(
                video['title'], key=video['id'],
                on_click=select_video_from_history, args=(video,)
            )
        
        st.markdown("---")
        if st.button("Pulisci Cronologia", type="primary"):
             clear_history()
             st.rerun()
    else:
        st.info("La cronologia è vuota.")

    st.markdown("---")
    st.header("Come funziona")
    st.markdown("1. **Inserisci un link**\n2. **Recupera titolo e trascrizione**\n3. **Genera il riassunto**\n4. **Salva nella cronologia**")

st.title("✨ YouTube Video Summarizer")
st.markdown("Incolla il link di un video di YouTube e ottieni un riassunto istantaneo generato da Gemini.")

video_url = st.text_input("Link del video di YouTube", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Genera Riassunto"):
    process_summarization(gemini_api_key, video_url)

if st.session_state.selected_video:
    st.markdown("---")
    video_data = st.session_state.selected_video
    st.subheader(f"🎬 {video_data['title']}")
    
    col1, col2 = st.columns([0.5, 0.5], gap="large")
    with col1:
        st.video(video_data['url'])
        with st.expander("Vedi la trascrizione completa"):
            st.text_area("Trascrizione", video_data['transcript'], height=250)
    with col2:
        st.markdown("#### 📝 Riassunto del Video")
        st.markdown(video_data['summary'])
