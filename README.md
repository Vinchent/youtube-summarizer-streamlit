# ✨ YouTube Video Summarizer with Gemini AI

A versatile and powerful application that transforms lengthy YouTube videos into concise, readable summaries using Google's Gemini AI. This tool offers two distinct modes of operation: a user-friendly web interface for summarizing single videos and a powerful command-line script for batch-processing entire playlists.

## Application Preview

![App Screenshot](https://i.imgur.com/OYJO7V7.png)

## 🚀 Key Features

- **Dual Operation Modes**: Use the interactive Streamlit app for single-video summaries or the command-line script to bulk-process an entire playlist.
- **AI-Powered Summarization**: Leverages Google's `gemini-2.5-flash-lite` model to generate accurate, high-quality summaries.
- **Intuitive Web Interface**: A clean and user-friendly interface built with Streamlit ensures accessibility for all users.
- **Persistent History**: All analyzed videos are stored in a local SQLite database, allowing you to review previous summaries anytime.
- **Concurrent Batch Processing**: The playlist script processes multiple videos in parallel, significantly speeding up bulk operations.
- **Automated Content Extraction**: Automatically retrieves video transcripts and metadata (title, channel author) directly from YouTube.

## ⚙️ How It Works

This application can be used in two ways:

### 1. Interactive Web App (`app.py`)
Run the Streamlit application to launch a web interface. Simply paste a single YouTube video URL and click "Genera Riassunto". The summary appears instantly and is automatically saved to the history. This is perfect for quick, on-demand analysis.

### 2. Batch Processing from a Playlist (`populate_from_playlist.py`)
Use the `populate_from_playlist.py` script to automatically fetch all videos from a specified YouTube playlist, generate a summary for each one, and save them directly into the database. This is ideal for pre-loading the application with a large amount of content.

## 🛠️ Technology Stack

- **Programming Language**: Python 3.9+
- **Web Framework**: Streamlit
- **AI Model**: Google Gemini (`gemini-2.5-flash-lite`)
- **Database**: SQLite
- **Core Dependencies**: `google-generativeai`, `youtube-transcript-api`, `yt_dlp`, `streamlit`

## 🗄️ Database Schema

The application uses a local SQLite database file (`history.db`) to store the summary history. The data is stored in a table named `history` with the following attributes:

| Attribute    | Type      | Description                                              |
|--------------|-----------|----------------------------------------------------------|
| `id`         | `TEXT`    | The unique YouTube video ID (Primary Key).               |
| `url`        | `TEXT`    | The full URL of the YouTube video.                       |
| `title`      | `TEXT`    | The title of the video.                                  |
| `author`     | `TEXT`    | The name of the YouTube channel/uploader.                |
| `summary`    | `TEXT`    | The AI-generated summary.                                |
| `transcript` | `TEXT`    | The full transcript of the video.                        |
| `created_at` | `TIMESTAMP`| The timestamp when the record was added.                |

## ⚙️ Installation & Setup

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.9 or higher
- Git
- A Google Gemini API key (obtain from [Google AI Studio](https://aistudio.google.com/))

### Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Vinchent/youtube-summarizer-streamlit.git
    cd youtube-summarizer-streamlit
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate on Windows
    venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### API Key Configuration

The two operation modes require **different methods** for setting the API key:

**A) For the Streamlit Web App (`app.py`):**

The app uses Streamlit's secrets management.

1.  Create a directory named `.streamlit` in the project root.
2.  Inside it, create a file named `secrets.toml`.
3.  Add your Gemini API key to the file like this:

    ```toml
    # .streamlit/secrets.toml
    GEMINI_API_KEY = "your_api_key_here"
    ```

**B) For the Playlist Script (`populate_from_playlist.py`):**

This script requires the API key to be set as an **environment variable**.

-   **On macOS/Linux:**
    ```bash
    export GEMINI_API_KEY="your_api_key_here"
    ```
-   **On Windows (Command Prompt):**
    ```bash
    set GEMINI_API_KEY="your_api_key_here"
    ```
-   **On Windows (PowerShell):**
    ```powershell
    $env:GEMINI_API_KEY="your_api_key_here"
    ```

## 🚀 Running the Application

### 1. To Launch the Web App
```bash
streamlit run app.py
