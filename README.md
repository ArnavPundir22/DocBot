
# DocBot

**Gemini DocBot** is a desktop-based application that allows you to summarize online documentation via URL and ask questions about the content. Built using Python and PyQt5, it integrates Google's Gemini API to provide intelligent summarization and Q&A functionality.

---

## ⚙️ Requirements

- **Python Version:** 3.10+
- All required libraries are listed in `requirements.txt`

---

## 📁 Project Structure

```
DocumentationSummarizer/
│
├── main.py                  # Entry point
├── gui.py                   # PyQt5 GUI
├── config.py                # Gemini API setup
├── scraper.py               # Web scraper for text content
├── summarizer.py            # Handles summarization logic
├── qa_engine.py             # Handles Q&A generation
├── requirements.txt         # Required dependencies
├── README.md                # Project documentation
```

---

## 📥 Setup Instructions

### 1. Install Python 3.10+

Make sure you have Python 3.10 or higher installed:

```bash
python --version
```

---

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/DocumentationSummarizer.git
cd DocumentationSummarizer
```

---

### 3. Create Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
```

---

### 4. Install Required Libraries

```bash
pip install -r requirements.txt
```

---

### 5. Configure Gemini API

In `config.py`, paste your API key:

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

from google.generativeai import GenerativeModel
client = GenerativeModel("gemini-1.5-pro")  # Use a valid available model
```

---

### 6. Run the Application

```bash
python main.py
```

---

## 📌 Notes

- Make sure your Gemini API key is valid and active.
- Internet connectivity is required for API requests.
- If you exceed quota limits, check your [Google AI Console](https://ai.google.dev/) for usage and limits.
- The system uses Gemini 1.5 Pro model (or configurable) for both summarization and Q&A.

---

## 🧠 Technologies Used

- PyQt5  
- Google Generative AI (`google-generativeai`)  
- Requests  
- Python Standard Libraries

---

## 👤 Developed by

**Arnav Pundir**
