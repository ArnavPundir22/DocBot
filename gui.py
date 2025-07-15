# gui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QMessageBox, QFileDialog, QHBoxLayout, QApplication,
    QDialog, QProgressBar
)
from PyQt5.QtCore import Qt
from fpdf import FPDF
from scraper import scrape_text_from_url
from summarizer import summarize_text, summarize_images
from qa_engine import answer_question
from pdf_handler import extract_text_from_pdf, extract_images_from_pdf
from typing_effect import type_text_effect
from cache_manager import get_cached_summary, cache_summary
import shutil
import os


class DocBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini DocBot")
        self.setGeometry(100, 100, 800, 600)
        self.scraped_text = ""
        self.pdf_text = ""
        self.pdf_images = []
        self.dark_mode_enabled = False

        self.setAcceptDrops(True)  # Enable drag & drop

        layout = QVBoxLayout()

        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter documentation URL...")
        layout.addWidget(QLabel("📎 URL:"))
        layout.addWidget(self.url_input)

        # Fetch & Summarize
        self.fetch_button = QPushButton("Fetch & Summarize")
        self.fetch_button.clicked.connect(self.fetch_and_summarize)
        layout.addWidget(self.fetch_button)

        # Load PDF
        self.load_pdf_button = QPushButton("📂 Load PDF")
        self.load_pdf_button.clicked.connect(self.load_pdf_file)
        layout.addWidget(self.load_pdf_button)

        # Summary output
        self.summary_output = QTextEdit()
        self.summary_output.setPlaceholderText("Summary will appear here...")
        layout.addWidget(QLabel("📄 Summary:"))
        layout.addWidget(self.summary_output)

        # Question input
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Ask a question about the document...")
        layout.addWidget(QLabel("❓ Question:"))
        layout.addWidget(self.question_input)

        # Ask button
        self.ask_button = QPushButton("Ask")
        self.ask_button.clicked.connect(self.ask_question)
        layout.addWidget(self.ask_button)

        # Answer output
        self.answer_output = QTextEdit()
        self.answer_output.setPlaceholderText("Answer will appear here...")
        layout.addWidget(QLabel("💬 Answer:"))
        layout.addWidget(self.answer_output)

        # Export buttons
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

        self.setLayout(layout)
        self.light_theme_css = """
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                background-color: #f5f7fa;
            }
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
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #004c99;
            }
            QLabel {
                font-weight: bold;
                margin-top: 10px;
                font-size: 15px;
            }
        """
        self.setStyleSheet(self.light_theme_css)

    def fetch_and_summarize(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a documentation URL.")
            return

        self.setDisabled(True)
        self.show_loading("Summarizing URL content...")

        self.scraped_text = scrape_text_from_url(url)
        summary = summarize_text(self.scraped_text)
        type_text_effect(self.summary_output, summary)

        self.hide_loading()
        self.setDisabled(False)

    def load_pdf_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.load_pdf_from_path(file_path)

    def load_pdf_from_path(self, file_path):
        self.setDisabled(True)
        self.show_loading("Summarizing PDF...")

        cached = get_cached_summary(file_path)
        if cached:
            type_text_effect(self.summary_output, cached)
            self.scraped_text = cached
            self.hide_loading()
            self.setDisabled(False)
            return

        self.pdf_text = extract_text_from_pdf(file_path)
        self.pdf_images = extract_images_from_pdf(file_path)

        summary_text = summarize_text(self.pdf_text)
        image_summary = summarize_images(self.pdf_images)
        full_summary = summary_text + "\n\n🖼️ Image Summary:\n" + image_summary

        type_text_effect(self.summary_output, full_summary)
        self.scraped_text = self.pdf_text + "\n\n" + image_summary

        if os.path.exists("pdf_images"):
            shutil.rmtree("pdf_images")

        cache_summary(file_path, full_summary)

        self.hide_loading()
        self.setDisabled(False)

    def ask_question(self):
        question = self.question_input.text().strip()
        if not self.scraped_text:
            QMessageBox.warning(self, "No Document", "Please fetch or load a document first.")
            return
        if not question:
            QMessageBox.warning(self, "No Question", "Please enter a question.")
            return

        self.setDisabled(True)
        self.show_loading("Thinking...")

        answer = answer_question(self.scraped_text, question)
        type_text_effect(self.answer_output, answer)

        self.hide_loading()
        self.setDisabled(False)

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
                    pdf.cell(200, 10, txt=line, ln=True)
                pdf.output(path)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
            QMessageBox.information(self, "Exported", f"{label} saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export {label}: {str(e)}")

    def toggle_theme(self):
        if not self.dark_mode_enabled:
            self.setStyleSheet("""
                QWidget {
                    background-color: #121212;
                    color: #e0e0e0;
                    font-family: 'Segoe UI';
                }
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
                    border: none;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
                QLabel {
                    font-weight: bold;
                    font-size: 15px;
                }
            """)
            self.toggle_theme_button.setText("☀️ Disable Dark Mode")
        else:
            self.setStyleSheet(self.light_theme_css)
            self.toggle_theme_button.setText("🌙 Enable Dark Mode")
        self.dark_mode_enabled = not self.dark_mode_enabled

    def show_loading(self, message="Loading..."):
        self.loading_dialog = QDialog(self)
        self.loading_dialog.setModal(True)
        self.loading_dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.loading_dialog.setStyleSheet("""
            QDialog {
                background-color: rgba(0, 0, 0, 150);
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout = QVBoxLayout()
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        progress = QProgressBar()
        progress.setRange(0, 0)
        layout.addWidget(progress)

        self.loading_dialog.setLayout(layout)
        self.loading_dialog.setFixedSize(300, 100)
        self.loading_dialog.move(
            self.geometry().center() - self.loading_dialog.rect().center()
        )
        self.loading_dialog.show()

    def hide_loading(self):
        if hasattr(self, "loading_dialog"):
            self.loading_dialog.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(".pdf"):
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(".pdf"):
                self.load_pdf_from_path(file_path)


# Run standalone
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = DocBotApp()
    window.show()
    sys.exit(app.exec_())
