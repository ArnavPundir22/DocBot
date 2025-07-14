# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui import DocBotApp

def main():
    app = QApplication(sys.argv)
    window = DocBotApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
