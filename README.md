# ✨ YouTube Video Summarizer with Gemini AI

A simple yet beautiful web application that transforms lengthy YouTube videos into concise, readable summaries using the power of Google Gemini AI. Skip the time-consuming process of watching long videos and extract key insights in seconds.

## Application Preview

![App Screenshot](https://i.imgur.com/qRCmWDm.png)

## 🚀 Key Features

- **AI-Powered Summarization**: Leverages Google's `gemini-2.5-flash-lite` model to generate accurate, high-quality video summaries (but you can change it)
- **Intuitive Web Interface**: Clean and user-friendly interface built with Streamlit, ensuring accessibility for all users
- **Persistent History**: All analyzed videos are stored in a local SQLite database, allowing you to review previous summaries anytime, even after application restarts
- **Automated Content Extraction**: Automatically retrieves video transcripts and metadata directly from YouTube
- **Streamlined Workflow**: Simply paste a YouTube URL and click to generate comprehensive summaries

## 🛠️ Technology Stack

- **Programming Language**: Python 3.9+
- **Web Framework**: Streamlit
- **AI Model**: Google Gemini (gemini-2.5-flash-lite)
- **Database**: SQLite
- **Core Dependencies**: `google-generativeai`, `youtube-transcript-api`, `yt_dlp`

## ⚙️ Installation & Setup

Follow these steps to set up and run the project locally.

### Prerequisites

- Python 3.9 or higher
- Git version control system
- Google Gemini API key (obtain from [Google AI Studio](https://aistudio.google.com/))

### Installation Process

#### 1. Clone the Repository

```bash
git clone https://github.com/Vinchent/youtube-summarizer-streamlit.git
cd youtube-summarizer-streamlit
```

#### 2. Environment Setup

Create and activate a virtual environment, then install dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

#### 3. API Configuration

The application uses Streamlit's secrets management for secure API key handling:

1. Create a `.streamlit` directory in the project root
2. Create a `secrets.toml` file within the `.streamlit` directory
3. Add your API key configuration:

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_api_key_here"
```

## 🚀 Running the Application

Launch the application using the following command:

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at the local development server address.

## 📁 Project Structure

```
.
├── .streamlit/
│   └── secrets.toml    # API credentials (excluded from version control)
├── app.py              # Main Streamlit application interface
├── summarizer.py       # Core logic for YouTube and Gemini AI integration
├── database.py         # SQLite database management functions
├── history.db          # Local database file (excluded from version control)
├── requirements.txt    # Python dependencies
├── .gitignore          # Version control exclusions
└── README.md           # Project documentation
```

## 🔒 Security Considerations

- API keys are managed through Streamlit's secure secrets system
- Sensitive files (credentials, database) are excluded from version control
- Local SQLite database ensures data privacy

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bug reports and feature requests.


## 📞 Support

For questions or support, please open an issue in the GitHub repository.
