
# 📘 DocBot

**DocBot** is a desktop-based intelligent document summarizer and Q&A assistant built using **Python** and **PyQt5**. It uses **Google Gemini 1.5 Flash API** to summarize content from online URLs and PDF files (text + images) and intelligently answer user questions.

---

## ⚙️ Requirements

- **Python Version:** 3.10+
- All dependencies listed in `requirements.txt`
- **Google Gemini API key(s)**
- **Google Chrome + ChromeDriver** (for URL scraping)

---

## 📁 Project Structure

```
GeminiDocBot/
├── main.py              # App entry point
├── gui.py               # PyQt5 GUI interface
├── summarizer.py        # Gemini summarization (text & image)
├── qa_engine.py         # Q&A using Gemini
├── scraper.py           # Web scraping using Selenium
├── pdf_handler.py       # PDF text + image extraction
├── key_manager.py       # API key rotation logic
├── config.py            # List of Gemini API keys
├── requirements.txt     # Required dependencies
└── README.md            # Project documentation
```

---

## 📥 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/GeminiDocBot.git
cd GeminiDocBot
```

---

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ✅ **Make sure** Google Chrome & ChromeDriver are installed and available in PATH (used for Selenium-based scraping).

---

### 4. Add Your API Keys

Edit `config.py` and add one or more Gemini API keys:

```python
GEMINI_API_KEYS = [
    "YOUR_API_KEY_1",
    "YOUR_API_KEY_2"
]
CURRENT_KEY_INDEX = 0
```

---

## ▶️ Run the App

```bash
python main.py
```

---

## 🔧 Features

| Feature               | Description |
|----------------------|-------------|
| 🌐 URL Summarization | Scrape and summarize text from a documentation site |
| 📂 PDF Analysis      | Upload PDF to extract + summarize both text and images |
| 🧠 Gemini 1.5 Flash  | Handles summarization and question answering |
| ❓ Ask Questions      | Get intelligent answers based on document context |
| 🔁 API Key Rotation  | Automatically switches keys if quota is exhausted |
| 🌗 Dark/Light Mode   | Toggle interface theme easily |
| 📤 Export Results    | Save summary and answers as `.txt` or `.pdf` |
| 🌀 Loading Indicator | Spinner shown while generating summary |
| 📊 Quota Display     | Gemini free-tier usage guide shown in app |

---

## 📊 Gemini Free Tier Quota

| Limit Type                | Free Tier Value |
|---------------------------|-----------------|
| Requests/day/model        | 50              |
| Requests/min/model        | 5–10            |
| Input tokens/minute       | ~60,000         |
| Output tokens/minute      | ~30,000         |

> 🔁 App automatically switches to the next API key when quota is reached.  
> 💡 [Upgrade your Gemini plan](https://ai.google.dev/pricing) for higher limits.

---

## 🧠 Tech Stack

- **PyQt5** – GUI framework  
- **google-generativeai** – Gemini API integration  
- **Selenium** – Dynamic webpage scraping  
- **PyMuPDF** – PDF text & image extraction  
- **FPDF** – PDF exporting  
- **Pillow** – Image handling  

---

## 👨‍💻 Developed By

**Arnav Pundir**  
B.Tech CSE | COER University Roorkee  
Email: *arnavp128@gmail.com*  
Portfolio: *arnavpundir22.github.io*  

---

**Built with using Google Gemini + Python**
