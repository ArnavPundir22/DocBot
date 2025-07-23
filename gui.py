import os
import shutil
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QFileDialog, QHBoxLayout, QApplication, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

from fpdf import FPDF

from scraper import scrape_text_from_url
from summarizer import summarize_text, summarize_images
from qa_engine import answer_question
from pdf_handler import extract_text_from_pdf, extract_images_from_pdf

class DocBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini DocBot")
        self.setGeometry(100, 100, 800, 600)
        self.setAcceptDrops(True)
        self.scraped_text = ""
        self.pdf_images = []
        self.dark_mode_enabled = False

        layout = QVBoxLayout()

        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter documentation URL...")
        layout.addWidget(QLabel("📎 URL:"))
        layout.addWidget(self.url_input)

        self.fetch_button = QPushButton("Fetch & Summarize")
        self.fetch_button.clicked.connect(self.fetch_and_summarize)
        layout.addWidget(self.fetch_button)

        # PDF Upload
        self.upload_button = QPushButton("📂 Upload PDF")
        self.upload_button.clicked.connect(self.upload_pdf)
        layout.addWidget(self.upload_button)

        # Progress Bar
        self.spinner = QProgressBar()
        self.spinner.setRange(0, 0)
        self.spinner.setVisible(False)
        layout.addWidget(self.spinner)

        # Summary Output
        self.summary_output = QTextEdit()
        self.summary_output.setPlaceholderText("Summary will appear here...")
        layout.addWidget(QLabel("📄 Summary:"))
        layout.addWidget(self.summary_output)

        # Question & Answer
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Ask a question about the document...")
        layout.addWidget(QLabel("❓ Question:"))
        layout.addWidget(self.question_input)

        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.ask_question)
        layout.addWidget(self.ask_button)

        self.answer_output = QTextEdit()
        self.answer_output.setPlaceholderText("Answer will appear here...")
        layout.addWidget(QLabel("💬 Answer:"))
        layout.addWidget(self.answer_output)

        # Export Buttons
        export_btns = QHBoxLayout()
        export_summary_btn = QPushButton("📝 Export Summary")
        export_summary_btn.clicked.connect(self.export_summary)
        export_answer_btn = QPushButton("📝 Export Answer")
        export_answer_btn.clicked.connect(self.export_answer)
        export_btns.addWidget(export_summary_btn)
        export_btns.addWidget(export_answer_btn)
        layout.addLayout(export_btns)

        # Theme toggle
        self.toggle_theme_button = QPushButton("🌙 Enable Dark Mode")
        self.toggle_theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.toggle_theme_button)

        # Quota Label
        self.quota_label = QLabel("""
<b>📊 Gemini Free Tier Quota Limits:</b><br>
• <b>50</b> requests per model <b>per day</b><br>
• <b>5–10</b> requests <b>per minute</b><br>
• <b>60K</b> input tokens/min • <b>30K</b> output tokens/min<br>
🔁 If you exceed these, switch API keys or wait 24 hrs.<br>
🔼 <a href='https://ai.google.dev/pricing'>Upgrade your plan</a> for higher limits.
""")
        self.quota_label.setOpenExternalLinks(True)
        self.quota_label.setStyleSheet("font-size: 12px; color: #555;")
        layout.addWidget(self.quota_label)

        self.setLayout(layout)
        self.light_theme_css = """
            QWidget { background-color: #f5f7fa; font-family: 'Segoe UI'; }
            QLineEdit, QTextEdit {
                background-color: #ffffff;
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #004c99; }
            QLabel { font-weight: bold; margin-top: 10px; font-size: 15px; }
        """
        self.setStyleSheet(self.light_theme_css)

    def fetch_and_summarize(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a documentation URL.")
            return

        self.spinner.setVisible(True)
        QApplication.processEvents()
        try:
            self.scraped_text = scrape_text_from_url(url)
            summary = summarize_text(self.scraped_text).strip() or "❗ No summary generated."
            self.summary_output.setText(summary)
        except Exception as e:
            self.summary_output.setText(f"Error: {e}")
        finally:
            self.spinner.setVisible(False)

    def upload_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if path:
            self.summarize_pdf(path)

    def summarize_pdf(self, path):
        self.spinner.setVisible(True)
        QApplication.processEvents()
        try:
            from cache_manager import get_cached_summary, cache_summary
            cached = get_cached_summary(path)
            if cached:
                self.summary_output.setText(cached)
                return

            self.scraped_text = extract_text_from_pdf(path)
            self.pdf_images = extract_images_from_pdf(path)
            text_summary = summarize_text(self.scraped_text)
            image_summary = summarize_images(self.pdf_images)
            full = f"📄 Text Summary:\n{text_summary}\n\n🖼️ Image Summary:\n{image_summary}"
            self.summary_output.setText(full)
            cache_summary(path, full)
        except Exception as e:
            self.summary_output.setText(f"Error: {e}")
        finally:
            self.cleanup_images()
            self.spinner.setVisible(False)

    def ask_question(self):
        question = self.question_input.text().strip()
        if not self.scraped_text:
            QMessageBox.warning(self, "No Document", "Please fetch or upload a document first.")
            return
        if not question:
            QMessageBox.warning(self, "No Question", "Please enter a question.")
            return

        try:
            answer = answer_question(self.scraped_text, question)
            self.answer_output.setText(answer.strip() or "❗ No answer generated.")
            if "Quota Error" in answer:
                QMessageBox.warning(self, "Quota Limit Reached", answer)
        except Exception as e:
            self.answer_output.setText(f"Error: {e}")

    def export_summary(self):
        self._export_text("Summary", self.summary_output.toPlainText())

    def export_answer(self):
        self._export_text("Answer", self.answer_output.toPlainText())

    def _export_text(self, label, content):
        if not content.strip():
            QMessageBox.warning(self, "Empty", f"No {label.lower()} to export.")
            return

        path, _ = QFileDialog.getSaveFileName(self, f"Save {label}", f"{label.lower()}.txt", "Text Files (*.txt);;PDF Files (*.pdf)")
        if not path:
            return

        try:
            if path.endswith('.pdf'):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in content.splitlines():
                    pdf.multi_cell(0, 10, txt=line)
                pdf.output(path)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
            QMessageBox.information(self, "Exported", f"{label} saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export {label}: {e}")

    def cleanup_images(self):
        if os.path.exists("pdf_images"):
            shutil.rmtree("pdf_images")

    def toggle_theme(self):
        if not self.dark_mode_enabled:
            self.setStyleSheet("""
                QWidget { background-color: #121212; color: #e0e0e0; }
                QLineEdit, QTextEdit {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border: 1px solid #444;
                    padding: 10px;
                    border-radius: 8px;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #0066cc;
                    color: white;
                    padding: 10px;
                    font-size: 14px;
                    border-radius: 6px;
                }
                QPushButton:hover { background-color: #555; }
                QLabel { font-weight: bold; font-size: 15px; }
            """)
            self.toggle_theme_button.setText("☀️ Disable Dark Mode")
        else:
            self.setStyleSheet(self.light_theme_css)
            self.toggle_theme_button.setText("🌙 Enable Dark Mode")
        self.dark_mode_enabled = not self.dark_mode_enabled

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            if url.toLocalFile().endswith(".pdf"):
                self.summarize_pdf(url.toLocalFile())

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = DocBotApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❗ Application Error: {e}")
