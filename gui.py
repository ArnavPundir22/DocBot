from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QMessageBox, QFileDialog, QHBoxLayout, QApplication
)
from fpdf import FPDF
from scraper import scrape_text_from_url
from summarizer import summarize_text
from qa_engine import answer_question

class DocBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini DocBot")
        self.setGeometry(100, 100, 800, 600)
        self.scraped_text = ""
        self.dark_mode_enabled = False

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

        # Apply layout & default theme
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

        self.scraped_text = scrape_text_from_url(url)
        summary = summarize_text(self.scraped_text)
        self.summary_output.setText(summary)

    def ask_question(self):
        question = self.question_input.text().strip()
        if not self.scraped_text:
            QMessageBox.warning(self, "No Document", "Please fetch and summarize a document first.")
            return
        if not question:
            QMessageBox.warning(self, "No Question", "Please enter a question.")
            return

        answer = answer_question(self.scraped_text, question)
        self.answer_output.setText(answer)

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


# Optional: only needed if you want to run this file directly
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = DocBotApp()
    window.show()
    sys.exit(app.exec_())
